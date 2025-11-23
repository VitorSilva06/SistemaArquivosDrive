"""Geração de relatórios de processamento."""
from typing import Dict, List


def build_report(
    nome: str,
    telefone: str,
    servico: str,
    field_status: Dict[str, Dict[str, str]],
    uploaded_files: List[Dict[str, str]],
    rejected_files: List[Dict[str, str]],
) -> str:
    """
    Gera relatório em texto do processamento.
    
    Args:
        nome: Nome do cliente
        telefone: Telefone do cliente
        servico: Serviço selecionado
        field_status: Status de cada campo do formulário
        uploaded_files: Lista de arquivos enviados
        rejected_files: Lista de arquivos rejeitados
        
    Returns:
        Conteúdo do relatório em texto
    """
    lines = [
        "Relatório do Atendimento",
        "========================",
        f"Nome: {nome}",
        f"Telefone: {telefone}",
        f"Serviço selecionado: {servico}",
        "",
        "Status dos campos:",
    ]

    for field_key, meta in field_status.items():
        label = meta.get("label", field_key)
        qty = meta.get("uploadedCount", 0)
        lines.append(
            f"- {label}: {'Documento anexado' if qty else 'Sem envio'} (Qtd: {qty})"
        )

    lines.extend(["", "Arquivos enviados ao Drive:"])
    if uploaded_files:
        for item in uploaded_files:
            lines.append(f"- {item['original_name']} -> {item['stored_name']}")
    else:
        lines.append("- Nenhum arquivo aprovado")

    if rejected_files:
        lines.extend(["", "Arquivos reprovados:"])
        for item in rejected_files:
            lines.append(f"- {item['filename']} ({item['reason']})")

    return "\n".join(lines)

