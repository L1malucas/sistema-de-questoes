# src/views/components/common/inputs.py
from PyQt6.QtWidgets import QLineEdit, QTextEdit, QComboBox, QDateEdit, QWidget, QHBoxLayout, QLabel, QStyle, QStyleOptionFrame, QApplication
from PyQt6.QtGui import QIcon, QPainter, QColor, QFont, QIntValidator
from PyQt6.QtCore import Qt, QSize, QDate
from src.views.design.constants import Color, Spacing, Typography, Dimensions

class TextInput(QLineEdit):
    def __init__(self, parent=None, placeholder_text="Enter text", object_name="text_input"):
        super().__init__(parent)
        self.setObjectName(object_name)
        self.setPlaceholderText(placeholder_text)
        self.setStyleSheet(f"""
            QLineEdit#{object_name} {{
                background-color: {Color.WHITE};
                border: 1px solid {Color.BORDER_MEDIUM};
                border-radius: {Dimensions.BORDER_RADIUS_MD};
                padding: {Spacing.SM}px;
                font-size: {Typography.FONT_SIZE_MD};
                color: {Color.DARK_TEXT};
            }}
            QLineEdit#{object_name}:focus {{
                border: 1px solid {Color.PRIMARY_BLUE};
            }}
        """)

class SearchInput(QLineEdit):
    def __init__(self, parent=None, placeholder_text="Search...", object_name="search_input"):
        super().__init__(parent)
        self.setObjectName(object_name)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setContentsMargins(Spacing.XL, 0, Spacing.SM, 0)
        self.setPlaceholderText(placeholder_text)
        self.setStyleSheet(f"""
            QLineEdit#search_input {{
                background-color: {Color.BORDER_LIGHT};
                border: none;
                border-radius: {Dimensions.BORDER_RADIUS_MD};
                padding: {Spacing.SM}px {Spacing.SM}px {Spacing.SM}px {Spacing.XL}px;
                font-size: {Typography.FONT_SIZE_MD};
                color: {Color.DARK_TEXT};
            }}
            QLineEdit#search_input::placeholder {{
                color: {Color.GRAY_TEXT};
            }}
        """)
        self.old_paintEvent = self.paintEvent
        self.paintEvent = self._custom_paint_event

    def _custom_paint_event(self, event):
        self.old_paintEvent(event)
        painter = QPainter(self)
        icon = QApplication.style().standardIcon(QStyle.StandardPixmap.SP_FileDialogToParent)
        pixmap = icon.pixmap(QSize(16, 16))
        painter.drawPixmap(Spacing.SM, (self.height() - pixmap.height()) // 2, pixmap)
        painter.end()


class TextAreaInput(QTextEdit):
    def __init__(self, parent=None, placeholder_text="Enter multi-line text", object_name="textarea_input"):
        super().__init__(parent)
        self.setObjectName(object_name)
        self.setPlaceholderText(placeholder_text)
        self.setMinimumHeight(100)
        self.setStyleSheet(f"""
            QTextEdit#{object_name} {{
                background-color: {Color.WHITE};
                border: 1px solid {Color.BORDER_MEDIUM};
                border-radius: {Dimensions.BORDER_RADIUS_MD};
                padding: {Spacing.SM}px;
                font-size: {Typography.FONT_SIZE_MD};
                color: {Color.DARK_TEXT};
            }}
            QTextEdit#{object_name}:focus {{
                border: 1px solid {Color.PRIMARY_BLUE};
            }}
        """)

class LatexTextArea(QTextEdit):
    def __init__(self, parent=None, placeholder_text="Enter LaTeX content", object_name="latex_textarea"):
        super().__init__(parent)
        self.setObjectName(object_name)
        self.setPlaceholderText(placeholder_text)
        self.setMinimumHeight(150)
        self.setStyleSheet(f"""
            QTextEdit#{object_name} {{
                background-color: {Color.WHITE};
                border: 1px solid {Color.BORDER_MEDIUM};
                border-radius: {Dimensions.BORDER_RADIUS_MD};
                padding: {Spacing.SM}px;
                font-size: {Typography.FONT_SIZE_MD};
                color: {Color.DARK_TEXT};
                font-family: "Consolas", "Monaco", "monospace";
            }}
            QTextEdit#{object_name}:focus {{
                border: 1px solid {Color.PRIMARY_BLUE};
            }}
        """)


class SelectInput(QComboBox):
    def __init__(self, parent=None, items=None, object_name="select_input"):
        super().__init__(parent)
        self.setObjectName(object_name)
        if items:
            self.addItems(items)
        self.setStyleSheet(f"""
            QComboBox#{object_name} {{
                background-color: {Color.WHITE};
                border: 1px solid {Color.BORDER_MEDIUM};
                border-radius: {Dimensions.BORDER_RADIUS_MD};
                padding: {Spacing.SM}px;
                font-size: {Typography.FONT_SIZE_MD};
                color: {Color.DARK_TEXT};
            }}
            QComboBox#{object_name}::drop-down {{
                border: 0px;
            }}
            QComboBox#{object_name}::down-arrow {{
                image: url(resources/icons/arrow_down.png);
                width: 12px;
                height: 12px;
            }}
            QComboBox#{object_name}:focus {{
                border: 1px solid {Color.PRIMARY_BLUE};
            }}
            QComboBox#{object_name} QAbstractItemView {{
                border: 1px solid {Color.BORDER_MEDIUM};
                border-radius: {Dimensions.BORDER_RADIUS_MD};
                background-color: {Color.WHITE};
                selection-background-color: {Color.LIGHT_BLUE_BG_1};
                selection-color: {Color.PRIMARY_BLUE};
            }}
        """)

class DateInput(QDateEdit):
    def __init__(self, parent=None, object_name="date_input"):
        super().__init__(parent)
        self.setObjectName(object_name)
        self.setCalendarPopup(True)
        self.setDate(QDate.currentDate())
        self.setDisplayFormat("dd/MM/yyyy")
        self.setStyleSheet(f"""
            QDateEdit#{object_name} {{
                background-color: {Color.WHITE};
                border: 1px solid {Color.BORDER_MEDIUM};
                border-radius: {Dimensions.BORDER_RADIUS_MD};
                padding: {Spacing.SM}px;
                font-size: {Typography.FONT_SIZE_MD};
                color: {Color.DARK_TEXT};
            }}
            QDateEdit#{object_name}::drop-down {{
                border: 0px;
            }}
            QDateEdit#{object_name}::down-arrow {{
                image: url(resources/icons/calendar.png);
                width: 16px;
                height: 16px;
            }}
            QDateEdit#{object_name}:focus {{
                border: 1px solid {Color.PRIMARY_BLUE};
            }}
        """)

if __name__ == '__main__':
    import sys
    from PyQt6.QtWidgets import QVBoxLayout

    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    from src.views.design.theme import ThemeManager
    ThemeManager.apply_global_theme(app)

    window = QWidget()
    layout = QVBoxLayout()

    text_input = TextInput(placeholder_text="Nome do Usuário")
    layout.addWidget(text_input)

    search_input = SearchInput(placeholder_text="Buscar questões...")
    layout.addWidget(search_input)

    textarea_input = TextAreaInput(placeholder_text="Descrição detalhada...")
    layout.addWidget(textarea_input)

    latex_textarea = LatexTextArea(placeholder_text="Digite sua equação LaTeX aqui...")
    layout.addWidget(latex_textarea)

    select_input = SelectInput(items=["Opção 1", "Opção 2", "Opção 3"])
    layout.addWidget(select_input)

    date_input = DateInput()
    layout.addWidget(date_input)

    window.setLayout(layout)
    window.setWindowTitle("Input Test")
    window.show()
    sys.exit(app.exec_())