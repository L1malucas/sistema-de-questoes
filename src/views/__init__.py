from src.views.widgets import (
    LatexEditor,
    ImagePicker,
    TagTreeWidget,
    QuestaoCard,
    DifficultySelector,
    ImageInsertDialog,
    TableSizeDialog,
    TableEditorDialog,
    ColorPickerDialog,
)

from src.views.tag_manager import TagManager
from src.views.export_dialog import ExportDialog
from src.views.lista_form import ListaForm
from src.views.questao_selector_dialog import QuestaoSelectorDialog
from src.views.questao_preview import QuestaoPreview
from src.views.search_panel import SearchPanel, SearchPage
from src.views.lista_panel import ListaPanel, ListaPage
from src.views.questao_form import QuestaoForm, QuestaoFormPage

# New imports
from src.views.components.layout.navbar import Navbar
from src.views.components.layout.sidebar import Sidebar
from src.views.components.question.editor_tab import EditorTab
from src.views.components.question.preview_tab import PreviewTab
from src.views.components.question.tags_tab import TagsTab
from src.views.pages.dashboard_page import DashboardPage
from src.views.pages.question_bank_page import QuestionBankPage
from src.views.pages.exam_list_page import ExamListPage
from src.views.pages.taxonomy_page import TaxonomyPage
from src.views.pages.question_editor_page import QuestionEditorPage


__all__ = [
    # Widgets/Componentes
    'LatexEditor',
    'ImagePicker',
    'TagTreeWidget',
    'QuestaoCard',
    'DifficultySelector',
    'ImageInsertDialog',
    'TableSizeDialog',
    'TableEditorDialog',
    'ColorPickerDialog',
    # Paginas/Dialogos
    'TagManager',
    'ExportDialog',
    'ListaForm',
    'QuestaoSelectorDialog',
    'QuestaoPreview',
    'SearchPanel',
    'SearchPage',
    'ListaPanel',
    'ListaPage',
    'QuestaoForm',
    'QuestaoFormPage',
    # New components and pages
    'Navbar',
    'Sidebar',
    'EditorTab',
    'PreviewTab',
    'TagsTab',
    'DashboardPage',
    'QuestionBankPage',
    'ExamListPage',
    'TaxonomyPage',
    'QuestionEditorPage',
]
