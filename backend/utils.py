"""Funções utilitárias para sanitização e formatação."""
import re
import unicodedata
from pathlib import Path
from typing import Optional

from config import MAX_FOLDER_NAME_LENGTH, MAX_FILENAME_LENGTH


def slugify(value: str) -> str:
    """
    Normaliza e sanitiza string para uso em nomes de pastas/arquivos.
    
    Args:
        value: String a ser normalizada
        
    Returns:
        String normalizada e sanitizada
    """
    if not value:
        return "cliente"
    
    # Normaliza caracteres unicode (remove acentos)
    value = unicodedata.normalize("NFKD", value)
    value = value.encode("ascii", "ignore").decode("ascii")
    value = value.strip().lower()
    
    # Remove caracteres especiais, mantém apenas letras, números, espaços e hífens
    value = re.sub(r"[^\w\s-]", "", value)
    # Substitui múltiplos espaços/hífens por um único hífen
    value = re.sub(r"[\s_-]+", "-", value)
    value = value.strip("-")
    
    # Limita tamanho
    if len(value) > MAX_FOLDER_NAME_LENGTH:
        value = value[:MAX_FOLDER_NAME_LENGTH].rstrip("-")
    
    return value or "cliente"


def sanitize_phone(phone: str) -> str:
    """
    Remove caracteres não numéricos do telefone.
    
    Args:
        phone: Número de telefone com formatação
        
    Returns:
        Apenas dígitos numéricos
    """
    if not phone:
        return ""
    return re.sub(r"\D", "", phone)


def sanitize_filename(filename: str) -> str:
    """
    Sanitiza nome de arquivo removendo caracteres inválidos.
    
    Args:
        filename: Nome do arquivo original
        
    Returns:
        Nome sanitizado e seguro
    """
    if not filename:
        return "arquivo"
    
    # Remove caracteres perigosos para sistemas de arquivos
    filename = re.sub(r'[<>:"/\\|?*]', "_", filename)
    # Remove espaços múltiplos
    filename = re.sub(r"\s+", "_", filename)
    
    # Limita tamanho (mantém extensão)
    if len(filename) > MAX_FILENAME_LENGTH:
        path_obj = Path(filename)
        stem = path_obj.stem[:190]
        ext = path_obj.suffix
        filename = stem + ext
    
    return filename or "arquivo"


def validate_file_extension(filename: str, allowed_extensions: Optional[set] = None) -> bool:
    """
    Valida extensão do arquivo.
    
    Args:
        filename: Nome do arquivo
        allowed_extensions: Set de extensões permitidas (None = todas)
        
    Returns:
        True se a extensão for permitida
    """
    if not filename:
        return False
    
    if allowed_extensions is None:
        return True
    
    ext = Path(filename).suffix.lower()
    return ext in allowed_extensions


def format_file_size(size_bytes: int) -> str:
    """
    Formata tamanho de arquivo em formato legível.
    
    Args:
        size_bytes: Tamanho em bytes
        
    Returns:
        String formatada (ex: "1.5 MB")
    """
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} TB"

