"""
Views: Pages
Paginas completas da aplicacao (telas principais)
"""

from src.views.pages.main_window import MainWindow
from src.views.pages.tag_manager_page import TagManager
from src.views.pages.export_page import ExportDialog
from src.views.pages.questao_selector_page import QuestaoSelectorDialog, SelectableQuestionCard
from src.views.pages.questao_preview_page import QuestaoPreview
from src.views.pages.dashboard_page import DashboardPage

__all__ = [
    'MainWindow',
    'TagManager',
    'ExportDialog',
    'QuestaoSelectorDialog',
    'SelectableQuestionCard',
    'QuestaoPreview',
    'DashboardPage',
]
