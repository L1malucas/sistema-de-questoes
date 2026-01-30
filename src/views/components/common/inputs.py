# src/views/components/common/inputs.py
from PyQt6.QtWidgets import (
    QLineEdit, QTextEdit, QComboBox, QDateEdit, QWidget, QHBoxLayout, QVBoxLayout,
    QLabel, QStyle, QStyleOptionFrame, QApplication, QPushButton, QMenu, QFrame,
    QDialog, QScrollArea, QDialogButtonBox, QSizePolicy, QSpinBox, QGridLayout,
    QTableWidget, QTableWidgetItem, QHeaderView, QCheckBox, QColorDialog
)
from PyQt6.QtGui import QIcon, QPainter, QColor, QFont, QIntValidator, QTextCursor, QAction, QBrush
from PyQt6.QtCore import Qt, QSize, QDate
from src.views.design.constants import Color, Spacing, Typography, Dimensions


class TableDialog(QDialog):
    """Diálogo para criar tabelas de forma intuitiva com formatação."""

    # Cores predefinidas
    PRESET_COLORS = [
        ('#ffffff', 'Branco'),
        ('#f3f4f6', 'Cinza claro'),
        ('#dbeafe', 'Azul claro'),
        ('#dcfce7', 'Verde claro'),
        ('#fef3c7', 'Amarelo claro'),
        ('#fee2e2', 'Vermelho claro'),
        ('#f3e8ff', 'Roxo claro'),
        ('#cffafe', 'Ciano claro'),
    ]

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Criar Tabela")
        self.setMinimumWidth(700)
        self.setMinimumHeight(550)

        # Armazenar formatações das células: {(row, col): {'bold': bool, 'italic': bool, ...}}
        self.cell_formats = {}

        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(Spacing.SM)

        # Frame de configuração (tamanho e cabeçalho)
        config_frame = QFrame(self)
        config_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {Color.LIGHT_BLUE_BG_1};
                border: 1px solid {Color.LIGHT_BLUE_BORDER};
                border-radius: {Dimensions.BORDER_RADIUS_MD};
            }}
        """)
        config_layout = QHBoxLayout(config_frame)
        config_layout.setContentsMargins(10, 8, 10, 8)
        config_layout.setSpacing(Spacing.MD)

        # Linhas
        config_layout.addWidget(QLabel("Linhas:"))
        self.rows_spin = QSpinBox()
        self.rows_spin.setRange(1, 20)
        self.rows_spin.setValue(3)
        self.rows_spin.setStyleSheet(self._get_spinbox_style())
        self.rows_spin.valueChanged.connect(self._update_table_size)
        config_layout.addWidget(self.rows_spin)

        # Colunas
        config_layout.addWidget(QLabel("Colunas:"))
        self.cols_spin = QSpinBox()
        self.cols_spin.setRange(1, 10)
        self.cols_spin.setValue(3)
        self.cols_spin.setStyleSheet(self._get_spinbox_style())
        self.cols_spin.valueChanged.connect(self._update_table_size)
        config_layout.addWidget(self.cols_spin)

        config_layout.addSpacing(20)

        # Checkbox para cabeçalho
        self.header_checkbox = QCheckBox("Primeira linha é cabeçalho")
        self.header_checkbox.setChecked(True)
        config_layout.addWidget(self.header_checkbox)

        config_layout.addStretch()
        layout.addWidget(config_frame)

        # Barra de ferramentas de formatação
        toolbar_frame = QFrame(self)
        toolbar_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {Color.LIGHT_BACKGROUND};
                border: 1px solid {Color.BORDER_LIGHT};
                border-radius: {Dimensions.BORDER_RADIUS_MD};
            }}
        """)
        toolbar_layout = QHBoxLayout(toolbar_frame)
        toolbar_layout.setContentsMargins(8, 6, 8, 6)
        toolbar_layout.setSpacing(4)

        btn_style = f"""
            QPushButton {{
                background-color: {Color.WHITE};
                border: 1px solid {Color.BORDER_MEDIUM};
                border-radius: 4px;
                padding: 4px 8px;
                font-size: 13px;
                min-width: 28px;
                min-height: 24px;
            }}
            QPushButton:hover {{
                background-color: {Color.LIGHT_BLUE_BG_2};
                border-color: {Color.PRIMARY_BLUE};
            }}
            QPushButton:pressed, QPushButton:checked {{
                background-color: {Color.LIGHT_BLUE_BG_1};
            }}
        """

        # Label
        toolbar_layout.addWidget(QLabel("Formatar:"))

        # Botão Negrito
        self.bold_btn = QPushButton("B")
        self.bold_btn.setToolTip("Negrito")
        self.bold_btn.setStyleSheet(btn_style + "QPushButton { font-weight: bold; }")
        self.bold_btn.clicked.connect(lambda: self._apply_format('bold'))
        toolbar_layout.addWidget(self.bold_btn)

        # Botão Itálico
        self.italic_btn = QPushButton("I")
        self.italic_btn.setToolTip("Itálico")
        self.italic_btn.setStyleSheet(btn_style + "QPushButton { font-style: italic; }")
        self.italic_btn.clicked.connect(lambda: self._apply_format('italic'))
        toolbar_layout.addWidget(self.italic_btn)

        # Botão Sublinhado
        self.underline_btn = QPushButton("U")
        self.underline_btn.setToolTip("Sublinhado")
        self.underline_btn.setStyleSheet(btn_style + "QPushButton { text-decoration: underline; }")
        self.underline_btn.clicked.connect(lambda: self._apply_format('underline'))
        toolbar_layout.addWidget(self.underline_btn)

        # Botão Sobrescrito
        self.sup_btn = QPushButton("X²")
        self.sup_btn.setToolTip("Sobrescrito")
        self.sup_btn.setStyleSheet(btn_style)
        self.sup_btn.clicked.connect(lambda: self._apply_format('superscript'))
        toolbar_layout.addWidget(self.sup_btn)

        # Botão Subescrito
        self.sub_btn = QPushButton("X₂")
        self.sub_btn.setToolTip("Subescrito")
        self.sub_btn.setStyleSheet(btn_style)
        self.sub_btn.clicked.connect(lambda: self._apply_format('subscript'))
        toolbar_layout.addWidget(self.sub_btn)

        # Separador
        sep1 = QFrame()
        sep1.setFrameShape(QFrame.Shape.VLine)
        sep1.setStyleSheet(f"background-color: {Color.BORDER_MEDIUM};")
        sep1.setFixedWidth(1)
        toolbar_layout.addWidget(sep1)

        # Label cor
        toolbar_layout.addWidget(QLabel("Cor:"))

        # Botão cor da célula
        self.cell_color_btn = QPushButton("Célula")
        self.cell_color_btn.setToolTip("Cor de fundo da célula")
        self.cell_color_btn.setStyleSheet(btn_style)
        self.cell_color_menu = self._create_color_menu('cell')
        self.cell_color_btn.setMenu(self.cell_color_menu)
        toolbar_layout.addWidget(self.cell_color_btn)

        # Botão cor da linha
        self.row_color_btn = QPushButton("Linha")
        self.row_color_btn.setToolTip("Cor de fundo da linha")
        self.row_color_btn.setStyleSheet(btn_style)
        self.row_color_menu = self._create_color_menu('row')
        self.row_color_btn.setMenu(self.row_color_menu)
        toolbar_layout.addWidget(self.row_color_btn)

        # Botão cor da coluna
        self.col_color_btn = QPushButton("Coluna")
        self.col_color_btn.setToolTip("Cor de fundo da coluna")
        self.col_color_btn.setStyleSheet(btn_style)
        self.col_color_menu = self._create_color_menu('column')
        self.col_color_btn.setMenu(self.col_color_menu)
        toolbar_layout.addWidget(self.col_color_btn)

        toolbar_layout.addStretch()
        layout.addWidget(toolbar_frame)

        # Instrução
        instruction = QLabel("Selecione células e use a barra acima para formatar. Clique duplo para editar.")
        instruction.setStyleSheet(f"color: {Color.GRAY_TEXT}; font-size: {Typography.FONT_SIZE_SM};")
        layout.addWidget(instruction)

        # Tabela
        self.table_widget = QTableWidget(3, 3, self)
        self.table_widget.setStyleSheet(f"""
            QTableWidget {{
                background-color: {Color.WHITE};
                border: 1px solid {Color.BORDER_MEDIUM};
                border-radius: {Dimensions.BORDER_RADIUS_MD};
                gridline-color: {Color.BORDER_LIGHT};
            }}
            QTableWidget::item {{
                padding: 8px;
            }}
            QTableWidget::item:selected {{
                background-color: {Color.LIGHT_BLUE_BG_2};
            }}
            QHeaderView::section {{
                background-color: {Color.LIGHT_BACKGROUND};
                padding: 6px;
                border: 1px solid {Color.BORDER_LIGHT};
                font-weight: bold;
            }}
        """)
        self.table_widget.setSelectionMode(QTableWidget.SelectionMode.ExtendedSelection)
        self.table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table_widget.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        self._init_table_headers()
        layout.addWidget(self.table_widget, 1)

        # Botões OK/Cancelar
        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

    def _get_spinbox_style(self) -> str:
        return f"""
            QSpinBox {{
                background-color: {Color.WHITE};
                border: 1px solid {Color.BORDER_MEDIUM};
                border-radius: {Dimensions.BORDER_RADIUS_SM};
                padding: 2px 6px;
                min-width: 50px;
            }}
        """

    def _create_color_menu(self, target: str) -> QMenu:
        """Cria menu de cores para célula, linha ou coluna."""
        menu = QMenu(self)
        menu.setStyleSheet(f"""
            QMenu {{
                background-color: {Color.WHITE};
                border: 1px solid {Color.BORDER_MEDIUM};
                padding: 4px;
            }}
            QMenu::item {{
                padding: 6px 12px;
            }}
            QMenu::item:selected {{
                background-color: {Color.LIGHT_BLUE_BG_1};
            }}
        """)

        for color_hex, color_name in self.PRESET_COLORS:
            action = QAction(f"  {color_name}", self)
            # Criar ícone colorido
            action.setIcon(self._create_color_icon(color_hex))
            action.triggered.connect(lambda checked, c=color_hex, t=target: self._apply_color(c, t))
            menu.addAction(action)

        menu.addSeparator()
        custom_action = QAction("Cor personalizada...", self)
        custom_action.triggered.connect(lambda: self._choose_custom_color(target))
        menu.addAction(custom_action)

        return menu

    def _create_color_icon(self, color_hex: str):
        """Cria um ícone de cor."""
        from PyQt6.QtGui import QPixmap
        pixmap = QPixmap(16, 16)
        pixmap.fill(QColor(color_hex))
        return QIcon(pixmap)

    def _choose_custom_color(self, target: str):
        """Abre diálogo para escolher cor personalizada."""
        color = QColorDialog.getColor(Qt.GlobalColor.white, self, "Escolher Cor")
        if color.isValid():
            self._apply_color(color.name(), target)

    def _apply_color(self, color_hex: str, target: str):
        """Aplica cor às células selecionadas, linha ou coluna."""
        selected = self.table_widget.selectedIndexes()
        if not selected:
            return

        cells_to_color = set()

        if target == 'cell':
            for idx in selected:
                cells_to_color.add((idx.row(), idx.column()))
        elif target == 'row':
            rows = set(idx.row() for idx in selected)
            for row in rows:
                for col in range(self.table_widget.columnCount()):
                    cells_to_color.add((row, col))
        elif target == 'column':
            cols = set(idx.column() for idx in selected)
            for col in cols:
                for row in range(self.table_widget.rowCount()):
                    cells_to_color.add((row, col))

        for row, col in cells_to_color:
            item = self.table_widget.item(row, col)
            if not item:
                item = QTableWidgetItem("")
                self.table_widget.setItem(row, col, item)
            item.setBackground(QBrush(QColor(color_hex)))

            # Armazenar cor no formato
            if (row, col) not in self.cell_formats:
                self.cell_formats[(row, col)] = {}
            self.cell_formats[(row, col)]['bg_color'] = color_hex

    def _apply_format(self, format_type: str):
        """Aplica formatação de texto às células selecionadas."""
        selected = self.table_widget.selectedIndexes()
        if not selected:
            return

        for idx in selected:
            row, col = idx.row(), idx.column()
            item = self.table_widget.item(row, col)
            if not item:
                item = QTableWidgetItem("")
                self.table_widget.setItem(row, col, item)

            # Obter fonte atual
            font = item.font()

            # Inicializar formatação da célula se não existir
            if (row, col) not in self.cell_formats:
                self.cell_formats[(row, col)] = {}

            # Toggle da formatação
            if format_type == 'bold':
                new_val = not font.bold()
                font.setBold(new_val)
                self.cell_formats[(row, col)]['bold'] = new_val
            elif format_type == 'italic':
                new_val = not font.italic()
                font.setItalic(new_val)
                self.cell_formats[(row, col)]['italic'] = new_val
            elif format_type == 'underline':
                new_val = not font.underline()
                font.setUnderline(new_val)
                self.cell_formats[(row, col)]['underline'] = new_val
            elif format_type == 'superscript':
                # Toggle superscript (armazenado apenas nos metadados)
                current = self.cell_formats[(row, col)].get('superscript', False)
                self.cell_formats[(row, col)]['superscript'] = not current
                self.cell_formats[(row, col)]['subscript'] = False  # Mutuamente exclusivo
            elif format_type == 'subscript':
                # Toggle subscript (armazenado apenas nos metadados)
                current = self.cell_formats[(row, col)].get('subscript', False)
                self.cell_formats[(row, col)]['subscript'] = not current
                self.cell_formats[(row, col)]['superscript'] = False  # Mutuamente exclusivo

            item.setFont(font)

    def _init_table_headers(self):
        """Inicializa os cabeçalhos da tabela."""
        for col in range(self.table_widget.columnCount()):
            self.table_widget.setHorizontalHeaderItem(col, QTableWidgetItem(f"Col {col + 1}"))
        for row in range(self.table_widget.rowCount()):
            self.table_widget.setVerticalHeaderItem(row, QTableWidgetItem(f"{row + 1}"))

    def _update_table_size(self):
        """Atualiza o tamanho da tabela."""
        rows = self.rows_spin.value()
        cols = self.cols_spin.value()

        # Salvar dados existentes
        old_data = {}
        for row in range(self.table_widget.rowCount()):
            for col in range(self.table_widget.columnCount()):
                item = self.table_widget.item(row, col)
                if item and item.text():
                    old_data[(row, col)] = item.text()

        # Redimensionar
        self.table_widget.setRowCount(rows)
        self.table_widget.setColumnCount(cols)

        # Restaurar dados
        for (row, col), text in old_data.items():
            if row < rows and col < cols:
                self.table_widget.setItem(row, col, QTableWidgetItem(text))

        # Atualizar cabeçalhos
        self._init_table_headers()

    def get_table_text(self) -> str:
        """Retorna o texto formatado da tabela com formatações."""
        rows = self.table_widget.rowCount()
        cols = self.table_widget.columnCount()
        has_header = self.header_checkbox.isChecked()

        lines = []
        lines.append("[TABELA]")

        for row in range(rows):
            cells = []
            for col in range(cols):
                item = self.table_widget.item(row, col)
                text = item.text() if item else ""

                # Obter formatações da célula
                fmt = self.cell_formats.get((row, col), {})

                # Aplicar formatações ao texto
                if fmt.get('superscript'):
                    text = f"<sup>{text}</sup>"
                elif fmt.get('subscript'):
                    text = f"<sub>{text}</sub>"

                if fmt.get('bold'):
                    text = f"<b>{text}</b>"
                if fmt.get('italic'):
                    text = f"<i>{text}</i>"
                if fmt.get('underline'):
                    text = f"<u>{text}</u>"

                # Adicionar cor de fundo se definida
                bg_color = fmt.get('bg_color')
                if bg_color and bg_color != '#ffffff':
                    text = f"[COR:{bg_color}]{text}[/COR]"

                cells.append(text)

            # Marcar cabeçalho
            if row == 0 and has_header:
                lines.append("[CABECALHO]" + " | ".join(cells) + "[/CABECALHO]")
            else:
                lines.append(" | ".join(cells))

        lines.append("[/TABELA]")

        return "\n".join(lines)


class ListDialog(QDialog):
    """Diálogo para criar listas itemizadas ou enumeradas de forma intuitiva."""

    # Símbolos disponíveis para lista itemizada
    ITEMIZE_SYMBOLS = [
        ('•', 'Círculo preenchido'),
        ('○', 'Círculo vazio'),
        ('■', 'Quadrado preenchido'),
        ('□', 'Quadrado vazio'),
        ('▸', 'Triângulo'),
        ('–', 'Travessão'),
        ('✓', 'Check'),
        ('★', 'Estrela'),
    ]

    # Formatos disponíveis para lista enumerada
    ENUMERATE_FORMATS = [
        ('arabic', '1, 2, 3...', 'Números arábicos'),
        ('alpha_lower', 'a, b, c...', 'Letras minúsculas'),
        ('alpha_upper', 'A, B, C...', 'Letras maiúsculas'),
        ('roman_lower', 'i, ii, iii...', 'Romano minúsculo'),
        ('roman_upper', 'I, II, III...', 'Romano maiúsculo'),
    ]

    def __init__(self, list_type: str = "itemized", parent=None):
        """
        Args:
            list_type: 'itemized' para lista com marcadores ou 'enumerated' para lista numerada
        """
        super().__init__(parent)
        self.list_type = list_type
        self.item_inputs = []
        self.current_symbol = '•'
        self.current_format = 'arabic'

        title = "Criar Lista com Marcadores" if list_type == "itemized" else "Criar Lista Numerada"
        self.setWindowTitle(title)
        self.setMinimumWidth(520)
        self.setMinimumHeight(450)

        self._setup_ui()
        self._add_item()
        self._add_item()
        self._add_item()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(Spacing.MD)

        # Frame de opções de formato
        format_frame = QFrame(self)
        format_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {Color.LIGHT_BLUE_BG_1};
                border: 1px solid {Color.LIGHT_BLUE_BORDER};
                border-radius: {Dimensions.BORDER_RADIUS_MD};
                padding: {Spacing.SM}px;
            }}
        """)
        format_layout = QVBoxLayout(format_frame)
        format_layout.setSpacing(Spacing.SM)

        # Título da seção de formato
        format_title = QLabel("Formato da Lista:", format_frame)
        format_title.setStyleSheet(f"""
            font-weight: bold;
            font-size: {Typography.FONT_SIZE_MD};
            color: {Color.PRIMARY_BLUE};
        """)
        format_layout.addWidget(format_title)

        # Opções específicas por tipo
        if self.list_type == "itemized":
            self._setup_itemize_options(format_layout)
        else:
            self._setup_enumerate_options(format_layout)

        layout.addWidget(format_frame)

        # Instrução
        instruction = QLabel(
            "Digite os itens da sua lista abaixo.\n"
            "Use os botões + e − para adicionar ou remover itens."
        )
        instruction.setStyleSheet(f"""
            color: {Color.GRAY_TEXT};
            font-size: {Typography.FONT_SIZE_SM};
            padding: {Spacing.XS}px;
        """)
        layout.addWidget(instruction)

        # Área de scroll para os itens
        scroll = QScrollArea(self)
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setStyleSheet("QScrollArea { background: transparent; }")

        self.items_container = QWidget()
        self.items_layout = QVBoxLayout(self.items_container)
        self.items_layout.setSpacing(Spacing.SM)
        self.items_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        scroll.setWidget(self.items_container)
        layout.addWidget(scroll, 1)

        # Botão adicionar item
        add_btn = QPushButton("+ Adicionar Item", self)
        add_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {Color.LIGHT_BLUE_BG_2};
                color: {Color.PRIMARY_BLUE};
                border: 1px dashed {Color.PRIMARY_BLUE};
                border-radius: {Dimensions.BORDER_RADIUS_MD};
                padding: {Spacing.SM}px {Spacing.MD}px;
                font-size: {Typography.FONT_SIZE_MD};
            }}
            QPushButton:hover {{
                background-color: {Color.LIGHT_BLUE_BG_1};
            }}
        """)
        add_btn.clicked.connect(self._add_item)
        layout.addWidget(add_btn)

        # Botões OK/Cancelar
        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        button_box.setStyleSheet(f"""
            QPushButton {{
                padding: {Spacing.SM}px {Spacing.LG}px;
                border-radius: {Dimensions.BORDER_RADIUS_MD};
                font-size: {Typography.FONT_SIZE_MD};
            }}
        """)
        layout.addWidget(button_box)

    def _setup_itemize_options(self, parent_layout):
        """Configura opções para lista itemizada (escolha de símbolo)."""
        options_layout = QHBoxLayout()
        options_layout.setSpacing(Spacing.XS)

        label = QLabel("Símbolo:", self)
        label.setStyleSheet(f"font-size: {Typography.FONT_SIZE_SM}; color: {Color.DARK_TEXT};")
        options_layout.addWidget(label)

        self.symbol_buttons = []
        for symbol, tooltip in self.ITEMIZE_SYMBOLS:
            btn = QPushButton(symbol, self)
            btn.setFixedSize(36, 36)
            btn.setToolTip(tooltip)
            btn.setStyleSheet(self._get_symbol_button_style(symbol == self.current_symbol))
            btn.clicked.connect(lambda checked, s=symbol: self._on_symbol_selected(s))
            options_layout.addWidget(btn)
            self.symbol_buttons.append((btn, symbol))

        options_layout.addStretch()
        parent_layout.addLayout(options_layout)

    def _setup_enumerate_options(self, parent_layout):
        """Configura opções para lista enumerada (formato de numeração)."""
        options_layout = QHBoxLayout()
        options_layout.setSpacing(Spacing.SM)

        label = QLabel("Numeração:", self)
        label.setStyleSheet(f"font-size: {Typography.FONT_SIZE_SM}; color: {Color.DARK_TEXT};")
        options_layout.addWidget(label)

        self.format_buttons = []
        for format_id, example, tooltip in self.ENUMERATE_FORMATS:
            btn = QPushButton(example, self)
            btn.setMinimumWidth(70)
            btn.setToolTip(tooltip)
            btn.setStyleSheet(self._get_format_button_style(format_id == self.current_format))
            btn.clicked.connect(lambda checked, f=format_id: self._on_format_selected(f))
            options_layout.addWidget(btn)
            self.format_buttons.append((btn, format_id))

        options_layout.addStretch()
        parent_layout.addLayout(options_layout)

    def _get_symbol_button_style(self, selected: bool) -> str:
        """Retorna estilo para botões de símbolo."""
        if selected:
            return f"""
                QPushButton {{
                    background-color: {Color.PRIMARY_BLUE};
                    color: white;
                    border: 2px solid {Color.PRIMARY_BLUE};
                    border-radius: 6px;
                    font-size: 16px;
                }}
            """
        return f"""
            QPushButton {{
                background-color: {Color.WHITE};
                color: {Color.DARK_TEXT};
                border: 1px solid {Color.BORDER_MEDIUM};
                border-radius: 6px;
                font-size: 16px;
            }}
            QPushButton:hover {{
                background-color: {Color.LIGHT_BLUE_BG_2};
                border-color: {Color.PRIMARY_BLUE};
            }}
        """

    def _get_format_button_style(self, selected: bool) -> str:
        """Retorna estilo para botões de formato."""
        if selected:
            return f"""
                QPushButton {{
                    background-color: {Color.PRIMARY_BLUE};
                    color: white;
                    border: 2px solid {Color.PRIMARY_BLUE};
                    border-radius: 6px;
                    font-size: {Typography.FONT_SIZE_SM};
                    padding: 4px 8px;
                }}
            """
        return f"""
            QPushButton {{
                background-color: {Color.WHITE};
                color: {Color.DARK_TEXT};
                border: 1px solid {Color.BORDER_MEDIUM};
                border-radius: 6px;
                font-size: {Typography.FONT_SIZE_SM};
                padding: 4px 8px;
            }}
            QPushButton:hover {{
                background-color: {Color.LIGHT_BLUE_BG_2};
                border-color: {Color.PRIMARY_BLUE};
            }}
        """

    def _on_symbol_selected(self, symbol: str):
        """Atualiza o símbolo selecionado."""
        self.current_symbol = symbol
        # Atualizar estilos dos botões
        for btn, sym in self.symbol_buttons:
            btn.setStyleSheet(self._get_symbol_button_style(sym == symbol))
        # Atualizar marcadores dos itens
        self._update_markers()

    def _on_format_selected(self, format_id: str):
        """Atualiza o formato de numeração selecionado."""
        self.current_format = format_id
        # Atualizar estilos dos botões
        for btn, fmt in self.format_buttons:
            btn.setStyleSheet(self._get_format_button_style(fmt == format_id))
        # Atualizar marcadores dos itens
        self._update_markers()

    def _get_marker_for_index(self, index: int) -> str:
        """Retorna o marcador para um índice específico."""
        if self.list_type == "itemized":
            return self.current_symbol
        else:
            if self.current_format == 'arabic':
                return f"{index}."
            elif self.current_format == 'alpha_lower':
                return f"{chr(ord('a') + index - 1)})"
            elif self.current_format == 'alpha_upper':
                return f"{chr(ord('A') + index - 1)})"
            elif self.current_format == 'roman_lower':
                return f"{self._to_roman(index).lower()}."
            elif self.current_format == 'roman_upper':
                return f"{self._to_roman(index)}."
        return f"{index}."

    def _to_roman(self, num: int) -> str:
        """Converte número para romano."""
        val = [1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1]
        syms = ['M', 'CM', 'D', 'CD', 'C', 'XC', 'L', 'XL', 'X', 'IX', 'V', 'IV', 'I']
        roman = ''
        for i, v in enumerate(val):
            while num >= v:
                roman += syms[i]
                num -= v
        return roman

    def _update_markers(self):
        """Atualiza todos os marcadores dos itens."""
        for i, (frame, _) in enumerate(self.item_inputs, 1):
            frame.marker.setText(self._get_marker_for_index(i))

    def _add_item(self):
        """Adiciona um novo campo de item à lista."""
        item_index = len(self.item_inputs) + 1

        # Container do item
        item_frame = QFrame(self.items_container)
        item_frame.setObjectName(f"item_frame_{item_index}")
        item_layout = QHBoxLayout(item_frame)
        item_layout.setContentsMargins(0, 0, 0, 0)
        item_layout.setSpacing(Spacing.SM)

        # Marcador visual
        marker = QLabel(self._get_marker_for_index(item_index), item_frame)
        marker.setFixedWidth(40)
        marker.setStyleSheet(f"""
            font-size: 14px;
            font-weight: bold;
            color: {Color.PRIMARY_BLUE};
        """)
        marker.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        item_layout.addWidget(marker)

        # Campo de texto
        text_input = QLineEdit(item_frame)
        text_input.setPlaceholderText(f"Digite o item {item_index}...")
        text_input.setStyleSheet(f"""
            QLineEdit {{
                background-color: {Color.WHITE};
                border: 1px solid {Color.BORDER_MEDIUM};
                border-radius: {Dimensions.BORDER_RADIUS_MD};
                padding: {Spacing.SM}px;
                font-size: {Typography.FONT_SIZE_MD};
            }}
            QLineEdit:focus {{
                border-color: {Color.PRIMARY_BLUE};
            }}
        """)
        item_layout.addWidget(text_input, 1)

        # Botão remover
        remove_btn = QPushButton("−", item_frame)
        remove_btn.setFixedSize(28, 28)
        remove_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: #fee2e2;
                color: #dc2626;
                border: 1px solid #fca5a5;
                border-radius: 14px;
                font-size: 16px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: #fecaca;
            }}
        """)
        remove_btn.clicked.connect(lambda: self._remove_item(item_frame, text_input))
        item_layout.addWidget(remove_btn)

        # Armazenar referências
        item_frame.marker = marker
        item_frame.text_input = text_input
        self.item_inputs.append((item_frame, text_input))

        self.items_layout.addWidget(item_frame)
        text_input.setFocus()

    def _remove_item(self, frame: QFrame, text_input: QLineEdit):
        """Remove um item da lista."""
        if len(self.item_inputs) <= 1:
            return  # Manter pelo menos um item

        # Remover da lista
        self.item_inputs = [(f, t) for f, t in self.item_inputs if f != frame]

        # Remover widget
        frame.setParent(None)
        frame.deleteLater()

        # Atualizar marcadores
        self._update_markers()

    def get_list_text(self) -> str:
        """Retorna o texto formatado da lista."""
        lines = []
        for i, (frame, text_input) in enumerate(self.item_inputs, 1):
            text = text_input.text().strip()
            if text:  # Ignorar itens vazios
                marker = self._get_marker_for_index(i)
                lines.append(f"   {marker} {text}")

        return "\n".join(lines)


class FormattingToolbar(QFrame):
    """Barra de ferramentas de formatação com negrito, itálico, sublinhado e letras gregas."""

    # Letras gregas minúsculas
    GREEK_LOWER = [
        ('α', 'alpha'), ('β', 'beta'), ('γ', 'gamma'), ('δ', 'delta'),
        ('ε', 'epsilon'), ('ζ', 'zeta'), ('η', 'eta'), ('θ', 'theta'),
        ('ι', 'iota'), ('κ', 'kappa'), ('λ', 'lambda'), ('μ', 'mu'),
        ('ν', 'nu'), ('ξ', 'xi'), ('ο', 'omicron'), ('π', 'pi'),
        ('ρ', 'rho'), ('σ', 'sigma'), ('τ', 'tau'), ('υ', 'upsilon'),
        ('φ', 'phi'), ('χ', 'chi'), ('ψ', 'psi'), ('ω', 'omega')
    ]

    # Letras gregas maiúsculas
    GREEK_UPPER = [
        ('Α', 'Alpha'), ('Β', 'Beta'), ('Γ', 'Gamma'), ('Δ', 'Delta'),
        ('Ε', 'Epsilon'), ('Ζ', 'Zeta'), ('Η', 'Eta'), ('Θ', 'Theta'),
        ('Ι', 'Iota'), ('Κ', 'Kappa'), ('Λ', 'Lambda'), ('Μ', 'Mu'),
        ('Ν', 'Nu'), ('Ξ', 'Xi'), ('Ο', 'Omicron'), ('Π', 'Pi'),
        ('Ρ', 'Rho'), ('Σ', 'Sigma'), ('Τ', 'Tau'), ('Υ', 'Upsilon'),
        ('Φ', 'Phi'), ('Χ', 'Chi'), ('Ψ', 'Psi'), ('Ω', 'Omega')
    ]

    def __init__(self, text_edit: QTextEdit, parent=None):
        super().__init__(parent)
        self.text_edit = text_edit
        self.setObjectName("formatting_toolbar")
        self.setStyleSheet(f"""
            QFrame#formatting_toolbar {{
                background-color: {Color.LIGHT_BACKGROUND};
                border: 1px solid {Color.BORDER_LIGHT};
                border-bottom: none;
                border-top-left-radius: {Dimensions.BORDER_RADIUS_MD};
                border-top-right-radius: {Dimensions.BORDER_RADIUS_MD};
                padding: 4px;
            }}
        """)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(8, 4, 8, 4)
        layout.setSpacing(4)

        # Estilo comum para botões
        button_style = f"""
            QPushButton {{
                background-color: {Color.WHITE};
                border: 1px solid {Color.BORDER_MEDIUM};
                border-radius: 4px;
                padding: 4px 8px;
                font-size: 14px;
                min-width: 28px;
                min-height: 24px;
            }}
            QPushButton:hover {{
                background-color: {Color.LIGHT_BLUE_BG_2};
                border-color: {Color.PRIMARY_BLUE};
            }}
            QPushButton:pressed {{
                background-color: {Color.LIGHT_BLUE_BG_1};
            }}
        """

        # Botão Negrito
        self.bold_btn = QPushButton("B", self)
        self.bold_btn.setToolTip("Negrito (Ctrl+B)")
        self.bold_btn.setStyleSheet(button_style + "QPushButton { font-weight: bold; }")
        self.bold_btn.clicked.connect(self._apply_bold)
        layout.addWidget(self.bold_btn)

        # Botão Itálico
        self.italic_btn = QPushButton("I", self)
        self.italic_btn.setToolTip("Itálico (Ctrl+I)")
        self.italic_btn.setStyleSheet(button_style + "QPushButton { font-style: italic; }")
        self.italic_btn.clicked.connect(self._apply_italic)
        layout.addWidget(self.italic_btn)

        # Botão Sublinhado
        self.underline_btn = QPushButton("U", self)
        self.underline_btn.setToolTip("Sublinhado (Ctrl+U)")
        self.underline_btn.setStyleSheet(button_style + "QPushButton { text-decoration: underline; }")
        self.underline_btn.clicked.connect(self._apply_underline)
        layout.addWidget(self.underline_btn)

        # Separador 1
        separator1 = QFrame(self)
        separator1.setFrameShape(QFrame.Shape.VLine)
        separator1.setStyleSheet(f"background-color: {Color.BORDER_MEDIUM};")
        separator1.setFixedWidth(1)
        layout.addWidget(separator1)

        # Botão Sobrescrito (superscript)
        self.superscript_btn = QPushButton("X²", self)
        self.superscript_btn.setToolTip("Sobrescrito")
        self.superscript_btn.setStyleSheet(button_style)
        self.superscript_btn.clicked.connect(self._apply_superscript)
        layout.addWidget(self.superscript_btn)

        # Botão Subescrito (subscript)
        self.subscript_btn = QPushButton("X₂", self)
        self.subscript_btn.setToolTip("Subescrito")
        self.subscript_btn.setStyleSheet(button_style)
        self.subscript_btn.clicked.connect(self._apply_subscript)
        layout.addWidget(self.subscript_btn)

        # Separador 2
        separator2 = QFrame(self)
        separator2.setFrameShape(QFrame.Shape.VLine)
        separator2.setStyleSheet(f"background-color: {Color.BORDER_MEDIUM};")
        separator2.setFixedWidth(1)
        layout.addWidget(separator2)

        # Botão Letras Gregas Minúsculas
        self.greek_lower_btn = QPushButton("αβγ", self)
        self.greek_lower_btn.setToolTip("Letras gregas minúsculas")
        self.greek_lower_btn.setStyleSheet(button_style)
        self.greek_lower_menu = self._create_greek_menu(self.GREEK_LOWER)
        self.greek_lower_btn.setMenu(self.greek_lower_menu)
        layout.addWidget(self.greek_lower_btn)

        # Botão Letras Gregas Maiúsculas
        self.greek_upper_btn = QPushButton("ΑΒΓ", self)
        self.greek_upper_btn.setToolTip("Letras gregas maiúsculas")
        self.greek_upper_btn.setStyleSheet(button_style)
        self.greek_upper_menu = self._create_greek_menu(self.GREEK_UPPER)
        self.greek_upper_btn.setMenu(self.greek_upper_menu)
        layout.addWidget(self.greek_upper_btn)

        # Separador 3
        separator3 = QFrame(self)
        separator3.setFrameShape(QFrame.Shape.VLine)
        separator3.setStyleSheet(f"background-color: {Color.BORDER_MEDIUM};")
        separator3.setFixedWidth(1)
        layout.addWidget(separator3)

        # Botão Lista Itemizada (marcadores)
        self.list_itemized_btn = QPushButton("• ─", self)
        self.list_itemized_btn.setToolTip("Lista com marcadores")
        self.list_itemized_btn.setStyleSheet(button_style)
        self.list_itemized_btn.clicked.connect(self._open_itemized_list_dialog)
        layout.addWidget(self.list_itemized_btn)

        # Botão Lista Enumerada (numerada)
        self.list_enumerated_btn = QPushButton("1. ─", self)
        self.list_enumerated_btn.setToolTip("Lista numerada")
        self.list_enumerated_btn.setStyleSheet(button_style)
        self.list_enumerated_btn.clicked.connect(self._open_enumerated_list_dialog)
        layout.addWidget(self.list_enumerated_btn)

        # Separador 4
        separator4 = QFrame(self)
        separator4.setFrameShape(QFrame.Shape.VLine)
        separator4.setStyleSheet(f"background-color: {Color.BORDER_MEDIUM};")
        separator4.setFixedWidth(1)
        layout.addWidget(separator4)

        # Botão Tabela
        self.table_btn = QPushButton("⊞", self)
        self.table_btn.setToolTip("Inserir tabela")
        self.table_btn.setStyleSheet(button_style + "QPushButton { font-size: 16px; }")
        self.table_btn.clicked.connect(self._open_table_dialog)
        layout.addWidget(self.table_btn)

        layout.addStretch()

    def _create_greek_menu(self, letters: list) -> QMenu:
        """Cria menu com letras gregas."""
        menu = QMenu(self)
        menu.setStyleSheet(f"""
            QMenu {{
                background-color: {Color.WHITE};
                border: 1px solid {Color.BORDER_MEDIUM};
                border-radius: 4px;
                padding: 4px;
            }}
            QMenu::item {{
                padding: 4px 12px;
                font-size: 12px;
            }}
            QMenu::item:selected {{
                background-color: {Color.LIGHT_BLUE_BG_1};
                color: {Color.PRIMARY_BLUE};
            }}
        """)

        # Criar grid de letras (4 colunas)
        for i, (letter, name) in enumerate(letters):
            action = QAction(f"{letter}  ({name})", self)
            action.triggered.connect(lambda checked, l=letter: self._insert_text(l))
            menu.addAction(action)

        return menu

    def _insert_text(self, text: str):
        """Insere texto na posição do cursor."""
        cursor = self.text_edit.textCursor()
        cursor.insertText(text)
        self.text_edit.setTextCursor(cursor)
        self.text_edit.setFocus()

    def _apply_bold(self):
        """Aplica formatação negrito ao texto selecionado."""
        cursor = self.text_edit.textCursor()
        if cursor.hasSelection():
            selected = cursor.selectedText()
            cursor.insertText(f"<b>{selected}</b>")
        else:
            cursor.insertText("<b></b>")
            cursor.movePosition(QTextCursor.MoveOperation.Left, QTextCursor.MoveMode.MoveAnchor, 4)
        self.text_edit.setTextCursor(cursor)
        self.text_edit.setFocus()

    def _apply_italic(self):
        """Aplica formatação itálico ao texto selecionado."""
        cursor = self.text_edit.textCursor()
        if cursor.hasSelection():
            selected = cursor.selectedText()
            cursor.insertText(f"<i>{selected}</i>")
        else:
            cursor.insertText("<i></i>")
            cursor.movePosition(QTextCursor.MoveOperation.Left, QTextCursor.MoveMode.MoveAnchor, 4)
        self.text_edit.setTextCursor(cursor)
        self.text_edit.setFocus()

    def _apply_underline(self):
        """Aplica formatação sublinhado ao texto selecionado."""
        cursor = self.text_edit.textCursor()
        if cursor.hasSelection():
            selected = cursor.selectedText()
            cursor.insertText(f"<u>{selected}</u>")
        else:
            cursor.insertText("<u></u>")
            cursor.movePosition(QTextCursor.MoveOperation.Left, QTextCursor.MoveMode.MoveAnchor, 4)
        self.text_edit.setTextCursor(cursor)
        self.text_edit.setFocus()

    def _apply_superscript(self):
        """Aplica formatação sobrescrito ao texto selecionado."""
        cursor = self.text_edit.textCursor()
        if cursor.hasSelection():
            selected = cursor.selectedText()
            cursor.insertText(f"<sup>{selected}</sup>")
        else:
            cursor.insertText("<sup></sup>")
            cursor.movePosition(QTextCursor.MoveOperation.Left, QTextCursor.MoveMode.MoveAnchor, 6)
        self.text_edit.setTextCursor(cursor)
        self.text_edit.setFocus()

    def _apply_subscript(self):
        """Aplica formatação subescrito ao texto selecionado."""
        cursor = self.text_edit.textCursor()
        if cursor.hasSelection():
            selected = cursor.selectedText()
            cursor.insertText(f"<sub>{selected}</sub>")
        else:
            cursor.insertText("<sub></sub>")
            cursor.movePosition(QTextCursor.MoveOperation.Left, QTextCursor.MoveMode.MoveAnchor, 6)
        self.text_edit.setTextCursor(cursor)
        self.text_edit.setFocus()

    def _open_itemized_list_dialog(self):
        """Abre diálogo para criar lista com marcadores."""
        dialog = ListDialog(list_type="itemized", parent=self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            list_text = dialog.get_list_text()
            if list_text:
                cursor = self.text_edit.textCursor()
                # Adicionar quebra de linha antes e depois se não estiver no início
                prefix = "\n" if cursor.position() > 0 else ""
                cursor.insertText(f"{prefix}{list_text}\n")
                self.text_edit.setTextCursor(cursor)
        self.text_edit.setFocus()

    def _open_enumerated_list_dialog(self):
        """Abre diálogo para criar lista numerada."""
        dialog = ListDialog(list_type="enumerated", parent=self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            list_text = dialog.get_list_text()
            if list_text:
                cursor = self.text_edit.textCursor()
                # Adicionar quebra de linha antes e depois se não estiver no início
                prefix = "\n" if cursor.position() > 0 else ""
                cursor.insertText(f"{prefix}{list_text}\n")
                self.text_edit.setTextCursor(cursor)
        self.text_edit.setFocus()

    def _open_table_dialog(self):
        """Abre diálogo para criar tabela."""
        dialog = TableDialog(parent=self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            table_text = dialog.get_table_text()
            if table_text:
                cursor = self.text_edit.textCursor()
                # Adicionar quebra de linha antes e depois se não estiver no início
                prefix = "\n" if cursor.position() > 0 else ""
                cursor.insertText(f"{prefix}{table_text}\n")
                self.text_edit.setTextCursor(cursor)
        self.text_edit.setFocus()


class TextInput(QLineEdit):
    def __init__(self, parent=None, placeholder_text="Enter text", object_name="text_input"):
        super().__init__(parent)
        self.setObjectName(object_name)
        self.setPlaceholderText(placeholder_text)
        self.setStyleSheet(f"""
            QLineEdit#{object_name} {{
                background-color: {Color.WHITE};
                border: 1px solid {Color.BORDER_MEDIUM};
                border-radius: {Dimensions.BORDER_RADIUS_MD};
                padding: {Spacing.SM}px;
                font-size: {Typography.FONT_SIZE_MD};
                color: {Color.DARK_TEXT};
            }}
            QLineEdit#{object_name}:focus {{
                border: 1px solid {Color.PRIMARY_BLUE};
            }}
        """)

class SearchInput(QLineEdit):
    def __init__(self, parent=None, placeholder_text="Search...", object_name="search_input"):
        super().__init__(parent)
        self.setObjectName(object_name)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setContentsMargins(Spacing.XL, 0, Spacing.SM, 0)
        self.setPlaceholderText(placeholder_text)
        self.setStyleSheet(f"""
            QLineEdit#search_input {{
                background-color: {Color.BORDER_LIGHT};
                border: none;
                border-radius: {Dimensions.BORDER_RADIUS_MD};
                padding: {Spacing.SM}px {Spacing.SM}px {Spacing.SM}px {Spacing.XL}px;
                font-size: {Typography.FONT_SIZE_MD};
                color: {Color.DARK_TEXT};
            }}
            QLineEdit#search_input::placeholder {{
                color: {Color.GRAY_TEXT};
            }}
        """)
        self.old_paintEvent = self.paintEvent
        self.paintEvent = self._custom_paint_event

    def _custom_paint_event(self, event):
        self.old_paintEvent(event)
        painter = QPainter(self)
        icon = QApplication.style().standardIcon(QStyle.StandardPixmap.SP_FileDialogToParent)
        pixmap = icon.pixmap(QSize(16, 16))
        painter.drawPixmap(Spacing.SM, (self.height() - pixmap.height()) // 2, pixmap)
        painter.end()


class TextAreaInput(QTextEdit):
    def __init__(self, parent=None, placeholder_text="Enter multi-line text", object_name="textarea_input"):
        super().__init__(parent)
        self.setObjectName(object_name)
        self.setPlaceholderText(placeholder_text)
        self.setMinimumHeight(100)
        self.setStyleSheet(f"""
            QTextEdit#{object_name} {{
                background-color: {Color.WHITE};
                border: 1px solid {Color.BORDER_MEDIUM};
                border-radius: {Dimensions.BORDER_RADIUS_MD};
                padding: {Spacing.SM}px;
                font-size: {Typography.FONT_SIZE_MD};
                color: {Color.DARK_TEXT};
            }}
            QTextEdit#{object_name}:focus {{
                border: 1px solid {Color.PRIMARY_BLUE};
            }}
        """)

class LatexTextArea(QTextEdit):
    def __init__(self, parent=None, placeholder_text="Enter LaTeX content", object_name="latex_textarea"):
        super().__init__(parent)
        self.setObjectName(object_name)
        self.setPlaceholderText(placeholder_text)
        self.setMinimumHeight(150)
        self.setStyleSheet(f"""
            QTextEdit#{object_name} {{
                background-color: {Color.WHITE};
                border: 1px solid {Color.BORDER_MEDIUM};
                border-radius: {Dimensions.BORDER_RADIUS_MD};
                padding: {Spacing.SM}px;
                font-size: {Typography.FONT_SIZE_MD};
                color: {Color.DARK_TEXT};
                font-family: "Consolas", "Monaco", "monospace";
            }}
            QTextEdit#{object_name}:focus {{
                border: 1px solid {Color.PRIMARY_BLUE};
            }}
        """)


class SelectInput(QComboBox):
    def __init__(self, parent=None, items=None, object_name="select_input"):
        super().__init__(parent)
        self.setObjectName(object_name)
        if items:
            self.addItems(items)
        self.setStyleSheet(f"""
            QComboBox#{object_name} {{
                background-color: {Color.WHITE};
                border: 1px solid {Color.BORDER_MEDIUM};
                border-radius: {Dimensions.BORDER_RADIUS_MD};
                padding: {Spacing.SM}px;
                font-size: {Typography.FONT_SIZE_MD};
                color: {Color.DARK_TEXT};
            }}
            QComboBox#{object_name}::drop-down {{
                border: 0px;
            }}
            QComboBox#{object_name}::down-arrow {{
                image: url(resources/icons/arrow_down.png);
                width: 12px;
                height: 12px;
            }}
            QComboBox#{object_name}:focus {{
                border: 1px solid {Color.PRIMARY_BLUE};
            }}
            QComboBox#{object_name} QAbstractItemView {{
                border: 1px solid {Color.BORDER_MEDIUM};
                border-radius: {Dimensions.BORDER_RADIUS_MD};
                background-color: {Color.WHITE};
                selection-background-color: {Color.LIGHT_BLUE_BG_1};
                selection-color: {Color.PRIMARY_BLUE};
            }}
        """)

class DateInput(QDateEdit):
    def __init__(self, parent=None, object_name="date_input"):
        super().__init__(parent)
        self.setObjectName(object_name)
        self.setCalendarPopup(True)
        self.setDate(QDate.currentDate())
        self.setDisplayFormat("dd/MM/yyyy")
        self.setStyleSheet(f"""
            QDateEdit#{object_name} {{
                background-color: {Color.WHITE};
                border: 1px solid {Color.BORDER_MEDIUM};
                border-radius: {Dimensions.BORDER_RADIUS_MD};
                padding: {Spacing.SM}px;
                font-size: {Typography.FONT_SIZE_MD};
                color: {Color.DARK_TEXT};
            }}
            QDateEdit#{object_name}::drop-down {{
                border: 0px;
            }}
            QDateEdit#{object_name}::down-arrow {{
                image: url(resources/icons/calendar.png);
                width: 16px;
                height: 16px;
            }}
            QDateEdit#{object_name}:focus {{
                border: 1px solid {Color.PRIMARY_BLUE};
            }}
        """)

if __name__ == '__main__':
    import sys
    from PyQt6.QtWidgets import QVBoxLayout

    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    from src.views.design.theme import ThemeManager
    ThemeManager.apply_global_theme(app)

    window = QWidget()
    layout = QVBoxLayout()

    text_input = TextInput(placeholder_text="Nome do Usuário")
    layout.addWidget(text_input)

    search_input = SearchInput(placeholder_text="Buscar questões...")
    layout.addWidget(search_input)

    textarea_input = TextAreaInput(placeholder_text="Descrição detalhada...")
    layout.addWidget(textarea_input)

    latex_textarea = LatexTextArea(placeholder_text="Digite sua equação LaTeX aqui...")
    layout.addWidget(latex_textarea)

    select_input = SelectInput(items=["Opção 1", "Opção 2", "Opção 3"])
    layout.addWidget(select_input)

    date_input = DateInput()
    layout.addWidget(date_input)

    window.setLayout(layout)
    window.setWindowTitle("Input Test")
    window.show()
    sys.exit(app.exec_())