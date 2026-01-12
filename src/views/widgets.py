"""
View: Widgets Personalizados
DESCRIÇÃO: Componentes reutilizáveis da interface
WIDGETS INCLUÍDOS:
    - LatexEditor: Editor de texto com suporte a LaTeX
    - ImagePicker: Seletor de imagens com preview
    - TagTreeWidget: Árvore de tags com checkboxes
    - QuestaoCard: Card de preview de questão
    - DifficultySelector: Seletor de dificuldade com ícones
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTextEdit, QLineEdit, QComboBox, QTreeWidget, QTreeWidgetItem,
    QFrame, QGroupBox, QFileDialog, QScrollArea, QRadioButton,
    QButtonGroup, QSpinBox, QTreeWidgetItemIterator
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QPixmap, QFont
import logging
from pathlib import Path
from typing import List

# Importar DTO para type hinting
from src.application.dtos.tag_dto import TagResponseDTO

logger = logging.getLogger(__name__)


class LatexEditor(QWidget):
    """
    Editor de texto com suporte a LaTeX.
    Permite inserir comandos LaTeX comuns via botões.
    """

    textChanged = pyqtSignal()

    def __init__(self, placeholder="Digite o texto (suporta LaTeX)...", parent=None):
        super().__init__(parent)
        self.init_ui(placeholder)

    def init_ui(self, placeholder):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        toolbar = QHBoxLayout()
        latex_buttons = [
            ("Fração", r"\frac{}{}"), ("Raiz", r"\sqrt{}"), ("Potência", r"^{}"),
            ("Subscrito", r"_{}"), ("Somatório", r"\sum_{}^{}"), ("Integral", r"\int_{}^{}"),
            ("Pi", r"\pi"), ("Alfa", r"\alpha"), ("Beta", r"\beta"),
        ]
        for label, command in latex_buttons:
            btn = QPushButton(label)
            btn.setMaximumWidth(80)
            btn.clicked.connect(lambda checked, cmd=command: self.insert_latex(cmd))
            toolbar.addWidget(btn)
        toolbar.addStretch()
        layout.addLayout(toolbar)
        self.text_edit = QTextEdit()
        self.text_edit.setPlaceholderText(placeholder)
        self.text_edit.setMinimumHeight(150)
        self.text_edit.textChanged.connect(self.textChanged.emit)
        layout.addWidget(self.text_edit)
        info_label = QLabel("Use comandos LaTeX para fórmulas matemáticas. Ex: $x^2 + y^2 = z^2$")
        info_label.setStyleSheet("color: #666; font-size: 10px;")
        layout.addWidget(info_label)

    def insert_latex(self, command):
        cursor = self.text_edit.textCursor()
        cursor.insertText(command)
        self.text_edit.setFocus()

    def get_text(self):
        return self.text_edit.toPlainText()

    def set_text(self, text):
        self.text_edit.setPlainText(text)

    def clear(self):
        self.text_edit.clear()


class ImagePicker(QWidget):
    """Seletor de imagens com preview."""
    imageChanged = pyqtSignal(str)

    def __init__(self, label="Imagem:", parent=None):
        super().__init__(parent)
        self.image_path = None
        self.init_ui(label)

    def init_ui(self, label):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        top_layout = QHBoxLayout()
        top_layout.addWidget(QLabel(label))
        self.btn_select = QPushButton("Selecionar Imagem")
        self.btn_select.clicked.connect(self.select_image)
        top_layout.addWidget(self.btn_select)
        self.btn_clear = QPushButton("Remover")
        self.btn_clear.clicked.connect(self.clear_image)
        self.btn_clear.setEnabled(False)
        top_layout.addWidget(self.btn_clear)
        top_layout.addStretch()
        layout.addLayout(top_layout)
        self.preview_label = QLabel("Nenhuma imagem selecionada")
        self.preview_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.preview_label.setMinimumHeight(150)
        self.preview_label.setMaximumHeight(300)
        self.preview_label.setStyleSheet("border: 2px dashed #ccc; border-radius: 5px; background-color: #f5f5f5;")
        layout.addWidget(self.preview_label)
        scale_layout = QHBoxLayout()
        scale_layout.addWidget(QLabel("Escala para LaTeX:"))
        self.scale_spin = QSpinBox()
        self.scale_spin.setRange(10, 100)
        self.scale_spin.setValue(70)
        self.scale_spin.setSuffix("%")
        scale_layout.addWidget(self.scale_spin)
        scale_layout.addStretch()
        layout.addLayout(scale_layout)

    def select_image(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Selecionar Imagem", "", "Imagens (*.png *.jpg *.jpeg *.gif *.bmp *.svg)")
        if file_path:
            self.image_path = file_path
            self.load_preview()
            self.btn_clear.setEnabled(True)
            self.imageChanged.emit(file_path)

    def load_preview(self):
        if self.image_path:
            pixmap = QPixmap(self.image_path)
            if not pixmap.isNull():
                scaled_pixmap = pixmap.scaled(400, 300, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
                self.preview_label.setPixmap(scaled_pixmap)
            else:
                self.preview_label.setText("Erro ao carregar imagem")

    def clear_image(self):
        self.image_path = None
        self.preview_label.clear()
        self.preview_label.setText("Nenhuma imagem selecionada")
        self.btn_clear.setEnabled(False)
        self.imageChanged.emit("")

    def get_image_path(self):
        return self.image_path

    def get_scale(self):
        return self.scale_spin.value() / 100.0

    def set_image(self, path, scale=0.7):
        if path and Path(path).exists():
            self.image_path = path
            self.load_preview()
            self.btn_clear.setEnabled(True)
            self.scale_spin.setValue(int(scale * 100))


class TagTreeWidget(QWidget):
    """Árvore de tags com checkboxes."""
    selectionChanged = pyqtSignal(list)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        label = QLabel("Tags:")
        label.setStyleSheet("font-weight: bold;")
        layout.addWidget(label)
        self.tree = QTreeWidget()
        self.tree.setHeaderLabel("Selecione as tags")
        self.tree.setMinimumHeight(200)
        self.tree.itemChanged.connect(self.on_item_changed)
        layout.addWidget(self.tree)
        btn_layout = QHBoxLayout()
        btn_expand = QPushButton("Expandir Tudo")
        btn_expand.clicked.connect(self.tree.expandAll)
        btn_layout.addWidget(btn_expand)
        btn_collapse = QPushButton("Recolher Tudo")
        btn_collapse.clicked.connect(self.tree.collapseAll)
        btn_layout.addWidget(btn_collapse)
        btn_clear = QPushButton("Limpar Seleção")
        btn_clear.clicked.connect(self.clear_selection)
        btn_layout.addWidget(btn_clear)
        btn_layout.addStretch()
        layout.addLayout(btn_layout)

    def _add_items_recursively(self, parent_item, tags: List[TagResponseDTO]):
        """Helper recursivo para popular a árvore a partir de DTOs."""
        for tag_dto in tags:
            item = QTreeWidgetItem(parent_item)
            item.setText(0, tag_dto.nome)
            item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
            item.setCheckState(0, Qt.CheckState.Unchecked)
            item.setData(0, Qt.ItemDataRole.UserRole, tag_dto.id_tag)
            if tag_dto.filhos:
                self._add_items_recursively(item, tag_dto.filhos)

    def load_tags(self, tags_arvore: List[TagResponseDTO]):
        """Carrega uma árvore de tags DTOs no widget."""
        self.tree.clear()
        self._add_items_recursively(self.tree, tags_arvore)
        self.tree.expandAll()

    def on_item_changed(self, item, column):
        self.selectionChanged.emit(self.get_selected_tag_ids())

    def get_selected_tag_ids(self) -> List[int]:
        """Retorna lista de IDs das tags selecionadas (marcadas)."""
        selected_ids = []
        iterator = QTreeWidgetItemIterator(self.tree)
        while iterator.value():
            item = iterator.value()
            if item.checkState(0) == Qt.CheckState.Checked:
                tag_id = item.data(0, Qt.ItemDataRole.UserRole)
                if tag_id is not None:
                    selected_ids.append(tag_id)
            iterator += 1
        return selected_ids

    def set_selected_tags(self, tag_ids: List[int]):
        """Marca os checkboxes para a lista de IDs de tags fornecida."""
        if not tag_ids:
            return
        
        # Usar um set para busca mais rápida
        ids_to_check = set(tag_ids)
        
        iterator = QTreeWidgetItemIterator(self.tree)
        while iterator.value():
            item = iterator.value()
            tag_id = item.data(0, Qt.ItemDataRole.UserRole)
            if tag_id in ids_to_check:
                # Bloquear sinais para evitar emissão massiva durante o carregamento
                self.tree.blockSignals(True)
                item.setCheckState(0, Qt.CheckState.Checked)
                self.tree.blockSignals(False)
            iterator += 1

    def clear_selection(self):
        iterator = QTreeWidgetItemIterator(self.tree)
        while iterator.value():
            iterator.value().setCheckState(0, Qt.CheckState.Unchecked)
            iterator += 1


class QuestaoCard(QFrame):
    """Card de preview de questão para exibição em listas."""
    clicked = pyqtSignal(int)
    editClicked = pyqtSignal(int)
    deleteClicked = pyqtSignal(int)
    addToListClicked = pyqtSignal(int) # Novo sinal para "Adicionar à Lista"

    def __init__(self, questao_dto: 'QuestaoResponseDTO', parent=None):
        super().__init__(parent)
        self.questao_id = questao_dto.id
        self.init_ui(questao_dto)

    def init_ui(self, dto: 'QuestaoResponseDTO'):
        self.setFrameStyle(QFrame.Shape.StyledPanel | QFrame.Shadow.Raised)
        self.setStyleSheet("""
            QFrame {
                border: 1px solid #ddd;
                border-radius: 5px;
                background-color: white;
                padding: 15px;
            }
            QFrame:hover {
                border-color: #1abc9c;
                background-color: #f0fff4;
            }
        """)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        layout = QVBoxLayout(self)

        # Cabeçalho
        header_layout = QHBoxLayout()

        # Título
        titulo = dto.titulo or 'Sem título'
        title_label = QLabel(titulo)
        title_label.setStyleSheet("font-weight: bold; font-size: 14px; color: #2c3e50;")
        title_label.setWordWrap(True)
        header_layout.addWidget(title_label, 1)

        # Badge de tipo
        tipo_label = QLabel(dto.tipo)
        tipo_color = "#2196f3" if dto.tipo == 'OBJETIVA' else "#9c27b0"
        tipo_label.setStyleSheet(f"""
            QLabel {{
                background-color: {tipo_color};
                color: white;
                padding: 4px 10px;
                border-radius: 3px;
                font-size: 11px;
                font-weight: bold;
            }}
        """)
        header_layout.addWidget(tipo_label)

        layout.addLayout(header_layout)

        # Preview do enunciado
        enunciado_preview = (dto.enunciado[:150] + "...") if len(dto.enunciado) > 150 else dto.enunciado
        enunciado_label = QLabel(enunciado_preview)
        enunciado_label.setStyleSheet("color: #555; margin-top: 8px; font-size: 12px;")
        enunciado_label.setWordWrap(True)
        layout.addWidget(enunciado_label)

        # Metadados
        meta_layout = QHBoxLayout()
        meta_layout.setContentsMargins(0, 10, 0, 5)

        meta_text = f"📚 {dto.fonte or 'N/A'} • 📅 {dto.ano or 'N/A'} • ⭐ {dto.dificuldade_nome or 'N/A'}"
        meta_label = QLabel(meta_text)
        meta_label.setStyleSheet("color: #777; font-size: 11px;")
        meta_layout.addWidget(meta_label)

        meta_layout.addStretch()
        layout.addLayout(meta_layout)

        # Botões de ação
        btn_layout = QHBoxLayout()

        btn_visualizar = QPushButton("👁️ Visualizar")
        btn_visualizar.setMaximumWidth(100)
        btn_visualizar.clicked.connect(lambda: self.clicked.emit(self.questao_id)) # Conectar ao clicked do card
        btn_layout.addWidget(btn_visualizar)

        btn_editar = QPushButton("✏️ Editar")
        btn_editar.setMaximumWidth(100)
        btn_editar.clicked.connect(lambda: self.editClicked.emit(self.questao_id))
        btn_layout.addWidget(btn_editar)

        btn_adicionar = QPushButton("➕ Adicionar à Lista")
        btn_adicionar.setMaximumWidth(150)
        btn_adicionar.clicked.connect(lambda: self.addToListClicked.emit(self.questao_id)) # Conectar ao novo sinal
        btn_layout.addWidget(btn_adicionar)

        btn_layout.addStretch()

        btn_excluir = QPushButton("🗑️")
        btn_excluir.setMaximumWidth(40)
        btn_excluir.setStyleSheet("QPushButton { color: #e74c3c; }")
        btn_excluir.clicked.connect(lambda: self.deleteClicked.emit(self.questao_id))
        btn_layout.addWidget(btn_excluir)

        layout.addLayout(btn_layout)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit(self.questao_id)
        super().mousePressEvent(event)


class DifficultySelector(QWidget):
    """Seletor de dificuldade com radio buttons."""
    difficultyChanged = pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        label = QLabel("Dificuldade:")
        layout.addWidget(label)
        self.button_group = QButtonGroup(self)
        difficulties = [
            (1, "⭐ FÁCIL", "#4caf50"),
            (2, "⭐⭐ MÉDIO", "#ff9800"),
            (3, "⭐⭐⭐ DIFÍCIL", "#f44336")
        ]
        for diff_id, label_text, color in difficulties:
            radio = QRadioButton(label_text)
            radio.setStyleSheet(f"QRadioButton {{ color: {color}; font-weight: bold; }}")
            self.button_group.addButton(radio, diff_id)
            layout.addWidget(radio)
        layout.addStretch()
        self.button_group.idClicked.connect(self.difficultyChanged.emit)

    def get_selected_difficulty(self):
        return self.button_group.checkedId()

    def set_difficulty(self, difficulty_id):
        button = self.button_group.button(difficulty_id)
        if button:
            button.setChecked(True)


logger.info("Widgets customizados carregados")