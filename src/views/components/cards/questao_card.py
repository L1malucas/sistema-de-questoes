"""
Component: QuestaoCard
Card de preview de questão para exibição em listas
"""

from PyQt6.QtWidgets import (
    QFrame, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QMessageBox
)
from PyQt6.QtCore import Qt, pyqtSignal
import logging

logger = logging.getLogger(__name__)


class QuestaoCard(QFrame):
    """Card de preview de questão para exibição em listas."""
    clicked = pyqtSignal(str)  # Emite codigo da questao
    editClicked = pyqtSignal(str)
    inactivateClicked = pyqtSignal(str)
    reactivateClicked = pyqtSignal(str)
    addToListClicked = pyqtSignal(str)

    def __init__(self, questao_dto, parent=None):
        super().__init__(parent)
        self.questao_dto = questao_dto
        # Aceitar tanto dict quanto DTO - priorizar codigo
        if isinstance(questao_dto, dict):
            self.questao_id = questao_dto.get('codigo') or questao_dto.get('uuid')
            self.is_ativa = questao_dto.get('ativo', True)
        else:
            self.questao_id = getattr(questao_dto, 'codigo', None) or getattr(questao_dto, 'uuid', None)
            self.is_ativa = getattr(questao_dto, 'ativo', True)
        self.init_ui(questao_dto)

    def _get_attr(self, obj, attr, default=None):
        """Helper para obter atributo tanto de dict quanto de objeto"""
        if isinstance(obj, dict):
            return obj.get(attr, default)
        return getattr(obj, attr, default)

    def init_ui(self, dto):
        self.setFrameStyle(QFrame.Shape.StyledPanel | QFrame.Shadow.Raised)

        # Estilo diferente para inativas
        if self.is_ativa:
            self.setStyleSheet("""
                QFrame {
                    border: 1px solid #ddd;
                    border-radius: 5px;
                    background-color: white;
                    padding: 15px;
                }
                QFrame:hover {
                    border-color: #1abc9c;
                    background-color: #f0fff4;
                }
            """)
        else:
            self.setStyleSheet("""
                QFrame {
                    border: 2px solid #e74c3c;
                    border-radius: 5px;
                    background-color: #fdf2f2;
                    padding: 15px;
                }
                QFrame:hover {
                    border-color: #c0392b;
                    background-color: #fce4e4;
                }
            """)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        layout = QVBoxLayout(self)

        # Cabeçalho
        header_layout = QHBoxLayout()

        # Título
        titulo = self._get_attr(dto, 'titulo') or 'Sem título'
        title_label = QLabel(titulo)
        title_style = "font-weight: bold; font-size: 14px; color: #2c3e50;"
        if not self.is_ativa:
            title_style = "font-weight: bold; font-size: 14px; color: #95a5a6; text-decoration: line-through;"
        title_label.setStyleSheet(title_style)
        title_label.setWordWrap(True)
        header_layout.addWidget(title_label, 1)

        # Badge de INATIVA (se aplicável)
        if not self.is_ativa:
            inativa_label = QLabel("INATIVA")
            inativa_label.setStyleSheet("""
                QLabel {
                    background-color: #e74c3c;
                    color: white;
                    padding: 4px 10px;
                    border-radius: 3px;
                    font-size: 10px;
                    font-weight: bold;
                }
            """)
            header_layout.addWidget(inativa_label)

        # Badge de tipo
        tipo = self._get_attr(dto, 'tipo', 'N/A')
        tipo_label = QLabel(tipo)
        tipo_color = "#2196f3" if tipo == 'OBJETIVA' else "#9c27b0"
        tipo_label.setStyleSheet(f"""
            QLabel {{
                background-color: {tipo_color};
                color: white;
                padding: 4px 10px;
                border-radius: 3px;
                font-size: 11px;
                font-weight: bold;
            }}
        """)
        header_layout.addWidget(tipo_label)

        layout.addLayout(header_layout)

        # Preview do enunciado
        enunciado = self._get_attr(dto, 'enunciado', '')
        enunciado_preview = (enunciado[:150] + "...") if len(enunciado) > 150 else enunciado
        enunciado_label = QLabel(enunciado_preview)
        enunciado_label.setStyleSheet("color: #555; margin-top: 8px; font-size: 12px;")
        enunciado_label.setWordWrap(True)
        layout.addWidget(enunciado_label)

        # Metadados
        meta_layout = QHBoxLayout()
        meta_layout.setContentsMargins(0, 10, 0, 5)

        fonte = self._get_attr(dto, 'fonte') or 'N/A'
        ano = self._get_attr(dto, 'ano') or 'N/A'
        dificuldade = self._get_attr(dto, 'dificuldade_nome') or self._get_attr(dto, 'dificuldade') or 'N/A'
        meta_text = f"📚 {fonte} • 📅 {ano} • ⭐ {dificuldade}"
        meta_label = QLabel(meta_text)
        meta_label.setStyleSheet("color: #777; font-size: 11px;")
        meta_layout.addWidget(meta_label)

        meta_layout.addStretch()
        layout.addLayout(meta_layout)

        # Botões de ação
        btn_layout = QHBoxLayout()

        btn_visualizar = QPushButton("Visualizar")
        btn_visualizar.setMaximumWidth(90)
        btn_visualizar.clicked.connect(lambda checked: self._show_preview())
        btn_layout.addWidget(btn_visualizar)

        btn_editar = QPushButton("Editar")
        btn_editar.setMaximumWidth(70)
        btn_editar.clicked.connect(lambda: self.editClicked.emit(self.questao_id))
        btn_layout.addWidget(btn_editar)

        if self.is_ativa:
            btn_adicionar = QPushButton("Add Lista")
            btn_adicionar.setMaximumWidth(80)
            btn_adicionar.clicked.connect(lambda: self.addToListClicked.emit(self.questao_id))
            btn_layout.addWidget(btn_adicionar)

        btn_layout.addStretch()

        if self.is_ativa:
            btn_inativar = QPushButton("Inativar")
            btn_inativar.setMaximumWidth(80)
            btn_inativar.setStyleSheet("QPushButton { color: #e67e22; font-weight: bold; }")
            btn_inativar.setToolTip("Inativar esta questao")
            btn_inativar.clicked.connect(lambda: self.inactivateClicked.emit(self.questao_id))
            btn_layout.addWidget(btn_inativar)
        else:
            btn_reativar = QPushButton("Reativar")
            btn_reativar.setMaximumWidth(80)
            btn_reativar.setStyleSheet("QPushButton { color: #27ae60; font-weight: bold; }")
            btn_reativar.setToolTip("Reativar esta questao")
            btn_reativar.clicked.connect(lambda: self.reactivateClicked.emit(self.questao_id))
            btn_layout.addWidget(btn_reativar)

        layout.addLayout(btn_layout)

    def mouseDoubleClickEvent(self, event):
        """Abre preview com duplo clique no card."""
        if event.button() == Qt.MouseButton.LeftButton:
            self._show_preview()
        super().mouseDoubleClickEvent(event)

    def _show_preview(self):
        """Abre o diálogo de preview da questão no formato PDF."""
        try:
            from src.views.questao_preview import QuestaoPreview
            from src.controllers.adapters import criar_questao_controller

            controller = criar_questao_controller()
            questao_completa = controller.obter_questao_completa(self.questao_id)

            if not questao_completa:
                QMessageBox.warning(self, "Aviso", f"Questão {self.questao_id} não encontrada.")
                return

            preview_data = {
                'id': self.questao_id,
                'titulo': getattr(questao_completa, 'titulo', None) or 'Sem título',
                'tipo': getattr(questao_completa, 'tipo', 'N/A'),
                'enunciado': getattr(questao_completa, 'enunciado', ''),
                'fonte': self._extrair_fonte(questao_completa),
                'ano': getattr(questao_completa, 'ano', None),
                'dificuldade': getattr(questao_completa, 'dificuldade', 'N/A'),
                'resolucao': getattr(questao_completa, 'resolucao', None),
                'tags': self._extrair_tags_nomes(questao_completa),
                'alternativas': []
            }

            alternativas = getattr(questao_completa, 'alternativas', [])
            if alternativas:
                for alt in alternativas:
                    if hasattr(alt, 'letra'):
                        preview_data['alternativas'].append({
                            'letra': alt.letra,
                            'texto': getattr(alt, 'texto', ''),
                            'correta': getattr(alt, 'correta', False)
                        })
                    elif isinstance(alt, dict):
                        preview_data['alternativas'].append({
                            'letra': alt.get('letra', ''),
                            'texto': alt.get('texto', ''),
                            'correta': alt.get('correta', False)
                        })

            preview_dialog = QuestaoPreview(preview_data, self)
            preview_dialog.exec()

        except Exception as e:
            logger.error(f"Erro ao abrir preview da questão {self.questao_id}: {e}")
            QMessageBox.critical(self, "Erro", f"Erro ao abrir preview:\n{str(e)}")

    def _extrair_fonte(self, questao):
        """Extrai o nome da fonte das tags da questão."""
        tags = getattr(questao, 'tags', []) or []
        for tag in tags:
            numeracao = getattr(tag, 'numeracao', '') or ''
            if numeracao.startswith('V'):
                return getattr(tag, 'nome', '') or ''
        return None

    def _extrair_tags_nomes(self, questao):
        """Extrai nomes das tags de conteúdo da questão."""
        nomes = []
        tags = getattr(questao, 'tags', []) or []
        for tag in tags:
            numeracao = getattr(tag, 'numeracao', '') or ''
            nome = getattr(tag, 'nome', '') or ''
            if numeracao and numeracao[0].isdigit() and nome:
                nomes.append(nome)
        return nomes
