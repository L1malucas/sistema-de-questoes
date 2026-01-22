"""
View: Menu Bar Component
DESCRIÇÃO: Componente de menu bar reutilizável
"""
from PyQt6.QtWidgets import QMenuBar, QMenu
from PyQt6.QtGui import QAction, QKeySequence
from PyQt6.QtCore import Qt
from typing import Callable, Optional
import logging

logger = logging.getLogger(__name__)


class MenuBarComponent:
    """
    Componente de menu bar que pode ser usado em qualquer QMainWindow
    """

    def __init__(self, parent, callbacks: dict):
        """
        Inicializa o componente de menu bar

        Args:
            parent: QMainWindow pai
            callbacks: Dicionário com callbacks para as ações
                {
                    'nova_questao': callable,
                    'nova_lista': callable,
                    'backup': callable,
                    'restaurar': callable,
                    'sair': callable,
                    'gerenciar_tags': callable,
                    'configuracoes': callable,
                    'visualizar_questoes': callable,
                    'visualizar_listas': callable,
                    'visualizar_estatisticas': callable,
                    'sobre': callable,
                    'documentacao': callable
                }
        """
        self.parent = parent
        self.callbacks = callbacks
        self.menubar = parent.menuBar()
        # No macOS, forçar menu bar a aparecer na janela (não no topo da tela)
        self.menubar.setNativeMenuBar(False)
        self.actions = []  # Armazenar ações para garantir que atalhos funcionem
        self._create_menus()

    def _create_menus(self):
        """Cria todos os menus"""
        self._create_menu_arquivo()
        self._create_menu_editar()
        self._create_menu_visualizar()
        self._create_menu_ajuda()

    def _create_menu_arquivo(self):
        """Cria menu Arquivo"""
        menu_arquivo = self.menubar.addMenu("&Arquivo")

        # Nova Questão
        action_nova_questao = QAction("&Nova Questão", self.parent)
        action_nova_questao.setShortcut(QKeySequence("Ctrl+N"))
        action_nova_questao.setShortcutContext(Qt.ShortcutContext.WindowShortcut)
        action_nova_questao.triggered.connect(
            self._get_callback('nova_questao')
        )
        menu_arquivo.addAction(action_nova_questao)
        self.parent.addAction(action_nova_questao)  # Adicionar ao widget principal para atalhos funcionarem
        self.actions.append(action_nova_questao)

        # Nova Lista
        action_nova_lista = QAction("Nova &Lista", self.parent)
        action_nova_lista.setShortcut(QKeySequence("Ctrl+L"))
        action_nova_lista.setShortcutContext(Qt.ShortcutContext.WindowShortcut)
        action_nova_lista.triggered.connect(
            self._get_callback('nova_lista')
        )
        menu_arquivo.addAction(action_nova_lista)
        self.parent.addAction(action_nova_lista)
        self.actions.append(action_nova_lista)

        menu_arquivo.addSeparator()

        # Backup
        action_backup = QAction("&Backup", self.parent)
        action_backup.setShortcut(QKeySequence("Ctrl+B"))
        action_backup.setShortcutContext(Qt.ShortcutContext.WindowShortcut)
        action_backup.triggered.connect(
            self._get_callback('backup')
        )
        menu_arquivo.addAction(action_backup)
        self.parent.addAction(action_backup)
        self.actions.append(action_backup)

        # Restaurar
        action_restaurar = QAction("&Restaurar", self.parent)
        action_restaurar.triggered.connect(
            self._get_callback('restaurar')
        )
        menu_arquivo.addAction(action_restaurar)

        menu_arquivo.addSeparator()

        # Sair
        action_sair = QAction("&Sair", self.parent)
        action_sair.setShortcut(QKeySequence("Ctrl+Q"))
        action_sair.setShortcutContext(Qt.ShortcutContext.WindowShortcut)
        action_sair.triggered.connect(
            self._get_callback('sair')
        )
        menu_arquivo.addAction(action_sair)
        self.parent.addAction(action_sair)
        self.actions.append(action_sair)

    def _create_menu_editar(self):
        """Cria menu Editar"""
        menu_editar = self.menubar.addMenu("&Editar")

        # Gerenciar Tags
        action_tags = QAction("Gerenciar &Tags", self.parent)
        action_tags.setShortcut(QKeySequence("Ctrl+T"))
        action_tags.setShortcutContext(Qt.ShortcutContext.WindowShortcut)
        action_tags.triggered.connect(
            self._get_callback('gerenciar_tags')
        )
        menu_editar.addAction(action_tags)
        self.parent.addAction(action_tags)
        self.actions.append(action_tags)

        menu_editar.addSeparator()

        # Configurações
        action_config = QAction("&Configurações", self.parent)
        action_config.setShortcut(QKeySequence("Ctrl+,"))
        action_config.setShortcutContext(Qt.ShortcutContext.WindowShortcut)
        action_config.triggered.connect(
            self._get_callback('configuracoes')
        )
        menu_editar.addAction(action_config)
        self.parent.addAction(action_config)
        self.actions.append(action_config)

    def _create_menu_visualizar(self):
        """Cria menu Visualizar"""
        menu_visualizar = self.menubar.addMenu("&Visualizar")

        # Questões
        action_questoes = QAction("&Questões", self.parent)
        action_questoes.setShortcut(QKeySequence("Ctrl+1"))
        action_questoes.setShortcutContext(Qt.ShortcutContext.WindowShortcut)
        action_questoes.triggered.connect(
            self._get_callback('visualizar_questoes')
        )
        menu_visualizar.addAction(action_questoes)
        self.parent.addAction(action_questoes)
        self.actions.append(action_questoes)

        # Listas
        action_listas = QAction("&Listas", self.parent)
        action_listas.setShortcut(QKeySequence("Ctrl+2"))
        action_listas.setShortcutContext(Qt.ShortcutContext.WindowShortcut)
        action_listas.triggered.connect(
            self._get_callback('visualizar_listas')
        )
        menu_visualizar.addAction(action_listas)
        self.parent.addAction(action_listas)
        self.actions.append(action_listas)

        # Estatísticas
        action_estatisticas = QAction("&Estatísticas", self.parent)
        action_estatisticas.setShortcut(QKeySequence("Ctrl+3"))
        action_estatisticas.setShortcutContext(Qt.ShortcutContext.WindowShortcut)
        action_estatisticas.triggered.connect(
            self._get_callback('visualizar_estatisticas')
        )
        menu_visualizar.addAction(action_estatisticas)
        self.parent.addAction(action_estatisticas)
        self.actions.append(action_estatisticas)

    def _create_menu_ajuda(self):
        """Cria menu Ajuda"""
        menu_ajuda = self.menubar.addMenu("A&juda")

        # Sobre
        action_sobre = QAction("&Sobre", self.parent)
        action_sobre.triggered.connect(
            self._get_callback('sobre')
        )
        menu_ajuda.addAction(action_sobre)

        # Documentação
        action_doc = QAction("&Documentação", self.parent)
        action_doc.setShortcut(QKeySequence("F1"))
        action_doc.setShortcutContext(Qt.ShortcutContext.WindowShortcut)
        action_doc.triggered.connect(
            self._get_callback('documentacao')
        )
        menu_ajuda.addAction(action_doc)
        self.parent.addAction(action_doc)
        self.actions.append(action_doc)

    def _get_callback(self, key: str) -> Callable:
        """
        Retorna o callback para uma ação ou uma função vazia se não existir

        Args:
            key: Chave do callback no dicionário

        Returns:
            Função callback
        """
        callback = self.callbacks.get(key)
        if callback:
            return callback
        
        # Retorna função vazia se callback não existir
        def empty_callback():
            logger.warning(f"Callback '{key}' não definido")
        
        return empty_callback
