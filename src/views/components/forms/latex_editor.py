"""
Component: LatexEditor
Editor de texto com suporte a LaTeX, imagens e tabelas
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTextEdit, QMenu, QDialog
)
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtGui import QAction
import logging

from src.views.components.dialogs.image_insert_dialog import ImageInsertDialog
from src.views.components.dialogs.table_editor_dialog import TableSizeDialog, TableEditorDialog

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
        self.images = {}
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
            cursor.insertText(f"{prefix}{selected_text}{suffix}")
        else:
            cursor.insertText(f"{prefix}{suffix}")
            cursor.movePosition(cursor.MoveOperation.Left, cursor.MoveMode.MoveAnchor, 1)
            self.text_edit.setTextCursor(cursor)

        self.text_edit.setFocus()

    def mostrar_menu_gregas(self):
        """Mostra menu com todas as letras gregas."""
        menu = QMenu(self)

        # Submenu minúsculas
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

        # Submenu maiúsculas
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

        # Variantes comuns
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
                placeholder = f"[IMG:{caminho}:{escala}]"

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
        size_dialog = TableSizeDialog(self)
        if size_dialog.exec() != QDialog.DialogCode.Accepted:
            return

        rows, cols = size_dialog.get_size()

        editor_dialog = TableEditorDialog(rows, cols, self)
        if editor_dialog.exec() == QDialog.DialogCode.Accepted:
            latex_code = editor_dialog.generate_latex()
            cursor = self.text_edit.textCursor()
            cursor.insertText("\n" + latex_code + "\n")
            self.text_edit.setFocus()

    def get_text(self):
        return self.text_edit.toPlainText()

    def set_text(self, text):
        self.text_edit.setPlainText(text)

    def get_images(self):
        """Retorna dicionário de imagens inseridas."""
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
