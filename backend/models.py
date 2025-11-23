"""Modelos de dados e schemas."""
from typing import Dict, List, Optional
from pydantic import BaseModel, Field


class RejectedFile(BaseModel):
    """Modelo para arquivo rejeitado."""
    filename: str
    reason: str
    field_id: str
    field_label: str


class ProcessedFile(BaseModel):
    """Modelo para arquivo processado."""
    path: str
    stored_name: str
    mime: str
    original_name: str
    field_id: str
    field_label: str


class SubmitResponse(BaseModel):
    """Resposta do endpoint de submissão."""
    message: str
    cliente: str
    prefixo_arquivos: str
    arquivos_aprovados: int
    arquivos_enviados: int
    arquivos_rejeitados: List[Dict]


class FieldStatus(BaseModel):
    """Status de um campo do formulário."""
    label: str
    uploadedCount: int = Field(alias="uploadedCount")
    value: Optional[str] = None

