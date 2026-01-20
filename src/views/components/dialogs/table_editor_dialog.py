"""
Component: TableSizeDialog e TableEditorDialog
Diálogos para criar e editar tabelas LaTeX
"""

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QSpinBox, QFormLayout, QDialogButtonBox, QTableWidget,
    QTableWidgetItem, QHeaderView, QComboBox
)
from PyQt6.QtGui import QColor, QBrush
import logging

from src.views.components.dialogs.color_picker_dialog import ColorPickerDialog

logger = logging.getLogger(__name__)


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
        "#FFFFFF", "#F8F9FA", "#E9ECEF", "#DEE2E6", "#CED4DA",
        "#FFE5E5", "#FFCCCC", "#FF9999", "#FF6666", "#FF3333",
        "#FFF3E0", "#FFE0B2", "#FFCC80", "#FFB74D", "#FFA726",
        "#FFFDE7", "#FFF9C4", "#FFF59D", "#FFF176", "#FFEE58",
        "#E8F5E9", "#C8E6C9", "#A5D6A7", "#81C784", "#66BB6A",
        "#E3F2FD", "#BBDEFB", "#90CAF9", "#64B5F6", "#42A5F5",
        "#F3E5F5", "#E1BEE7", "#CE93D8", "#BA68C8", "#AB47BC",
    ]

    def __init__(self, rows: int, cols: int, parent=None):
        super().__init__(parent)
        self.rows = rows
        self.cols = cols
        self.cell_formats = {}
        self.col_alignments = ['c'] * cols
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
                self.cell_formats[(r, c)] = {
                    'bold': False, 'italic': False, 'underline': False, 'color': None
                }

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
        border_style = self.border_combo.currentIndex()

        # Construir especificação de colunas
        if border_style == 0:  # Todas as bordas
            col_spec = '|' + '|'.join(self.col_alignments) + '|'
        elif border_style == 2:  # Apenas externas
            col_spec = '|' + ' '.join(self.col_alignments) + '|'
        else:  # Sem bordas verticais ou sem bordas
            col_spec = ' '.join(self.col_alignments)

        lines = []
        lines.append("\\resizebox{\\columnwidth}{!}{%")
        lines.append(f"\\begin{{tabular}}{{{col_spec}}}")

        if border_style in [0, 1, 2]:
            lines.append("\\hline")

        for r in range(self.rows):
            row_cells = []
            for c in range(self.cols):
                item = self.table.item(r, c)
                text = item.text() if item else ""
                fmt = self.cell_formats.get((r, c), {})

                if fmt.get('bold'):
                    text = f"\\textbf{{{text}}}"
                if fmt.get('italic'):
                    text = f"\\textit{{{text}}}"
                if fmt.get('underline'):
                    text = f"\\underline{{{text}}}"

                color = fmt.get('color')
                if color and color.upper() != '#FFFFFF':
                    r_val, g_val, b_val = self._hex_to_rgb(color)
                    text = f"\\cellcolor[rgb]{{{r_val:.2f},{g_val:.2f},{b_val:.2f}}}{text}"

                row_cells.append(text)

            lines.append(" & ".join(row_cells) + " \\\\")

            if border_style in [0, 1]:
                lines.append("\\hline")

        if border_style == 2:
            lines.append("\\hline")

        lines.append("\\end{tabular}")
        lines.append("}")

        return "\n".join(lines)
