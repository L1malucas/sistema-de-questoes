# src/views/pages/dashboard_page.py
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QGridLayout,
    QScrollArea, QTableWidget, QTableWidgetItem, QHeaderView,
    QSpacerItem, QSizePolicy
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont

# Matplotlib for plotting
import matplotlib
matplotlib.use('QtAgg') # Ensure using QtAgg backend
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from src.views.design.constants import Color, Spacing, Typography, Dimensions, Text
from src.views.components.common.cards import StatCard
from src.views.components.common.buttons import SecondaryButton # For filter buttons

class MplCanvas(FigureCanvas):
    """
    A Matplotlib canvas widget for embedding plots in PyQt applications.
    """
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)
        super(MplCanvas, self).__init__(self.fig)
        self.setParent(parent)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.updateGeometry()

class DashboardPage(QWidget):
    """
    Page displaying various statistics and metrics for the MathBank application.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("dashboard_page")

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(Spacing.XL, Spacing.LG, Spacing.XL, Spacing.LG)
        main_layout.setSpacing(Spacing.LG)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # 1. Filter Row
        filter_row_layout = QHBoxLayout()
        filter_row_layout.setSpacing(Spacing.SM)
        filter_row_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)

        period_filter = SecondaryButton("Period: Last 30 Days ▼", parent=self)
        filter_row_layout.addWidget(period_filter)

        tags_filter = SecondaryButton("Tags: All ▼", parent=self)
        filter_row_layout.addWidget(tags_filter)

        difficulty_filter = SecondaryButton("Difficulty: All ▼", parent=self)
        filter_row_layout.addWidget(difficulty_filter)

        filter_row_layout.addStretch()
        main_layout.addLayout(filter_row_layout)

        # 2. Metric Cards
        metric_cards_layout = QHBoxLayout()
        metric_cards_layout.setSpacing(Spacing.LG)
        metric_cards_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)

        metric_cards_layout.addWidget(StatCard("Total Questions", "1,234", "+87", parent=self))
        metric_cards_layout.addWidget(StatCard("New Questions", "87", parent=self))
        metric_cards_layout.addWidget(StatCard("Avg Success Rate", "68.5%", "-2%", parent=self))
        metric_cards_layout.addWidget(StatCard("Avg Time Spent", "4m 32s", parent=self))

        metric_cards_layout.addStretch()
        main_layout.addLayout(metric_cards_layout)

        # 3. Charts Row (Questions Over Time & Difficulty Distribution)
        charts_row_layout = QHBoxLayout()
        charts_row_layout.setSpacing(Spacing.LG)
        charts_row_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)

        # Questions Over Time (Line Chart)
        self.line_chart_canvas = MplCanvas(self, width=6, height=4, dpi=100)
        self._plot_questions_over_time(self.line_chart_canvas.axes)
        charts_row_layout.addWidget(self.line_chart_canvas)

        # Difficulty Distribution (Donut Chart)
        self.donut_chart_canvas = MplCanvas(self, width=4, height=4, dpi=100)
        self._plot_difficulty_distribution(self.donut_chart_canvas.axes)
        charts_row_layout.addWidget(self.donut_chart_canvas)

        charts_row_layout.addStretch()
        main_layout.addLayout(charts_row_layout)

        # 4. Accuracy Rate by Topic (Horizontal Bar Chart)
        accuracy_label = QLabel("Taxa de Acerto por Tópico", self)
        accuracy_label.setObjectName("section_title")
        accuracy_label.setStyleSheet(f"font-size: {Typography.FONT_SIZE_XL}; font-weight: {Typography.FONT_WEIGHT_SEMIBOLD}; color: {Color.DARK_TEXT};")
        main_layout.addWidget(accuracy_label)

        self.bar_chart_canvas = MplCanvas(self, width=10, height=3, dpi=100)
        self._plot_accuracy_by_topic(self.bar_chart_canvas.axes)
        main_layout.addWidget(self.bar_chart_canvas)


        # 5. Top 10 Hardest Questions Table
        hard_questions_header_layout = QHBoxLayout()
        hard_questions_label = QLabel("Top 10 Hardest Questions", self)
        hard_questions_label.setObjectName("section_title")
        hard_questions_label.setStyleSheet(f"font-size: {Typography.FONT_SIZE_XL}; font-weight: {Typography.FONT_WEIGHT_SEMIBOLD}; color: {Color.DARK_TEXT};")
        hard_questions_header_layout.addWidget(hard_questions_label)
        hard_questions_header_layout.addStretch()
        export_csv_button = SecondaryButton("Export CSV", parent=self)
        hard_questions_header_layout.addWidget(export_csv_button)
        main_layout.addLayout(hard_questions_header_layout)

        self.hard_questions_table = QTableWidget(self)
        self.hard_questions_table.setObjectName("hard_questions_table")
        self.hard_questions_table.setColumnCount(5)
        self.hard_questions_table.setHorizontalHeaderLabels(["ID", "Topic", "Tag", "Success Rate", "Actions"])
        self.hard_questions_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.hard_questions_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers) # Make table read-only
        self._populate_hard_questions_table() # Populate with dummy data

        self.hard_questions_table.setStyleSheet(f"""
            QTableWidget#hard_questions_table {{
                background-color: {Color.WHITE};
                border: 1px solid {Color.BORDER_LIGHT};
                border-radius: {Dimensions.BORDER_RADIUS_MD};
                font-size: {Typography.FONT_SIZE_MD};
                color: {Color.DARK_TEXT};
                gridline-color: {Color.BORDER_LIGHT};
            }}
            QTableWidget#hard_questions_table QHeaderView::section {{
                background-color: {Color.LIGHT_BACKGROUND};
                color: {Color.DARK_TEXT};
                font-weight: {Typography.FONT_WEIGHT_SEMIBOLD};
                padding: {Spacing.SM}px;
                border: 1px solid {Color.BORDER_LIGHT};
            }}
            QTableWidget#hard_questions_table::item {{
                padding: {Spacing.SM}px;
            }}
            QTableWidget#hard_questions_table::item:selected {{
                background-color: {Color.LIGHT_BLUE_BG_2};
                color: {Color.PRIMARY_BLUE};
            }}
        """)
        main_layout.addWidget(self.hard_questions_table)


        main_layout.addStretch(1) # Push all content to the top


    def _plot_questions_over_time(self, ax):
        # Dummy data
        days = ['Day 1', 'Day 2', 'Day 3', 'Day 4', 'Day 5']
        questions_added = [10, 12, 8, 15, 11]
        ax.plot(days, questions_added, marker='o', color=Color.PRIMARY_BLUE)
        ax.set_title('Questions Over Time', fontsize=12)
        ax.set_ylabel('Questions Added', fontsize=10)
        ax.tick_params(axis='x', rotation=45)
        ax.grid(True, linestyle='--', alpha=0.6)
        self.line_chart_canvas.fig.tight_layout() # Adjust layout to prevent labels overlapping

    def _plot_difficulty_distribution(self, ax):
        # Dummy data
        difficulty_labels = ['Easy', 'Medium', 'Hard']
        sizes = [40, 30, 30] # Percentage for each slice
        colors = [Color.TAG_GREEN, Color.TAG_YELLOW, Color.TAG_RED]
        ax.pie(sizes, labels=difficulty_labels, autopct='%1.1f%%', startangle=90, colors=colors,
               wedgeprops={'edgecolor': 'white', 'linewidth': 1})
        ax.set_title('Difficulty Distribution', fontsize=12)
        ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        self.donut_chart_canvas.fig.tight_layout()

    def _plot_accuracy_by_topic(self, ax):
        # Dummy data
        topics = ['Algebra', 'Calculus', 'Geometry', 'Probability']
        accuracy = [75, 60, 80, 55]
        y_pos = range(len(topics))
        ax.barh(y_pos, accuracy, color=Color.TAG_BLUE)
        ax.set_yticks(y_pos)
        ax.set_yticklabels(topics)
        ax.set_xlabel('Accuracy (%)', fontsize=10)
        ax.set_title('Accuracy by Topic', fontsize=12)
        ax.set_xlim(0, 100)
        self.bar_chart_canvas.fig.tight_layout()

    def _populate_hard_questions_table(self):
        # Dummy data for the table
        data = [
            ["Q-001", "Algebra", "Equations", "45%", "View | Edit"],
            ["Q-005", "Calculus", "Derivatives", "38%", "View | Edit"],
            ["Q-012", "Geometry", "Trigonometry", "52%", "View | Edit"],
            ["Q-020", "Algebra", "Logarithms", "48%", "View | Edit"],
            ["Q-025", "Calculus", "Integrals", "40%", "View | Edit"],
            ["Q-030", "Probability", "Distributions", "50%", "View | Edit"],
            ["Q-033", "Geometry", "Vectors", "55%", "View | Edit"],
            ["Q-040", "Algebra", "Matrices", "42%", "View | Edit"],
            ["Q-045", "Calculus", "Limits", "47%", "View | Edit"],
            ["Q-050", "Probability", "Combinatorics", "49%", "View | Edit"],
        ]

        self.hard_questions_table.setRowCount(len(data))
        for row_idx, row_data in enumerate(data):
            for col_idx, item_data in enumerate(row_data):
                self.hard_questions_table.setItem(row_idx, col_idx, QTableWidgetItem(item_data))


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
            self.setWindowTitle("Dashboard Page Test")
            self.setGeometry(100, 100, 1200, 900)

            self.dashboard_page = DashboardPage(self)
            self.setCentralWidget(self.dashboard_page)

    window = TestMainWindow()
    window.show()
    sys.exit(app.exec())