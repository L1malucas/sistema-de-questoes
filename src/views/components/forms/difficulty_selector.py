"""
Component: DifficultySelector
Seletor de dificuldade com radio buttons
"""

from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel, QRadioButton, QButtonGroup
from PyQt6.QtCore import pyqtSignal
import logging

logger = logging.getLogger(__name__)


class DifficultySelector(QWidget):
    """Seletor de dificuldade com radio buttons."""
    difficultyChanged = pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        label = QLabel("Dificuldade:")
        layout.addWidget(label)
        self.button_group = QButtonGroup(self)
        difficulties = [
            (1, "⭐ FÁCIL", "#4caf50"),
            (2, "⭐⭐ MÉDIO", "#ff9800"),
            (3, "⭐⭐⭐ DIFÍCIL", "#f44336")
        ]
        for diff_id, label_text, color in difficulties:
            radio = QRadioButton(label_text)
            radio.setStyleSheet(f"QRadioButton {{ color: {color}; font-weight: bold; }}")
            self.button_group.addButton(radio, diff_id)
            layout.addWidget(radio)
        layout.addStretch()
        self.button_group.idClicked.connect(self.difficultyChanged.emit)

    def get_selected_difficulty(self):
        return self.button_group.checkedId()

    def set_difficulty(self, difficulty_id):
        button = self.button_group.button(difficulty_id)
        if button:
            button.setChecked(True)
