"""
View: Search Panel
DESCRIÇÃO: Painel de busca e filtros de questões
"""
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QLineEdit, QComboBox, QScrollArea, QFrame, QSpinBox,
    QGroupBox, QSplitter, QStyle
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QIcon
import logging

from src.controllers.adapters import criar_questao_controller
from src.controllers.adapters import criar_tag_controller
from src.application.dtos import FiltroQuestaoDTO
from src.utils import ErrorHandler
from src.views.widgets import QuestaoCard
from src.database.session_manager import session_manager
from src.repositories import FonteQuestaoRepository, NivelEscolarRepository

logger = logging.getLogger(__name__)


class SearchPanel(QWidget):
    """Painel de busca e filtros de questões."""
    questaoSelected = pyqtSignal(str)  # Emite codigo da questao
    editQuestao = pyqtSignal(str)
    inactivateQuestao = pyqtSignal(str)
    reactivateQuestao = pyqtSignal(str)  # Novo sinal para reativar
    addToListQuestao = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.controller = criar_questao_controller()
        self.tag_controller = criar_tag_controller()
        self.init_ui()
        self.load_tags()
        self.load_fontes()
        # Inicializar filtros avançados como None (serão criados quando necessário)
        self.ano_de_spin = None
        self.ano_ate_spin = None
        self.nivel_combo = None
        self.incluir_inativas_check = None
        logger.info("SearchPanel inicializado")

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(15)
        
        # Barra horizontal de filtros
        filters_bar = self._create_filters_bar()
        layout.addWidget(filters_bar)
        
        # Painel de resultados
        results_panel = self._create_results_panel()
        layout.addWidget(results_panel)

    def _create_filters_bar(self):
        """Cria barra horizontal de filtros"""
        container = QFrame()
        container.setStyleSheet("""
            QFrame {
                background-color: #f5f5f5;
                border-radius: 8px;
                padding: 12px;
            }
        """)
        layout = QHBoxLayout(container)
        layout.setContentsMargins(15, 10, 15, 10)
        layout.setSpacing(10)
        
        # Campo de busca principal (com ícone)
        search_container = QWidget()
        search_layout = QHBoxLayout(search_container)
        search_layout.setContentsMargins(0, 0, 0, 0)
        search_layout.setSpacing(0)
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Buscar por ID, trecho do enunciado ou tags...")
        self.search_input.setStyleSheet("""
            QLineEdit {
                padding: 10px 15px;
                border: 2px solid #ddd;
                border-radius: 6px;
                font-size: 14px;
                background-color: white;
            }
            QLineEdit:focus {
                border-color: #1abc9c;
            }
        """)
        self.search_input.returnPressed.connect(self.perform_search)
        search_layout.addWidget(self.search_input)
        layout.addWidget(search_container, 2)  # Campo de busca ocupa mais espaço
        
        # Dropdown Fonte
        self.fonte_combo = QComboBox()
        self.fonte_combo.addItem("Fonte", None)
        self.fonte_combo.setStyleSheet("""
            QComboBox {
                padding: 10px 15px;
                border: 2px solid #ddd;
                border-radius: 6px;
                background-color: white;
                min-width: 120px;
            }
            QComboBox:hover {
                border-color: #1abc9c;
            }
        """)
        layout.addWidget(self.fonte_combo)
        
        # Dropdown Dificuldade
        self.dificuldade_combo = QComboBox()
        self.dificuldade_combo.addItem("Dificuldade", None)
        self.dificuldade_combo.addItem("Fácil", "FACIL")
        self.dificuldade_combo.addItem("Médio", "MEDIO")
        self.dificuldade_combo.addItem("Difícil", "DIFICIL")
        self.dificuldade_combo.setStyleSheet("""
            QComboBox {
                padding: 10px 15px;
                border: 2px solid #ddd;
                border-radius: 6px;
                background-color: white;
                min-width: 120px;
            }
            QComboBox:hover {
                border-color: #1abc9c;
            }
        """)
        layout.addWidget(self.dificuldade_combo)
        
        # Dropdown Tipo
        self.tipo_combo = QComboBox()
        self.tipo_combo.addItem("Tipo", None)
        self.tipo_combo.addItem("Objetiva", "OBJETIVA")
        self.tipo_combo.addItem("Discursiva", "DISCURSIVA")
        self.tipo_combo.setStyleSheet("""
            QComboBox {
                padding: 10px 15px;
                border: 2px solid #ddd;
                border-radius: 6px;
                background-color: white;
                min-width: 120px;
            }
            QComboBox:hover {
                border-color: #1abc9c;
            }
        """)
        layout.addWidget(self.tipo_combo)
        
        # Dropdown Tags
        self.tag_combo = QComboBox()
        self.tag_combo.addItem("Tags", None)
        self.tag_combo.setStyleSheet("""
            QComboBox {
                padding: 10px 15px;
                border: 2px solid #ddd;
                border-radius: 6px;
                background-color: white;
                min-width: 150px;
            }
            QComboBox:hover {
                border-color: #1abc9c;
            }
        """)
        layout.addWidget(self.tag_combo)
        
        # Botão Buscar
        btn_search = QPushButton("Buscar")
        btn_search.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_FileDialogStart))
        btn_search.clicked.connect(self.perform_search)
        btn_search.setStyleSheet("""
            QPushButton {
                background-color: #1abc9c;
                color: white;
                padding: 10px 20px;
                border-radius: 6px;
                font-weight: bold;
                border: none;
            }
            QPushButton:hover {
                background-color: #16a085;
            }
        """)
        layout.addWidget(btn_search)
        
        # Botão Filtros (para filtros avançados)
        btn_filters = QPushButton("Filtros")
        btn_filters.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_FileDialogDetailedView))
        btn_filters.setStyleSheet("""
            QPushButton {
                background-color: #34495e;
                color: white;
                padding: 10px 20px;
                border-radius: 6px;
                font-weight: bold;
                border: none;
            }
            QPushButton:hover {
                background-color: #2c3e50;
            }
        """)
        btn_filters.clicked.connect(self._show_advanced_filters)
        layout.addWidget(btn_filters)
        
        # Contador de resultados
        self.results_count_label = QLabel("0 resultados")
        self.results_count_label.setStyleSheet("""
            font-weight: bold;
            color: #7f8c8d;
            padding: 0 10px;
            min-width: 100px;
        """)
        layout.addWidget(self.results_count_label)
        
        return container
    
    def _show_advanced_filters(self):
        """Mostra diálogo com filtros avançados (ano, nível escolar, etc)"""
        from PyQt6.QtWidgets import QDialog, QDialogButtonBox
        dialog = QDialog(self)
        dialog.setWindowTitle("Filtros Avançados")
        dialog.setMinimumWidth(400)
        
        layout = QVBoxLayout(dialog)
        
        # Ano
        ano_group = QGroupBox("Ano")
        ano_layout = QHBoxLayout(ano_group)
        ano_layout.addWidget(QLabel("De:"))
        self.ano_de_spin = QSpinBox()
        self.ano_de_spin.setRange(1900, 2100)
        self.ano_de_spin.setValue(2000)
        ano_layout.addWidget(self.ano_de_spin)
        ano_layout.addWidget(QLabel("Até:"))
        self.ano_ate_spin = QSpinBox()
        self.ano_ate_spin.setRange(1900, 2100)
        self.ano_ate_spin.setValue(datetime.now().year)
        ano_layout.addWidget(self.ano_ate_spin)
        layout.addWidget(ano_group)
        
        # Nível Escolar
        nivel_group = QGroupBox("Nível Escolar")
        nivel_layout = QVBoxLayout(nivel_group)
        nivel_combo = QComboBox()
        nivel_combo.addItem("Todos os Níveis", None)
        self._load_series_to_combo(nivel_combo)
        nivel_layout.addWidget(nivel_combo)
        layout.addWidget(nivel_group)
        
        # Armazenar referência para uso posterior
        self.nivel_combo = nivel_combo
        
        # Incluir inativas
        from PyQt6.QtWidgets import QCheckBox
        self.incluir_inativas_check = QCheckBox("Incluir questões inativas")
        self.incluir_inativas_check.setStyleSheet("color: #e67e22; font-weight: bold;")
        layout.addWidget(self.incluir_inativas_check)
        
        # Botões
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        layout.addWidget(buttons)
        
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.perform_search()

    def _create_results_panel(self):
        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(0, 0, 0, 0)
        header_layout = QHBoxLayout()
        title_label = QLabel("Resultados da Busca")
        title_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        
        # Botão Nova Questão
        btn_nova_questao = QPushButton("Nova Questão")
        btn_nova_questao.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_FileDialogNewFolder))
        btn_nova_questao.clicked.connect(self.abrir_form_nova_questao)
        btn_nova_questao.setStyleSheet("background-color: #1abc9c; color: white; padding: 8px 15px; font-weight: bold; border-radius: 4px;")
        header_layout.addWidget(btn_nova_questao)
        
        layout.addLayout(header_layout)
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; background-color: #f5f5f5; }")
        
        self.results_container = QWidget()
        # Layout em grid para os cards
        from PyQt6.QtWidgets import QGridLayout
        self.results_layout = QGridLayout(self.results_container)
        self.results_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.results_layout.setSpacing(15)
        self.results_layout.setContentsMargins(10, 10, 10, 10)
        scroll.setWidget(self.results_container)
        layout.addWidget(scroll)
        self.show_empty_state()
        return panel

    def load_tags(self):
        """Carrega tags no dropdown (apenas tags de conteúdo)"""
        try:
            tags_arvore = self.tag_controller.obter_arvore_conteudos()
            self._populate_tag_combo(tags_arvore)
        except Exception as e:
            ErrorHandler.handle_exception(self, e, "Erro ao carregar tags para filtro.")
    
    def _populate_tag_combo(self, tags, parent_text=""):
        """Popula o dropdown de tags recursivamente"""
        for tag in tags:
            display_text = f"{parent_text} > {tag.nome}" if parent_text else tag.nome
            self.tag_combo.addItem(display_text, tag.uuid)
            if tag.filhos:
                self._populate_tag_combo(tag.filhos, display_text)

    def load_fontes(self):
        """Carrega as fontes de questões do repositório"""
        try:
            with session_manager.session_scope() as session:
                fonte_repo = FonteQuestaoRepository(session)
                fontes = fonte_repo.listar_todas()
                for fonte in fontes:
                    self.fonte_combo.addItem(fonte.nome_completo, fonte.sigla)
        except Exception as e:
            ErrorHandler.handle_exception(self, e, "Erro ao carregar fontes/vestibulares.")

    def _load_series_to_combo(self, combo):
        """Carrega os níveis escolares no combo fornecido"""
        try:
            with session_manager.session_scope() as session:
                nivel_repo = NivelEscolarRepository(session)
                niveis = nivel_repo.listar_todos()
                for nivel in niveis:
                    combo.addItem(nivel.nome, nivel.codigo)
        except Exception as e:
            ErrorHandler.handle_exception(self, e, "Erro ao carregar níveis escolares.")

    def show_empty_state(self):
        self.clear_results()
        empty_widget = QWidget()
        empty_layout = QVBoxLayout(empty_widget)
        empty_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon_label = QLabel()
        icon = self.style().standardIcon(QStyle.StandardPixmap.SP_FileDialogInfoView)
        if not icon.isNull():
            icon_label.setPixmap(icon.pixmap(64, 64))
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        empty_layout.addWidget(icon_label)
        msg_label = QLabel("Nenhuma questão encontrada")
        msg_label.setStyleSheet("font-size: 18px; color: #666; margin-top: 10px;")
        msg_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        empty_layout.addWidget(msg_label)
        hint_label = QLabel("Ajuste os filtros e clique em Buscar")
        hint_label.setStyleSheet("font-size: 14px; color: #999; margin-top: 5px;")
        hint_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        empty_layout.addWidget(hint_label)
        # Adicionar no grid ocupando todas as colunas
        self.results_layout.addWidget(empty_widget, 0, 0, 1, 3)

    def clear_results(self):
        # Limpar todos os widgets do grid
        while self.results_layout.count():
            child = self.results_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def clear_filters(self):
        logger.info("Limpando filtros")
        self.search_input.clear()
        self.tipo_combo.setCurrentIndex(0)
        self.dificuldade_combo.setCurrentIndex(0)
        self.fonte_combo.setCurrentIndex(0)
        self.tag_combo.setCurrentIndex(0)
        if self.ano_de_spin is not None:
            self.ano_de_spin.setValue(2000)
            self.ano_ate_spin.setValue(datetime.now().year)
        if self.nivel_combo is not None:
            self.nivel_combo.setCurrentIndex(0)
        if self.incluir_inativas_check is not None:
            self.incluir_inativas_check.setChecked(False)
        self.show_empty_state()
        self.results_count_label.setText("0 resultados")

    def perform_search(self):
        logger.info("Executando busca")
        self.clear_results()
        try:
            filtro_dto = self._get_filtros()
            # Converter DTO para dict
            filtro = {
                'titulo': filtro_dto.titulo,
                'tipo': filtro_dto.tipo,
                'ano_inicio': filtro_dto.ano_inicio,
                'ano_fim': filtro_dto.ano_fim,
                'fonte': filtro_dto.fonte,
                'niveis': filtro_dto.niveis,
                'dificuldade': filtro_dto.dificuldade,
                'tags': filtro_dto.tags,
                'ativa': filtro_dto.ativa
            }
            questoes_dto = self.controller.buscar_questoes(filtro)
            if not questoes_dto:
                self.show_empty_state()
            else:
                # Limpar layout anterior
                while self.results_layout.count():
                    child = self.results_layout.takeAt(0)
                    if child.widget():
                        child.widget().deleteLater()
                
                # Adicionar cards em grid (3 colunas)
                cols = 3
                for idx, questao_dto in enumerate(questoes_dto):
                    card = QuestaoCard(questao_dto)
                    card.clicked.connect(self.questaoSelected.emit)
                    card.editClicked.connect(self.editQuestao.emit)
                    card.inactivateClicked.connect(self.inactivateQuestao.emit)
                    card.reactivateClicked.connect(self.reactivateQuestao.emit)
                    card.addToListClicked.connect(self.addToListQuestao.emit)
                    
                    row = idx // cols
                    col = idx % cols
                    self.results_layout.addWidget(card, row, col)
            self.results_count_label.setText(f"{len(questoes_dto)} resultados")
            logger.info(f"Busca concluída: {len(questoes_dto)} questões encontradas")
        except Exception as e:
            self.results_count_label.setText("Erro ao buscar questões")
            ErrorHandler.handle_exception(self, e, "Erro ao buscar questões")

    def _get_filtros(self) -> FiltroQuestaoDTO:
        titulo = self.search_input.text().strip() or None
        tipo = self.tipo_combo.currentData()  # Retorna o código ou None
        dificuldade_texto = self.dificuldade_combo.currentData()  # Retorna o código ou None
        
        # Obter fonte selecionada (sigla)
        fonte_sigla = self.fonte_combo.currentData()
        
        # Obter tag selecionada (UUID)
        tag_uuid = self.tag_combo.currentData()
        tags = [tag_uuid] if tag_uuid else None
        
        # Valores padrão para filtros avançados
        ano_inicio = 2000
        ano_fim = datetime.now().year
        niveis = None
        ativa = True
        
        # Se os filtros avançados foram configurados, usar seus valores
        if self.ano_de_spin is not None:
            ano_inicio = self.ano_de_spin.value()
            ano_fim = self.ano_ate_spin.value()
        
        if self.nivel_combo is not None:
            nivel_codigo = self.nivel_combo.currentData()
            niveis = [nivel_codigo] if nivel_codigo else None
        
        if self.incluir_inativas_check is not None:
            incluir_inativas = self.incluir_inativas_check.isChecked()
            ativa = None if incluir_inativas else True

        return FiltroQuestaoDTO(
            titulo=titulo,
            tipo=tipo,
            ano_inicio=ano_inicio,
            ano_fim=ano_fim,
            fonte=fonte_sigla,
            niveis=niveis,
            dificuldade=dificuldade_texto,
            tags=tags if tags else None,
            ativa=ativa
        )

    def abrir_form_nova_questao(self):
        """Abre o formulário para criar uma nova questão"""
        from src.views.questao_form import QuestaoForm
        dialog = QuestaoForm(parent=self)
        dialog.questaoSaved.connect(self._on_questao_salva)
        dialog.exec()
    
    def _on_questao_salva(self, codigo_questao: int):
        """Callback quando uma questão é salva"""
        # Recarregar busca para mostrar a nova questão
        self.perform_search()

from datetime import datetime
