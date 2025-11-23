"""Validações de entrada e segurança."""
from fastapi import HTTPException
from PIL import Image
from typing import Tuple

from config import (
    MIN_WIDTH,
    MIN_HEIGHT,
    MIN_FILESIZE_KB,
    MAX_FILESIZE_MB,
    MIN_NAME_LENGTH,
    MIN_PHONE_LENGTH,
)
from utils import sanitize_phone


def validate_name(name: str) -> None:
    """
    Valida nome do cliente.
    
    Args:
        name: Nome a ser validado
        
    Raises:
        HTTPException: Se o nome for inválido
    """
    if not name or len(name.strip()) < MIN_NAME_LENGTH:
        raise HTTPException(
            status_code=400,
            detail=f"Nome deve ter pelo menos {MIN_NAME_LENGTH} caracteres."
        )


def validate_phone(phone: str) -> str:
    """
    Valida e sanitiza telefone.
    
    Args:
        phone: Telefone a ser validado
        
    Returns:
        Telefone sanitizado (apenas dígitos)
        
    Raises:
        HTTPException: Se o telefone for inválido
    """
    phone_digits = sanitize_phone(phone)
    if len(phone_digits) < MIN_PHONE_LENGTH:
        raise HTTPException(
            status_code=400,
            detail=f"Telefone inválido. Deve conter pelo menos {MIN_PHONE_LENGTH} dígitos."
        )
    return phone_digits


def validate_file_size(file_size_bytes: int) -> None:
    """
    Valida tamanho do arquivo.
    
    Args:
        file_size_bytes: Tamanho do arquivo em bytes
        
    Raises:
        HTTPException: Se o arquivo for muito grande
    """
    file_size_mb = file_size_bytes / (1024 * 1024)
    if file_size_mb > MAX_FILESIZE_MB:
        raise HTTPException(
            status_code=400,
            detail=(
                f"Arquivo muito grande ({file_size_mb:.2f} MB). "
                f"Máximo permitido: {MAX_FILESIZE_MB} MB."
            )
        )


def evaluate_image_quality(image: Image.Image, file_size_kb: float) -> Tuple[bool, str]:
    """
    Avalia qualidade da imagem.
    
    Args:
        image: Objeto PIL Image
        file_size_kb: Tamanho do arquivo em KB
        
    Returns:
        Tupla (is_valid, reason)
    """
    width, height = image.size
    
    if width < MIN_WIDTH or height < MIN_HEIGHT:
        return False, (
            f"Resolução insuficiente ({width}x{height} px). "
            f"Mínimo: {MIN_WIDTH}x{MIN_HEIGHT} px."
        )
    
    if file_size_kb < MIN_FILESIZE_KB:
        return False, (
            f"Tamanho do arquivo muito pequeno ({int(file_size_kb)} KB). "
            f"Mínimo: {MIN_FILESIZE_KB} KB."
        )
    
    return True, "OK"


def is_image_file(content_type: str, filename: str) -> bool:
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
    
    from pathlib import Path
    image_extensions = {".jpg", ".jpeg", ".png", ".bmp", ".gif", ".webp"}
    return Path(filename or "").suffix.lower() in image_extensions

