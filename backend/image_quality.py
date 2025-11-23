"""Análise avançada de qualidade de imagem."""
import logging
import numpy as np
from PIL import Image
from typing import Tuple

logger = logging.getLogger(__name__)

# Thresholds para qualidade
MIN_SHARPNESS_SCORE = 100  # Variância de Laplaciano mínima
MIN_CONTRAST_SCORE = 0.15  # Contraste mínimo (desvio padrão normalizado)
MIN_BRIGHTNESS = 0.1  # Brilho mínimo (para evitar imagens muito escuras)
MAX_BRIGHTNESS = 0.95  # Brilho máximo (para evitar imagens muito claras)


def calculate_sharpness(image: Image.Image) -> float:
    """
    Calcula nitidez da imagem usando variância de Laplaciano.
    
    Valores mais altos indicam imagens mais nítidas.
    Valores baixos indicam imagens desfocadas/blur.
    
    Args:
        image: Imagem PIL
        
    Returns:
        Score de nitidez (0-1000+)
    """
    try:
        # Converte para escala de cinza e redimensiona se muito grande (para performance)
        gray = image.convert('L')
        width, height = gray.size
        
        # Redimensiona se muito grande (mantém proporção)
        max_dimension = 800
        if width > max_dimension or height > max_dimension:
            if width > height:
                new_width = max_dimension
                new_height = int(height * (max_dimension / width))
            else:
                new_height = max_dimension
                new_width = int(width * (max_dimension / height))
            gray = gray.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        img_array = np.array(gray, dtype=np.float32)
        
        # Aplica kernel Laplaciano usando slicing (mais eficiente)
        # Laplaciano: [[0, -1, 0], [-1, 4, -1], [0, -1, 0]]
        laplacian = (
            -img_array[1:-1, 0:-2]  # -1 * top
            - img_array[0:-2, 1:-1]  # -1 * left
            + 4 * img_array[1:-1, 1:-1]  # 4 * center
            - img_array[2:, 1:-1]  # -1 * bottom
            - img_array[1:-1, 2:]  # -1 * right
        )
        
        # Variância de Laplaciano = medida de nitidez
        variance = float(np.var(laplacian))
        return variance
    except Exception as e:
        logger.warning(f"Erro ao calcular nitidez: {e}")
        return 0.0


def calculate_contrast(image: Image.Image) -> float:
    """
    Calcula contraste da imagem usando desvio padrão.
    
    Args:
        image: Imagem PIL
        
    Returns:
        Score de contraste (0-1)
    """
    try:
        gray = image.convert('L')
        img_array = np.array(gray)
        
        # Desvio padrão normalizado (0-1)
        std = np.std(img_array)
        contrast = std / 255.0
        
        return contrast
    except Exception as e:
        logger.warning(f"Erro ao calcular contraste: {e}")
        return 0.0


def calculate_brightness(image: Image.Image) -> float:
    """
    Calcula brilho médio da imagem.
    
    Args:
        image: Imagem PIL
        
    Returns:
        Brilho médio (0-1)
    """
    try:
        gray = image.convert('L')
        img_array = np.array(gray)
        
        # Média normalizada
        brightness = np.mean(img_array) / 255.0
        
        return brightness
    except Exception as e:
        logger.warning(f"Erro ao calcular brilho: {e}")
        return 0.5


def evaluate_image_quality_advanced(
    image: Image.Image,
    file_size_kb: float,
    width: int,
    height: int
) -> Tuple[bool, str]:
    """
    Avalia qualidade da imagem usando múltiplas métricas.
    
    Args:
        image: Objeto PIL Image
        file_size_kb: Tamanho do arquivo em KB
        width: Largura da imagem
        height: Altura da imagem
        
    Returns:
        Tupla (is_valid, reason)
    """
    from config import MIN_WIDTH, MIN_HEIGHT, MIN_FILESIZE_KB
    
    # Validação básica de resolução
    if width < MIN_WIDTH or height < MIN_HEIGHT:
        return False, (
            f"Resolução insuficiente ({width}x{height} px). "
            f"Mínimo: {MIN_WIDTH}x{MIN_HEIGHT} px."
        )
    
    # Validação de tamanho
    if file_size_kb < MIN_FILESIZE_KB:
        return False, (
            f"Tamanho do arquivo muito pequeno ({int(file_size_kb)} KB). "
            f"Mínimo: {MIN_FILESIZE_KB} KB."
        )
    
    # Análise de nitidez
    sharpness = calculate_sharpness(image)
    if sharpness < MIN_SHARPNESS_SCORE:
        return False, (
            f"Imagem desfocada ou de baixa nitidez. "
            f"Score de nitidez: {sharpness:.1f} (mínimo: {MIN_SHARPNESS_SCORE}). "
            f"Por favor, tire uma nova foto com melhor foco e iluminação."
        )
    
    # Análise de contraste
    contrast = calculate_contrast(image)
    if contrast < MIN_CONTRAST_SCORE:
        return False, (
            f"Imagem com baixo contraste. "
            f"Score de contraste: {contrast:.3f} (mínimo: {MIN_CONTRAST_SCORE}). "
            f"Por favor, tire uma nova foto com melhor iluminação."
        )
    
    # Análise de brilho
    brightness = calculate_brightness(image)
    if brightness < MIN_BRIGHTNESS:
        return False, (
            f"Imagem muito escura. "
            f"Brilho: {brightness:.3f} (mínimo: {MIN_BRIGHTNESS}). "
            f"Por favor, tire uma nova foto com melhor iluminação."
        )
    
    if brightness > MAX_BRIGHTNESS:
        return False, (
            f"Imagem muito clara (superexposta). "
            f"Brilho: {brightness:.3f} (máximo: {MAX_BRIGHTNESS}). "
            f"Por favor, tire uma nova foto com iluminação adequada."
        )
    
    logger.info(
        f"Imagem aprovada - Nitidez: {sharpness:.1f}, "
        f"Contraste: {contrast:.3f}, Brilho: {brightness:.3f}"
    )
    
    return True, "OK"

