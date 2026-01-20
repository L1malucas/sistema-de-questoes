"""
View: Widgets Personalizados
DESCRIÇÃO: Componentes reutilizáveis da interface

NOTA: Este arquivo agora re-exporta os componentes da nova estrutura modular.
Os componentes foram movidos para src/views/components/ para melhor organização.

WIDGETS INCLUÍDOS:
    - LatexEditor: Editor de texto com suporte a LaTeX
    - ImagePicker: Seletor de imagens com preview
    - TagTreeWidget: Árvore de tags com checkboxes
    - QuestaoCard: Card de preview de questão
    - DifficultySelector: Seletor de dificuldade com ícones
    - ImageInsertDialog: Diálogo para inserir imagem
    - TableSizeDialog: Diálogo para tamanho de tabela
    - TableEditorDialog: Editor visual de tabelas
    - ColorPickerDialog: Seletor de cores
"""

import logging

# Re-exportar componentes da nova estrutura para manter compatibilidade
from src.views.components.forms.latex_editor import LatexEditor
from src.views.components.forms.image_picker import ImagePicker
from src.views.components.forms.tag_tree import TagTreeWidget
from src.views.components.forms.difficulty_selector import DifficultySelector
from src.views.components.cards.questao_card import QuestaoCard
from src.views.components.dialogs.image_insert_dialog import ImageInsertDialog
from src.views.components.dialogs.table_editor_dialog import TableSizeDialog, TableEditorDialog
from src.views.components.dialogs.color_picker_dialog import ColorPickerDialog

logger = logging.getLogger(__name__)

__all__ = [
    'LatexEditor',
    'ImagePicker',
    'TagTreeWidget',
    'QuestaoCard',
    'DifficultySelector',
    'ImageInsertDialog',
    'TableSizeDialog',
    'TableEditorDialog',
    'ColorPickerDialog',
]

logger.info("Widgets customizados carregados (via re-export)")
