"""
Component: ImagePicker
Seletor de imagens com preview
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFileDialog, QSpinBox
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QPixmap
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


class ImagePicker(QWidget):
    """Seletor de imagens com preview."""
    imageChanged = pyqtSignal(str)

    def __init__(self, label="Imagem:", parent=None):
        super().__init__(parent)
        self.image_path = None
        self.init_ui(label)

    def init_ui(self, label):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        top_layout = QHBoxLayout()
        top_layout.addWidget(QLabel(label))
        self.btn_select = QPushButton("Selecionar Imagem")
        self.btn_select.clicked.connect(self.select_image)
        top_layout.addWidget(self.btn_select)
        self.btn_clear = QPushButton("Remover")
        self.btn_clear.clicked.connect(self.clear_image)
        self.btn_clear.setEnabled(False)
        top_layout.addWidget(self.btn_clear)
        top_layout.addStretch()
        layout.addLayout(top_layout)
        self.preview_label = QLabel("Nenhuma imagem selecionada")
        self.preview_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.preview_label.setMinimumHeight(150)
        self.preview_label.setMaximumHeight(300)
        self.preview_label.setStyleSheet("border: 2px dashed #ccc; border-radius: 5px; background-color: #f5f5f5;")
        layout.addWidget(self.preview_label)
        scale_layout = QHBoxLayout()
        scale_layout.addWidget(QLabel("Escala para LaTeX:"))
        self.scale_spin = QSpinBox()
        self.scale_spin.setRange(10, 100)
        self.scale_spin.setValue(70)
        self.scale_spin.setSuffix("%")
        scale_layout.addWidget(self.scale_spin)
        scale_layout.addStretch()
        layout.addLayout(scale_layout)

    def select_image(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Selecionar Imagem", "",
            "Imagens (*.png *.jpg *.jpeg *.gif *.bmp *.svg)"
        )
        if file_path:
            self.image_path = file_path
            self.load_preview()
            self.btn_clear.setEnabled(True)
            self.imageChanged.emit(file_path)

    def load_preview(self):
        if self.image_path:
            pixmap = QPixmap(self.image_path)
            if not pixmap.isNull():
                scaled_pixmap = pixmap.scaled(
                    400, 300,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation
                )
                self.preview_label.setPixmap(scaled_pixmap)
            else:
                self.preview_label.setText("Erro ao carregar imagem")

    def clear_image(self):
        self.image_path = None
        self.preview_label.clear()
        self.preview_label.setText("Nenhuma imagem selecionada")
        self.btn_clear.setEnabled(False)
        self.imageChanged.emit("")

    def get_image_path(self):
        return self.image_path

    def get_scale(self):
        return self.scale_spin.value() / 100.0

    def set_image(self, path, scale=0.7):
        if path and Path(path).exists():
            self.image_path = path
            self.load_preview()
            self.btn_clear.setEnabled(True)
            self.scale_spin.setValue(int(scale * 100))
