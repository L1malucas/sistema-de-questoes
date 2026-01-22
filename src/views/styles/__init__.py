"""
Styles
Temas e estilos da aplicação
"""
from pathlib import Path

# Caminho do arquivo de estilos
STYLES_DIR = Path(__file__).parent
MATHBANK_QSS = STYLES_DIR / "mathbank.qss"


def load_stylesheet(name: str = "mathbank") -> str:
    """
    Carrega um arquivo de estilos.

    Args:
        name: Nome do arquivo de estilos (sem extensão)

    Returns:
        Conteúdo do arquivo de estilos ou string vazia se não encontrado
    """
    style_file = STYLES_DIR / f"{name}.qss"
    if style_file.exists():
        return style_file.read_text(encoding='utf-8')
    return ""


__all__ = ['load_stylesheet', 'MATHBANK_QSS', 'STYLES_DIR']
