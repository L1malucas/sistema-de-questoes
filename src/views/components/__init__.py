"""
Views: Components
Componentes reutilizáveis da interface
"""

# Re-exports para facilitar imports
from src.views.components.forms.latex_editor import LatexEditor
from src.views.components.forms.tag_tree import TagTreeWidget
from src.views.components.forms.difficulty_selector import DifficultySelector
from src.views.components.forms.image_picker import ImagePicker
from src.views.components.cards.questao_card import QuestaoCard
from src.views.components.dialogs.image_insert_dialog import ImageInsertDialog
from src.views.components.dialogs.table_editor_dialog import TableSizeDialog, TableEditorDialog
from src.views.components.dialogs.color_picker_dialog import ColorPickerDialog

__all__ = [
    'LatexEditor',
    'TagTreeWidget',
    'DifficultySelector',
    'ImagePicker',
    'QuestaoCard',
    'ImageInsertDialog',
    'TableSizeDialog',
    'TableEditorDialog',
    'ColorPickerDialog',
]
