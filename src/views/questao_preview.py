"""
View: Questão Preview
DESCRIÇÃO: Janela modal de visualização da questão no formato PDF

NOTA: Este arquivo re-exporta da nova estrutura modular.
A implementação foi movida para src/views/pages/questao_preview_page.py
"""

import logging

# Re-exportar da nova estrutura para manter compatibilidade
from src.views.pages.questao_preview_page import QuestaoPreview

logger = logging.getLogger(__name__)

__all__ = ['QuestaoPreview']

logger.info("QuestaoPreview carregado (via re-export)")
