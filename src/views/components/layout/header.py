"""
Component: Header
Cabeçalho da aplicação com logo, navegação e ações
Baseado no design do mathbank_dashboard.py
"""

from PyQt6.QtWidgets import (
    QWidget, QHBoxLayout, QLabel, QPushButton, QFrame
)
from PyQt6.QtCore import Qt, pyqtSignal
import logging

logger = logging.getLogger(__name__)


class Header(QFrame):
    """Cabeçalho da aplicação com navegação e ações"""

    # Sinais de navegação
    dashboardClicked = pyqtSignal()
    questoesClicked = pyqtSignal()
    listasClicked = pyqtSignal()
    novaQuestaoClicked = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("header")
        self.setFixedHeight(60)
        self.init_ui()

    def init_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(40, 0, 40, 0)

        # Seção esquerda
        left_layout = QHBoxLayout()
        left_layout.setSpacing(32)

        # Logo e título
        logo_layout = QHBoxLayout()
        logo_layout.setSpacing(12)

        logo_label = QLabel("ƒ")
        logo_label.setObjectName("logo")
        logo_label.setFixedSize(32, 32)
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        title_label = QLabel("MathBank")
        title_label.setObjectName("title")

        logo_layout.addWidget(logo_label)
        logo_layout.addWidget(title_label)

        left_layout.addLayout(logo_layout)

        # Navegação
        nav_layout = QHBoxLayout()
        nav_layout.setSpacing(24)

        self.btn_dashboard = QPushButton("Dashboard")
        self.btn_dashboard.setObjectName("nav_active")
        self.btn_dashboard.clicked.connect(self.dashboardClicked.emit)

        self.btn_questoes = QPushButton("Questões")
        self.btn_questoes.setObjectName("nav_link")
        self.btn_questoes.clicked.connect(self.questoesClicked.emit)

        self.btn_listas = QPushButton("Listas")
        self.btn_listas.setObjectName("nav_link")
        self.btn_listas.clicked.connect(self.listasClicked.emit)

        nav_layout.addWidget(self.btn_dashboard)
        nav_layout.addWidget(self.btn_questoes)
        nav_layout.addWidget(self.btn_listas)

        left_layout.addLayout(nav_layout)

        layout.addLayout(left_layout)
        layout.addStretch()

        # Seção direita
        right_layout = QHBoxLayout()
        right_layout.setSpacing(16)

        create_btn = QPushButton("+ Nova Questão")
        create_btn.setObjectName("create_button")
        create_btn.setMinimumWidth(140)
        create_btn.clicked.connect(self.novaQuestaoClicked.emit)

        # Avatar/perfil
        avatar_label = QLabel()
        avatar_label.setObjectName("avatar")
        avatar_label.setFixedSize(40, 40)
        avatar_label.setScaledContents(True)

        right_layout.addWidget(create_btn)
        right_layout.addWidget(avatar_label)

        layout.addLayout(right_layout)

    def set_active_nav(self, nav_name: str):
        """Define qual botão de navegação está ativo"""
        # Resetar todos
        self.btn_dashboard.setObjectName("nav_link")
        self.btn_questoes.setObjectName("nav_link")
        self.btn_listas.setObjectName("nav_link")

        # Ativar o selecionado
        if nav_name == "dashboard":
            self.btn_dashboard.setObjectName("nav_active")
        elif nav_name == "questoes":
            self.btn_questoes.setObjectName("nav_active")
        elif nav_name == "listas":
            self.btn_listas.setObjectName("nav_active")

        # Forçar atualização do estilo
        self.btn_dashboard.style().unpolish(self.btn_dashboard)
        self.btn_dashboard.style().polish(self.btn_dashboard)
        self.btn_questoes.style().unpolish(self.btn_questoes)
        self.btn_questoes.style().polish(self.btn_questoes)
        self.btn_listas.style().unpolish(self.btn_listas)
        self.btn_listas.style().polish(self.btn_listas)
