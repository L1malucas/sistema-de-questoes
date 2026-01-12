"""
View: Export Dialog
DESCRIÇÃO: Diálogo de configuração de exportação
RELACIONAMENTOS: ExportController
COMPONENTES:
    - Radio buttons: Exportação Direta / Manual
    - Checkbox: Incluir Gabarito
    - Checkbox: Incluir Resoluções
    - Checkbox: Randomizar Questões
    - Spinner: Colunas (1 ou 2)
    - Spinner: Espaço para respostas (linhas)
    - Slider: Escala de imagens
    - ComboBox: Template LaTeX
    - Botões: Exportar, Cancelar
"""

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QCheckBox, QRadioButton, QButtonGroup, QSpinBox, QSlider,
    QComboBox, QGroupBox, QFileDialog, QMessageBox
)
from PyQt6.QtCore import Qt
import logging

logger = logging.getLogger(__name__)


class ExportDialog(QDialog):
    """Diálogo de configuração de exportação LaTeX"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Exportar para LaTeX")
        self.setMinimumSize(500, 600)
        self.init_ui()
        logger.info("ExportDialog inicializado")

    def init_ui(self):
        layout = QVBoxLayout(self)

        # Título
        header = QLabel("📄 Configuração de Exportação LaTeX")
        header.setStyleSheet("font-size: 16px; font-weight: bold; margin-bottom: 10px;")
        layout.addWidget(header)

        # Modo de exportação
        mode_group = QGroupBox("Modo de Exportação")
        mode_layout = QVBoxLayout(mode_group)

        self.direct_radio = QRadioButton("Exportação Direta (compilar automaticamente)")
        self.manual_radio = QRadioButton("Exportação Manual (apenas gerar .tex)")
        self.manual_radio.setChecked(True)

        mode_layout.addWidget(self.direct_radio)
        mode_layout.addWidget(self.manual_radio)

        layout.addWidget(mode_group)

        # Opções de conteúdo
        content_group = QGroupBox("Conteúdo")
        content_layout = QVBoxLayout(content_group)

        self.gabarito_check = QCheckBox("Incluir Gabarito")
        self.gabarito_check.setChecked(True)
        content_layout.addWidget(self.gabarito_check)

        self.resolucao_check = QCheckBox("Incluir Resoluções")
        content_layout.addWidget(self.resolucao_check)

        self.randomizar_check = QCheckBox("Randomizar ordem das questões")
        content_layout.addWidget(self.randomizar_check)

        layout.addWidget(content_group)

        # Layout
        layout_group = QGroupBox("Layout")
        layout_layout = QVBoxLayout(layout_group)

        # Colunas
        col_layout = QHBoxLayout()
        col_layout.addWidget(QLabel("Número de colunas:"))
        self.colunas_spin = QSpinBox()
        self.colunas_spin.setRange(1, 2)
        self.colunas_spin.setValue(1)
        col_layout.addWidget(self.colunas_spin)
        col_layout.addStretch()
        layout_layout.addLayout(col_layout)

        # Espaço para respostas
        espaco_layout = QHBoxLayout()
        espaco_layout.addWidget(QLabel("Linhas para resposta:"))
        self.espaco_spin = QSpinBox()
        self.espaco_spin.setRange(0, 20)
        self.espaco_spin.setValue(5)
        espaco_layout.addWidget(self.espaco_spin)
        espaco_layout.addStretch()
        layout_layout.addLayout(espaco_layout)

        layout.addWidget(layout_group)

        # Imagens
        img_group = QGroupBox("Imagens")
        img_layout = QVBoxLayout(img_group)

        scale_layout = QHBoxLayout()
        scale_layout.addWidget(QLabel("Escala:"))
        self.escala_slider = QSlider(Qt.Orientation.Horizontal)
        self.escala_slider.setRange(10, 100)
        self.escala_slider.setValue(70)
        self.escala_slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.escala_slider.setTickInterval(10)
        scale_layout.addWidget(self.escala_slider)
        self.escala_label = QLabel("70%")
        self.escala_slider.valueChanged.connect(lambda v: self.escala_label.setText(f"{v}%"))
        scale_layout.addWidget(self.escala_label)
        img_layout.addLayout(scale_layout)

        layout.addWidget(img_group)

        # Template
        template_group = QGroupBox("Template")
        template_layout = QVBoxLayout(template_group)

        template_h_layout = QHBoxLayout()
        template_h_layout.addWidget(QLabel("Template LaTeX:"))
        self.template_combo = QComboBox()
        self.template_combo.addItems(["default.tex", "prova.tex", "lista.tex", "simulado.tex"])
        template_h_layout.addWidget(self.template_combo)
        template_layout.addLayout(template_h_layout)

        layout.addWidget(template_group)

        # Botões
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()

        btn_cancel = QPushButton("❌ Cancelar")
        btn_cancel.clicked.connect(self.reject)
        btn_layout.addWidget(btn_cancel)

        btn_export = QPushButton("📄 Exportar")
        btn_export.setStyleSheet("""
            QPushButton {
                background-color: #2980b9;
                color: white;
                padding: 8px 20px;
                font-weight: bold;
                border-radius: 4px;
            }
            QPushButton:hover { background-color: #3498db; }
        """)
        btn_export.clicked.connect(self.exportar)
        btn_layout.addWidget(btn_export)

        layout.addLayout(btn_layout)

    def exportar(self):
        """Executa a exportação"""
        # Escolher local para salvar
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Salvar arquivo LaTeX",
            "",
            "LaTeX Files (*.tex)"
        )

        if file_path:
            logger.info(f"Exportando para: {file_path}")
            # TODO: Implementar lógica de exportação
            QMessageBox.information(
                self,
                "Sucesso",
                f"Arquivo exportado com sucesso!\n\n{file_path}\n\n(Geração LaTeX será implementada)"
            )
            self.accept()


logger.info("ExportDialog carregado")
