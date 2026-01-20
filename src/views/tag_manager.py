"""
View: Tag Manager
DESCRIÇÃO: Interface de gerenciamento de tags

NOTA: Este arquivo re-exporta da nova estrutura modular.
A implementação foi movida para src/views/pages/tag_manager_page.py
"""

import logging

# Re-exportar da nova estrutura para manter compatibilidade
from src.views.pages.tag_manager_page import TagManager

logger = logging.getLogger(__name__)

__all__ = ['TagManager']

logger.info("TagManager carregado (via re-export)")
