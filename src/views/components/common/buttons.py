# src/views/components/common/buttons.py
from PyQt6.QtWidgets import QPushButton, QApplication
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt, QSize
from src.views.design.constants import Color, Spacing, Typography, Dimensions
from src.views.design.enums import ButtonTypeEnum, ActionEnum

class BaseButton(QPushButton):
    """
    Base button class applying common styles and properties.
    """
    def __init__(self, text="", icon=None, button_type=None, parent=None):
        super().__init__(text, parent)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setMinimumHeight(40) # Common minimum height

        if icon:
            self.setIcon(QIcon(icon))
            self.setIconSize(QSize(18, 18)) # Default icon size

        if button_type:
            self.setObjectName(f"button_{button_type.value}")
            self._apply_base_style(button_type)

    def _apply_base_style(self, button_type):
        # Base styles will be applied via QSS object names
        pass # Actual QSS will be in styles.py

class PrimaryButton(BaseButton):
    def __init__(self, text="Primary Button", icon=None, parent=None):
        super().__init__(text, icon, ButtonTypeEnum.PRIMARY, parent)
        self.setObjectName("create_button") # Matches style for create_button in mathbank_styles.css

class SecondaryButton(BaseButton):
    def __init__(self, text="Secondary Button", icon=None, parent=None):
        super().__init__(text, icon, ButtonTypeEnum.SECONDARY, parent)
        # Specific QSS for secondary will need to be added to styles.py
        self.setStyleSheet(f"""
            QPushButton#button_{ButtonTypeEnum.SECONDARY.value} {{
                background-color: {Color.WHITE};
                color: {Color.PRIMARY_BLUE};
                border: 2px solid {Color.PRIMARY_BLUE};
                border-radius: {Dimensions.BORDER_RADIUS_MD};
                font-size: {Typography.FONT_SIZE_MD};
                font-weight: {Typography.FONT_WEIGHT_BOLD};
                padding: {Spacing.SM}px {Spacing.LG}px;
            }}
            QPushButton#button_{ButtonTypeEnum.SECONDARY.value}:hover {{
                background-color: {Color.LIGHT_BLUE_BG_2};
            }}
        """)

class DangerButton(BaseButton):
    def __init__(self, text="Danger Button", icon=None, parent=None):
        super().__init__(text, icon, ButtonTypeEnum.DANGER, parent)
        # Specific QSS for danger will need to be added to styles.py
        self.setStyleSheet(f"""
            QPushButton#button_{ButtonTypeEnum.DANGER.value} {{
                background-color: {Color.TAG_RED};
                color: {Color.WHITE};
                border: none;
                border-radius: {Dimensions.BORDER_RADIUS_MD};
                font-size: {Typography.FONT_SIZE_MD};
                font-weight: {Typography.FONT_WEIGHT_BOLD};
                padding: {Spacing.SM}px {Spacing.LG}px;
            }}
            QPushButton#button_{ButtonTypeEnum.DANGER.value}:hover {{
                background-color: #A00000; /* Darker red */
            }}
        """)


class IconButton(BaseButton):
    def __init__(self, icon_path, size=QSize(24, 24), parent=None):
        super().__init__("", icon=icon_path, button_type=ButtonTypeEnum.ICON, parent=parent)
        self.setIconSize(size)
        self.setFixedSize(size.width() + Spacing.SM, size.height() + Spacing.SM) # Add some padding
        self.setText("")
        self.setStyleSheet(f"""
            QPushButton#button_{ButtonTypeEnum.ICON.value} {{
                background-color: transparent;
                border: none;
                border-radius: {Dimensions.BORDER_RADIUS_MD};
            }}
            QPushButton#button_{ButtonTypeEnum.ICON.value}:hover {{
                background-color: {Color.BORDER_LIGHT};
            }}
        """)

class ContextualActionButton(BaseButton):
    def __init__(self, text="", icon=None, action_type=None, parent=None):
        super().__init__(text, icon, ButtonTypeEnum.CONTEXTUAL, parent)
        self.action_type = action_type
        # Default style, can be overridden by specific objectName in QSS
        self.setStyleSheet(f"""
            QPushButton#button_{ButtonTypeEnum.CONTEXTUAL.value} {{
                background-color: transparent;
                border: none;
                color: {Color.PRIMARY_BLUE};
                font-size: {Typography.FONT_SIZE_MD};
                font-weight: {Typography.FONT_WEIGHT_MEDIUM};
            }}
            QPushButton#button_{ButtonTypeEnum.CONTEXTUAL.value}:hover {{
                text-decoration: underline;
            }}
        """)

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    app.setStyle("Fusion") # Better visual consistency

    from PyQt6.QtWidgets import QWidget, QVBoxLayout

    window = QWidget()
    layout = QVBoxLayout()

    # Apply global stylesheet for testing
    from src.views.design.theme import ThemeManager
    ThemeManager.apply_global_theme(app)

    primary_btn = PrimaryButton("Save Changes")
    layout.addWidget(primary_btn)

    secondary_btn = SecondaryButton("Cancel")
    layout.addWidget(secondary_btn)

    danger_btn = DangerButton("Delete Item")
    layout.addWidget(danger_btn)

    # Assuming you have an icon named 'settings.png' in some 'icons' folder for example
    # For a real application, you'd provide actual paths
    icon_btn = IconButton(icon_path="images/icons/settings.png") # Placeholder path
    icon_btn.setToolTip("Settings")
    layout.addWidget(icon_btn)

    ctx_btn = ContextualActionButton("View Details", action_type=ActionEnum.EDIT)
    layout.addWidget(ctx_btn)

    window.setLayout(layout)
    window.setWindowTitle("Button Test")
    window.show()
    sys.exit(app.exec())
