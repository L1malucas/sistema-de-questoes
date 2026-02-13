# src/views/pages/taxonomy_page.py
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame,
    QGridLayout, QScrollArea, QTableWidget, QTableWidgetItem,
    QHeaderView, QPushButton, QSizePolicy, QSpacerItem, QMessageBox,
    QComboBox, QListWidget, QListWidgetItem, QTabWidget,
    QAbstractItemView, QInputDialog, QLineEdit, QSpinBox
)
from PyQt6.QtCore import Qt, pyqtSignal, QSize
from PyQt6.QtGui import QIcon, QColor
from typing import Dict, List, Any, Optional

from src.views.design.constants import Color, Spacing, Typography, Dimensions, Text
from src.views.components.common.inputs import TextInput
from src.views.components.common.buttons import PrimaryButton, SecondaryButton
from src.views.components.layout.sidebar import TagTreeView
from src.controllers.tag_controller_orm import TagControllerORM
from src.controllers.adapters import (
    criar_tag_controller,
    listar_disciplinas_completas, criar_disciplina, atualizar_disciplina, inativar_disciplina,
    listar_fontes_questao_completas, criar_fonte_questao, atualizar_fonte_questao, inativar_fonte_questao,
    listar_niveis_escolares, criar_nivel_escolar, atualizar_nivel_escolar, inativar_nivel_escolar,
    buscar_arvore_disciplina,
)


class TaxonomyPage(QWidget):
    """
    Page for managing tags (by discipline) and CRUD for disciplines, sources, school levels.
    Left panel: discipline selector + tag tree + tag edit form.
    Right panel: tabs for disciplines, sources, school levels CRUD.
    """
    tag_selected = pyqtSignal(str)
    save_tag_requested = pyqtSignal(dict)
    delete_tag_requested = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("taxonomy_page")

        self.tag_controller = criar_tag_controller()
        self.current_tag_uuid: Optional[str] = None
        self.current_tag_data: Optional[Dict] = None

        # Right panel state
        self._current_disc_uuid: Optional[str] = None
        self._current_fonte_uuid: Optional[str] = None
        self._current_nivel_uuid: Optional[str] = None

        self._setup_ui()
        self._load_disciplines_combo()
        self._load_disciplines_list()
        self._load_fontes_list()
        self._load_niveis_list()

    # ================================================================
    # UI Setup
    # ================================================================

    def _setup_ui(self):
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(Spacing.XL, Spacing.LG, Spacing.XL, Spacing.LG)
        main_layout.setSpacing(Spacing.LG)

        # Left panel - tags by discipline
        left_frame = self._create_left_panel()
        main_layout.addWidget(left_frame, 3)

        # Right panel - CRUD tabs
        right_frame = self._create_right_panel()
        main_layout.addWidget(right_frame, 2)

    def _create_frame(self, object_name: str) -> QFrame:
        frame = QFrame(self)
        frame.setObjectName(object_name)
        frame.setStyleSheet(f"""
            QFrame#{object_name} {{
                background-color: {Color.WHITE};
                border: 1px solid {Color.BORDER_LIGHT};
                border-radius: {Dimensions.BORDER_RADIUS_LG};
            }}
        """)
        return frame

    # ----------------------------------------------------------------
    # LEFT PANEL
    # ----------------------------------------------------------------

    def _create_left_panel(self) -> QFrame:
        frame = self._create_frame("taxonomy_left_frame")
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(Spacing.MD, Spacing.MD, Spacing.MD, Spacing.MD)
        layout.setSpacing(Spacing.SM)

        # Title
        title = QLabel(Text.TAXONOMY_TITLE, frame)
        title.setStyleSheet(f"""
            font-weight: {Typography.FONT_WEIGHT_BOLD};
            font-size: {Typography.FONT_SIZE_LG};
            color: {Color.DARK_TEXT};
        """)
        layout.addWidget(title)

        # Discipline combo
        disc_layout = QHBoxLayout()
        disc_label = QLabel("Disciplina:", frame)
        disc_label.setStyleSheet(f"font-weight: {Typography.FONT_WEIGHT_SEMIBOLD}; color: {Color.DARK_TEXT};")
        disc_layout.addWidget(disc_label)

        self.disciplina_combo = QComboBox(frame)
        self.disciplina_combo.setMinimumWidth(250)
        self.disciplina_combo.setStyleSheet(f"""
            QComboBox {{
                padding: {Spacing.SM}px {Spacing.MD}px;
                border: 1px solid {Color.BORDER_LIGHT};
                border-radius: {Dimensions.BORDER_RADIUS_SM};
                background-color: {Color.WHITE};
                font-size: {Typography.FONT_SIZE_MD};
            }}
            QComboBox:hover {{ border-color: {Color.PRIMARY_BLUE}; }}
            QComboBox::drop-down {{ border: none; padding-right: {Spacing.SM}px; }}
        """)
        self.disciplina_combo.currentIndexChanged.connect(self._on_disciplina_changed)
        disc_layout.addWidget(self.disciplina_combo, 1)
        layout.addLayout(disc_layout)

        # Tags count
        self.tags_count_label = QLabel("", frame)
        self.tags_count_label.setStyleSheet(f"font-size: {Typography.FONT_SIZE_SM}; color: {Color.GRAY_TEXT};")
        layout.addWidget(self.tags_count_label)

        # Tag tree
        self.tag_tree_view = TagTreeView(frame)
        self.tag_tree_view.tag_selected.connect(self._on_tree_tag_selected)
        layout.addWidget(self.tag_tree_view, 1)

        # Placeholder when no discipline
        self.no_discipline_label = QLabel(Text.TAXONOMY_NO_DISCIPLINE, frame)
        self.no_discipline_label.setStyleSheet(f"color: {Color.GRAY_TEXT}; font-style: italic; padding: {Spacing.LG}px;")
        self.no_discipline_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.no_discipline_label)

        # Separator
        sep = QFrame(frame)
        sep.setFrameShape(QFrame.Shape.HLine)
        sep.setStyleSheet(f"color: {Color.BORDER_LIGHT};")
        layout.addWidget(sep)

        # Tag edit form
        form_grid = QGridLayout()
        form_grid.setSpacing(Spacing.SM)

        form_grid.addWidget(QLabel(Text.TAXONOMY_TAG_NAME, frame), 0, 0)
        self.tag_name_input = TextInput(parent=frame)
        form_grid.addWidget(self.tag_name_input, 0, 1)

        form_grid.addWidget(QLabel(Text.TAXONOMY_TAG_NUM, frame), 1, 0)
        self.tag_num_input = TextInput(parent=frame)
        self.tag_num_input.setReadOnly(True)
        form_grid.addWidget(self.tag_num_input, 1, 1)

        layout.addLayout(form_grid)

        # Buttons
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(Spacing.SM)

        self.btn_create_root = SecondaryButton(Text.TAXONOMY_CREATE_ROOT, parent=frame)
        self.btn_create_root.clicked.connect(self._on_create_root_tag)
        self.btn_create_root.setEnabled(False)
        btn_layout.addWidget(self.btn_create_root)

        self.btn_create_sub = SecondaryButton(Text.TAXONOMY_CREATE_SUB, parent=frame)
        self.btn_create_sub.clicked.connect(self._on_create_sub_tag)
        self.btn_create_sub.setEnabled(False)
        btn_layout.addWidget(self.btn_create_sub)

        self.btn_save_tag = PrimaryButton(Text.TAXONOMY_SAVE_CHANGES, parent=frame)
        self.btn_save_tag.clicked.connect(self._on_save_tag)
        self.btn_save_tag.setEnabled(False)
        btn_layout.addWidget(self.btn_save_tag)

        self.btn_delete_tag = SecondaryButton(Text.TAXONOMY_DELETE_TAG, parent=frame)
        self.btn_delete_tag.clicked.connect(self._on_delete_tag)
        self.btn_delete_tag.setEnabled(False)
        self.btn_delete_tag.setStyleSheet(f"""
            QPushButton {{ color: {Color.TAG_RED}; border-color: {Color.TAG_RED}; }}
            QPushButton:hover {{ background-color: rgba(220, 38, 38, 0.1); }}
        """)
        btn_layout.addWidget(self.btn_delete_tag)

        layout.addLayout(btn_layout)

        return frame

    # ----------------------------------------------------------------
    # RIGHT PANEL
    # ----------------------------------------------------------------

    def _create_right_panel(self) -> QFrame:
        frame = self._create_frame("taxonomy_right_frame")
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(Spacing.MD, Spacing.MD, Spacing.MD, Spacing.MD)
        layout.setSpacing(Spacing.SM)

        self.tabs = QTabWidget(frame)
        self.tabs.setStyleSheet(f"""
            QTabWidget::pane {{
                border: 1px solid {Color.BORDER_LIGHT};
                border-radius: {Dimensions.BORDER_RADIUS_SM};
                background-color: {Color.WHITE};
            }}
            QTabBar::tab {{
                padding: {Spacing.SM}px {Spacing.MD}px;
                font-size: {Typography.FONT_SIZE_MD};
                border: 1px solid {Color.BORDER_LIGHT};
                border-bottom: none;
                border-top-left-radius: {Dimensions.BORDER_RADIUS_SM};
                border-top-right-radius: {Dimensions.BORDER_RADIUS_SM};
                margin-right: 2px;
            }}
            QTabBar::tab:selected {{
                background-color: {Color.WHITE};
                font-weight: {Typography.FONT_WEIGHT_SEMIBOLD};
                color: {Color.PRIMARY_BLUE};
            }}
            QTabBar::tab:!selected {{
                background-color: {Color.LIGHT_BACKGROUND};
                color: {Color.GRAY_TEXT};
            }}
        """)

        # Tab 1: Disciplinas
        disc_tab = self._create_disciplinas_tab()
        self.tabs.addTab(disc_tab, Text.TAXONOMY_TAB_DISCIPLINES)

        # Tab 2: Fontes
        fontes_tab = self._create_fontes_tab()
        self.tabs.addTab(fontes_tab, Text.TAXONOMY_TAB_SOURCES)

        # Tab 3: Niveis Escolares
        niveis_tab = self._create_niveis_tab()
        self.tabs.addTab(niveis_tab, Text.TAXONOMY_TAB_LEVELS)

        layout.addWidget(self.tabs)
        return frame

    def _create_list_widget_style(self) -> str:
        return f"""
            QListWidget {{
                border: 1px solid {Color.BORDER_LIGHT};
                border-radius: {Dimensions.BORDER_RADIUS_SM};
                background-color: {Color.WHITE};
                font-size: {Typography.FONT_SIZE_MD};
            }}
            QListWidget::item {{
                padding: {Spacing.SM}px;
                border-bottom: 1px solid {Color.BORDER_LIGHT};
            }}
            QListWidget::item:selected {{
                background-color: {Color.PRIMARY_BLUE};
                color: {Color.WHITE};
            }}
            QListWidget::item:hover {{
                background-color: {Color.LIGHT_BACKGROUND};
            }}
        """

    # --- Disciplinas Tab ---

    def _create_disciplinas_tab(self) -> QWidget:
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(Spacing.SM, Spacing.SM, Spacing.SM, Spacing.SM)
        layout.setSpacing(Spacing.SM)

        self.disc_list = QListWidget(tab)
        self.disc_list.setStyleSheet(self._create_list_widget_style())
        self.disc_list.currentRowChanged.connect(self._on_disc_list_selected)
        layout.addWidget(self.disc_list, 1)

        # Form
        form = QGridLayout()
        form.setSpacing(Spacing.SM)

        form.addWidget(QLabel(Text.TAXONOMY_CODE, tab), 0, 0)
        self.disc_code_input = TextInput(parent=tab)
        self.disc_code_input.setMaximumWidth(120)
        form.addWidget(self.disc_code_input, 0, 1)

        form.addWidget(QLabel(Text.TAXONOMY_NAME, tab), 1, 0)
        self.disc_name_input = TextInput(parent=tab)
        form.addWidget(self.disc_name_input, 1, 1)

        form.addWidget(QLabel(Text.TAXONOMY_DESCRIPTION, tab), 2, 0)
        self.disc_desc_input = TextInput(parent=tab)
        form.addWidget(self.disc_desc_input, 2, 1)

        form.addWidget(QLabel(Text.TAXONOMY_COLOR, tab), 3, 0)
        color_container = QVBoxLayout()
        color_container.setSpacing(Spacing.XS)

        # Palette row
        palette_layout = QHBoxLayout()
        palette_layout.setSpacing(Spacing.XS)
        self._disc_color_buttons = []
        palette_colors = [
            "#3498db", "#2563eb", "#1abc9c", "#16a34a",
            "#e74c3c", "#dc2626", "#f39c12", "#ca8a04",
            "#9b59b6", "#9333ea", "#ea580c", "#e91e63",
            "#34495e", "#1e293b", "#7c3aed", "#0891b2",
        ]
        for pc in palette_colors:
            btn = QPushButton(tab)
            btn.setFixedSize(24, 24)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setToolTip(pc)
            btn.setProperty("color_value", pc)
            btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {pc};
                    border: 2px solid transparent;
                    border-radius: 12px;
                }}
                QPushButton:hover {{
                    border-color: {Color.DARK_TEXT};
                }}
            """)
            btn.clicked.connect(lambda checked, c=pc: self._select_disc_color(c))
            palette_layout.addWidget(btn)
            self._disc_color_buttons.append(btn)
        palette_layout.addStretch()
        color_container.addLayout(palette_layout)

        # Hex input + preview row
        hex_layout = QHBoxLayout()
        hex_layout.setSpacing(Spacing.SM)
        self.disc_color_input = TextInput(parent=tab)
        self.disc_color_input.setPlaceholderText("#3498db")
        self.disc_color_input.setMaximumWidth(100)
        self.disc_color_input.textChanged.connect(self._on_disc_color_changed)
        hex_layout.addWidget(self.disc_color_input)
        self.disc_color_preview = QLabel(tab)
        self.disc_color_preview.setFixedSize(28, 28)
        self.disc_color_preview.setStyleSheet(f"""
            background-color: #3498db;
            border: 1px solid {Color.BORDER_LIGHT};
            border-radius: {Dimensions.BORDER_RADIUS_SM};
        """)
        hex_layout.addWidget(self.disc_color_preview)
        hex_layout.addStretch()
        color_container.addLayout(hex_layout)

        form.addLayout(color_container, 3, 1)

        layout.addLayout(form)

        # Buttons
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(Spacing.SM)

        btn_new = SecondaryButton(Text.TAXONOMY_BTN_NEW, parent=tab)
        btn_new.clicked.connect(self._on_disc_new)
        btn_layout.addWidget(btn_new)

        btn_save = PrimaryButton(Text.TAXONOMY_BTN_SAVE, parent=tab)
        btn_save.clicked.connect(self._on_disc_save)
        btn_layout.addWidget(btn_save)

        btn_del = SecondaryButton(Text.TAXONOMY_BTN_DELETE, parent=tab)
        btn_del.clicked.connect(self._on_disc_delete)
        btn_del.setStyleSheet(f"""
            QPushButton {{ color: {Color.TAG_RED}; border-color: {Color.TAG_RED}; }}
            QPushButton:hover {{ background-color: rgba(220, 38, 38, 0.1); }}
        """)
        btn_layout.addWidget(btn_del)

        layout.addLayout(btn_layout)
        return tab

    # --- Fontes Tab ---

    def _create_fontes_tab(self) -> QWidget:
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(Spacing.SM, Spacing.SM, Spacing.SM, Spacing.SM)
        layout.setSpacing(Spacing.SM)

        self.fonte_list = QListWidget(tab)
        self.fonte_list.setStyleSheet(self._create_list_widget_style())
        self.fonte_list.currentRowChanged.connect(self._on_fonte_list_selected)
        layout.addWidget(self.fonte_list, 1)

        form = QGridLayout()
        form.setSpacing(Spacing.SM)

        form.addWidget(QLabel("Sigla:", tab), 0, 0)
        self.fonte_sigla_input = TextInput(parent=tab)
        self.fonte_sigla_input.setMaximumWidth(150)
        form.addWidget(self.fonte_sigla_input, 0, 1)

        form.addWidget(QLabel(Text.TAXONOMY_FULL_NAME, tab), 1, 0)
        self.fonte_nome_input = TextInput(parent=tab)
        form.addWidget(self.fonte_nome_input, 1, 1)

        form.addWidget(QLabel(Text.TAXONOMY_TYPE, tab), 2, 0)
        self.fonte_tipo_combo = QComboBox(tab)
        self.fonte_tipo_combo.addItems(["VESTIBULAR", "CONCURSO", "AUTORAL"])
        self.fonte_tipo_combo.setStyleSheet(f"""
            QComboBox {{
                padding: {Spacing.SM}px {Spacing.MD}px;
                border: 1px solid {Color.BORDER_LIGHT};
                border-radius: {Dimensions.BORDER_RADIUS_SM};
                background-color: {Color.WHITE};
            }}
        """)
        form.addWidget(self.fonte_tipo_combo, 2, 1)

        layout.addLayout(form)

        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(Spacing.SM)

        btn_new = SecondaryButton(Text.TAXONOMY_BTN_NEW, parent=tab)
        btn_new.clicked.connect(self._on_fonte_new)
        btn_layout.addWidget(btn_new)

        btn_save = PrimaryButton(Text.TAXONOMY_BTN_SAVE, parent=tab)
        btn_save.clicked.connect(self._on_fonte_save)
        btn_layout.addWidget(btn_save)

        btn_del = SecondaryButton(Text.TAXONOMY_BTN_DELETE, parent=tab)
        btn_del.clicked.connect(self._on_fonte_delete)
        btn_del.setStyleSheet(f"""
            QPushButton {{ color: {Color.TAG_RED}; border-color: {Color.TAG_RED}; }}
            QPushButton:hover {{ background-color: rgba(220, 38, 38, 0.1); }}
        """)
        btn_layout.addWidget(btn_del)

        layout.addLayout(btn_layout)
        return tab

    # --- Niveis Escolares Tab ---

    def _create_niveis_tab(self) -> QWidget:
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(Spacing.SM, Spacing.SM, Spacing.SM, Spacing.SM)
        layout.setSpacing(Spacing.SM)

        self.nivel_list = QListWidget(tab)
        self.nivel_list.setStyleSheet(self._create_list_widget_style())
        self.nivel_list.currentRowChanged.connect(self._on_nivel_list_selected)
        layout.addWidget(self.nivel_list, 1)

        form = QGridLayout()
        form.setSpacing(Spacing.SM)

        form.addWidget(QLabel(Text.TAXONOMY_CODE, tab), 0, 0)
        self.nivel_code_input = TextInput(parent=tab)
        self.nivel_code_input.setMaximumWidth(120)
        form.addWidget(self.nivel_code_input, 0, 1)

        form.addWidget(QLabel(Text.TAXONOMY_NAME, tab), 1, 0)
        self.nivel_name_input = TextInput(parent=tab)
        form.addWidget(self.nivel_name_input, 1, 1)

        form.addWidget(QLabel(Text.TAXONOMY_DESCRIPTION, tab), 2, 0)
        self.nivel_desc_input = TextInput(parent=tab)
        form.addWidget(self.nivel_desc_input, 2, 1)

        form.addWidget(QLabel(Text.TAXONOMY_ORDER, tab), 3, 0)
        self.nivel_order_input = QSpinBox(tab)
        self.nivel_order_input.setRange(0, 999)
        self.nivel_order_input.setMaximumWidth(120)
        form.addWidget(self.nivel_order_input, 3, 1)

        layout.addLayout(form)

        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(Spacing.SM)

        btn_new = SecondaryButton(Text.TAXONOMY_BTN_NEW, parent=tab)
        btn_new.clicked.connect(self._on_nivel_new)
        btn_layout.addWidget(btn_new)

        btn_save = PrimaryButton(Text.TAXONOMY_BTN_SAVE, parent=tab)
        btn_save.clicked.connect(self._on_nivel_save)
        btn_layout.addWidget(btn_save)

        btn_del = SecondaryButton(Text.TAXONOMY_BTN_DELETE, parent=tab)
        btn_del.clicked.connect(self._on_nivel_delete)
        btn_del.setStyleSheet(f"""
            QPushButton {{ color: {Color.TAG_RED}; border-color: {Color.TAG_RED}; }}
            QPushButton:hover {{ background-color: rgba(220, 38, 38, 0.1); }}
        """)
        btn_layout.addWidget(btn_del)

        layout.addLayout(btn_layout)
        return tab

    # ================================================================
    # LEFT PANEL LOGIC - Tags by Discipline
    # ================================================================

    def _load_disciplines_combo(self):
        self.disciplina_combo.blockSignals(True)
        self.disciplina_combo.clear()
        self.disciplina_combo.addItem(Text.TAXONOMY_SELECT_DISCIPLINE, None)
        try:
            disciplinas = self.tag_controller.listar_disciplinas()
            for disc in disciplinas:
                self.disciplina_combo.addItem(disc['texto'], disc['uuid'])
        except Exception as e:
            print(f"Erro ao carregar disciplinas no combo: {e}")
        self.disciplina_combo.blockSignals(False)

    def _on_disciplina_changed(self, index):
        uuid_disciplina = self.disciplina_combo.currentData()
        self._clear_tag_form()

        if not uuid_disciplina:
            self.tag_tree_view.setVisible(False)
            self.no_discipline_label.setVisible(True)
            self.tags_count_label.setText("")
            self.btn_create_root.setEnabled(False)
            return

        self.tag_tree_view.setVisible(True)
        self.no_discipline_label.setVisible(False)
        self.btn_create_root.setEnabled(True)
        self._load_tags_for_discipline(uuid_disciplina)

    def _load_tags_for_discipline(self, uuid_disciplina: str):
        try:
            tree_data = buscar_arvore_disciplina(uuid_disciplina)
            self.tag_tree_view.clear()

            if not tree_data:
                self.tags_count_label.setText(Text.TAXONOMY_TAGS_COUNT.format(count=0))
                return

            self.tag_tree_view._add_tags_to_tree(self.tag_tree_view, tree_data, level=0)

            # Expand first level
            for i in range(self.tag_tree_view.topLevelItemCount()):
                item = self.tag_tree_view.topLevelItem(i)
                if item:
                    self.tag_tree_view.expandItem(item)

            # Count tags
            tags = TagControllerORM.listar_tags_por_disciplina(uuid_disciplina)
            self.tags_count_label.setText(Text.TAXONOMY_TAGS_COUNT.format(count=len(tags) if tags else 0))

        except Exception as e:
            print(f"Erro ao carregar tags da disciplina: {e}")
            self.tags_count_label.setText("Erro ao carregar tags")

    def _on_tree_tag_selected(self, tag_uuid: str, tag_path: str, is_checked: bool):
        self.current_tag_uuid = tag_uuid
        self._load_tag_details(tag_uuid)
        self.tag_selected.emit(tag_uuid)

    def _load_tag_details(self, tag_uuid: str):
        try:
            tag_data = self.tag_controller.buscar_tag_por_uuid(tag_uuid)
            if not tag_data:
                return

            self.current_tag_data = tag_data
            self.tag_name_input.setText(tag_data.get('nome', ''))
            self.tag_num_input.setText(tag_data.get('numeracao', ''))
            self.btn_save_tag.setEnabled(True)
            self.btn_delete_tag.setEnabled(True)
            self.btn_create_sub.setEnabled(True)
        except Exception as e:
            print(f"Erro ao carregar detalhes da tag: {e}")

    def _clear_tag_form(self):
        self.current_tag_uuid = None
        self.current_tag_data = None
        self.tag_name_input.clear()
        self.tag_num_input.clear()
        self.btn_save_tag.setEnabled(False)
        self.btn_delete_tag.setEnabled(False)
        self.btn_create_sub.setEnabled(False)

    def _on_save_tag(self):
        if not self.current_tag_uuid or not self.current_tag_data:
            return

        new_name = self.tag_name_input.text().strip()
        if not new_name:
            QMessageBox.warning(self, "Aviso", "O nome da tag não pode estar vazio.")
            return

        try:
            result = TagControllerORM.atualizar_tag(
                numeracao_atual=self.current_tag_data.get('numeracao', ''),
                novo_nome=new_name
            )
            if result:
                QMessageBox.information(self, "Sucesso", "Tag atualizada com sucesso!")
                uuid_disc = self.disciplina_combo.currentData()
                if uuid_disc:
                    self._load_tags_for_discipline(uuid_disc)
            else:
                QMessageBox.warning(self, "Erro", "Não foi possível atualizar a tag.")
        except Exception as e:
            QMessageBox.warning(self, "Erro", f"Erro ao salvar: {str(e)}")

    def _on_delete_tag(self):
        if not self.current_tag_uuid:
            return

        reply = QMessageBox.question(
            self, "Confirmar Inativação",
            f"Tem certeza que deseja inativar a tag '{self.tag_name_input.text()}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply != QMessageBox.StandardButton.Yes:
            return

        try:
            result = TagControllerORM.inativar_tag(self.current_tag_uuid)
            if result:
                QMessageBox.information(self, "Sucesso", "Tag inativada com sucesso!")
                self._clear_tag_form()
                uuid_disc = self.disciplina_combo.currentData()
                if uuid_disc:
                    self._load_tags_for_discipline(uuid_disc)
            else:
                QMessageBox.warning(self, "Erro", "Não foi possível inativar a tag.")
        except Exception as e:
            QMessageBox.warning(self, "Erro", f"Erro ao inativar: {str(e)}")

    def _on_create_root_tag(self):
        uuid_disciplina = self.disciplina_combo.currentData()
        if not uuid_disciplina:
            return

        nome, ok = QInputDialog.getText(self, "Nova Tag Raiz", "Nome da nova tag:")
        if ok and nome.strip():
            try:
                result = TagControllerORM.criar_tag(nome.strip(), None, 'CONTEUDO', uuid_disciplina)
                if result:
                    QMessageBox.information(self, "Sucesso", f"Tag '{nome.strip()}' criada com sucesso!")
                    self._load_tags_for_discipline(uuid_disciplina)
                else:
                    QMessageBox.warning(self, "Erro", "Não foi possível criar a tag.")
            except Exception as e:
                QMessageBox.warning(self, "Erro", f"Erro ao criar tag: {str(e)}")

    def _on_create_sub_tag(self):
        if not self.current_tag_uuid:
            return

        uuid_disciplina = self.disciplina_combo.currentData()
        if not uuid_disciplina:
            return

        if not self.tag_controller.pode_criar_subtag(self.current_tag_uuid):
            QMessageBox.warning(self, "Aviso", "Esta tag não permite a criação de sub-tags.")
            return

        parent_name = self.tag_name_input.text()
        nome, ok = QInputDialog.getText(self, "Nova Sub-tag", f"Nome da sub-tag de '{parent_name}':")
        if ok and nome.strip():
            try:
                result = TagControllerORM.criar_tag(nome.strip(), self.current_tag_uuid, 'CONTEUDO', uuid_disciplina)
                if result:
                    QMessageBox.information(self, "Sucesso", f"Sub-tag '{nome.strip()}' criada com sucesso!")
                    self._load_tags_for_discipline(uuid_disciplina)
                else:
                    QMessageBox.warning(self, "Erro", "Não foi possível criar a sub-tag.")
            except Exception as e:
                QMessageBox.warning(self, "Erro", f"Erro ao criar sub-tag: {str(e)}")

    # ================================================================
    # RIGHT PANEL LOGIC - Disciplinas
    # ================================================================

    def _load_disciplines_list(self):
        self.disc_list.clear()
        try:
            discs = listar_disciplinas_completas()
            for d in discs:
                item = QListWidgetItem(f"{d['codigo']} - {d['nome']}")
                item.setData(Qt.ItemDataRole.UserRole, d['uuid'])
                item.setData(Qt.ItemDataRole.UserRole + 1, d)
                self.disc_list.addItem(item)
        except Exception as e:
            print(f"Erro ao carregar disciplinas: {e}")

    def _select_disc_color(self, color: str):
        """Called when a palette button is clicked."""
        self.disc_color_input.setText(color)

    def _on_disc_color_changed(self, text: str):
        color = text.strip() if text.strip().startswith('#') else '#3498db'
        if len(color) in (4, 7):
            self.disc_color_preview.setStyleSheet(f"""
                background-color: {color};
                border: 1px solid {Color.BORDER_LIGHT};
                border-radius: {Dimensions.BORDER_RADIUS_SM};
            """)
        # Highlight matching palette button
        for btn in self._disc_color_buttons:
            pc = btn.property("color_value")
            if pc == color:
                btn.setStyleSheet(f"""
                    QPushButton {{
                        background-color: {pc};
                        border: 3px solid {Color.DARK_TEXT};
                        border-radius: 12px;
                    }}
                """)
            else:
                btn.setStyleSheet(f"""
                    QPushButton {{
                        background-color: {pc};
                        border: 2px solid transparent;
                        border-radius: 12px;
                    }}
                    QPushButton:hover {{
                        border-color: {Color.DARK_TEXT};
                    }}
                """)

    def _on_disc_list_selected(self, row):
        if row < 0:
            self._on_disc_new()
            return
        item = self.disc_list.item(row)
        if not item:
            return
        data = item.data(Qt.ItemDataRole.UserRole + 1)
        self._current_disc_uuid = data.get('uuid')
        self.disc_code_input.setText(data.get('codigo', ''))
        self.disc_name_input.setText(data.get('nome', ''))
        self.disc_desc_input.setText(data.get('descricao', '') or '')
        self.disc_color_input.setText(data.get('cor', '#3498db'))

    def _on_disc_new(self):
        self._current_disc_uuid = None
        self.disc_list.clearSelection()
        self.disc_code_input.clear()
        self.disc_name_input.clear()
        self.disc_desc_input.clear()
        self.disc_color_input.setText("#3498db")

    def _on_disc_save(self):
        codigo = self.disc_code_input.text().strip()
        nome = self.disc_name_input.text().strip()
        if not codigo or not nome:
            QMessageBox.warning(self, "Aviso", "Código e nome são obrigatórios.")
            return

        dados = {
            'codigo': codigo,
            'nome': nome,
            'descricao': self.disc_desc_input.text().strip() or None,
            'cor': self.disc_color_input.text().strip() or '#3498db',
        }

        try:
            if self._current_disc_uuid:
                result = atualizar_disciplina(self._current_disc_uuid, dados)
                msg = "Disciplina atualizada com sucesso!"
            else:
                result = criar_disciplina(dados)
                msg = "Disciplina criada com sucesso!"

            if result:
                QMessageBox.information(self, "Sucesso", msg)
                self._load_disciplines_list()
                self._load_disciplines_combo()
                self._on_disc_new()
            else:
                QMessageBox.warning(self, "Erro", "Não foi possível salvar a disciplina.")
        except Exception as e:
            QMessageBox.warning(self, "Erro", f"Erro: {str(e)}")

    def _on_disc_delete(self):
        if not self._current_disc_uuid:
            QMessageBox.warning(self, "Aviso", "Selecione uma disciplina para inativar.")
            return

        reply = QMessageBox.question(
            self, "Confirmar Inativação",
            f"Inativar a disciplina '{self.disc_code_input.text()}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply != QMessageBox.StandardButton.Yes:
            return

        try:
            if inativar_disciplina(self._current_disc_uuid):
                QMessageBox.information(self, "Sucesso", "Disciplina inativada com sucesso!")
                self._load_disciplines_list()
                self._load_disciplines_combo()
                self._on_disc_new()
            else:
                QMessageBox.warning(self, "Erro", "Não foi possível inativar a disciplina.")
        except Exception as e:
            QMessageBox.warning(self, "Erro", f"Erro: {str(e)}")

    # ================================================================
    # RIGHT PANEL LOGIC - Fontes
    # ================================================================

    def _load_fontes_list(self):
        self.fonte_list.clear()
        try:
            fontes = listar_fontes_questao_completas()
            for f in fontes:
                item = QListWidgetItem(f"{f['sigla']} - {f['nome_completo']}")
                item.setData(Qt.ItemDataRole.UserRole, f['uuid'])
                item.setData(Qt.ItemDataRole.UserRole + 1, f)
                self.fonte_list.addItem(item)
        except Exception as e:
            print(f"Erro ao carregar fontes: {e}")

    def _on_fonte_list_selected(self, row):
        if row < 0:
            self._on_fonte_new()
            return
        item = self.fonte_list.item(row)
        if not item:
            return
        data = item.data(Qt.ItemDataRole.UserRole + 1)
        self._current_fonte_uuid = data.get('uuid')
        self.fonte_sigla_input.setText(data.get('sigla', ''))
        self.fonte_nome_input.setText(data.get('nome_completo', ''))
        tipo = data.get('tipo_instituicao', 'VESTIBULAR')
        idx = self.fonte_tipo_combo.findText(tipo)
        if idx >= 0:
            self.fonte_tipo_combo.setCurrentIndex(idx)

    def _on_fonte_new(self):
        self._current_fonte_uuid = None
        self.fonte_list.clearSelection()
        self.fonte_sigla_input.clear()
        self.fonte_nome_input.clear()
        self.fonte_tipo_combo.setCurrentIndex(0)

    def _on_fonte_save(self):
        sigla = self.fonte_sigla_input.text().strip()
        nome = self.fonte_nome_input.text().strip()
        if not sigla or not nome:
            QMessageBox.warning(self, "Aviso", "Sigla e nome completo são obrigatórios.")
            return

        dados = {
            'sigla': sigla,
            'nome_completo': nome,
            'tipo_instituicao': self.fonte_tipo_combo.currentText(),
        }

        try:
            if self._current_fonte_uuid:
                result = atualizar_fonte_questao(self._current_fonte_uuid, dados)
                msg = "Fonte atualizada com sucesso!"
            else:
                result = criar_fonte_questao(dados)
                msg = "Fonte criada com sucesso!"

            if result:
                QMessageBox.information(self, "Sucesso", msg)
                self._load_fontes_list()
                self._on_fonte_new()
            else:
                QMessageBox.warning(self, "Erro", "Não foi possível salvar a fonte.")
        except Exception as e:
            QMessageBox.warning(self, "Erro", f"Erro: {str(e)}")

    def _on_fonte_delete(self):
        if not self._current_fonte_uuid:
            QMessageBox.warning(self, "Aviso", "Selecione uma fonte para inativar.")
            return

        reply = QMessageBox.question(
            self, "Confirmar Inativação",
            f"Inativar a fonte '{self.fonte_sigla_input.text()}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply != QMessageBox.StandardButton.Yes:
            return

        try:
            if inativar_fonte_questao(self._current_fonte_uuid):
                QMessageBox.information(self, "Sucesso", "Fonte inativada com sucesso!")
                self._load_fontes_list()
                self._on_fonte_new()
            else:
                QMessageBox.warning(self, "Erro", "Não foi possível inativar a fonte.")
        except Exception as e:
            QMessageBox.warning(self, "Erro", f"Erro: {str(e)}")

    # ================================================================
    # RIGHT PANEL LOGIC - Niveis Escolares
    # ================================================================

    def _load_niveis_list(self):
        self.nivel_list.clear()
        try:
            niveis = listar_niveis_escolares()
            for n in niveis:
                item = QListWidgetItem(f"{n['codigo']} - {n['nome']}")
                item.setData(Qt.ItemDataRole.UserRole, n['uuid'])
                item.setData(Qt.ItemDataRole.UserRole + 1, n)
                self.nivel_list.addItem(item)
        except Exception as e:
            print(f"Erro ao carregar níveis: {e}")

    def _on_nivel_list_selected(self, row):
        if row < 0:
            self._on_nivel_new()
            return
        item = self.nivel_list.item(row)
        if not item:
            return
        data = item.data(Qt.ItemDataRole.UserRole + 1)
        self._current_nivel_uuid = data.get('uuid')
        self.nivel_code_input.setText(data.get('codigo', ''))
        self.nivel_name_input.setText(data.get('nome', ''))
        self.nivel_desc_input.setText(data.get('descricao', '') or '')
        self.nivel_order_input.setValue(data.get('ordem', 0))

    def _on_nivel_new(self):
        self._current_nivel_uuid = None
        self.nivel_list.clearSelection()
        self.nivel_code_input.clear()
        self.nivel_name_input.clear()
        self.nivel_desc_input.clear()
        self.nivel_order_input.setValue(0)

    def _on_nivel_save(self):
        codigo = self.nivel_code_input.text().strip()
        nome = self.nivel_name_input.text().strip()
        if not codigo or not nome:
            QMessageBox.warning(self, "Aviso", "Código e nome são obrigatórios.")
            return

        dados = {
            'codigo': codigo,
            'nome': nome,
            'descricao': self.nivel_desc_input.text().strip() or None,
            'ordem': self.nivel_order_input.value(),
        }

        try:
            if self._current_nivel_uuid:
                result = atualizar_nivel_escolar(self._current_nivel_uuid, dados)
                msg = "Nível escolar atualizado com sucesso!"
            else:
                result = criar_nivel_escolar(dados)
                msg = "Nível escolar criado com sucesso!"

            if result:
                QMessageBox.information(self, "Sucesso", msg)
                self._load_niveis_list()
                self._on_nivel_new()
            else:
                QMessageBox.warning(self, "Erro", "Não foi possível salvar o nível escolar.")
        except Exception as e:
            QMessageBox.warning(self, "Erro", f"Erro: {str(e)}")

    def _on_nivel_delete(self):
        if not self._current_nivel_uuid:
            QMessageBox.warning(self, "Aviso", "Selecione um nível para inativar.")
            return

        reply = QMessageBox.question(
            self, "Confirmar Inativação",
            f"Inativar o nível '{self.nivel_code_input.text()}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply != QMessageBox.StandardButton.Yes:
            return

        try:
            if inativar_nivel_escolar(self._current_nivel_uuid):
                QMessageBox.information(self, "Sucesso", "Nível escolar inativado com sucesso!")
                self._load_niveis_list()
                self._on_nivel_new()
            else:
                QMessageBox.warning(self, "Erro", "Não foi possível inativar o nível escolar.")
        except Exception as e:
            QMessageBox.warning(self, "Erro", f"Erro: {str(e)}")

    # ================================================================
    # Public API
    # ================================================================

    def refresh_data(self):
        """Public method to refresh all data."""
        self._load_disciplines_combo()
        self._load_disciplines_list()
        self._load_fontes_list()
        self._load_niveis_list()
        uuid_disc = self.disciplina_combo.currentData()
        if uuid_disc:
            self._load_tags_for_discipline(uuid_disc)


if __name__ == '__main__':
    import sys
    from PyQt6.QtWidgets import QApplication, QMainWindow

    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    from src.views.design.theme import ThemeManager
    ThemeManager.apply_global_theme(app)

    class TestMainWindow(QMainWindow):
        def __init__(self):
            super().__init__()
            self.setWindowTitle("Taxonomy Page Test")
            self.setGeometry(100, 100, 1200, 900)

            self.taxonomy_page = TaxonomyPage(self)
            self.setCentralWidget(self.taxonomy_page)

            self.taxonomy_page.tag_selected.connect(
                lambda uuid: print(f"Tag selected: {uuid}")
            )

    window = TestMainWindow()
    window.show()
    sys.exit(app.exec())
