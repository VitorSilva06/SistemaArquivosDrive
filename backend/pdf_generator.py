"""Geração de PDFs a partir de texto."""
import logging
from pathlib import Path
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

logger = logging.getLogger(__name__)


def create_password_pdf(password: str, output_path: Path) -> bool:
    """
    Cria um PDF com a senha informada.
    
    Args:
        password: Senha a ser incluída no PDF
        output_path: Caminho onde salvar o PDF
        
    Returns:
        True se criado com sucesso
    """
    try:
        c = canvas.Canvas(str(output_path), pagesize=letter)
        width, height = letter
        
        # Título
        c.setFont("Helvetica-Bold", 16)
        c.drawString(100, height - 100, "Senha do Meu INSS")
        
        # Senha
        c.setFont("Helvetica", 14)
        c.drawString(100, height - 150, f"Senha: {password}")
        
        c.save()
        logger.info(f"PDF de senha criado: {output_path}")
        return True
    except Exception as e:
        logger.error(f"Erro ao criar PDF de senha: {e}")
        return False

