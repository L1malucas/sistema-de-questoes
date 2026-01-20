"""
View: Main Window
DESCRIÇÃO: Janela principal da aplicação

NOTA: Este arquivo re-exporta da nova estrutura modular.
A implementação foi movida para src/views/pages/main_window.py
"""

import logging

# Re-exportar da nova estrutura para manter compatibilidade
from src.views.pages.main_window import MainWindow

logger = logging.getLogger(__name__)

__all__ = ['MainWindow']

logger.info("MainWindow carregado (via re-export)")
