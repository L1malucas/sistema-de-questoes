"""
View: Questao Selector Dialog
DESCRICAO: Dialogo para selecionar questoes para adicionar a uma lista

NOTA: Este arquivo re-exporta da nova estrutura modular.
A implementação foi movida para src/views/pages/questao_selector_page.py
"""

import logging

# Re-exportar da nova estrutura para manter compatibilidade
from src.views.pages.questao_selector_page import QuestaoSelectorDialog, QuestaoSelectorCard

logger = logging.getLogger(__name__)

__all__ = ['QuestaoSelectorDialog', 'QuestaoSelectorCard']

logger.info("QuestaoSelectorDialog carregado (via re-export)")
