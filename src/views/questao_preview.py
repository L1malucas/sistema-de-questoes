"""
View: Questão Preview
DESCRIÇÃO: Janela modal de visualização completa de questão
RELACIONAMENTOS: QuestaoModel, AlternativaModel, LaTeXRenderer
COMPONENTES:
    - Enunciado renderizado (LaTeX compilado)
    - Imagem do enunciado
    - Alternativas (se objetiva)
    - Indicação de alternativa correta (modo revisão)
    - Resolução (se preenchida)
    - Tags aplicadas
    - Metadados (data criação, última edição)
"""

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QScrollArea, QWidget, QGroupBox, QFrame
)
from PyQt6.QtCore import Qt
import logging

from src.utils import ErrorHandler

logger = logging.getLogger(__name__)


class QuestaoPreview(QDialog):
    """Janela de preview de questão"""

    def __init__(self, questao_data, parent=None):
        super().__init__(parent)
        self.questao_data = questao_data
        self.setWindowTitle("Preview da Questão")
        self.setMinimumSize(800, 600)
        self.resize(900, 700)

        try:
            self.init_ui()
            logger.info(f"QuestaoPreview inicializado (ID: {questao_data.get('id')})")
        except Exception as e:
            ErrorHandler.handle_exception(
                self,
                e,
                "Erro ao carregar preview"
            )
            self.close()

    def init_ui(self):
        layout = QVBoxLayout(self)

        # Cabeçalho
        header_layout = QHBoxLayout()

        title = self.questao_data.get('titulo', 'Sem título')
        header_label = QLabel(f"👁️ Preview: {title}")
        header_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        header_layout.addWidget(header_label)

        header_layout.addStretch()

        # Badge de tipo
        tipo = self.questao_data.get('tipo', 'N/A')
        tipo_label = QLabel(tipo)
        color = "#2196f3" if tipo == 'OBJETIVA' else "#9c27b0"
        tipo_label.setStyleSheet(f"""
            QLabel {{
                background-color: {color};
                color: white;
                padding: 5px 15px;
                border-radius: 4px;
                font-weight: bold;
            }}
        """)
        header_layout.addWidget(tipo_label)

        layout.addLayout(header_layout)

        # Metadados
        meta_text = f"📚 {self.questao_data.get('fonte', 'N/A')} • 📅 {self.questao_data.get('ano', 'N/A')} • ⭐ {self.questao_data.get('dificuldade', 'N/A')}"
        meta_label = QLabel(meta_text)
        meta_label.setStyleSheet("color: #666; margin-bottom: 10px;")
        layout.addWidget(meta_label)

        # Área de scroll
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; }")

        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)

        # Enunciado
        enunciado_group = QGroupBox("Enunciado")
        enunciado_layout = QVBoxLayout(enunciado_group)

        enunciado_label = QLabel(self.questao_data.get('enunciado', ''))
        enunciado_label.setWordWrap(True)
        enunciado_label.setStyleSheet("font-size: 13px; padding: 10px;")
        enunciado_layout.addWidget(enunciado_label)

        # TODO: Renderizar LaTeX
        latex_note = QLabel("<i>Renderização LaTeX será implementada</i>")
        latex_note.setStyleSheet("color: #999; font-size: 11px;")
        enunciado_layout.addWidget(latex_note)

        scroll_layout.addWidget(enunciado_group)

        # Alternativas (se objetiva)
        if tipo == 'OBJETIVA' and 'alternativas' in self.questao_data:
            alt_group = QGroupBox("Alternativas")
            alt_layout = QVBoxLayout(alt_group)

            for alt in self.questao_data['alternativas']:
                alt_frame = QFrame()
                alt_frame_layout = QHBoxLayout(alt_frame)

                letra_label = QLabel(f"<b>{alt['letra']})</b>")
                letra_label.setFixedWidth(30)
                alt_frame_layout.addWidget(letra_label)

                texto_label = QLabel(alt['texto'])
                texto_label.setWordWrap(True)
                alt_frame_layout.addWidget(texto_label)

                if alt.get('correta'):
                    correto_label = QLabel("✓")
                    correto_label.setStyleSheet("color: green; font-size: 18px; font-weight: bold;")
                    alt_frame_layout.addWidget(correto_label)

                alt_layout.addWidget(alt_frame)

            scroll_layout.addWidget(alt_group)

        # Resolução
        if self.questao_data.get('resolucao'):
            res_group = QGroupBox("Resolução")
            res_layout = QVBoxLayout(res_group)

            res_label = QLabel(self.questao_data['resolucao'])
            res_label.setWordWrap(True)
            res_label.setStyleSheet("padding: 10px;")
            res_layout.addWidget(res_label)

            scroll_layout.addWidget(res_group)

        # Tags
        if self.questao_data.get('tags'):
            tags_group = QGroupBox("Tags")
            tags_layout = QHBoxLayout(tags_group)

            for tag in self.questao_data['tags']:
                tag_label = QLabel(tag)
                tag_label.setStyleSheet("""
                    QLabel {
                        background-color: #e3f2fd;
                        color: #1976d2;
                        padding: 4px 10px;
                        border-radius: 3px;
                        font-size: 11px;
                    }
                """)
                tags_layout.addWidget(tag_label)

            tags_layout.addStretch()
            scroll_layout.addWidget(tags_group)

        scroll.setWidget(scroll_widget)
        layout.addWidget(scroll)

        # Botão fechar
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()

        btn_close = QPushButton("✔️ Fechar")
        btn_close.clicked.connect(self.accept)
        btn_layout.addWidget(btn_close)

        layout.addLayout(btn_layout)


logger.info("QuestaoPreview carregado")
