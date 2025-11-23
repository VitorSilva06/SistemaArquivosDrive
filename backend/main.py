"""API principal para cadastro de clientes e upload de documentos."""
import json
import logging
import tempfile
from collections import defaultdict
from pathlib import Path
from typing import Dict, List

from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from config import ALLOWED_ORIGINS, LOG_LEVEL
from drive_service import DriveService
from image_processor import ImageProcessor
from pdf_generator import create_password_pdf
from report_generator import build_report
from utils import sanitize_filename, slugify
from validators import (
    is_image_file,
    validate_file_size,
    validate_name,
    validate_phone,
)

# Configuração de logging
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL.upper(), logging.INFO),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Inicialização do app
app = FastAPI(
    title="Cadastro de Clientes",
    version="2.0.0",
    description="API para receber documentos, validar imagens, converter em PDF e enviar ao Google Drive.",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS if "*" not in ALLOWED_ORIGINS else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Instâncias globais (singleton)
drive_service = None
image_processor = ImageProcessor()


@app.on_event("startup")
async def startup_event():
    """Inicializa serviços na startup."""
    global drive_service
    try:
        drive_service = DriveService()
        logger.info("Serviços inicializados com sucesso")
    except Exception as e:
        logger.error(f"Erro ao inicializar serviços: {e}")
        raise


@app.get("/")
async def root():
    """Endpoint raiz."""
    return {
        "message": "API de Cadastro de Clientes",
        "version": "2.0.0",
        "docs": "/docs",
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "drive_service": drive_service is not None}


@app.post("/api/submit")
async def submit_form(
    nome: str = Form(...),
    telefone: str = Form(...),
    servico: str = Form(...),
    field_status: str = Form(""),
    file_field_map: str = Form(""),
    extra_values: str = Form(""),
    documentos: List[UploadFile] = File(default_factory=list),
):
    """
    Endpoint principal para receber e processar documentos do cliente.
    
    Args:
        nome: Nome completo do cliente
        telefone: Telefone do cliente
        servico: Tipo de serviço selecionado
        field_status: JSON com status dos campos do formulário
        file_field_map: JSON com mapeamento arquivo -> campo
        documentos: Lista de arquivos enviados
        
    Returns:
        JSON com resultado do processamento
    """
    logger.info(f"Iniciando processamento para cliente: {nome} ({telefone})")

    # Validações iniciais
    if not documentos:
        logger.warning("Tentativa de envio sem documentos")
        raise HTTPException(status_code=400, detail="Nenhum documento enviado.")

    validate_name(nome)
    phone_digits = validate_phone(telefone)

    # Parse de JSONs
    try:
        status_payload = json.loads(field_status) if field_status else {}
    except json.JSONDecodeError as e:
        logger.warning(f"Erro ao parsear field_status: {e}")
        raise HTTPException(status_code=400, detail="field_status inválido.")

    try:
        file_field_mapping = json.loads(file_field_map) if file_field_map else {}
    except json.JSONDecodeError as e:
        logger.warning(f"Erro ao parsear file_field_map: {e}")
        file_field_mapping = {}

    try:
        extra_values_dict = json.loads(extra_values) if extra_values else {}
    except json.JSONDecodeError as e:
        logger.warning(f"Erro ao parsear extra_values: {e}")
        extra_values_dict = {}

    # Nome da pasta do cliente e do serviço
    client_folder_name = f"{slugify(nome)}-{phone_digits}"
    service_folder_name = sanitize_filename(servico.replace(" ", "_")) or "Servico"
    processed: List[Dict[str, str]] = []
    rejected: List[Dict[str, str]] = []

    # Processa arquivos
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir_path = Path(tmpdir)
        
        for upload in documentos:
            try:
                contents = await upload.read()
                source_field = upload.filename or "arquivo"
                
                # Valida tamanho
                if len(contents) == 0:
                    field_info = file_field_mapping.get(source_field, {})
                    rejected.append({
                        "filename": source_field,
                        "reason": "Arquivo vazio.",
                        "field_id": field_info.get("fieldId", "desconhecido"),
                        "field_label": field_info.get("fieldLabel", "Campo desconhecido"),
                    })
                    continue

                validate_file_size(len(contents))

                # Obtém informações do campo
                field_info = file_field_mapping.get(source_field, {})
                field_id = field_info.get("fieldId", "desconhecido")
                field_label = field_info.get("fieldLabel", "Campo desconhecido")
                
                # Gera nome do arquivo baseado no campo
                field_name_clean = sanitize_filename(field_label.replace(" ", "_"))
                if not field_name_clean or field_name_clean == "Campo_desconhecido":
                    # Fallback: usa nome do arquivo original
                    field_name_clean = sanitize_filename(Path(source_field).stem)

                # Processa imagem ou arquivo normal
                if image_processor.is_image(upload.content_type, source_field):
                    # Para imagens, sempre converte para PDF
                    pdf_filename = f"{field_name_clean}.pdf"
                    pdf_path = tmpdir_path / pdf_filename
                    
                    success, pdf_path_result, error_msg = image_processor.process_image(
                        contents, source_field, pdf_path
                    )
                    
                    if success and pdf_path_result:
                        processed.append({
                            "path": pdf_path_result,
                            "stored_name": pdf_filename,
                            "mime": "application/pdf",
                            "original_name": source_field,
                            "field_id": field_id,
                            "field_label": field_label,
                        })
                    else:
                        rejected.append({
                            "filename": source_field,
                            "reason": error_msg or "Erro ao processar imagem",
                            "field_id": field_id,
                            "field_label": field_label,
                        })
                else:
                    # Arquivo não-imagem - mantém extensão original
                    original_ext = Path(upload.filename or "documento").suffix
                    stored_name = f"{field_name_clean}{original_ext}"
                    file_path = tmpdir_path / stored_name
                    file_path.write_bytes(contents)
                    
                    processed.append({
                        "path": str(file_path),
                        "stored_name": stored_name,
                        "mime": upload.content_type or "application/octet-stream",
                        "original_name": source_field,
                        "field_id": field_id,
                        "field_label": field_label,
                    })
                    logger.info(f"Arquivo {source_field} preparado para upload: {stored_name}")

            except HTTPException:
                raise
            except Exception as e:
                logger.error(f"Erro inesperado ao processar {upload.filename}: {e}")
                field_info = file_field_mapping.get(upload.filename or "arquivo", {})
                rejected.append({
                    "filename": upload.filename or "arquivo",
                    "reason": f"Erro inesperado: {str(e)}",
                    "field_id": field_info.get("fieldId", "desconhecido"),
                    "field_label": field_info.get("fieldLabel", "Campo desconhecido"),
                })
                continue

        # Processa senha se existir
        for field_id, field_value in extra_values_dict.items():
            if field_value and "senha" in field_id.lower():
                # Cria PDF da senha
                password_pdf_path = tmpdir_path / "Senha_do_Meu_INSS.pdf"
                if create_password_pdf(str(field_value), password_pdf_path):
                    # Busca label do campo no status
                    field_label = "Senha do Meu INSS"
                    if field_id in status_payload:
                        field_label = status_payload[field_id].get("label", field_label)
                    
                    processed.append({
                        "path": str(password_pdf_path),
                        "stored_name": "Senha_do_Meu_INSS.pdf",
                        "mime": "application/pdf",
                        "original_name": "senha",
                        "field_id": field_id,
                        "field_label": field_label,
                    })
                    logger.info(f"PDF de senha criado para campo {field_id}")

        # Valida se há arquivos processados
        if not processed:
            logger.warning(f"Nenhum arquivo aprovado para {nome}. Rejeitados: {len(rejected)}")
            raise HTTPException(
                status_code=400,
                detail=(
                    f"Nenhum arquivo aprovado. {len(rejected)} arquivo(s) rejeitado(s). "
                    "Revise a qualidade das imagens e tente novamente."
                ),
            )

        # Upload para Google Drive
        uploaded_count = 0
        try:
            logger.info(f"Conectando ao Google Drive para cliente {nome}")
            root_folder = drive_service.get_root_folder_id()
            
            # Cria pasta do cliente
            client_folder_id = drive_service.ensure_folder(root_folder, client_folder_name)
            logger.info(f"Pasta do cliente criada/encontrada: {client_folder_id}")

            # Agrupa arquivos por field_id para detectar múltiplos
            files_by_field = defaultdict(list)
            for item in processed:
                files_by_field[item["field_id"]].append(item)

            # Pasta do serviço dentro do cliente
            service_folder_id = drive_service.ensure_folder(client_folder_id, service_folder_name)

            # Upload dos arquivos processados
            for item in processed:
                try:
                    field_id = item["field_id"]
                    field_files = files_by_field[field_id]

                    # Define pasta alvo: se múltiplos no mesmo campo, cria subpasta do campo dentro do serviço
                    if len(field_files) > 1:
                        field_label_clean = sanitize_filename(item["field_label"].replace(" ", "_"))
                        target_folder = drive_service.ensure_folder(service_folder_id, field_label_clean)
                    else:
                        target_folder = service_folder_id

                    # Upload com política de "não sobrescrever e não duplicar": se existir, pula
                    filename = Path(item["path"]).name
                    if drive_service.find_file_by_name(filename, target_folder):
                        logger.info(f"Arquivo já existente em destino, ignorando upload: {filename}")
                    else:
                        drive_service.upload_file(
                            Path(item["path"]),
                            item["mime"],
                            target_folder
                        )
                        uploaded_count += 1
                except Exception as e:
                    logger.error(f"Erro ao enviar {item['stored_name']}: {e}")
                    rejected.append({
                        "filename": item["original_name"],
                        "reason": f"Falha no upload: {str(e)}",
                        "field_id": item.get("field_id", "desconhecido"),
                        "field_label": item.get("field_label", "Campo desconhecido"),
                    })

            # Gera e envia relatório
            report_content = build_report(
                nome,
                telefone,
                servico,
                status_payload,
                processed,
                rejected,
            )
            report_name = "relatorio.txt"
            report_path = tmpdir_path / report_name
            report_path.write_text(report_content, encoding="utf-8")
            
            try:
                # Salva o relatório na pasta do serviço (sem sobrescrever)
                if not drive_service.find_file_by_name(report_name, service_folder_id):
                    drive_service.upload_file(report_path, "text/plain", service_folder_id)
                    logger.info(f"Relatório enviado para pasta do serviço {service_folder_id}")
                else:
                    logger.info("Relatório já existe na pasta do serviço; mantendo o existente.")
            except Exception as e:
                logger.error(f"Erro ao enviar relatório: {e}")

            logger.info(
                f"Processamento concluído para {nome}: {uploaded_count} arquivo(s) enviado(s), "
                f"{len(rejected)} rejeitado(s)"
            )

        except Exception as err:
            logger.exception(f"Erro ao processar requisição: {err}")
            raise HTTPException(
                status_code=500,
                detail=f"Erro interno: {str(err)}"
            ) from err

    return JSONResponse(
        {
            "message": (
                "Arquivos enviados com sucesso." if uploaded_count > 0
                else "Processamento concluído com erros."
            ),
            "cliente": nome,
            "pasta": client_folder_name,
            "arquivos_aprovados": len(processed),
            "arquivos_enviados": uploaded_count,
            "arquivos_rejeitados": rejected,
        }
    )
