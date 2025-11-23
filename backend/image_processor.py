"""Processamento e conversão de imagens."""
import io
import logging
from pathlib import Path
from typing import Tuple, Optional

from PIL import Image, UnidentifiedImageError

from image_quality import evaluate_image_quality_advanced

logger = logging.getLogger(__name__)


class ImageProcessor:
    """Classe para processar e converter imagens."""
    
    @staticmethod
    def is_image(content_type: Optional[str], filename: str) -> bool:
        """
        Verifica se o arquivo é uma imagem.
        
        Args:
            content_type: Content-Type do arquivo
            filename: Nome do arquivo
            
        Returns:
            True se for imagem
        """
        if content_type:
            return content_type.startswith("image/")
        
        image_extensions = {".jpg", ".jpeg", ".png", ".bmp", ".gif", ".webp"}
        return Path(filename or "").suffix.lower() in image_extensions
    
    @staticmethod
    def process_image(
        contents: bytes,
        source_filename: str,
        output_path: Path
    ) -> Tuple[bool, Optional[str], Optional[str]]:
        """
        Processa imagem: valida qualidade e converte para PDF.
        
        Args:
            contents: Conteúdo binário da imagem
            source_filename: Nome do arquivo original
            output_path: Caminho onde salvar o PDF
            
        Returns:
            Tupla (success, pdf_path, error_message)
        """
        try:
            with Image.open(io.BytesIO(contents)) as image:
                file_size_kb = len(contents) / 1024
                width, height = image.size
                
                # Valida qualidade avançada (nitidez, contraste, brilho)
                is_valid, reason = evaluate_image_quality_advanced(
                    image, file_size_kb, width, height
                )
                if not is_valid:
                    return False, None, reason
                
                # Converte para PDF
                try:
                    pdf_path = output_path
                    image_rgb = image.convert("RGB")
                    image_rgb.save(pdf_path, "PDF", resolution=300.0)
                    logger.info(f"Imagem {source_filename} convertida para PDF: {pdf_path.name}")
                    return True, str(pdf_path), None
                except Exception as e:
                    logger.error(f"Erro ao converter imagem para PDF: {e}")
                    return False, None, f"Erro ao converter imagem: {str(e)}"
        
        except UnidentifiedImageError:
            return False, None, "Imagem inválida ou corrompida."
        except Exception as e:
            logger.error(f"Erro ao processar imagem {source_filename}: {e}")
            return False, None, f"Erro ao processar imagem: {str(e)}"

