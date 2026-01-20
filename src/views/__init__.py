"""
Views Package
Contém todas as views (páginas e componentes) da aplicação

Estrutura:
    - pages/: Páginas completas (telas principais)
    - components/: Componentes reutilizáveis
        - layout/: Componentes de layout (header, sidebar)
        - cards/: Cards de exibição de dados
        - forms/: Componentes de formulário
        - filters/: Componentes de filtro e busca
        - dialogs/: Diálogos modais
        - common/: Componentes genéricos
    - styles/: Estilos e temas
"""

# Re-exports para compatibilidade com imports existentes
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
    # Páginas/Diálogos
    'TagManager',
    'ExportDialog',
    'ListaForm',
    'QuestaoSelectorDialog',
    'QuestaoPreview',
]
