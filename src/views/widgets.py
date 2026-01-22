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
    QButtonGroup, QSpinBox, QTreeWidgetItemIterator, QDialog,
    QFormLayout, QDialogButtonBox, QMenu, QTableWidget, QTableWidgetItem,
    QHeaderView, QToolBar, QSizePolicy, QColorDialog, QGridLayout
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QPixmap, QFont, QAction, QIcon, QColor, QBrush
from PyQt6.QtWidgets import QStyle
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
    Suporta inserção de imagens e listas (itemize/enumerate).
    """

    textChanged = pyqtSignal()
    imageInserted = pyqtSignal(str, str)  # (caminho, placeholder_id)

    def __init__(self, placeholder="Digite o texto (suporta LaTeX)...", parent=None):
        super().__init__(parent)
        self.images = {}  # Dicionário para armazenar imagens inseridas {placeholder_id: caminho}
        self.image_counter = 0
        self.init_ui(placeholder)

    def init_ui(self, placeholder):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # Toolbar 1: Formatação de texto
        toolbar_format = QHBoxLayout()
        toolbar_format.addWidget(QLabel("Formato:"))

        btn_bold = QPushButton("N")
        btn_bold.setToolTip("Negrito (\\textbf)")
        btn_bold.setMaximumWidth(30)
        btn_bold.setStyleSheet("font-weight: bold;")
        btn_bold.clicked.connect(lambda: self.insert_format("bold"))
        toolbar_format.addWidget(btn_bold)

        btn_italic = QPushButton("I")
        btn_italic.setToolTip("Itálico (\\textit)")
        btn_italic.setMaximumWidth(30)
        btn_italic.setStyleSheet("font-style: italic;")
        btn_italic.clicked.connect(lambda: self.insert_format("italic"))
        toolbar_format.addWidget(btn_italic)

        btn_underline = QPushButton("S")
        btn_underline.setToolTip("Sublinhado (\\underline)")
        btn_underline.setMaximumWidth(30)
        btn_underline.setStyleSheet("text-decoration: underline;")
        btn_underline.clicked.connect(lambda: self.insert_format("underline"))
        toolbar_format.addWidget(btn_underline)

        toolbar_format.addWidget(QLabel("  |  "))

        # Comandos LaTeX matemáticos
        toolbar_format.addWidget(QLabel("Matemática:"))
        latex_buttons = [
            ("Fração", r"\frac{}{}"), ("Raiz", r"\sqrt{}"), ("Potência", r"^{}"),
            ("Subscrito", r"_{}"), ("Somatório", r"\sum_{}^{}"), ("Integral", r"\int_{}^{}"),
        ]
        for label, command in latex_buttons:
            btn = QPushButton(label)
            btn.setMaximumWidth(75)
            btn.clicked.connect(lambda checked, cmd=command: self.insert_latex(cmd))
            toolbar_format.addWidget(btn)

        # Botão de letras gregas com menu
        btn_greek = QPushButton("Letras Gregas")
        btn_greek.setToolTip("Inserir letras gregas")
        btn_greek.clicked.connect(self.mostrar_menu_gregas)
        toolbar_format.addWidget(btn_greek)

        toolbar_format.addStretch()
        layout.addLayout(toolbar_format)

        # Toolbar 2: Imagem e Listas
        toolbar2 = QHBoxLayout()

        # Botão de inserir imagem
        btn_imagem = QPushButton("Inserir Imagem")
        btn_imagem.setToolTip("Inserir imagem na posição do cursor")
        btn_imagem.clicked.connect(self.inserir_imagem)
        toolbar2.addWidget(btn_imagem)

        toolbar2.addWidget(QLabel(" | "))

        # Botão de lista com marcadores (itemize)
        btn_itemize = QPushButton("Lista Marcadores")
        btn_itemize.setToolTip("Inserir lista com marcadores")
        btn_itemize.clicked.connect(self.mostrar_menu_itemize)
        toolbar2.addWidget(btn_itemize)

        # Botão de lista numerada (enumerate)
        btn_enumerate = QPushButton("Lista Numerada")
        btn_enumerate.setToolTip("Inserir lista numerada")
        btn_enumerate.clicked.connect(self.mostrar_menu_enumerate)
        toolbar2.addWidget(btn_enumerate)

        toolbar2.addWidget(QLabel(" | "))

        # Botão de criar tabela
        btn_tabela = QPushButton("Criar Tabela")
        btn_tabela.setToolTip("Criar tabela com editor visual")
        btn_tabela.clicked.connect(self.criar_tabela)
        toolbar2.addWidget(btn_tabela)

        toolbar2.addStretch()
        layout.addLayout(toolbar2)

        self.text_edit = QTextEdit()
        self.text_edit.setPlaceholderText(placeholder)
        self.text_edit.setMinimumHeight(150)
        self.text_edit.textChanged.connect(self.textChanged.emit)
        layout.addWidget(self.text_edit)

        info_label = QLabel("Use comandos LaTeX para fórmulas. Clique em 'Inserir Imagem' para adicionar figuras.")
        info_label.setStyleSheet("color: #666; font-size: 10px;")
        layout.addWidget(info_label)

    def insert_latex(self, command):
        cursor = self.text_edit.textCursor()
        cursor.insertText(command)
        self.text_edit.setFocus()

    def insert_format(self, format_type: str):
        """Insere formatação de texto (negrito, itálico, sublinhado)."""
        cursor = self.text_edit.textCursor()
        selected_text = cursor.selectedText()

        format_map = {
            "bold": (r"\textbf{", "}"),
            "italic": (r"\textit{", "}"),
            "underline": (r"\underline{", "}"),
        }

        prefix, suffix = format_map.get(format_type, ("", ""))

        if selected_text:
            # Se há texto selecionado, envolve com a formatação
            cursor.insertText(f"{prefix}{selected_text}{suffix}")
        else:
            # Se não há seleção, insere comando vazio
            cursor.insertText(f"{prefix}{suffix}")
            # Posicionar cursor dentro das chaves
            cursor.movePosition(cursor.MoveOperation.Left, cursor.MoveMode.MoveAnchor, 1)
            self.text_edit.setTextCursor(cursor)

        self.text_edit.setFocus()

    def mostrar_menu_gregas(self):
        """Mostra menu com todas as letras gregas."""
        menu = QMenu(self)

        # Submenu minúsculas (com delimitadores $ para modo matemático)
        submenu_lower = menu.addMenu("Minúsculas")
        gregas_lower = [
            ("α - alfa", r"$\alpha$"), ("β - beta", r"$\beta$"), ("γ - gama", r"$\gamma$"),
            ("δ - delta", r"$\delta$"), ("ε - épsilon", r"$\epsilon$"), ("ζ - zeta", r"$\zeta$"),
            ("η - eta", r"$\eta$"), ("θ - teta", r"$\theta$"), ("ι - iota", r"$\iota$"),
            ("κ - capa", r"$\kappa$"), ("λ - lambda", r"$\lambda$"), ("μ - mi", r"$\mu$"),
            ("ν - ni", r"$\nu$"), ("ξ - csi", r"$\xi$"), ("π - pi", r"$\pi$"),
            ("ρ - rô", r"$\rho$"), ("σ - sigma", r"$\sigma$"), ("τ - tau", r"$\tau$"),
            ("υ - úpsilon", r"$\upsilon$"), ("φ - fi", r"$\phi$"), ("χ - qui", r"$\chi$"),
            ("ψ - psi", r"$\psi$"), ("ω - ômega", r"$\omega$"),
        ]
        for label, cmd in gregas_lower:
            action = QAction(label, self)
            action.triggered.connect(lambda checked, c=cmd: self.insert_latex(c))
            submenu_lower.addAction(action)

        # Submenu maiúsculas (com delimitadores $ para modo matemático)
        submenu_upper = menu.addMenu("Maiúsculas")
        gregas_upper = [
            ("Γ - Gama", r"$\Gamma$"), ("Δ - Delta", r"$\Delta$"), ("Θ - Teta", r"$\Theta$"),
            ("Λ - Lambda", r"$\Lambda$"), ("Ξ - Csi", r"$\Xi$"), ("Π - Pi", r"$\Pi$"),
            ("Σ - Sigma", r"$\Sigma$"), ("Υ - Úpsilon", r"$\Upsilon$"), ("Φ - Fi", r"$\Phi$"),
            ("Ψ - Psi", r"$\Psi$"), ("Ω - Ômega", r"$\Omega$"),
        ]
        for label, cmd in gregas_upper:
            action = QAction(label, self)
            action.triggered.connect(lambda checked, c=cmd: self.insert_latex(c))
            submenu_upper.addAction(action)

        # Variantes comuns (com delimitadores $ para modo matemático)
        submenu_var = menu.addMenu("Variantes")
        gregas_var = [
            ("ε variante", r"$\varepsilon$"), ("θ variante", r"$\vartheta$"),
            ("π variante", r"$\varpi$"), ("ρ variante", r"$\varrho$"),
            ("σ variante", r"$\varsigma$"), ("φ variante", r"$\varphi$"),
        ]
        for label, cmd in gregas_var:
            action = QAction(label, self)
            action.triggered.connect(lambda checked, c=cmd: self.insert_latex(c))
            submenu_var.addAction(action)

        btn = self.sender()
        menu.exec(btn.mapToGlobal(btn.rect().bottomLeft()))

    def inserir_imagem(self):
        """Abre diálogo para selecionar e inserir imagem na posição do cursor."""
        dialog = ImageInsertDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            caminho = dialog.get_image_path()
            escala = dialog.get_scale()
            if caminho:
                self.image_counter += 1
                # Formato: [IMG:caminho:escala] para ser auto-contido
                placeholder = f"[IMG:{caminho}:{escala}]"

                # Inserir placeholder no texto
                cursor = self.text_edit.textCursor()
                cursor.insertText(placeholder)
                self.text_edit.setFocus()
                self.imageInserted.emit(caminho, str(self.image_counter))

    def mostrar_menu_itemize(self):
        """Mostra menu com opções de marcadores para lista."""
        menu = QMenu(self)
        opcoes = [
            ("Ponto (padrão)", r"\begin{itemize}" + "\n\\item \n\\item \n\\item \n" + r"\end{itemize}"),
            ("Traço (-)", r"\begin{itemize}[label=--]" + "\n\\item \n\\item \n\\item \n" + r"\end{itemize}"),
            ("Asterisco (*)", r"\begin{itemize}[label=$\ast$]" + "\n\\item \n\\item \n\\item \n" + r"\end{itemize}"),
            ("Seta (>)", r"\begin{itemize}[label=$\triangleright$]" + "\n\\item \n\\item \n\\item \n" + r"\end{itemize}"),
            ("Quadrado", r"\begin{itemize}[label=$\square$]" + "\n\\item \n\\item \n\\item \n" + r"\end{itemize}"),
        ]
        for label, comando in opcoes:
            action = QAction(label, self)
            action.triggered.connect(lambda checked, cmd=comando: self.insert_latex(cmd))
            menu.addAction(action)
        # Posicionar menu abaixo do botão
        btn = self.sender()
        menu.exec(btn.mapToGlobal(btn.rect().bottomLeft()))

    def mostrar_menu_enumerate(self):
        """Mostra menu com opções de numeração para lista."""
        menu = QMenu(self)
        opcoes = [
            ("Números (1, 2, 3...)", r"\begin{enumerate}" + "\n\\item \n\\item \n\\item \n" + r"\end{enumerate}"),
            ("Algarismos romanos (i, ii, iii...)", r"\begin{enumerate}[label=\roman*)]" + "\n\\item \n\\item \n\\item \n" + r"\end{enumerate}"),
            ("Romanos maiúsculos (I, II, III...)", r"\begin{enumerate}[label=\Roman*)]" + "\n\\item \n\\item \n\\item \n" + r"\end{enumerate}"),
            ("Letras minúsculas (a, b, c...)", r"\begin{enumerate}[label=\alph*)]" + "\n\\item \n\\item \n\\item \n" + r"\end{enumerate}"),
            ("Letras maiúsculas (A, B, C...)", r"\begin{enumerate}[label=\Alph*)]" + "\n\\item \n\\item \n\\item \n" + r"\end{enumerate}"),
        ]
        for label, comando in opcoes:
            action = QAction(label, self)
            action.triggered.connect(lambda checked, cmd=comando: self.insert_latex(cmd))
            menu.addAction(action)
        btn = self.sender()
        menu.exec(btn.mapToGlobal(btn.rect().bottomLeft()))

    def criar_tabela(self):
        """Abre diálogo para criar tabela com editor visual."""
        # Primeiro, perguntar o tamanho
        size_dialog = TableSizeDialog(self)
        if size_dialog.exec() != QDialog.DialogCode.Accepted:
            return

        rows, cols = size_dialog.get_size()

        # Abrir editor de tabela
        editor_dialog = TableEditorDialog(rows, cols, self)
        if editor_dialog.exec() == QDialog.DialogCode.Accepted:
            latex_code = editor_dialog.generate_latex()
            # Inserir no texto
            cursor = self.text_edit.textCursor()
            cursor.insertText("\n" + latex_code + "\n")
            self.text_edit.setFocus()

    def get_text(self):
        return self.text_edit.toPlainText()

    def set_text(self, text):
        self.text_edit.setPlainText(text)

    def get_images(self):
        """Retorna dicionário de imagens inseridas {placeholder_id: {caminho, escala}}."""
        return self.images

    def set_images(self, images_dict):
        """Define dicionário de imagens (para edição)."""
        self.images = images_dict
        if images_dict:
            self.image_counter = max(int(k.replace('IMG', '')) for k in images_dict.keys())

    def clear(self):
        self.text_edit.clear()
        self.images = {}
        self.image_counter = 0


class ImageInsertDialog(QDialog):
    """Diálogo para inserir imagem no texto."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.image_path = None
        self.setWindowTitle("Inserir Imagem")
        self.setMinimumWidth(400)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        # Seleção de imagem
        img_layout = QHBoxLayout()
        self.path_label = QLabel("Nenhuma imagem selecionada")
        self.path_label.setStyleSheet("color: #666;")
        img_layout.addWidget(self.path_label, 1)
        btn_select = QPushButton("Selecionar...")
        btn_select.clicked.connect(self.select_image)
        img_layout.addWidget(btn_select)
        layout.addLayout(img_layout)

        # Preview
        self.preview_label = QLabel()
        self.preview_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.preview_label.setMinimumHeight(150)
        self.preview_label.setStyleSheet("border: 1px dashed #ccc; background: #f9f9f9;")
        layout.addWidget(self.preview_label)

        # Escala
        form_layout = QFormLayout()
        self.scale_spin = QSpinBox()
        self.scale_spin.setRange(10, 100)
        self.scale_spin.setValue(70)
        self.scale_spin.setSuffix("%")
        form_layout.addRow("Escala:", self.scale_spin)
        layout.addLayout(form_layout)

        # Botões
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def select_image(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Selecionar Imagem", "",
            "Imagens (*.png *.jpg *.jpeg *.gif *.bmp *.svg)"
        )
        if file_path:
            self.image_path = file_path
            self.path_label.setText(file_path.split('/')[-1].split('\\')[-1])
            # Preview
            pixmap = QPixmap(file_path)
            if not pixmap.isNull():
                scaled = pixmap.scaled(
                    300, 150,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation
                )
                self.preview_label.setPixmap(scaled)

    def get_image_path(self):
        return self.image_path

    def get_scale(self):
        return self.scale_spin.value() / 100.0


class TableSizeDialog(QDialog):
    """Diálogo para definir o tamanho da tabela."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Tamanho da Tabela")
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        form = QFormLayout()

        self.rows_spin = QSpinBox()
        self.rows_spin.setRange(1, 20)
        self.rows_spin.setValue(3)
        form.addRow("Linhas:", self.rows_spin)

        self.cols_spin = QSpinBox()
        self.cols_spin.setRange(1, 10)
        self.cols_spin.setValue(3)
        form.addRow("Colunas:", self.cols_spin)

        layout.addLayout(form)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def get_size(self):
        return self.rows_spin.value(), self.cols_spin.value()


class TableEditorDialog(QDialog):
    """Editor de tabela estilo planilha com formatação."""

    # Paleta de cores predefinidas
    COLOR_PALETTE = [
        "#FFFFFF", "#F8F9FA", "#E9ECEF", "#DEE2E6", "#CED4DA",  # Cinzas claros
        "#FFE5E5", "#FFCCCC", "#FF9999", "#FF6666", "#FF3333",  # Vermelhos
        "#FFF3E0", "#FFE0B2", "#FFCC80", "#FFB74D", "#FFA726",  # Laranjas
        "#FFFDE7", "#FFF9C4", "#FFF59D", "#FFF176", "#FFEE58",  # Amarelos
        "#E8F5E9", "#C8E6C9", "#A5D6A7", "#81C784", "#66BB6A",  # Verdes
        "#E3F2FD", "#BBDEFB", "#90CAF9", "#64B5F6", "#42A5F5",  # Azuis
        "#F3E5F5", "#E1BEE7", "#CE93D8", "#BA68C8", "#AB47BC",  # Roxos
    ]

    def __init__(self, rows: int, cols: int, parent=None):
        super().__init__(parent)
        self.rows = rows
        self.cols = cols
        self.cell_formats = {}  # {(row, col): {'bold': bool, 'italic': bool, 'underline': bool, 'color': str}}
        self.col_alignments = ['c'] * cols  # 'l', 'c', 'r' para cada coluna
        self.setWindowTitle("Editor de Tabela")
        self.setMinimumSize(800, 550)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        # Toolbar de formatação
        toolbar_layout = QHBoxLayout()

        # Formatação de texto
        toolbar_layout.addWidget(QLabel("Formatação:"))

        self.btn_bold = QPushButton("N")
        self.btn_bold.setToolTip("Negrito")
        self.btn_bold.setCheckable(True)
        self.btn_bold.setMaximumWidth(30)
        self.btn_bold.setStyleSheet("font-weight: bold;")
        self.btn_bold.clicked.connect(self.toggle_bold)
        toolbar_layout.addWidget(self.btn_bold)

        self.btn_italic = QPushButton("I")
        self.btn_italic.setToolTip("Itálico")
        self.btn_italic.setCheckable(True)
        self.btn_italic.setMaximumWidth(30)
        self.btn_italic.setStyleSheet("font-style: italic;")
        self.btn_italic.clicked.connect(self.toggle_italic)
        toolbar_layout.addWidget(self.btn_italic)

        self.btn_underline = QPushButton("S")
        self.btn_underline.setToolTip("Sublinhado")
        self.btn_underline.setCheckable(True)
        self.btn_underline.setMaximumWidth(30)
        self.btn_underline.setStyleSheet("text-decoration: underline;")
        self.btn_underline.clicked.connect(self.toggle_underline)
        toolbar_layout.addWidget(self.btn_underline)

        toolbar_layout.addWidget(QLabel("  |  "))

        # Alinhamento da coluna
        toolbar_layout.addWidget(QLabel("Alinhamento da Coluna:"))

        self.btn_align_left = QPushButton("Esq")
        self.btn_align_left.setToolTip("Alinhar à Esquerda")
        self.btn_align_left.setMaximumWidth(40)
        self.btn_align_left.clicked.connect(lambda: self.set_column_alignment('l'))
        toolbar_layout.addWidget(self.btn_align_left)

        self.btn_align_center = QPushButton("Centro")
        self.btn_align_center.setToolTip("Centralizar")
        self.btn_align_center.setMaximumWidth(50)
        self.btn_align_center.clicked.connect(lambda: self.set_column_alignment('c'))
        toolbar_layout.addWidget(self.btn_align_center)

        self.btn_align_right = QPushButton("Dir")
        self.btn_align_right.setToolTip("Alinhar à Direita")
        self.btn_align_right.setMaximumWidth(40)
        self.btn_align_right.clicked.connect(lambda: self.set_column_alignment('r'))
        toolbar_layout.addWidget(self.btn_align_right)

        toolbar_layout.addWidget(QLabel("  |  "))

        # Cor da célula
        toolbar_layout.addWidget(QLabel("Cor:"))

        self.btn_color = QPushButton("")
        self.btn_color.setToolTip("Cor de fundo da célula")
        self.btn_color.setMaximumWidth(30)
        self.btn_color.setMinimumHeight(25)
        self.btn_color.setStyleSheet("background-color: #FFFFFF; border: 1px solid #999;")
        self.btn_color.clicked.connect(self.show_color_picker)
        toolbar_layout.addWidget(self.btn_color)

        self.btn_clear_color = QPushButton("Limpar")
        self.btn_clear_color.setToolTip("Remover cor de fundo")
        self.btn_clear_color.setMaximumWidth(50)
        self.btn_clear_color.clicked.connect(self.clear_cell_color)
        toolbar_layout.addWidget(self.btn_clear_color)

        toolbar_layout.addStretch()
        layout.addLayout(toolbar_layout)

        # Dica de uso
        hint = QLabel("Dica: Use $...$ para equações. Ex: $x^2 + y^2$")
        hint.setStyleSheet("color: #666; font-size: 10px; margin: 5px 0;")
        layout.addWidget(hint)

        # Tabela editável
        self.table = QTableWidget(self.rows, self.cols)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        self.table.currentCellChanged.connect(self.on_cell_changed)

        # Inicializar células
        for r in range(self.rows):
            for c in range(self.cols):
                item = QTableWidgetItem("")
                self.table.setItem(r, c, item)
                self.cell_formats[(r, c)] = {'bold': False, 'italic': False, 'underline': False, 'color': None}

        layout.addWidget(self.table)

        # Opções de bordas
        border_layout = QHBoxLayout()
        border_layout.addWidget(QLabel("Bordas:"))

        self.border_combo = QComboBox()
        self.border_combo.addItems([
            "Todas as bordas",
            "Apenas horizontais",
            "Apenas externas",
            "Sem bordas"
        ])
        border_layout.addWidget(self.border_combo)
        border_layout.addStretch()
        layout.addLayout(border_layout)

        # Botões OK/Cancelar
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def on_cell_changed(self, row, col, prev_row, prev_col):
        """Atualiza estado dos botões de formatação quando célula muda."""
        if row >= 0 and col >= 0:
            fmt = self.cell_formats.get((row, col), {})
            self.btn_bold.setChecked(fmt.get('bold', False))
            self.btn_italic.setChecked(fmt.get('italic', False))
            self.btn_underline.setChecked(fmt.get('underline', False))
            # Atualizar cor do botão
            color = fmt.get('color')
            if color:
                self.btn_color.setStyleSheet(f"background-color: {color}; border: 1px solid #999;")
            else:
                self.btn_color.setStyleSheet("background-color: #FFFFFF; border: 1px solid #999;")

    def toggle_bold(self):
        row, col = self.table.currentRow(), self.table.currentColumn()
        if row >= 0 and col >= 0:
            self.cell_formats[(row, col)]['bold'] = self.btn_bold.isChecked()
            self._update_cell_style(row, col)

    def toggle_italic(self):
        row, col = self.table.currentRow(), self.table.currentColumn()
        if row >= 0 and col >= 0:
            self.cell_formats[(row, col)]['italic'] = self.btn_italic.isChecked()
            self._update_cell_style(row, col)

    def toggle_underline(self):
        row, col = self.table.currentRow(), self.table.currentColumn()
        if row >= 0 and col >= 0:
            self.cell_formats[(row, col)]['underline'] = self.btn_underline.isChecked()
            self._update_cell_style(row, col)

    def _update_cell_style(self, row, col):
        """Atualiza estilo visual da célula."""
        item = self.table.item(row, col)
        if item:
            font = item.font()
            fmt = self.cell_formats[(row, col)]
            font.setBold(fmt['bold'])
            font.setItalic(fmt['italic'])
            font.setUnderline(fmt['underline'])
            item.setFont(font)
            # Aplicar cor de fundo
            color = fmt.get('color')
            if color:
                item.setBackground(QBrush(QColor(color)))
            else:
                item.setBackground(QBrush(QColor("#FFFFFF")))

    def show_color_picker(self):
        """Mostra seletor de cores com paleta e opção de código HTML."""
        row, col = self.table.currentRow(), self.table.currentColumn()
        if row < 0 or col < 0:
            return

        dialog = ColorPickerDialog(self.COLOR_PALETTE, self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            color = dialog.get_selected_color()
            if color:
                self.cell_formats[(row, col)]['color'] = color
                self.btn_color.setStyleSheet(f"background-color: {color}; border: 1px solid #999;")
                self._update_cell_style(row, col)

    def clear_cell_color(self):
        """Remove cor de fundo da célula atual."""
        row, col = self.table.currentRow(), self.table.currentColumn()
        if row >= 0 and col >= 0:
            self.cell_formats[(row, col)]['color'] = None
            self.btn_color.setStyleSheet("background-color: #FFFFFF; border: 1px solid #999;")
            self._update_cell_style(row, col)

    def set_column_alignment(self, alignment: str):
        """Define alinhamento para a coluna atual."""
        col = self.table.currentColumn()
        if col >= 0:
            self.col_alignments[col] = alignment
            # Feedback visual
            align_map = {'l': 'Esquerda', 'c': 'Centro', 'r': 'Direita'}
            logger.info(f"Coluna {col + 1} alinhada: {align_map[alignment]}")

    def _hex_to_rgb(self, hex_color: str) -> tuple:
        """Converte cor hexadecimal para RGB (0-1)."""
        hex_color = hex_color.lstrip('#')
        r = int(hex_color[0:2], 16) / 255.0
        g = int(hex_color[2:4], 16) / 255.0
        b = int(hex_color[4:6], 16) / 255.0
        return (r, g, b)

    def generate_latex(self) -> str:
        """Gera código LaTeX da tabela com resizebox para ajuste automático."""
        # Definir tipo de borda
        border_style = self.border_combo.currentIndex()

        # Verificar se há cores usadas
        has_colors = any(fmt.get('color') for fmt in self.cell_formats.values())

        # Construir especificação de colunas
        if border_style == 0:  # Todas as bordas
            col_spec = '|' + '|'.join(self.col_alignments) + '|'
        elif border_style == 2:  # Apenas externas
            col_spec = '|' + ' '.join(self.col_alignments) + '|'
        else:  # Sem bordas verticais ou sem bordas
            col_spec = ' '.join(self.col_alignments)

        lines = []

        # Usar resizebox para ajustar tabelas grandes automaticamente
        # \resizebox{\columnwidth}{!}{...} redimensiona para caber na largura da coluna
        # Usa \columnwidth em vez de \linewidth para funcionar corretamente em multicols
        lines.append("\\resizebox{\\columnwidth}{!}{%")
        lines.append(f"\\begin{{tabular}}{{{col_spec}}}")

        # Adicionar linhas horizontais conforme estilo
        if border_style in [0, 1, 2]:  # Com bordas horizontais
            lines.append("\\hline")

        for r in range(self.rows):
            row_cells = []
            for c in range(self.cols):
                item = self.table.item(r, c)
                text = item.text() if item else ""
                fmt = self.cell_formats.get((r, c), {})

                # Aplicar formatação de texto
                if fmt.get('bold'):
                    text = f"\\textbf{{{text}}}"
                if fmt.get('italic'):
                    text = f"\\textit{{{text}}}"
                if fmt.get('underline'):
                    text = f"\\underline{{{text}}}"

                # Aplicar cor de fundo
                color = fmt.get('color')
                if color and color.upper() != '#FFFFFF':
                    r_val, g_val, b_val = self._hex_to_rgb(color)
                    text = f"\\cellcolor[rgb]{{{r_val:.2f},{g_val:.2f},{b_val:.2f}}}{text}"

                row_cells.append(text)

            lines.append(" & ".join(row_cells) + " \\\\")

            # Adicionar hline após cada linha (se bordas horizontais)
            if border_style in [0, 1]:
                lines.append("\\hline")

        # Borda inferior para "apenas externas"
        if border_style == 2:
            lines.append("\\hline")

        lines.append("\\end{tabular}")
        lines.append("}")  # Fecha o resizebox

        return "\n".join(lines)


class ColorPickerDialog(QDialog):
    """Diálogo para selecionar cor com paleta e código HTML."""

    def __init__(self, palette: list, parent=None):
        super().__init__(parent)
        self.palette = palette
        self.selected_color = None
        self.setWindowTitle("Selecionar Cor")
        self.setMinimumWidth(350)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        # Paleta de cores
        layout.addWidget(QLabel("Paleta de Cores:"))

        palette_widget = QWidget()
        palette_layout = QGridLayout(palette_widget)
        palette_layout.setSpacing(3)

        cols_per_row = 5
        for i, color in enumerate(self.palette):
            btn = QPushButton()
            btn.setFixedSize(40, 30)
            btn.setStyleSheet(f"background-color: {color}; border: 1px solid #666;")
            btn.setToolTip(color)
            btn.clicked.connect(lambda checked, c=color: self.select_color(c))
            row = i // cols_per_row
            col = i % cols_per_row
            palette_layout.addWidget(btn, row, col)

        layout.addWidget(palette_widget)

        # Separador
        layout.addWidget(QLabel(""))

        # Código HTML manual
        html_layout = QHBoxLayout()
        html_layout.addWidget(QLabel("Código HTML:"))
        self.html_input = QLineEdit()
        self.html_input.setPlaceholderText("#RRGGBB (ex: #FF5733)")
        self.html_input.setMaximumWidth(120)
        html_layout.addWidget(self.html_input)

        self.btn_apply_html = QPushButton("Aplicar")
        self.btn_apply_html.clicked.connect(self.apply_html_color)
        html_layout.addWidget(self.btn_apply_html)

        html_layout.addStretch()
        layout.addLayout(html_layout)

        # Preview da cor selecionada
        preview_layout = QHBoxLayout()
        preview_layout.addWidget(QLabel("Cor selecionada:"))
        self.preview_label = QLabel()
        self.preview_label.setFixedSize(60, 30)
        self.preview_label.setStyleSheet("background-color: #FFFFFF; border: 2px solid #333;")
        preview_layout.addWidget(self.preview_label)

        # Botão para abrir seletor completo do sistema
        btn_more = QPushButton("Mais cores...")
        btn_more.clicked.connect(self.open_system_color_picker)
        preview_layout.addWidget(btn_more)

        preview_layout.addStretch()
        layout.addLayout(preview_layout)

        # Botões OK/Cancelar
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def select_color(self, color: str):
        """Seleciona uma cor da paleta."""
        self.selected_color = color
        self.preview_label.setStyleSheet(f"background-color: {color}; border: 2px solid #333;")
        self.html_input.setText(color)

    def apply_html_color(self):
        """Aplica cor do código HTML digitado."""
        color = self.html_input.text().strip()
        if color and not color.startswith('#'):
            color = '#' + color
        # Validar formato
        if len(color) == 7 and color.startswith('#'):
            try:
                int(color[1:], 16)  # Validar hex
                self.selected_color = color.upper()
                self.preview_label.setStyleSheet(f"background-color: {color}; border: 2px solid #333;")
            except ValueError:
                pass

    def open_system_color_picker(self):
        """Abre o seletor de cores do sistema."""
        initial = QColor(self.selected_color) if self.selected_color else QColor("#FFFFFF")
        color = QColorDialog.getColor(initial, self, "Selecionar Cor")
        if color.isValid():
            hex_color = color.name().upper()
            self.selected_color = hex_color
            self.preview_label.setStyleSheet(f"background-color: {hex_color}; border: 2px solid #333;")
            self.html_input.setText(hex_color)

    def get_selected_color(self) -> str:
        """Retorna a cor selecionada."""
        return self.selected_color


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
        layout.setSpacing(5)

        # Botões de controle (acima da árvore)
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(3)
        btn_expand = QPushButton("+")
        btn_expand.setToolTip("Expandir Tudo")
        btn_expand.setFixedWidth(30)
        btn_expand.clicked.connect(self.tree_expand_all)
        btn_layout.addWidget(btn_expand)
        btn_collapse = QPushButton("-")
        btn_collapse.setToolTip("Recolher Tudo")
        btn_collapse.setFixedWidth(30)
        btn_collapse.clicked.connect(self.tree_collapse_all)
        btn_layout.addWidget(btn_collapse)
        btn_clear = QPushButton("Limpar")
        btn_clear.setToolTip("Limpar Seleção")
        btn_clear.setFixedWidth(60)
        btn_clear.clicked.connect(self.clear_selection)
        btn_layout.addWidget(btn_clear)
        btn_layout.addStretch()
        layout.addLayout(btn_layout)

        # Árvore de tags
        self.tree = QTreeWidget()
        self.tree.setHeaderLabel("Selecione as tags")
        self.tree.setMinimumHeight(150)
        self.tree.itemChanged.connect(self.on_item_changed)
        layout.addWidget(self.tree)

    def tree_expand_all(self):
        self.tree.expandAll()

    def tree_collapse_all(self):
        self.tree.collapseAll()

    def _add_items_recursively(self, parent_item, tags: List[TagResponseDTO]):
        """Helper recursivo para popular a árvore a partir de DTOs."""
        for tag_dto in tags:
            item = QTreeWidgetItem(parent_item)
            item.setText(0, tag_dto.nome)
            item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
            item.setCheckState(0, Qt.CheckState.Unchecked)
            # Armazenar UUID para lookup correto no banco
            item.setData(0, Qt.ItemDataRole.UserRole, tag_dto.uuid)
            # Armazenar numeração para identificar tipo de tag (UserRole+1)
            item.setData(0, Qt.ItemDataRole.UserRole + 1, tag_dto.numeracao)
            if tag_dto.filhos:
                self._add_items_recursively(item, tag_dto.filhos)

    def load_tags(self, tags_arvore: List[TagResponseDTO]):
        """Carrega uma árvore de tags DTOs no widget."""
        self.tree.clear()
        self._add_items_recursively(self.tree, tags_arvore)
        self.tree.expandAll()

    def on_item_changed(self, item, column):
        self.selectionChanged.emit(self.get_selected_tag_ids())

    def get_selected_tag_ids(self) -> List[str]:
        """Retorna lista de UUIDs das tags selecionadas (marcadas)."""
        selected_ids = []
        iterator = QTreeWidgetItemIterator(self.tree)
        while iterator.value():
            item = iterator.value()
            if item.checkState(0) == Qt.CheckState.Checked:
                tag_uuid = item.data(0, Qt.ItemDataRole.UserRole)
                if tag_uuid is not None:
                    selected_ids.append(tag_uuid)
            iterator += 1
        return selected_ids

    def get_selected_content_tags(self) -> List[str]:
        """
        Retorna lista de UUIDs das tags de conteúdo selecionadas.
        Tags de conteúdo são aquelas cuja numeração começa com dígito (não V ou N).
        """
        selected_ids = []
        iterator = QTreeWidgetItemIterator(self.tree)
        while iterator.value():
            item = iterator.value()
            if item.checkState(0) == Qt.CheckState.Checked:
                tag_uuid = item.data(0, Qt.ItemDataRole.UserRole)
                numeracao = item.data(0, Qt.ItemDataRole.UserRole + 1) or ""
                # Verificar se é tag de conteúdo (numeração começa com dígito)
                if tag_uuid and numeracao and numeracao[0].isdigit():
                    selected_ids.append(tag_uuid)
            iterator += 1
        return selected_ids

    def get_selected_content_tags_with_names(self) -> List[tuple]:
        """
        Retorna lista de tuplas (uuid, nome) das tags de conteúdo selecionadas.
        Tags de conteúdo são aquelas cuja numeração começa com dígito (não V ou N).
        """
        selected_tags = []
        iterator = QTreeWidgetItemIterator(self.tree)
        while iterator.value():
            item = iterator.value()
            if item.checkState(0) == Qt.CheckState.Checked:
                tag_uuid = item.data(0, Qt.ItemDataRole.UserRole)
                numeracao = item.data(0, Qt.ItemDataRole.UserRole + 1) or ""
                tag_nome = item.text(0)
                # Verificar se é tag de conteúdo (numeração começa com dígito)
                if tag_uuid and numeracao and numeracao[0].isdigit():
                    selected_tags.append((tag_uuid, tag_nome))
            iterator += 1
        return selected_tags

    def set_selected_tags(self, tag_uuids: List[str]):
        """Marca os checkboxes para a lista de UUIDs de tags fornecida."""
        if not tag_uuids:
            return

        # Usar um set para busca mais rápida
        uuids_to_check = set(tag_uuids)

        iterator = QTreeWidgetItemIterator(self.tree)
        while iterator.value():
            item = iterator.value()
            tag_uuid = item.data(0, Qt.ItemDataRole.UserRole)
            if tag_uuid in uuids_to_check:
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
    clicked = pyqtSignal(str)  # Emite codigo da questao
    editClicked = pyqtSignal(str)
    inactivateClicked = pyqtSignal(str)
    reactivateClicked = pyqtSignal(str)  # Novo sinal para reativar
    addToListClicked = pyqtSignal(str)

    def __init__(self, questao_dto, parent=None):
        super().__init__(parent)
        self.questao_dto = questao_dto  # Guardar DTO para preview
        # Aceitar tanto dict quanto DTO - priorizar codigo
        if isinstance(questao_dto, dict):
            self.questao_id = questao_dto.get('codigo') or questao_dto.get('uuid')
            self.is_ativa = questao_dto.get('ativo', True)
        else:
            self.questao_id = getattr(questao_dto, 'codigo', None) or getattr(questao_dto, 'uuid', None)
            self.is_ativa = getattr(questao_dto, 'ativo', True)
        self.init_ui(questao_dto)

    def _get_attr(self, obj, attr, default=None):
        """Helper para obter atributo tanto de dict quanto de objeto"""
        if isinstance(obj, dict):
            return obj.get(attr, default)
        return getattr(obj, attr, default)

    def init_ui(self, dto):
        self.setFrameStyle(QFrame.Shape.StyledPanel | QFrame.Shadow.Raised)
        
        # Estilo do card (arredondado, branco)
        self.setStyleSheet("""
            QFrame {
                border: 1px solid #e0e0e0;
                border-radius: 12px;
                background-color: white;
                padding: 16px;
            }
            QFrame:hover {
                border-color: #1abc9c;
            }
        """)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setMinimumHeight(200)
        self.setMaximumHeight(280)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)

        # Cabeçalho: ID à esquerda, ícones à direita
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(0, 0, 0, 0)
        
        # ID da questão (#Q-XXXX)
        questao_id_display = f"#Q-{self.questao_id}" if self.questao_id else "#Q-XXXX"
        id_label = QLabel(questao_id_display)
        id_label.setStyleSheet("""
            font-weight: bold;
            font-size: 13px;
            color: #3498db;
        """)
        header_layout.addWidget(id_label)
        
        header_layout.addStretch()
        
        # Ícones de ação (olho/lápis e três pontos)
        actions_layout = QHBoxLayout()
        actions_layout.setSpacing(8)
        
        # Ícone de visualizar/editar
        btn_view_edit = QPushButton()
        from PyQt6.QtWidgets import QApplication
        app = QApplication.instance()
        if app:
            style = app.style()
            if self.is_ativa:
                icon = style.standardIcon(QStyle.StandardPixmap.SP_FileDialogDetailedView)
            else:
                icon = style.standardIcon(QStyle.StandardPixmap.SP_FileDialogInfoView)
            if icon:
                btn_view_edit.setIcon(icon)
        btn_view_edit.setFixedSize(24, 24)
        btn_view_edit.setStyleSheet("""
            QPushButton {
                border: none;
                background-color: transparent;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #f0f0f0;
            }
        """)
        if self.is_ativa:
            btn_view_edit.clicked.connect(lambda: self.editClicked.emit(self.questao_id))
        else:
            btn_view_edit.clicked.connect(lambda checked: self._show_preview())
        actions_layout.addWidget(btn_view_edit)
        
        # Menu de três pontos
        btn_menu = QPushButton("⋯")
        btn_menu.setFixedSize(24, 24)
        btn_menu.setStyleSheet("""
            QPushButton {
                border: none;
                background-color: transparent;
                border-radius: 4px;
                font-size: 18px;
                font-weight: bold;
                color: #7f8c8d;
            }
            QPushButton:hover {
                background-color: #f0f0f0;
            }
        """)
        btn_menu.clicked.connect(self._show_context_menu)
        actions_layout.addWidget(btn_menu)
        
        header_layout.addLayout(actions_layout)
        layout.addLayout(header_layout)

        # Título da questão
        titulo = self._get_attr(dto, 'titulo') or 'Sem título'
        title_label = QLabel(titulo)
        title_label.setStyleSheet("""
            font-weight: bold;
            font-size: 15px;
            color: #2c3e50;
            margin-top: 4px;
        """)
        title_label.setWordWrap(True)
        layout.addWidget(title_label)

        # Área de conteúdo (preview do enunciado com borda tracejada)
        enunciado = self._get_attr(dto, 'enunciado', '')
        # Extrair primeira fórmula ou trecho relevante
        enunciado_preview = self._extract_preview(enunciado)
        
        content_frame = QFrame()
        content_frame.setStyleSheet("""
            QFrame {
                background-color: #f8f9fa;
                border: 2px dashed #d0d0d0;
                border-radius: 6px;
                padding: 12px;
                min-height: 60px;
            }
        """)
        content_layout = QVBoxLayout(content_frame)
        content_layout.setContentsMargins(8, 8, 8, 8)
        
        content_label = QLabel(enunciado_preview)
        content_label.setStyleSheet("""
            color: #555;
            font-size: 13px;
            font-family: 'Courier New', monospace;
        """)
        content_label.setWordWrap(True)
        content_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        content_layout.addWidget(content_label)
        
        layout.addWidget(content_frame)

        layout.addStretch()

        # Tags na parte inferior
        tags_layout = QHBoxLayout()
        tags_layout.setContentsMargins(0, 8, 0, 0)
        tags_layout.setSpacing(6)
        
        # Extrair tags e metadados
        tags = self._extract_tags(dto)
        for tag_text, tag_color in tags:
            tag_label = QLabel(tag_text)
            tag_label.setStyleSheet(f"""
                background-color: {tag_color};
                color: white;
                padding: 4px 10px;
                border-radius: 12px;
                font-size: 10px;
                font-weight: bold;
            """)
            tags_layout.addWidget(tag_label)
        
        tags_layout.addStretch()
        layout.addLayout(tags_layout)
    
    def _extract_preview(self, enunciado):
        """Extrai preview do enunciado (fórmula ou trecho)"""
        if not enunciado:
            return ""
        
        # Tentar encontrar fórmula LaTeX
        import re
        # Procurar por padrões de fórmula
        formula_patterns = [
            r'\\[a-zA-Z]+\{[^}]+\}',  # Comandos LaTeX simples
            r'\$[^$]+\$',  # Fórmulas inline
            r'\\begin\{[^}]+\}.*?\\end\{[^}]+\}',  # Ambientes LaTeX
        ]
        
        for pattern in formula_patterns:
            matches = re.findall(pattern, enunciado, re.DOTALL)
            if matches:
                # Pegar primeira fórmula encontrada
                preview = matches[0]
                # Limpar para exibição
                preview = preview.replace('$', '').replace('\\', '')
                if len(preview) > 80:
                    preview = preview[:80] + "..."
                return preview
        
        # Se não encontrar fórmula, pegar primeiras palavras
        preview = enunciado.strip()
        # Remover LaTeX básico para preview
        preview = re.sub(r'\\[a-zA-Z]+\{([^}]+)\}', r'\1', preview)
        preview = re.sub(r'\{|\}', '', preview)
        if len(preview) > 100:
            preview = preview[:100] + "..."
        return preview
    
    def _extract_tags(self, dto):
        """Extrai tags e metadados para exibição"""
        tags = []
        
        # Fonte/Banca
        fonte = self._get_attr(dto, 'fonte') or self._get_attr(dto, 'fonte_nome')
        if fonte and fonte != 'N/A':
            tags.append((fonte.upper(), "#3498db"))  # Azul
        
        # Dificuldade
        dificuldade = self._get_attr(dto, 'dificuldade_nome') or self._get_attr(dto, 'dificuldade')
        if dificuldade and dificuldade != 'N/A':
            dificuldade_upper = dificuldade.upper()
            if dificuldade_upper in ['FÁCIL', 'FACIL', 'EASY']:
                tags.append((dificuldade_upper, "#27ae60"))  # Verde
            elif dificuldade_upper in ['MÉDIO', 'MEDIO', 'MEDIUM']:
                tags.append((dificuldade_upper, "#f39c12"))  # Laranja
            elif dificuldade_upper in ['DIFÍCIL', 'DIFICIL', 'HARD']:
                tags.append((dificuldade_upper, "#e74c3c"))  # Vermelho
        
        # Tags de conteúdo (primeiras 2)
        try:
            questao_tags = self._get_attr(dto, 'tags', [])
            if questao_tags:
                count = 0
                for tag in questao_tags:
                    if count >= 2:
                        break
                    if isinstance(tag, dict):
                        nome = tag.get('nome', '')
                        numeracao = tag.get('numeracao', '')
                    else:
                        nome = getattr(tag, 'nome', '')
                        numeracao = getattr(tag, 'numeracao', '')
                    
                    # Apenas tags de conteúdo (não vestibular/série)
                    if numeracao and numeracao[0].isdigit() and nome:
                        tags.append((nome.upper(), "#95a5a6"))  # Cinza
                        count += 1
        except:
            pass
        
        # Status se inativa
        if not self.is_ativa:
            tags.append(("INATIVA", "#e74c3c"))
        
        return tags
    
    def _show_context_menu(self):
        """Mostra menu de contexto com ações"""
        from PyQt6.QtWidgets import QMenu
        menu = QMenu(self)
        
        action_view = menu.addAction("Visualizar")
        action_view.triggered.connect(lambda: self._show_preview())
        
        if self.is_ativa:
            action_edit = menu.addAction("Editar")
            action_edit.triggered.connect(lambda: self.editClicked.emit(self.questao_id))
            
            menu.addSeparator()
            
            action_add_list = menu.addAction("Adicionar à Lista")
            action_add_list.triggered.connect(lambda: self.addToListClicked.emit(self.questao_id))
            
            menu.addSeparator()
            
            action_inactivate = menu.addAction("Inativar")
            action_inactivate.triggered.connect(lambda: self.inactivateClicked.emit(self.questao_id))
        else:
            action_reactivate = menu.addAction("Reativar")
            action_reactivate.triggered.connect(lambda: self.reactivateClicked.emit(self.questao_id))
        
        menu.exec(self.mapToGlobal(self.sender().pos()))

    def mouseDoubleClickEvent(self, event):
        """Abre preview com duplo clique no card."""
        if event.button() == Qt.MouseButton.LeftButton:
            self._show_preview()
        super().mouseDoubleClickEvent(event)

    def _show_preview(self):
        """Abre o diálogo de preview da questão no formato PDF."""
        from PyQt6.QtWidgets import QMessageBox
        try:
            # Importação local para evitar dependência circular
            from src.views.questao_preview import QuestaoPreview
            from src.controllers.adapters import criar_questao_controller

            # Buscar dados completos da questão
            controller = criar_questao_controller()
            questao_completa = controller.obter_questao_completa(self.questao_id)

            if not questao_completa:
                QMessageBox.warning(self, "Aviso", f"Questão {self.questao_id} não encontrada.")
                return

            # Montar dados para o preview
            preview_data = {
                'id': self.questao_id,
                'titulo': getattr(questao_completa, 'titulo', None) or 'Sem título',
                'tipo': getattr(questao_completa, 'tipo', 'N/A'),
                'enunciado': getattr(questao_completa, 'enunciado', ''),
                'fonte': self._extrair_fonte(questao_completa),
                'ano': getattr(questao_completa, 'ano', None),
                'dificuldade': getattr(questao_completa, 'dificuldade', 'N/A'),
                'resolucao': getattr(questao_completa, 'resolucao', None),
                'tags': self._extrair_tags_nomes(questao_completa),
                'alternativas': []
            }

            # Extrair alternativas se objetiva
            alternativas = getattr(questao_completa, 'alternativas', [])
            if alternativas:
                for alt in alternativas:
                    if hasattr(alt, 'letra'):
                        preview_data['alternativas'].append({
                            'letra': alt.letra,
                            'texto': getattr(alt, 'texto', ''),
                            'correta': getattr(alt, 'correta', False)
                        })
                    elif isinstance(alt, dict):
                        preview_data['alternativas'].append({
                            'letra': alt.get('letra', ''),
                            'texto': alt.get('texto', ''),
                            'correta': alt.get('correta', False)
                        })

            # Abrir diálogo de preview
            preview_dialog = QuestaoPreview(preview_data, self)
            preview_dialog.exec()

        except Exception as e:
            logger.error(f"Erro ao abrir preview da questão {self.questao_id}: {e}")
            QMessageBox.critical(self, "Erro", f"Erro ao abrir preview:\n{str(e)}")

    def _extrair_fonte(self, questao):
        """Extrai o nome da fonte das tags da questão."""
        tags = getattr(questao, 'tags', []) or []
        for tag in tags:
            numeracao = getattr(tag, 'numeracao', '') or ''
            if numeracao.startswith('V'):
                return getattr(tag, 'nome', '') or ''
        return None

    def _extrair_tags_nomes(self, questao):
        """Extrai nomes das tags de conteúdo da questão."""
        nomes = []
        tags = getattr(questao, 'tags', []) or []
        for tag in tags:
            numeracao = getattr(tag, 'numeracao', '') or ''
            nome = getattr(tag, 'nome', '') or ''
            # Incluir apenas tags de conteúdo (numeração começa com dígito)
            if numeracao and numeracao[0].isdigit() and nome:
                nomes.append(nome)
        return nomes


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
            (1, "FÁCIL", "#4caf50"),
            (2, "MÉDIO", "#ff9800"),
            (3, "DIFÍCIL", "#f44336")
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