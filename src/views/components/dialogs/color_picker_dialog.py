"""
Component: ColorPickerDialog
Diálogo para selecionar cor com paleta e código HTML
"""

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QLineEdit, QDialogButtonBox, QWidget, QGridLayout, QColorDialog
)
from PyQt6.QtGui import QColor
import logging

logger = logging.getLogger(__name__)


class ColorPickerDialog(QDialog):
    """Diálogo para selecionar cor com paleta e código HTML."""

    # Paleta de cores predefinidas
    DEFAULT_PALETTE = [
        "#FFFFFF", "#F8F9FA", "#E9ECEF", "#DEE2E6", "#CED4DA",  # Cinzas claros
        "#FFE5E5", "#FFCCCC", "#FF9999", "#FF6666", "#FF3333",  # Vermelhos
        "#FFF3E0", "#FFE0B2", "#FFCC80", "#FFB74D", "#FFA726",  # Laranjas
        "#FFFDE7", "#FFF9C4", "#FFF59D", "#FFF176", "#FFEE58",  # Amarelos
        "#E8F5E9", "#C8E6C9", "#A5D6A7", "#81C784", "#66BB6A",  # Verdes
        "#E3F2FD", "#BBDEFB", "#90CAF9", "#64B5F6", "#42A5F5",  # Azuis
        "#F3E5F5", "#E1BEE7", "#CE93D8", "#BA68C8", "#AB47BC",  # Roxos
    ]

    def __init__(self, palette: list = None, parent=None):
        super().__init__(parent)
        self.palette = palette or self.DEFAULT_PALETTE
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
