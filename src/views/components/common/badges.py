# src/views/components/common/badges.py
from PyQt6.QtWidgets import QLabel, QWidget, QHBoxLayout, QPushButton
from PyQt6.QtCore import Qt, pyqtSignal, QSize
from PyQt6.QtGui import QIcon
from src.views.design.constants import Color, Spacing, Typography, Dimensions
from src.views.design.enums import DifficultyEnum

class BaseBadge(QLabel):
    """
    Base class for badge widgets to apply common styling.
    """
    def __init__(self, text="", parent=None, object_name="base_badge"):
        super().__init__(text, parent)
        self.setObjectName(object_name)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setMinimumHeight(20) # A reasonable minimum height for a badge
        self.setContentsMargins(Spacing.XS, Spacing.XXS, Spacing.XS, Spacing.XXS)
        self.setWordWrap(False)
        self.setText(text.strip().upper())

        self.setStyleSheet(f"""
            QLabel#{object_name} {{
                padding: {Spacing.XXS}px {Spacing.XS}px;
                border-radius: {Dimensions.BORDER_RADIUS_SM};
                font-size: {Typography.FONT_SIZE_XS};
                font-weight: {Typography.FONT_WEIGHT_BOLD};
                background-color: {Color.TAG_GRAY}; /* Default gray */
                color: {Color.WHITE}; /* Default text color */
                min-width: 20px;
            }}
        """)

class Badge(BaseBadge):
    """
    Generic badge with customizable text and color.
    """
    def __init__(self, text, color=Color.TAG_GRAY, text_color=Color.WHITE, parent=None):
        super().__init__(text, parent, object_name="badge")
        self.setStyleSheet(f"""
            QLabel#badge {{
                padding: {Spacing.XXS}px {Spacing.XS}px;
                border-radius: {Dimensions.BORDER_RADIUS_SM};
                font-size: {Typography.FONT_SIZE_XS};
                font-weight: {Typography.FONT_WEIGHT_BOLD};
                background-color: {color};
                color: {text_color};
                min-width: 20px;
            }}
        """)

class DifficultyBadge(BaseBadge):
    """
    Badge displaying difficulty level with specific colors.
    """
    def __init__(self, difficulty: DifficultyEnum, parent=None):
        super().__init__(difficulty.value.upper(), parent, object_name="difficulty_badge")
        color = Color.TAG_GRAY
        text_color = Color.WHITE
        if difficulty == DifficultyEnum.EASY:
            color = Color.TAG_GREEN
        elif difficulty == DifficultyEnum.MEDIUM:
            color = Color.TAG_YELLOW
            text_color = Color.DARK_TEXT # Yellow tags often need dark text
        elif difficulty == DifficultyEnum.HARD:
            color = Color.TAG_ORANGE
        elif difficulty == DifficultyEnum.VERY_HARD:
            color = Color.TAG_RED

        self.setStyleSheet(f"""
            QLabel#difficulty_badge {{
                padding: {Spacing.XXS}px {Spacing.XS}px;
                border-radius: {Dimensions.BORDER_RADIUS_SM};
                font-size: {Typography.FONT_SIZE_XS};
                font-weight: {Typography.FONT_WEIGHT_BOLD};
                background-color: {color};
                color: {text_color};
                min-width: 20px;
            }}
        """)

class SourceBadge(BaseBadge):
    """
    Badge displaying the source of a question (e.g., ENEM, FUVEST).
    """
    def __init__(self, source_text, parent=None):
        super().__init__(source_text, parent, object_name="source_badge")
        # Default to a specific tag color for sources, e.g., TAG_BLUE or TAG_PURPLE
        self.setStyleSheet(f"""
            QLabel#source_badge {{
                padding: {Spacing.XXS}px {Spacing.XS}px;
                border-radius: {Dimensions.BORDER_RADIUS_SM};
                font-size: {Typography.FONT_SIZE_XS};
                font-weight: {Typography.FONT_WEIGHT_BOLD};
                background-color: {Color.TAG_BLUE};
                color: {Color.WHITE};
                min-width: 20px;
            }}
        """)

class RemovableBadge(QWidget):
    """
    Badge with a close button to allow removal.
    """
    removed = pyqtSignal(str) # Signal emitted with the text of the removed badge

    def __init__(self, text, color=Color.TAG_GRAY, text_color=Color.WHITE, parent=None):
        super().__init__(parent)
        self.text = text
        self.setObjectName("removable_badge_container")

        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(Spacing.XXS)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.badge_label = Badge(text, color, text_color, self)
        self.layout.addWidget(self.badge_label)

        self.close_button = QPushButton("x", self)
        self.close_button.setFixedSize(QSize(16, 16))
        self.close_button.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                border: none;
                color: {text_color};
                font-weight: {Typography.FONT_WEIGHT_BOLD};
                font-size: {Typography.FONT_SIZE_XS};
                padding: 0px;
                margin: 0px;
            }}
            QPushButton:hover {{
                color: {Color.WHITE};
                background-color: rgba(0,0,0,0.2);
                border-radius: 8px;
            }}
        """)
        self.close_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.close_button.clicked.connect(self._on_close_clicked)
        self.layout.addWidget(self.close_button)

        # Apply container style
        self.setStyleSheet(f"""
            QWidget#removable_badge_container {{
                background-color: {color};
                border-radius: {Dimensions.BORDER_RADIUS_SM};
                padding-left: {Spacing.XS}px;
                padding-right: {Spacing.XXS}px;
                min-height: 20px;
            }}
        """)
        # Ensure label and button inherit some properties or adjust their styles
        self.badge_label.setStyleSheet(self.badge_label.styleSheet() + f"""
            QLabel#badge {{
                background-color: transparent; /* Container handles background */
                color: {text_color};
                padding: 0;
            }}
        """)

    def _on_close_clicked(self):
        self.removed.emit(self.text)
        self.deleteLater() # Remove the widget

if __name__ == '__main__':
    import sys
    from PyQt6.QtWidgets import QApplication, QVBoxLayout, QWidget

    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    from src.views.design.theme import ThemeManager
    ThemeManager.apply_global_theme(app)

    window = QWidget()
    layout = QVBoxLayout()
    layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)

    layout.addWidget(QLabel("Generic Badges:"))
    layout.addWidget(Badge("Matemática", color=Color.TAG_PURPLE))
    layout.addWidget(Badge("Cálculo", color=Color.TAG_BLUE))
    layout.addWidget(Badge("Geometria", color=Color.TAG_GREEN, text_color=Color.WHITE))

    layout.addWidget(QLabel("\nDifficulty Badges:"))
    layout.addWidget(DifficultyBadge(DifficultyEnum.EASY))
    layout.addWidget(DifficultyBadge(DifficultyEnum.MEDIUM))
    layout.addWidget(DifficultyBadge(DifficultyEnum.HARD))
    layout.addWidget(DifficultyBadge(DifficultyEnum.VERY_HARD))

    layout.addWidget(QLabel("\nSource Badges:"))
    layout.addWidget(SourceBadge("ENEM 2023"))
    layout.addWidget(SourceBadge("FUVEST"))

    layout.addWidget(QLabel("\nRemovable Badges:"))
    removable_badge1 = RemovableBadge("Tag A", Color.TAG_BLUE)
    removable_badge1.removed.connect(lambda text: print(f"Removed: {text}"))
    layout.addWidget(removable_badge1)

    removable_badge2 = RemovableBadge("Tag B", Color.TAG_GREEN, text_color=Color.WHITE)
    removable_badge2.removed.connect(lambda text: print(f"Removed: {text}"))
    layout.addWidget(removable_badge2)

    window.setLayout(layout)
    window.setWindowTitle("Badge Test")
    window.show()
    sys.exit(app.exec())
