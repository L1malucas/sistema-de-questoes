"""
View: Lista Form
DESCRIÇÃO: Formulário de criação/edição de listas
RELACIONAMENTOS: ListaController, QuestaoController
COMPONENTES:
    - Campo título (obrigatório)
    - Campo tipo (opcional)
    - Editor de cabeçalho personalizado
    - Editor de instruções
    - Painel de busca de questões
    - Lista de questões selecionadas
    - Botões: Adicionar, Remover, Salvar, Cancelar
"""

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QLineEdit, QTextEdit, QListWidget, QListWidgetItem, QMessageBox,
    QGroupBox, QSplitter
)
from PyQt6.QtCore import Qt
import logging

from src.utils import ErrorHandler

logger = logging.getLogger(__name__)


class ListaForm(QDialog):
    """Formulário para criar/editar listas de questões"""

    def __init__(self, lista_id=None, parent=None):
        super().__init__(parent)
        self.lista_id = lista_id
        self.setWindowTitle("Editar Lista" if lista_id else "Nova Lista")
        self.setMinimumSize(1000, 700)
        self.init_ui()
        logger.info(f"ListaForm inicializado (ID: {lista_id})")

    def init_ui(self):
        layout = QVBoxLayout(self)

        # Título
        header = QLabel("📋 " + ("Editar Lista" if self.lista_id else "Nova Lista"))
        header.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 10px;")
        layout.addWidget(header)

        # Informações básicas
        info_group = QGroupBox("Informações da Lista")
        info_layout = QVBoxLayout(info_group)

        # Título da lista
        titulo_layout = QHBoxLayout()
        titulo_layout.addWidget(QLabel("Título:"))
        self.titulo_input = QLineEdit()
        self.titulo_input.setPlaceholderText("Ex: Prova de Matemática - 1º Bimestre")
        titulo_layout.addWidget(self.titulo_input)
        info_layout.addLayout(titulo_layout)

        # Tipo
        tipo_layout = QHBoxLayout()
        tipo_layout.addWidget(QLabel("Tipo:"))
        self.tipo_input = QLineEdit()
        self.tipo_input.setPlaceholderText("Ex: Prova, Lista de Exercícios, Simulado...")
        tipo_layout.addWidget(self.tipo_input)
        info_layout.addLayout(tipo_layout)

        layout.addWidget(info_group)

        # Cabeçalho e instruções
        text_group = QGroupBox("Cabeçalho e Instruções")
        text_layout = QVBoxLayout(text_group)

        text_layout.addWidget(QLabel("Cabeçalho (aparecerá no topo do documento):"))
        self.cabecalho_edit = QTextEdit()
        self.cabecalho_edit.setPlaceholderText("Nome da Instituição\nDisciplina\nData...")
        self.cabecalho_edit.setMaximumHeight(100)
        text_layout.addWidget(self.cabecalho_edit)

        text_layout.addWidget(QLabel("Instruções gerais:"))
        self.instrucoes_edit = QTextEdit()
        self.instrucoes_edit.setPlaceholderText("Instruções para os alunos...")
        self.instrucoes_edit.setMaximumHeight(100)
        text_layout.addWidget(self.instrucoes_edit)

        layout.addWidget(text_group)

        # Questões
        questoes_group = QGroupBox("Questões da Lista")
        questoes_layout = QVBoxLayout(questoes_group)

        # Lista de questões
        self.questoes_list = QListWidget()
        self.questoes_list.setMinimumHeight(200)
        questoes_layout.addWidget(self.questoes_list)

        # Botões para gerenciar questões
        btn_questoes_layout = QHBoxLayout()
        btn_add = QPushButton("➕ Adicionar Questões")
        btn_add.clicked.connect(self.adicionar_questoes)
        btn_questoes_layout.addWidget(btn_add)

        btn_remove = QPushButton("➖ Remover Selecionada")
        btn_remove.clicked.connect(self.remover_questao)
        btn_questoes_layout.addWidget(btn_remove)

        btn_reorder = QPushButton("↕️ Reordenar")
        btn_questoes_layout.addWidget(btn_reorder)

        btn_questoes_layout.addStretch()
        questoes_layout.addLayout(btn_questoes_layout)

        layout.addWidget(questoes_group)

        # Botões finais
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()

        btn_cancel = QPushButton("❌ Cancelar")
        btn_cancel.clicked.connect(self.reject)
        btn_layout.addWidget(btn_cancel)

        btn_save = QPushButton("💾 Salvar")
        btn_save.setStyleSheet("""
            QPushButton {
                background-color: #1abc9c;
                color: white;
                padding: 8px 20px;
                font-weight: bold;
                border-radius: 4px;
            }
            QPushButton:hover { background-color: #16a085; }
        """)
        btn_save.clicked.connect(self.salvar_lista)
        btn_layout.addWidget(btn_save)

        btn_export = QPushButton("📄 Exportar LaTeX")
        btn_export.clicked.connect(self.exportar_latex)
        btn_layout.addWidget(btn_export)

        layout.addLayout(btn_layout)

    def adicionar_questoes(self):
        """Abre diálogo para adicionar questões"""
        try:
            # TODO: Abrir busca de questões via controller
            ErrorHandler.show_info(
                self,
                "Em Desenvolvimento",
                "Funcionalidade de busca de questões será implementada"
            )
        except Exception as e:
            ErrorHandler.handle_exception(
                self,
                e,
                "Erro ao adicionar questões"
            )

    def remover_questao(self):
        """Remove questão selecionada"""
        current = self.questoes_list.currentRow()
        if current >= 0:
            self.questoes_list.takeItem(current)

    def salvar_lista(self):
        """Salva a lista com tratamento de erros"""
        try:
            # Validação básica
            if not self.titulo_input.text().strip():
                ErrorHandler.show_warning(
                    self,
                    "Validação",
                    "O título é obrigatório!"
                )
                return

            titulo = self.titulo_input.text().strip()
            tipo = self.tipo_input.text().strip()
            cabecalho = self.cabecalho_edit.toPlainText().strip()
            instrucoes = self.instrucoes_edit.toPlainText().strip()

            logger.info(f"Salvando lista: {titulo}")

            # TODO: Salvar via controller
            # id_lista = controller.criar_lista(titulo, tipo, cabecalho, instrucoes)

            ErrorHandler.show_success(
                self,
                "Sucesso",
                f"Lista '{titulo}' salva com sucesso!"
            )
            self.accept()

        except Exception as e:
            ErrorHandler.handle_exception(
                self,
                e,
                "Erro ao salvar lista"
            )

    def exportar_latex(self):
        """Exporta lista para LaTeX com tratamento de erros"""
        try:
            from src.views.export_dialog import ExportDialog
            dialog = ExportDialog(parent=self)
            dialog.exec()

        except Exception as e:
            ErrorHandler.handle_exception(
                self,
                e,
                "Erro ao abrir diálogo de exportação"
            )


logger.info("ListaForm carregado")
