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
    QButtonGroup, QSpinBox
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QPixmap, QFont
import logging
from pathlib import Path

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

        # Barra de ferramentas LaTeX
        toolbar = QHBoxLayout()

        # Botões de comandos LaTeX comuns
        latex_buttons = [
            ("Fração", r"\frac{}{}"),
            ("Raiz", r"\sqrt{}"),
            ("Potência", r"^{}"),
            ("Subscrito", r"_{}"),
            ("Somatório", r"\sum_{}^{}"),
            ("Integral", r"\int_{}^{}"),
            ("Pi", r"\pi"),
            ("Alfa", r"\alpha"),
            ("Beta", r"\beta"),
        ]

        for label, command in latex_buttons:
            btn = QPushButton(label)
            btn.setMaximumWidth(80)
            btn.clicked.connect(lambda checked, cmd=command: self.insert_latex(cmd))
            toolbar.addWidget(btn)

        toolbar.addStretch()
        layout.addLayout(toolbar)

        # Editor de texto
        self.text_edit = QTextEdit()
        self.text_edit.setPlaceholderText(placeholder)
        self.text_edit.setMinimumHeight(150)
        self.text_edit.textChanged.connect(self.textChanged.emit)
        layout.addWidget(self.text_edit)

        # Label informativo
        info_label = QLabel("Use comandos LaTeX para fórmulas matemáticas. Ex: $x^2 + y^2 = z^2$")
        info_label.setStyleSheet("color: #666; font-size: 10px;")
        layout.addWidget(info_label)

    def insert_latex(self, command):
        """Insere comando LaTeX no cursor"""
        cursor = self.text_edit.textCursor()
        cursor.insertText(command)
        self.text_edit.setFocus()

    def get_text(self):
        """Retorna o texto do editor"""
        return self.text_edit.toPlainText()

    def set_text(self, text):
        """Define o texto do editor"""
        self.text_edit.setPlainText(text)

    def clear(self):
        """Limpa o editor"""
        self.text_edit.clear()


class ImagePicker(QWidget):
    """
    Seletor de imagens com preview.
    Permite selecionar arquivo de imagem e visualizar.
    """

    imageChanged = pyqtSignal(str)  # Emite caminho da imagem

    def __init__(self, label="Imagem:", parent=None):
        super().__init__(parent)
        self.image_path = None
        self.init_ui(label)

    def init_ui(self, label):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # Label e botão
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

        # Preview da imagem
        self.preview_label = QLabel("Nenhuma imagem selecionada")
        self.preview_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.preview_label.setMinimumHeight(150)
        self.preview_label.setMaximumHeight(300)
        self.preview_label.setStyleSheet("""
            QLabel {
                border: 2px dashed #ccc;
                border-radius: 5px;
                background-color: #f5f5f5;
            }
        """)
        layout.addWidget(self.preview_label)

        # Escala da imagem
        scale_layout = QHBoxLayout()
        scale_layout.addWidget(QLabel("Escala para LaTeX:"))

        self.scale_spin = QSpinBox()
        self.scale_spin.setMinimum(10)
        self.scale_spin.setMaximum(100)
        self.scale_spin.setValue(70)
        self.scale_spin.setSuffix("%")
        scale_layout.addWidget(self.scale_spin)
        scale_layout.addStretch()

        layout.addLayout(scale_layout)

    def select_image(self):
        """Abre diálogo para selecionar imagem"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Selecionar Imagem",
            "",
            "Imagens (*.png *.jpg *.jpeg *.gif *.bmp *.svg)"
        )

        if file_path:
            self.image_path = file_path
            self.load_preview()
            self.btn_clear.setEnabled(True)
            self.imageChanged.emit(file_path)

    def load_preview(self):
        """Carrega preview da imagem"""
        if self.image_path:
            pixmap = QPixmap(self.image_path)
            if not pixmap.isNull():
                # Redimensionar mantendo proporção
                scaled_pixmap = pixmap.scaled(
                    400, 300,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation
                )
                self.preview_label.setPixmap(scaled_pixmap)
            else:
                self.preview_label.setText("Erro ao carregar imagem")

    def clear_image(self):
        """Remove imagem selecionada"""
        self.image_path = None
        self.preview_label.clear()
        self.preview_label.setText("Nenhuma imagem selecionada")
        self.btn_clear.setEnabled(False)
        self.imageChanged.emit("")

    def get_image_path(self):
        """Retorna caminho da imagem"""
        return self.image_path

    def get_scale(self):
        """Retorna escala da imagem (0.0 a 1.0)"""
        return self.scale_spin.value() / 100.0

    def set_image(self, path, scale=0.7):
        """Define imagem e escala"""
        if path and Path(path).exists():
            self.image_path = path
            self.load_preview()
            self.btn_clear.setEnabled(True)
            self.scale_spin.setValue(int(scale * 100))


class TagTreeWidget(QWidget):
    """
    Árvore de tags com checkboxes.
    Exibe tags hierárquicas e permite seleção múltipla.
    """

    selectionChanged = pyqtSignal(list)  # Emite lista de IDs selecionados

    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # Label
        label = QLabel("Tags:")
        label.setStyleSheet("font-weight: bold;")
        layout.addWidget(label)

        # Tree widget
        self.tree = QTreeWidget()
        self.tree.setHeaderLabel("Selecione as tags")
        self.tree.setMinimumHeight(200)
        self.tree.itemChanged.connect(self.on_item_changed)
        layout.addWidget(self.tree)

        # Botões
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

    def load_tags(self, tags_data):
        """
        Carrega tags na árvore.
        tags_data: lista de dicts com {id, nome, id_pai, nivel}
        """
        self.tree.clear()

        # Criar dicionário de items por ID
        items = {}

        # Ordenar por nível para garantir que pais sejam criados antes
        sorted_tags = sorted(tags_data, key=lambda x: x.get('nivel', 0))

        for tag in sorted_tags:
            tag_id = tag['id']
            nome = tag['nome']
            id_pai = tag.get('id_pai')

            # Criar item
            if id_pai and id_pai in items:
                # Adicionar como filho
                item = QTreeWidgetItem(items[id_pai])
            else:
                # Adicionar na raiz
                item = QTreeWidgetItem(self.tree)

            item.setText(0, nome)
            item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
            item.setCheckState(0, Qt.CheckState.Unchecked)
            item.setData(0, Qt.ItemDataRole.UserRole, tag_id)

            items[tag_id] = item

        self.tree.expandAll()

    def on_item_changed(self, item, column):
        """Callback quando item é alterado"""
        self.selectionChanged.emit(self.get_selected_tag_ids())

    def get_selected_tag_ids(self):
        """Retorna lista de IDs das tags selecionadas"""
        selected = []

        def traverse(item):
            if item.checkState(0) == Qt.CheckState.Checked:
                tag_id = item.data(0, Qt.ItemDataRole.UserRole)
                selected.append(tag_id)

            for i in range(item.childCount()):
                traverse(item.child(i))

        for i in range(self.tree.topLevelItemCount()):
            traverse(self.tree.topLevelItem(i))

        return selected

    def set_selected_tags(self, tag_ids):
        """Define tags selecionadas por ID"""
        def traverse(item):
            tag_id = item.data(0, Qt.ItemDataRole.UserRole)
            if tag_id in tag_ids:
                item.setCheckState(0, Qt.CheckState.Checked)

            for i in range(item.childCount()):
                traverse(item.child(i))

        for i in range(self.tree.topLevelItemCount()):
            traverse(self.tree.topLevelItem(i))

    def clear_selection(self):
        """Limpa todas as seleções"""
        def traverse(item):
            item.setCheckState(0, Qt.CheckState.Unchecked)
            for i in range(item.childCount()):
                traverse(item.child(i))

        for i in range(self.tree.topLevelItemCount()):
            traverse(self.tree.topLevelItem(i))


class QuestaoCard(QFrame):
    """
    Card de preview de questão para exibição em listas.
    """

    clicked = pyqtSignal(int)  # Emite ID da questão
    editClicked = pyqtSignal(int)
    deleteClicked = pyqtSignal(int)

    def __init__(self, questao_data, parent=None):
        super().__init__(parent)
        self.questao_id = questao_data.get('id')
        self.init_ui(questao_data)

    def init_ui(self, data):
        self.setFrameStyle(QFrame.Shape.StyledPanel | QFrame.Shadow.Raised)
        self.setStyleSheet("""
            QFrame {
                border: 1px solid #ddd;
                border-radius: 5px;
                background-color: white;
                padding: 10px;
            }
            QFrame:hover {
                border-color: #0078d4;
                background-color: #f0f8ff;
            }
        """)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        layout = QVBoxLayout(self)

        # Cabeçalho
        header_layout = QHBoxLayout()

        # Título ou preview do enunciado
        titulo = data.get('titulo', 'Sem título')
        enunciado = data.get('enunciado', '')
        preview_text = titulo if titulo else enunciado[:100] + "..."

        title_label = QLabel(preview_text)
        title_label.setStyleSheet("font-weight: bold; font-size: 13px;")
        title_label.setWordWrap(True)
        header_layout.addWidget(title_label, 1)

        # Tipo
        tipo_label = QLabel(data.get('tipo', 'N/A'))
        tipo_label.setStyleSheet("""
            QLabel {
                background-color: #e3f2fd;
                color: #1976d2;
                padding: 3px 8px;
                border-radius: 3px;
                font-size: 10px;
            }
        """)
        header_layout.addWidget(tipo_label)

        layout.addLayout(header_layout)

        # Metadados
        meta_layout = QHBoxLayout()

        fonte = data.get('fonte', 'N/A')
        ano = data.get('ano', 'N/A')
        dificuldade = data.get('dificuldade', 'N/A')

        meta_text = f"📚 {fonte} | 📅 {ano} | ⭐ {dificuldade}"
        meta_label = QLabel(meta_text)
        meta_label.setStyleSheet("color: #666; font-size: 11px;")
        meta_layout.addWidget(meta_label)

        meta_layout.addStretch()
        layout.addLayout(meta_layout)

        # Botões de ação
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()

        btn_edit = QPushButton("Editar")
        btn_edit.setMaximumWidth(80)
        btn_edit.clicked.connect(lambda: self.editClicked.emit(self.questao_id))
        btn_layout.addWidget(btn_edit)

        btn_delete = QPushButton("Excluir")
        btn_delete.setMaximumWidth(80)
        btn_delete.setStyleSheet("QPushButton { color: #d32f2f; }")
        btn_delete.clicked.connect(lambda: self.deleteClicked.emit(self.questao_id))
        btn_layout.addWidget(btn_delete)

        layout.addLayout(btn_layout)

    def mousePressEvent(self, event):
        """Emite sinal ao clicar no card"""
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit(self.questao_id)
        super().mousePressEvent(event)


class DifficultySelector(QWidget):
    """
    Seletor de dificuldade com radio buttons.
    """

    difficultyChanged = pyqtSignal(int)  # Emite ID da dificuldade

    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        label = QLabel("Dificuldade:")
        layout.addWidget(label)

        self.button_group = QButtonGroup(self)

        # Opções de dificuldade (IDs fixos: 1=FÁCIL, 2=MÉDIO, 3=DIFÍCIL)
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

        # Conectar sinal
        self.button_group.idClicked.connect(self.difficultyChanged.emit)

    def get_selected_difficulty(self):
        """Retorna ID da dificuldade selecionada"""
        return self.button_group.checkedId()

    def set_difficulty(self, difficulty_id):
        """Define dificuldade selecionada"""
        button = self.button_group.button(difficulty_id)
        if button:
            button.setChecked(True)


logger.info("Widgets customizados carregados")
