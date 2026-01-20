# src/views/pages/question_bank_page.py
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QGridLayout,
    QScrollArea, QSizePolicy, QSpacerItem, QFrame
)
from PyQt6.QtCore import Qt, pyqtSignal, QSize
from PyQt6.QtGui import QIcon
from src.views.design.constants import Color, Spacing, Typography, Dimensions, Text
from src.views.design.enums import DifficultyEnum
from src.views.components.common.inputs import SearchInput, SelectInput
from src.views.components.common.buttons import PrimaryButton, SecondaryButton # Using these for filter buttons
from src.views.components.common.cards import QuestionCard # Reusing our QuestionCard

class QuestionBankPage(QWidget):
    """
    Page displaying a bank of questions with search, filters, and pagination.
    """
    filter_changed = pyqtSignal(dict) # Emits current filter state
    page_changed = pyqtSignal(int) # Emits new page number
    question_selected = pyqtSignal(str) # Emits UUID of selected question

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("question_bank_page")
        self.current_filters = {} # Store current filter state
        self.current_page = 1
        self.total_results = 0

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(Spacing.XL, Spacing.LG, Spacing.XL, Spacing.LG)
        main_layout.setSpacing(Spacing.LG)

        # 1. Breadcrumb (Placeholder for now)
        breadcrumb_label = QLabel("Breadcrumb: Algebra / Functions", self)
        breadcrumb_label.setObjectName("breadcrumb_label")
        breadcrumb_label.setStyleSheet(f"color: {Color.GRAY_TEXT}; font-size: {Typography.FONT_SIZE_MD};")
        main_layout.addWidget(breadcrumb_label)

        # 2. Page Header
        header_layout = QHBoxLayout()
        page_title = QLabel("Question Explorer", self)
        page_title.setObjectName("page_title")
        page_title.setStyleSheet(f"""
            QLabel#page_title {{
                font-size: {Typography.FONT_SIZE_PAGE_TITLE};
                font-weight: {Typography.FONT_WEIGHT_BOLD};
                color: {Color.DARK_TEXT};
            }}
        """)
        header_layout.addWidget(page_title)
        header_layout.addStretch()

        self.results_count_label = QLabel("Showing 0 of 0 results", self)
        self.results_count_label.setObjectName("results_count")
        self.results_count_label.setStyleSheet(f"""
            QLabel#results_count {{
                font-size: {Typography.FONT_SIZE_MD};
                color: {Color.GRAY_TEXT};
            }}
        """)
        header_layout.addWidget(self.results_count_label)
        main_layout.addLayout(header_layout)

        # 3. Filter Bar
        filter_bar_frame = QFrame(self)
        filter_bar_frame.setObjectName("filters")
        filter_bar_frame.setStyleSheet(f"""
            QFrame#filters {{
                background-color: {Color.WHITE};
                border: 1px solid {Color.BORDER_LIGHT};
                border-radius: {Dimensions.BORDER_RADIUS_LG};
                padding: {Spacing.SM}px;
            }}
        """)
        filter_layout = QHBoxLayout(filter_bar_frame)
        filter_layout.setContentsMargins(Spacing.SM, Spacing.SM, Spacing.SM, Spacing.SM)
        filter_layout.setSpacing(Spacing.SM)

        self.search_input = SearchInput(placeholder_text=Text.SEARCH_PLACEHOLDER, parent=self)
        self.search_input.setMinimumWidth(250)
        self.search_input.textChanged.connect(self._on_search_changed)
        filter_layout.addWidget(self.search_input)

        # Filter Buttons (Placeholders - ideally custom dropdowns)
        self.enem_filter_btn = SecondaryButton("ENEM ▼", parent=self)
        filter_layout.addWidget(self.enem_filter_btn)

        self.difficulty_filter_btn = SecondaryButton("Easy ▼", parent=self)
        filter_layout.addWidget(self.difficulty_filter_btn)

        self.type_filter_btn = SecondaryButton("Type ▼", parent=self)
        filter_layout.addWidget(self.type_filter_btn)

        filter_layout.addStretch()

        settings_filter_btn = SecondaryButton("", icon="images/icons/settings.png", parent=self) # Placeholder settings icon
        filter_layout.addWidget(settings_filter_btn)

        main_layout.addWidget(filter_bar_frame)

        # 4. Question Grid (Scrollable)
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setObjectName("main_scroll")
        self.scroll_area.setStyleSheet(f"""
            QScrollArea#main_scroll {{
                border: none;
                background-color: transparent;
            }}
        """)

        self.questions_container = QWidget()
        self.questions_container.setObjectName("questions_container")
        self.questions_container.setStyleSheet(f"""
            QWidget#questions_container {{
                background-color: transparent;
            }}
        """)
        self.grid_layout = QGridLayout(self.questions_container)
        self.grid_layout.setContentsMargins(0, 0, 0, 0)
        self.grid_layout.setSpacing(Spacing.LG)
        self.scroll_area.setWidget(self.questions_container)
        main_layout.addWidget(self.scroll_area)

        # 5. Pagination (Placeholder for now)
        pagination_layout = QHBoxLayout()
        pagination_layout.addStretch()
        pagination_label = QLabel("Pagination controls here", self)
        pagination_label.setStyleSheet(f"color: {Color.GRAY_TEXT}; font-size: {Typography.FONT_SIZE_MD};")
        pagination_layout.addWidget(pagination_label)
        pagination_layout.addStretch()
        main_layout.addLayout(pagination_layout)


        self.setLayout(main_layout)
        self._load_placeholder_questions()
        self.update_results_count(len(self.placeholder_questions), 1240)


    def _on_search_changed(self, text: str):
        self.current_filters['search'] = text
        self._apply_filters()
        # For now, just print and show dummy results
        print(f"Search changed: {text}. Applying filters.")
        self._load_placeholder_questions(search_term=text)
        self.update_results_count(len(self.placeholder_questions), 1240) # Update based on filtered results


    def _apply_filters(self):
        # In a real app, this would trigger a data fetch
        self.filter_changed.emit(self.current_filters)


    def _load_placeholder_questions(self, search_term=""):
        # Clear existing cards
        while self.grid_layout.count():
            item = self.grid_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        # Dummy data for demonstration
        all_questions = [
            {"id": "#Q-1042", "title": "Integral definida de funções trigonométricas", "formula": "$$\\int_{0}^{\\pi/2} \\sin^2(x) dx$$", "tags": ["Cálculo", "Integrais"], "difficulty": DifficultyEnum.MEDIUM},
            {"id": "#Q-2051", "title": "Problema de otimização com derivadas", "tags": ["Otimização", "Derivadas"], "difficulty": DifficultyEnum.HARD},
            {"id": "#Q-4592", "title": "Equações lineares e sistemas", "formula": "$A\\mathbf{x} = \\mathbf{b}$", "tags": ["Álgebra", "Sistemas Lineares"], "difficulty": DifficultyEnum.EASY},
            {"id": "#Q-5000", "title": "Geometria analítica: distância entre pontos", "tags": ["Geometria", "Distância"], "difficulty": DifficultyEnum.EASY},
            {"id": "#Q-1100", "title": "Teorema de Pitágoras e suas aplicações", "tags": ["Geometria", "Ensino Médio"], "difficulty": DifficultyEnum.EASY},
            {"id": "#Q-1200", "title": "Cálculo de volume de sólidos de revolução", "tags": ["Cálculo", "Geometria"], "difficulty": DifficultyEnum.HARD},
            {"id": "#Q-1300", "title": "Fatoração de polinômios", "tags": ["Álgebra", "Polinômios"], "difficulty": DifficultyEnum.MEDIUM},
            {"id": "#Q-1400", "title": "Probabilidade condicional", "tags": ["Estatística", "Probabilidade"], "difficulty": DifficultyEnum.MEDIUM},
        ]

        self.placeholder_questions = [
            q for q in all_questions if search_term.lower() in q['title'].lower() or
            (q.get('formula') and search_term.lower() in q['formula'].lower())
        ]

        row = 0
        col = 0
        for q_data in self.placeholder_questions:
            card = QuestionCard(
                question_id=q_data['id'],
                title=q_data['title'],
                formula=q_data.get('formula'),
                tags=q_data['tags'],
                difficulty=q_data['difficulty'],
                parent=self
            )
            self.grid_layout.addWidget(card, row, col)
            col += 1
            if col >= 3: # 3 columns per row
                col = 0
                row += 1

        # Add spacers to fill empty grid cells if necessary
        while col < 3:
            self.grid_layout.addItem(QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum), row, col)
            col += 1
        self.grid_layout.addItem(QSpacerItem(0, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding), row + 1, 0)


    def update_results_count(self, current_shown: int, total_available: int):
        self.total_results = total_available
        self.results_count_label.setText(f"Showing {current_shown} of {total_available} results")


if __name__ == '__main__':
    import sys
    from PyQt6.QtWidgets import QApplication, QMainWindow

    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    from src.views.design.theme import ThemeManager
    ThemeManager.apply_global_theme(app)

    class TestMainWindow(QMainWindow):
        def __init__(self):
            super().__init__()
            self.setWindowTitle("Question Bank Page Test")
            self.setGeometry(100, 100, 1200, 800)

            self.question_bank_page = QuestionBankPage(self)
            self.setCentralWidget(self.question_bank_page)

            self.question_bank_page.filter_changed.connect(lambda filters: print(f"Filters applied: {filters}"))
            self.question_bank_page.page_changed.connect(lambda page_num: print(f"Page changed to: {page_num}"))
            self.question_bank_page.question_selected.connect(lambda q_uuid: print(f"Question selected: {q_uuid}"))

    window = TestMainWindow()
    window.show()
    sys.exit(app.exec())