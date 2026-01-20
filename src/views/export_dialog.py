"""
View: Export Dialog
DESCRIÇÃO: Diálogo de configuração de exportação

NOTA: Este arquivo re-exporta da nova estrutura modular.
A implementação foi movida para src/views/pages/export_page.py
"""

import logging

# Re-exportar da nova estrutura para manter compatibilidade
from src.views.pages.export_page import ExportDialog

logger = logging.getLogger(__name__)

__all__ = ['ExportDialog']

logger.info("ExportDialog carregado (via re-export)")
