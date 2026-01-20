"""
Component: Sidebar
Barra lateral com árvore de tags hierárquica
Baseado no design do mathbank_sidebar.py
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QFrame, QScrollArea
)
from PyQt6.QtCore import Qt, pyqtSignal
from typing import List
import logging

from src.application.dtos.tag_dto import TagResponseDTO

logger = logging.getLogger(__name__)


class Sidebar(QWidget):
    """Barra lateral com árvore de tags e ações"""

    tagSelected = pyqtSignal(str, str)  # uuid, nome
    exportClicked = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("sidebar")
        self.setFixedWidth(288)
        self.selected_tag_uuid = None
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(24)

        # Header
        header_layout = QHBoxLayout()

        header_info = QVBoxLayout()
        header_info.setSpacing(4)

        title = QLabel("CONTEÚDOS")
        title.setObjectName("sidebar_title")

        subtitle = QLabel("Tags Hierárquicas")
        subtitle.setObjectName("sidebar_subtitle")

        header_info.addWidget(title)
        header_info.addWidget(subtitle)

        header_layout.addLayout(header_info)
        header_layout.addStretch()

        expand_btn = QLabel("⋮")
        expand_btn.setObjectName("sidebar_icon")
        header_layout.addWidget(expand_btn)

        layout.addLayout(header_layout)

        # Árvore de navegação
        self.tree_scroll = QScrollArea()
        self.tree_scroll.setWidgetResizable(True)
        self.tree_scroll.setFrameShape(QFrame.Shape.NoFrame)

        self.tree_widget = QWidget()
        self.tree_layout = QVBoxLayout(self.tree_widget)
        self.tree_layout.setSpacing(4)
        self.tree_layout.setContentsMargins(0, 0, 0, 0)

        # Placeholder inicial
        placeholder = QLabel("Carregando tags...")
        placeholder.setStyleSheet("color: #616f89; padding: 20px;")
        self.tree_layout.addWidget(placeholder)
        self.tree_layout.addStretch()

        self.tree_scroll.setWidget(self.tree_widget)
        layout.addWidget(self.tree_scroll, 1)

        # Botão de exportar
        export_btn = QPushButton("📄 Exportar para PDF")
        export_btn.setObjectName("export_button")
        export_btn.setMinimumHeight(40)
        export_btn.clicked.connect(self.exportClicked.emit)

        layout.addWidget(export_btn)

    def load_tags(self, tags_arvore: List[TagResponseDTO]):
        """Carrega a árvore de tags na sidebar"""
        # Limpar layout atual
        while self.tree_layout.count():
            child = self.tree_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        # Adicionar tags
        self._add_tags_recursively(tags_arvore, level=0)

        self.tree_layout.addStretch()

    def _add_tags_recursively(self, tags: List[TagResponseDTO], level: int = 0, parent_expanded: bool = True):
        """Adiciona tags recursivamente à árvore"""
        for tag in tags:
            item = self._create_tree_item(tag, level)
            self.tree_layout.addWidget(item)

            # Adicionar filhos
            if tag.filhos:
                self._add_tags_recursively(tag.filhos, level + 1)

    def _create_tree_item(self, tag: TagResponseDTO, level: int) -> QFrame:
        """Cria um item da árvore de tags"""
        item = QFrame()
        item.setObjectName("tree_item")
        item.setCursor(Qt.CursorShape.PointingHandCursor)

        item_layout = QHBoxLayout(item)
        item_layout.setContentsMargins(12 + (level * 16), 8, 12, 8)
        item_layout.setSpacing(8)

        # Ícone de expansão
        has_children = bool(tag.filhos)
        if has_children:
            arrow_label = QLabel("▶")
        else:
            arrow_label = QLabel(" ")
        arrow_label.setFixedWidth(12)
        item_layout.addWidget(arrow_label)

        # Ícone da tag (baseado na numeração)
        icon = self._get_tag_icon(tag.numeracao)
        icon_label = QLabel(icon)
        item_layout.addWidget(icon_label)

        # Nome da tag
        text_label = QLabel(tag.nome)
        text_label.setObjectName("tree_item_text_inactive")
        item_layout.addWidget(text_label)
        item_layout.addStretch()

        # Armazenar dados da tag
        item.setProperty("tag_uuid", tag.uuid)
        item.setProperty("tag_nome", tag.nome)

        # Evento de clique
        item.mousePressEvent = lambda e, t=tag: self._on_tag_clicked(t)

        return item

    def _get_tag_icon(self, numeracao: str) -> str:
        """Retorna ícone baseado na numeração da tag"""
        if not numeracao:
            return "📁"

        if numeracao.startswith('V'):
            return "🏛️"  # Vestibular
        elif numeracao.startswith('N'):
            return "📚"  # Série/Nível
        elif numeracao.startswith('1'):
            return "≈"   # Álgebra
        elif numeracao.startswith('2'):
            return "▦"   # Geometria
        elif numeracao.startswith('3'):
            return "📈"  # Cálculo
        elif numeracao.startswith('4'):
            return "📊"  # Estatística
        elif numeracao.startswith('5'):
            return "△"   # Trigonometria
        else:
            return "📁"

    def _on_tag_clicked(self, tag: TagResponseDTO):
        """Callback quando uma tag é clicada"""
        self.selected_tag_uuid = tag.uuid
        self.tagSelected.emit(tag.uuid, tag.nome)
        logger.info(f"Tag selecionada: {tag.nome} ({tag.uuid})")

    def get_selected_tag_uuid(self) -> str:
        """Retorna UUID da tag selecionada"""
        return self.selected_tag_uuid
