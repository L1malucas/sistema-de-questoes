"""
View: Tag Manager
DESCRIÇÃO: Interface de gerenciamento de tags
RELACIONAMENTOS: TagController
COMPONENTES:
    - Árvore hierárquica de tags
    - Botões: Nova Tag, Editar, Inativar, Reativar
    - Drag-and-drop para reorganizar (opcional)
    - Contador de questões por tag
    - Validação de nomes duplicados
"""

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTreeWidget, QTreeWidgetItem, QLineEdit, QMessageBox,
    QGroupBox, QSpinBox, QInputDialog
)
from PyQt6.QtCore import Qt
import logging

from src.utils import ErrorHandler

logger = logging.getLogger(__name__)


class TagManager(QDialog):
    """
    Gerenciador de tags hierárquicas.
    Permite criar, editar e organizar tags.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Gerenciar Tags")
        self.setMinimumSize(800, 600)
        self.resize(900, 700)

        self.init_ui()
        self.load_tags()

        logger.info("TagManager inicializado")

    def init_ui(self):
        """Configura a interface"""
        layout = QVBoxLayout(self)

        # Cabeçalho
        header = QLabel("🏷️ Gerenciamento de Tags Hierárquicas")
        header.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 10px;")
        layout.addWidget(header)

        # Área principal
        main_layout = QHBoxLayout()

        # Árvore de tags (esquerda)
        tree_group = QGroupBox("Tags Existentes")
        tree_layout = QVBoxLayout(tree_group)

        self.tree = QTreeWidget()
        self.tree.setHeaderLabels(["Nome", "Numeração", "Questões"])
        self.tree.setColumnWidth(0, 300)
        self.tree.setColumnWidth(1, 100)
        self.tree.itemSelectionChanged.connect(self.on_selection_changed)
        tree_layout.addWidget(self.tree)

        # Botões de expansão
        expand_layout = QHBoxLayout()
        btn_expand = QPushButton("Expandir Tudo")
        btn_expand.clicked.connect(self.tree.expandAll)
        expand_layout.addWidget(btn_expand)

        btn_collapse = QPushButton("Recolher Tudo")
        btn_collapse.clicked.connect(self.tree.collapseAll)
        expand_layout.addWidget(btn_collapse)

        tree_layout.addLayout(expand_layout)
        main_layout.addWidget(tree_group, 2)

        # Painel de ações (direita)
        actions_group = QGroupBox("Ações")
        actions_layout = QVBoxLayout(actions_group)

        # Info da tag selecionada
        self.info_label = QLabel("Selecione uma tag para ver detalhes")
        self.info_label.setStyleSheet("padding: 10px; background-color: #f0f0f0; border-radius: 5px;")
        self.info_label.setWordWrap(True)
        self.info_label.setMinimumHeight(100)
        actions_layout.addWidget(self.info_label)

        actions_layout.addSpacing(20)

        # Botões de ação
        btn_nova = QPushButton("➕ Nova Tag")
        btn_nova.clicked.connect(self.criar_tag)
        btn_nova.setStyleSheet("""
            QPushButton {
                background-color: #1abc9c;
                color: white;
                padding: 10px;
                font-weight: bold;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #16a085;
            }
        """)
        actions_layout.addWidget(btn_nova)

        self.btn_editar = QPushButton("✏️ Editar")
        self.btn_editar.clicked.connect(self.editar_tag)
        self.btn_editar.setEnabled(False)
        actions_layout.addWidget(self.btn_editar)

        self.btn_criar_filho = QPushButton("➕ Criar Sub-tag")
        self.btn_criar_filho.clicked.connect(self.criar_subtag)
        self.btn_criar_filho.setEnabled(False)
        actions_layout.addWidget(self.btn_criar_filho)

        self.btn_inativar = QPushButton("🚫 Inativar")
        self.btn_inativar.clicked.connect(self.inativar_tag)
        self.btn_inativar.setEnabled(False)
        self.btn_inativar.setStyleSheet("QPushButton { color: #e74c3c; }")
        actions_layout.addWidget(self.btn_inativar)

        actions_layout.addStretch()

        # Info
        info_text = QLabel(
            "<b>Dica:</b><br>"
            "• Tags podem ser hierárquicas (níveis)<br>"
            "• Use numeração para organizar (1, 1.1, 1.1.1)<br>"
            "• Tags inativas não aparecem nos filtros"
        )
        info_text.setStyleSheet("color: #666; font-size: 11px; padding: 10px;")
        info_text.setWordWrap(True)
        actions_layout.addWidget(info_text)

        main_layout.addWidget(actions_group, 1)

        layout.addLayout(main_layout)

        # Botão fechar
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()

        btn_close = QPushButton("✔️ Fechar")
        btn_close.clicked.connect(self.accept)
        btn_layout.addWidget(btn_close)

        layout.addLayout(btn_layout)

    def load_tags(self):
        """Carrega tags do banco com tratamento de erros"""
        try:
            self.tree.clear()

            # TODO: Buscar do banco de dados via controller
            # Por enquanto, usar dados de exemplo
            exemplo_tags = [
            {'id': 1, 'nome': 'ÁLGEBRA', 'numeracao': '1', 'nivel': 1, 'id_pai': None, 'questoes': 15},
            {'id': 2, 'nome': 'FUNÇÕES', 'numeracao': '1.1', 'nivel': 2, 'id_pai': 1, 'questoes': 10},
            {'id': 3, 'nome': 'FUNÇÃO QUADRÁTICA', 'numeracao': '1.1.1', 'nivel': 3, 'id_pai': 2, 'questoes': 5},
            {'id': 4, 'nome': 'EQUAÇÕES', 'numeracao': '1.2', 'nivel': 2, 'id_pai': 1, 'questoes': 5},
            {'id': 5, 'nome': 'GEOMETRIA', 'numeracao': '2', 'nivel': 1, 'id_pai': None, 'questoes': 20},
            {'id': 6, 'nome': 'GEOMETRIA PLANA', 'numeracao': '2.1', 'nivel': 2, 'id_pai': 5, 'questoes': 12},
            {'id': 7, 'nome': 'GEOMETRIA ESPACIAL', 'numeracao': '2.2', 'nivel': 2, 'id_pai': 5, 'questoes': 8},
        ]

        # Criar dicionário de items
        items = {}

        # Ordenar por nível
        sorted_tags = sorted(exemplo_tags, key=lambda x: x['nivel'])

        for tag in sorted_tags:
            if tag['id_pai'] and tag['id_pai'] in items:
                item = QTreeWidgetItem(items[tag['id_pai']])
            else:
                item = QTreeWidgetItem(self.tree)

            item.setText(0, tag['nome'])
            item.setText(1, tag['numeracao'])
            item.setText(2, str(tag['questoes']))
            item.setData(0, Qt.ItemDataRole.UserRole, tag['id'])

            items[tag['id']] = item

            self.tree.expandAll()

        except Exception as e:
            ErrorHandler.handle_exception(
                self,
                e,
                "Erro ao carregar tags"
            )

    def on_selection_changed(self):
        """Callback quando seleção muda"""
        selected = self.tree.selectedItems()

        if selected:
            item = selected[0]
            nome = item.text(0)
            numeracao = item.text(1)
            questoes = item.text(2)

            self.info_label.setText(
                f"<b>{nome}</b><br>"
                f"Numeração: {numeracao}<br>"
                f"Questões: {questoes}<br>"
            )

            self.btn_editar.setEnabled(True)
            self.btn_criar_filho.setEnabled(True)
            self.btn_inativar.setEnabled(True)
        else:
            self.info_label.setText("Selecione uma tag para ver detalhes")
            self.btn_editar.setEnabled(False)
            self.btn_criar_filho.setEnabled(False)
            self.btn_inativar.setEnabled(False)

    def criar_tag(self):
        """Cria nova tag raiz com tratamento de erros"""
        try:
            nome, ok = QInputDialog.getText(self, "Nova Tag", "Nome da tag:")

            if not ok or not nome.strip():
                return

            nome = nome.strip()

            logger.info(f"Criando tag: {nome}")
            # TODO: Salvar no banco via controller
            # controller.criar_tag(nome, nivel=1, id_pai=None)

            ErrorHandler.show_success(
                self,
                "Sucesso",
                f"Tag '{nome}' criada com sucesso!"
            )
            self.load_tags()

        except Exception as e:
            ErrorHandler.handle_exception(
                self,
                e,
                "Erro ao criar tag"
            )

    def criar_subtag(self):
        """Cria sub-tag da tag selecionada com tratamento de erros"""
        try:
            selected = self.tree.selectedItems()
            if not selected:
                return

            pai_nome = selected[0].text(0)
            pai_id = selected[0].data(0, Qt.ItemDataRole.UserRole)

            nome, ok = QInputDialog.getText(self, "Nova Sub-tag", f"Nome da sub-tag de '{pai_nome}':")

            if not ok or not nome.strip():
                return

            nome = nome.strip()

            logger.info(f"Criando sub-tag: {nome} (pai: {pai_nome})")
            # TODO: Salvar no banco via controller
            # controller.criar_tag(nome, nivel=2, id_pai=pai_id)

            ErrorHandler.show_success(
                self,
                "Sucesso",
                f"Sub-tag '{nome}' criada com sucesso!"
            )
            self.load_tags()

        except Exception as e:
            ErrorHandler.handle_exception(
                self,
                e,
                "Erro ao criar sub-tag"
            )

    def editar_tag(self):
        """Edita tag selecionada com tratamento de erros"""
        try:
            selected = self.tree.selectedItems()
            if not selected:
                return

            nome_atual = selected[0].text(0)
            tag_id = selected[0].data(0, Qt.ItemDataRole.UserRole)

            nome, ok = QInputDialog.getText(self, "Editar Tag", "Novo nome:", text=nome_atual)

            if not ok or not nome.strip():
                return

            nome = nome.strip()

            if nome == nome_atual:
                return  # Sem mudança

            logger.info(f"Editando tag: {nome_atual} -> {nome}")
            # TODO: Atualizar no banco via controller
            # controller.atualizar_tag(tag_id, nome=nome)

            ErrorHandler.show_success(
                self,
                "Sucesso",
                "Tag atualizada com sucesso!"
            )
            self.load_tags()

        except Exception as e:
            ErrorHandler.handle_exception(
                self,
                e,
                "Erro ao editar tag"
            )

    def inativar_tag(self):
        """Inativa tag selecionada com tratamento de erros"""
        try:
            selected = self.tree.selectedItems()
            if not selected:
                return

            nome = selected[0].text(0)
            tag_id = selected[0].data(0, Qt.ItemDataRole.UserRole)

            reply = QMessageBox.question(
                self,
                "Confirmar",
                f"Deseja inativar a tag '{nome}'?\n\n"
                "Tags inativas não aparecem nos filtros mas os dados são mantidos.",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )

            if reply != QMessageBox.StandardButton.Yes:
                return

            logger.info(f"Inativando tag: {nome}")
            # TODO: Inativar no banco via controller
            # controller.inativar_tag(tag_id)

            ErrorHandler.show_success(
                self,
                "Sucesso",
                "Tag inativada com sucesso!"
            )
            self.load_tags()

        except Exception as e:
            ErrorHandler.handle_exception(
                self,
                e,
                "Erro ao inativar tag"
            )


logger.info("TagManager carregado")
