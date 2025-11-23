"""Serviço de integração com Google Drive."""
import json
import logging
import os
import pickle
from pathlib import Path
from typing import Optional

from google.auth.transport.requests import Request as GoogleAuthRequest
from google.oauth2.credentials import Credentials
from google.oauth2.service_account import Credentials as SACredentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseUpload

from config import (
    CLIENT_SECRET_FILE,
    TOKEN_FILE,
    GOOGLE_DRIVE_ROOT_FOLDER_ID,
    SCOPES,
    USE_SERVICE_ACCOUNT,
)

logger = logging.getLogger(__name__)


class DriveService:
    """Classe para gerenciar operações com Google Drive."""
    
    def __init__(self):
        """Inicializa o serviço do Drive."""
        self.service = None
        self.credentials = None
        self._authenticate()
    
    def _authenticate(self) -> None:
        """
        Autentica com Google Drive usando OAuth 2.0.
        
        Raises:
            RuntimeError: Se a autenticação falhar
        """
        # Caminho 1: Service Account em produção (sem interação)
        if USE_SERVICE_ACCOUNT:
            try:
                sa_json = os.environ["GOOGLE_CLIENT_SECRET_JSON"]
                info = json.loads(sa_json)
                creds = SACredentials.from_service_account_info(info, scopes=SCOPES)
                logger.info("Autenticado com Service Account")
            except KeyError:
                raise RuntimeError("GOOGLE_CLIENT_SECRET_JSON não definido para Service Account")
            except Exception as e:
                logger.error(f"Erro na autenticação Service Account: {e}")
                raise RuntimeError(f"Falha na autenticação Service Account: {e}") from e
        else:
            # Caminho 2: OAuth de usuário (local/dev) com token persistente
            creds = None
            token_path = Path(TOKEN_FILE)

            # Semeia token a partir de variável de ambiente (opcional)
            token_json_env = os.getenv("GOOGLE_TOKEN_JSON")
            if token_json_env and not token_path.exists():
                try:
                    token_path.write_text(token_json_env, encoding="utf-8")
                    logger.info("Token escrito a partir da variável de ambiente GOOGLE_TOKEN_JSON")
                except Exception as e:
                    logger.warning(f"Falha ao escrever token da env: {e}")
            
            # Carrega token salvo (formato JSON preferencial). Mantém compatibilidade com pickle antigo.
            if token_path.exists():
                try:
                    creds = Credentials.from_authorized_user_file(str(token_path), SCOPES)
                    logger.info("Token (JSON) carregado do arquivo")
                except Exception as e_json:
                    logger.warning(f"Falha ao carregar token JSON: {e_json}. Tentando pickle legado.")
                    try:
                        with open(token_path, "rb") as token_fh:
                            creds = pickle.load(token_fh)
                        logger.info("Token (pickle legado) carregado do arquivo")
                    except Exception as e_pickle:
                        logger.warning(f"Erro ao carregar token legado: {e_pickle}")
            
            # Se não há credenciais válidas, faz login
            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    try:
                        creds.refresh(GoogleAuthRequest())
                        logger.info("Token de autenticação renovado")
                    except Exception as e:
                        logger.error(f"Erro ao renovar token: {e}")
                        creds = None
                
                if not creds:
                    try:
                        flow = InstalledAppFlow.from_client_secrets_file(
                            CLIENT_SECRET_FILE, SCOPES
                        )
                        creds = flow.run_local_server(port=0)
                        logger.info("Nova autenticação realizada")
                    except Exception as e:
                        logger.error(f"Erro na autenticação: {e}")
                        raise RuntimeError(f"Falha na autenticação: {e}") from e
                
                # Salva o token em formato JSON para uso futuro
                try:
                    token_path.write_text(creds.to_json(), encoding="utf-8")
                    logger.info("Token salvo (JSON) para uso futuro")
                except Exception as e:
                    logger.warning(f"Erro ao salvar token: {e}")
        
        self.credentials = creds
        self.service = build(
            "drive",
            "v3",
            credentials=creds,
            cache_discovery=False,
            static_discovery=False,
        )
        logger.info("Serviço do Google Drive inicializado")
        logger.info("Serviço do Google Drive inicializado")
    
    def find_file_by_name(
        self,
        filename: str,
        folder_id: str
    ) -> Optional[str]:
        """
        Busca arquivo pelo nome na pasta especificada.
        
        Args:
            filename: Nome do arquivo
            folder_id: ID da pasta
            
        Returns:
            ID do arquivo se encontrado, None caso contrário
        """
        try:
            filename_escaped = filename.replace("'", "\\'")
            query = (
                f"name='{filename_escaped}' and "
                f"'{folder_id}' in parents and "
                f"trashed=false"
            )
            response = (
                self.service.files()
                .list(
                    q=query,
                    fields="files(id, name)",
                    pageSize=1,
                    supportsAllDrives=True,
                    includeItemsFromAllDrives=True,
                    corpora="allDrives",
                )
                .execute()
            )
            files = response.get("files", [])
            if files:
                return files[0]["id"]
            return None
        except HttpError as e:
            logger.warning(f"Erro ao buscar arquivo {filename}: {e}")
            return None
    
    # Mantido para uso futuro se desejar sufixos. Não utilizado no fluxo atual (pular duplicados).
    def _generate_available_name(self, desired_name: str, folder_id: str) -> str:
        if not self.find_file_by_name(desired_name, folder_id):
            return desired_name
        i = 2
        base, dot, ext = desired_name.rpartition('.')
        base = base if dot else desired_name
        ext = f".{ext}" if dot else ""
        while True:
            candidate = f"{base}({i}){ext}"
            if not self.find_file_by_name(candidate, folder_id):
                return candidate
            i += 1

    def upload_file(
        self,
        file_path: Path,
        mime_type: str,
        folder_id: Optional[str] = None
    ) -> str:
        """
        Faz upload de arquivo para o Google Drive.
        Política atual: se já existir arquivo com o mesmo nome na pasta de destino, não sobrescreve e não duplica (pula o upload).
        
        Args:
            file_path: Caminho do arquivo local
            mime_type: Tipo MIME do arquivo
            folder_id: ID da pasta de destino (None = pasta raiz)
            
        Returns:
            ID do arquivo criado no Drive
            
        Raises:
            RuntimeError: Se o upload falhar
        """
        target_folder = folder_id or GOOGLE_DRIVE_ROOT_FOLDER_ID
        filename = file_path.name

        # Se já existe, pula
        if self.find_file_by_name(filename, target_folder):
            logger.info(f"Já existe arquivo '{filename}' em {target_folder}. Ignorando upload.")
            return ""
        
        try:
            with file_path.open("rb") as fh:
                media = MediaIoBaseUpload(fh, mimetype=mime_type, resumable=False)
                
                file_metadata = {
                    "name": filename,
                    "parents": [target_folder]
                }
                created = (
                    self.service.files()
                    .create(
                        body=file_metadata,
                        media_body=media,
                        fields="id, webViewLink",
                        supportsAllDrives=True,
                    )
                    .execute()
                )
                logger.info(
                    f"Arquivo {filename} enviado com sucesso: {created.get('id')}"
                )
                return created["id"]
        except HttpError as e:
            error_details = json.loads(e.content.decode("utf-8")) if e.content else {}
            logger.error(f"Erro ao enviar {filename}: {error_details}")
            raise RuntimeError(
                f"Falha ao enviar arquivo {filename}: {error_details.get('error', {}).get('message', str(e))}"
            ) from e
        except Exception as e:
            logger.error(f"Erro inesperado ao enviar {filename}: {e}")
            raise RuntimeError(f"Falha ao enviar arquivo {filename}: {e}") from e
    
    def get_root_folder_id(self) -> str:
        """
        Retorna o ID da pasta raiz configurada.
        
        Returns:
            ID da pasta raiz
        """
        return GOOGLE_DRIVE_ROOT_FOLDER_ID
    
    def ensure_folder(self, parent_id: str, folder_name: str) -> str:
        """
        Garante que a pasta existe, criando se necessário.
        
        Args:
            parent_id: ID da pasta pai
            folder_name: Nome da pasta a criar/buscar
            
        Returns:
            ID da pasta
            
        Raises:
            RuntimeError: Se não conseguir criar/buscar a pasta
        """
        # Escapa aspas simples na query
        folder_name_escaped = folder_name.replace("'", "\\'")
        query = (
            f"mimeType='application/vnd.google-apps.folder' and "
            f"trashed=false and name='{folder_name_escaped}' and '{parent_id}' in parents"
        )
        
        try:
            response = (
                self.service.files()
                .list(
                    q=query,
                    fields="files(id, name)",
                    pageSize=1,
                    supportsAllDrives=True,
                    includeItemsFromAllDrives=True,
                    corpora="allDrives",
                )
                .execute()
            )
            files = response.get("files", [])
            if files:
                logger.info(f"Pasta '{folder_name}' já existe: {files[0]['id']}")
                return files[0]["id"]
        except HttpError as e:
            logger.warning(f"Erro ao buscar pasta: {e}")
        
        # Cria a pasta se não existir
        metadata = {
            "name": folder_name,
            "mimeType": "application/vnd.google-apps.folder",
            "parents": [parent_id],
        }
        try:
            folder = (
                self.service.files()
                .create(body=metadata, fields="id", supportsAllDrives=True)
                .execute()
            )
            logger.info(f"Pasta '{folder_name}' criada: {folder['id']}")
            return folder["id"]
        except HttpError as e:
            logger.error(f"Erro ao criar pasta '{folder_name}': {e}")
            raise RuntimeError(f"Falha ao criar pasta no Drive: {e}") from e

