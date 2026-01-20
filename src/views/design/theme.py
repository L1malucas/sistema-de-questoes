# src/views/design/theme.py
from PyQt6.QtWidgets import QApplication
from src.views.design.styles import StyleSheet

class ThemeManager:
    """
    Manages the application's visual theme, applying stylesheets globally or to specific widgets.
    """
    @staticmethod
    def apply_global_theme(app: QApplication):
        """
        Applies the global stylesheet to the entire application.
        """
        app.setStyleSheet(StyleSheet.get_global_stylesheet())
        # Concatenate other major stylesheets if they are meant to be global
        app.setStyleSheet(app.styleSheet() + StyleSheet.get_navbar_stylesheet())
        app.setStyleSheet(app.styleSheet() + StyleSheet.get_sidebar_stylesheet())
        app.setStyleSheet(app.styleSheet() + StyleSheet.get_main_content_stylesheet())
        app.setStyleSheet(app.styleSheet() + StyleSheet.get_filter_bar_stylesheet())
        app.setStyleSheet(app.styleSheet() + StyleSheet.get_question_card_stylesheet())
        app.setStyleSheet(app.styleSheet() + StyleSheet.get_scrollbar_stylesheet())


    @staticmethod
    def get_tag_style(tag_color_name: str) -> str:
        """
        Retrieves the stylesheet for a specific tag color.
        """
        return StyleSheet.get_tag_stylesheet(tag_color_name)

    # Future methods could include:
    # - switch_theme(theme_name)
    # - apply_component_theme(widget, component_name)
