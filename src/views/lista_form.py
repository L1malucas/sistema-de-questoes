"""
View: Lista Form
DESCRIÇÃO: Formulário de criação/edição de listas de questões

NOTA: Este arquivo re-exporta da nova estrutura modular.
A implementação foi movida para src/views/pages/lista_form_page.py
"""

import logging

# Re-exportar da nova estrutura para manter compatibilidade
from src.views.pages.lista_form_page import ListaForm

logger = logging.getLogger(__name__)

__all__ = ['ListaForm']

logger.info("ListaForm carregado (via re-export)")
