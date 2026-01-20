"""
Component: TagTreeWidget
Árvore de tags com checkboxes para seleção múltipla
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QTreeWidget, QTreeWidgetItem, QTreeWidgetItemIterator
)
from PyQt6.QtCore import Qt, pyqtSignal
from typing import List
import logging

# Importar DTO para type hinting
from src.application.dtos.tag_dto import TagResponseDTO

logger = logging.getLogger(__name__)


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
