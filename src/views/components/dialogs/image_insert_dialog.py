"""
Component: ImageInsertDialog
Diálogo para inserir imagem no texto
"""

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFileDialog, QSpinBox, QFormLayout, QDialogButtonBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
import logging

logger = logging.getLogger(__name__)


class ImageInsertDialog(QDialog):
    """Diálogo para inserir imagem no texto."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.image_path = None
        self.setWindowTitle("Inserir Imagem")
        self.setMinimumWidth(400)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        # Seleção de imagem
        img_layout = QHBoxLayout()
        self.path_label = QLabel("Nenhuma imagem selecionada")
        self.path_label.setStyleSheet("color: #666;")
        img_layout.addWidget(self.path_label, 1)
        btn_select = QPushButton("Selecionar...")
        btn_select.clicked.connect(self.select_image)
        img_layout.addWidget(btn_select)
        layout.addLayout(img_layout)

        # Preview
        self.preview_label = QLabel()
        self.preview_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.preview_label.setMinimumHeight(150)
        self.preview_label.setStyleSheet("border: 1px dashed #ccc; background: #f9f9f9;")
        layout.addWidget(self.preview_label)

        # Escala
        form_layout = QFormLayout()
        self.scale_spin = QSpinBox()
        self.scale_spin.setRange(10, 100)
        self.scale_spin.setValue(70)
        self.scale_spin.setSuffix("%")
        form_layout.addRow("Escala:", self.scale_spin)
        layout.addLayout(form_layout)

        # Botões
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def select_image(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Selecionar Imagem", "",
            "Imagens (*.png *.jpg *.jpeg *.gif *.bmp *.svg)"
        )
        if file_path:
            self.image_path = file_path
            self.path_label.setText(file_path.split('/')[-1].split('\\')[-1])
            # Preview
            pixmap = QPixmap(file_path)
            if not pixmap.isNull():
                scaled = pixmap.scaled(
                    300, 150,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation
                )
                self.preview_label.setPixmap(scaled)

    def get_image_path(self):
        return self.image_path

    def get_scale(self):
        return self.scale_spin.value() / 100.0
