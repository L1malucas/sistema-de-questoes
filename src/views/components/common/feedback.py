# src/views/components/common/feedback.py
from PyQt6.QtWidgets import (
    QDialog, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QWidget,
    QMessageBox, QGraphicsDropShadowEffect, QApplication, QSizePolicy
)
from PyQt6.QtCore import Qt, QTimer, QSize, pyqtSignal
from PyQt6.QtGui import QColor, QMovie, QFont, QIcon
from src.views.design.constants import Color, Spacing, Typography, Dimensions
from src.views.design.enums import ButtonTypeEnum
from src.views.components.common.buttons import PrimaryButton, SecondaryButton, DangerButton


class Toast(QWidget):
    """
    A temporary, non-blocking notification message.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.BypassWindowManagerHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(Spacing.LG, Spacing.SM, Spacing.LG, Spacing.SM)
        self.layout.setSpacing(0)

        self.label = QLabel("")
        self.label.setObjectName("toast_label")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.label)

        self.shadow_effect = QGraphicsDropShadowEffect(self)
        self.shadow_effect.setBlurRadius(10)
        self.shadow_effect.setColor(QColor(0, 0, 0, 100))
        self.shadow_effect.setOffset(0, 2)
        self.setGraphicsEffect(self.shadow_effect)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.hide)
        self.timer.setSingleShot(True) # Ensure it only runs once per show
        self.hide() # Initially hidden
    def show_message(self, message: str, toast_type: str = "info", duration_ms: int = 3000):
        self.label.setText(message)

        bg_color = Color.DARK_TEXT
        text_color = Color.WHITE

        if toast_type == "success":
            bg_color = Color.TAG_GREEN
        elif toast_type == "error":
            bg_color = Color.TAG_RED
        elif toast_type == "warning":
            bg_color = Color.TAG_YELLOW
            text_color = Color.DARK_TEXT
        elif toast_type == "info":
            bg_color = Color.PRIMARY_BLUE

        self.setStyleSheet(f"""
            QWidget {{
                background-color: {bg_color};
                color: {text_color};
                border-radius: {Dimensions.BORDER_RADIUS_MD};
                font-size: {Typography.FONT_SIZE_MD};
                padding: {Spacing.SM}px {Spacing.LG}px;
            }}
            QLabel#toast_label {{
                color: {text_color};
                font-weight: {Typography.FONT_WEIGHT_MEDIUM};
            }}
        """)
        self.adjustSize() # Adjust size to new message
        self.show()
        self.timer.start(duration_ms)

    def showEvent(self, event):
        # Position the toast at the bottom center of the parent or screen
        if self.parentWidget():
            parent_rect = self.parentWidget().geometry()
            x = parent_rect.x() + (parent_rect.width() - self.width()) // 2
            y = parent_rect.y() + parent_rect.height() - self.height() - Spacing.XL
            self.move(x, y)
        else:
            screen_rect = QApplication.primaryScreen().geometry()
            x = (screen_rect.width() - self.width()) // 2
            y = screen_rect.height() - self.height() - Spacing.XL
            self.move(x, y)
        super().showEvent(event)


class LoadingSpinner(QWidget):
    """
    A widget displaying a loading spinner animation.
    Requires a GIF file for animation.
    """
    def __init__(self, parent=None, size: int = 48, gif_path: str = "imagens/loaders/loading.gif"):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.movie_label = QLabel(self)
        self.movie_label.setFixedSize(QSize(size, size))
        self.movie_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        try:
            self.movie = QMovie(gif_path)
            self.movie.setScaledSize(QSize(size, size))
            self.movie_label.setMovie(self.movie)
            self.movie.start()
        except Exception as e:
            print(f"Error loading GIF for spinner: {e}. Displaying static text.")
            self.movie_label.setText("Loading...")
            self.movie_label.setStyleSheet(f"color: {Color.GRAY_TEXT}; font-size: {Typography.FONT_SIZE_MD};")

        self.layout.addWidget(self.movie_label)
        self.setLayout(self.layout)
        self.hide() # Start hidden

    def start_loading(self):
        if hasattr(self, 'movie') and isinstance(self.movie, QMovie):
            self.movie.start()
        self.show()

    def stop_loading(self):
        if hasattr(self, 'movie') and isinstance(self.movie, QMovie):
            self.movie.stop()
        self.hide()


class EmptyState(QWidget):
    """
    A widget to display when there is no content, featuring an icon and a message.
    """
    def __init__(self, message: str, icon_path: str = None, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.setContentsMargins(Spacing.XL, Spacing.XL, Spacing.XL, Spacing.XL)
        self.layout.setSpacing(Spacing.LG)

        if icon_path:
            self.icon_label = QLabel(self)
            self.icon_label.setPixmap(QIcon(icon_path).pixmap(QSize(64, 64)))
            self.icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.layout.addWidget(self.icon_label)

        self.message_label = QLabel(message, self)
        self.message_label.setObjectName("empty_state_message")
        self.message_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.message_label.setWordWrap(True)
        self.message_label.setStyleSheet(f"""
            QLabel#empty_state_message {{
                color: {Color.GRAY_TEXT};
                font-size: {Typography.FONT_SIZE_LG};
                font-weight: {Typography.FONT_WEIGHT_MEDIUM};
            }}
        """)
        self.layout.addWidget(self.message_label)
        self.setLayout(self.layout)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)


class ConfirmDialog(QDialog):
    """
    A custom confirmation dialog.
    """
    confirmed = pyqtSignal()
    rejected = pyqtSignal()

    def __init__(self, title: str, message: str, confirm_text: str = "Confirmar", cancel_text: str = "Cancelar", parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setModal(True)
        self.setFixedSize(400, 200) # Example fixed size

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(Spacing.XL, Spacing.XL, Spacing.XL, Spacing.XL)
        self.layout.setSpacing(Spacing.LG)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.message_label = QLabel(message, self)
        self.message_label.setObjectName("confirm_dialog_message")
        self.message_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.message_label.setWordWrap(True)
        self.message_label.setStyleSheet(f"""
            QLabel#confirm_dialog_message {{
                color: {Color.DARK_TEXT};
                font-size: {Typography.FONT_SIZE_LG};
                font-weight: {Typography.FONT_WEIGHT_REGULAR};
            }}
        """)
        self.layout.addWidget(self.message_label)

        button_layout = QHBoxLayout()
        button_layout.addStretch()

        self.cancel_button = SecondaryButton(cancel_text, parent=self)
        self.cancel_button.clicked.connect(self._on_cancel)
        button_layout.addWidget(self.cancel_button)

        self.confirm_button = PrimaryButton(confirm_text, parent=self)
        self.confirm_button.clicked.connect(self._on_confirm)
        button_layout.addWidget(self.confirm_button)

        button_layout.addStretch()
        self.layout.addLayout(button_layout)

        self.setStyleSheet(f"""
            QDialog {{
                background-color: {Color.WHITE};
                border-radius: {Dimensions.BORDER_RADIUS_LG};
                border: 1px solid {Color.BORDER_LIGHT};
            }}
            QDialog QLabel {{
                color: {Color.DARK_TEXT};
            }}
            QDialog QPushButtton {{
                min-width: 80px;
                min-height: 35px;
            }}
        """)

    def _on_confirm(self):
        self.confirmed.emit()
        self.accept()

    def _on_cancel(self):
        self.rejected.emit()
        self.reject()

if __name__ == '__main__':
    import sys
    from PyQt6.QtWidgets import QVBoxLayout, QWidget, QPushButton

    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    from src.views.design.theme import ThemeManager
    ThemeManager.apply_global_theme(app)

    main_window = QWidget()
    main_layout = QVBoxLayout(main_window)
    main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

    # Toast Test
    main_layout.addWidget(QLabel("<h3>Toast Examples:</h3>"))
    toast_info_btn = QPushButton("Show Info Toast")
    toast_info_btn.clicked.connect(lambda: Toast("This is an info message!", "info", parent=main_window).show())
    main_layout.addWidget(toast_info_btn)

    toast_success_btn = QPushButton("Show Success Toast")
    toast_success_btn.clicked.connect(lambda: Toast("Operation completed successfully!", "success", parent=main_window).show())
    main_layout.addWidget(toast_success_btn)

    toast_error_btn = QPushButton("Show Error Toast")
    toast_error_btn.clicked.connect(lambda: Toast("An error occurred!", "error", parent=main_window).show())
    main_layout.addWidget(toast_error_btn)

    toast_warning_btn = QPushButton("Show Warning Toast")
    toast_warning_btn.clicked.connect(lambda: Toast("Proceed with caution!", "warning", parent=main_window).show())
    main_layout.addWidget(toast_warning_btn)

    # Loading Spinner Test
    main_layout.addWidget(QLabel("<h3>Loading Spinner:</h3>"))
    spinner = LoadingSpinner(parent=main_window, gif_path="imagens/logos/lampada.png") # Using an existing image as placeholder
    main_layout.addWidget(spinner)
    spinner_start_btn = QPushButton("Start Loading")
    spinner_start_btn.clicked.connect(spinner.start_loading)
    main_layout.addWidget(spinner_start_btn)
    spinner_stop_btn = QPushButton("Stop Loading")
    spinner_stop_btn.clicked.connect(spinner.stop_loading)
    main_layout.addWidget(spinner_stop_btn)


    # Empty State Test
    main_layout.addWidget(QLabel("<h3>Empty State:</h3>"))
    empty_state = EmptyState("Nenhuma questão encontrada com os filtros aplicados.", icon_path="imagens/logos/lampada.png", parent=main_window)
    empty_state.setFixedSize(300, 200) # Example size for display
    main_layout.addWidget(empty_state)

    # Confirm Dialog Test
    main_layout.addWidget(QLabel("<h3>Confirm Dialog:</h3>"))
    confirm_dialog_btn = QPushButton("Show Confirm Dialog")
    def show_confirm_dialog():
        dialog = ConfirmDialog("Confirmar Exclusão", "Tem certeza que deseja excluir este item permanentemente?", parent=main_window)
        dialog.confirmed.connect(lambda: print("Confirmed!"))
        dialog.rejected.connect(lambda: print("Rejected!"))
        dialog.exec()
    confirm_dialog_btn.clicked.connect(show_confirm_dialog)
    main_layout.addWidget(confirm_dialog_btn)


    main_window.setWindowTitle("Feedback Components Test")
    main_window.show()
    sys.exit(app.exec())