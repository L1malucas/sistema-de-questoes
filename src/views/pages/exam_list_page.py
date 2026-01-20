# src/views/pages/exam_list_page.py
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame,
    QListWidget, QListWidgetItem, QCheckBox, QRadioButton,
    QButtonGroup, QScrollArea, QSizePolicy, QGridLayout
)
from PyQt6.QtCore import Qt, pyqtSignal, QSize, QMimeData
from PyQt6.QtGui import QDrag
from src.views.design.constants import Color, Spacing, Typography, Dimensions, Text
from src.views.components.common.inputs import TextInput, LatexTextArea
from src.views.components.common.buttons import PrimaryButton, SecondaryButton

class QuestionListItem(QListWidgetItem):
    """
    Custom QListWidgetItem to hold question data for drag and drop.
    """
    def __init__(self, question_id: str, title: str):
        super().__init__(f"{question_id} {title}")
        self.question_id = question_id
        self.title = title
        # Store other question details as needed
        self.setFlags(self.flags() | Qt.ItemFlag.ItemIsDragEnabled)


class ExamListPage(QWidget):
    """
    Page for managing exam lists, including creating, editing, and exporting exams.
    """
    exam_selected = pyqtSignal(str) # Emits exam ID
    add_question_requested = pyqtSignal() # Request to open question bank
    generate_pdf_requested = pyqtSignal(dict) # Emits export config
    export_latex_requested = pyqtSignal(dict) # Emits export config

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("exam_list_page")

        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(Spacing.XL, Spacing.LG, Spacing.XL, Spacing.LG)
        main_layout.setSpacing(Spacing.LG)

        # 1. Exam List Sidebar
        exam_list_frame = QFrame(self)
        exam_list_frame.setObjectName("exam_list_sidebar")
        exam_list_frame.setFixedWidth(250)
        exam_list_frame.setStyleSheet(f"""
            QFrame#exam_list_sidebar {{
                background-color: {Color.WHITE};
                border: 1px solid {Color.BORDER_LIGHT};
                border-radius: {Dimensions.BORDER_RADIUS_LG};
            }}
        """)
        exam_list_layout = QVBoxLayout(exam_list_frame)
        exam_list_layout.setContentsMargins(Spacing.MD, Spacing.MD, Spacing.MD, Spacing.MD)
        exam_list_layout.setSpacing(Spacing.SM)

        exam_list_title = QLabel("MY EXAMS", exam_list_frame)
        exam_list_title.setStyleSheet(f"font-weight: {Typography.FONT_WEIGHT_BOLD}; font-size: {Typography.FONT_SIZE_MD}; color: {Color.DARK_TEXT};")
        exam_list_layout.addWidget(exam_list_title)

        create_new_exam_btn = PrimaryButton("+ Create New", parent=exam_list_frame)
        exam_list_layout.addWidget(create_new_exam_btn)

        self.exam_list_widget = QListWidget(exam_list_frame)
        self.exam_list_widget.setObjectName("exam_list_widget")
        self.exam_list_widget.itemClicked.connect(lambda item: self.exam_selected.emit(item.text())) # Placeholder for actual ID
        self.exam_list_widget.setStyleSheet(f"""
            QListWidget#exam_list_widget {{
                border: none;
                background-color: transparent;
                font-size: {Typography.FONT_SIZE_MD};
                color: {Color.DARK_TEXT};
            }}
            QListWidget#exam_list_widget::item {{
                padding: {Spacing.XS}px;
                border-radius: {Dimensions.BORDER_RADIUS_SM};
            }}
            QListWidget#exam_list_widget::item:selected {{
                background-color: {Color.LIGHT_BLUE_BG_2};
                color: {Color.PRIMARY_BLUE};
            }}
            QListWidget#exam_list_widget::item:hover {{
                background-color: {Color.BORDER_LIGHT};
            }}
        """)
        self._populate_exam_list() # Populate with dummy data
        exam_list_layout.addWidget(self.exam_list_widget)

        main_layout.addWidget(exam_list_frame)


        # 2. Exam Editor Area
        editor_area_frame = QFrame(self)
        editor_area_frame.setObjectName("exam_editor_area")
        editor_area_frame.setStyleSheet(f"""
            QFrame#exam_editor_area {{
                background-color: {Color.WHITE};
                border: 1px solid {Color.BORDER_LIGHT};
                border-radius: {Dimensions.BORDER_RADIUS_LG};
                padding: {Spacing.LG}px;
            }}
        """)
        editor_area_layout = QVBoxLayout(editor_area_frame)
        editor_area_layout.setContentsMargins(0, 0, 0, 0)
        editor_area_layout.setSpacing(Spacing.LG)


        # Header & Instructions
        header_instr_layout = QGridLayout()
        header_instr_layout.setSpacing(Spacing.SM)

        header_instr_layout.addWidget(QLabel("School Name:", editor_area_frame), 0, 0)
        self.school_name_input = TextInput(parent=editor_area_frame)
        header_instr_layout.addWidget(self.school_name_input, 0, 1)

        header_instr_layout.addWidget(QLabel("Professor:", editor_area_frame), 1, 0)
        self.professor_input = TextInput(parent=editor_area_frame)
        header_instr_layout.addWidget(self.professor_input, 1, 1)

        header_instr_layout.addWidget(QLabel("Exam Date:", editor_area_frame), 2, 0)
        self.exam_date_input = TextInput(parent=editor_area_frame) # Using text input for simplicity
        header_instr_layout.addWidget(self.exam_date_input, 2, 1)

        header_instr_layout.addWidget(QLabel("Department:", editor_area_frame), 3, 0)
        self.department_input = TextInput(parent=editor_area_frame)
        header_instr_layout.addWidget(self.department_input, 3, 1)

        header_instr_layout.addWidget(QLabel("Instructions (LaTeX):", editor_area_frame), 4, 0, 1, 2)
        self.instructions_input = LatexTextArea(parent=editor_area_frame)
        self.instructions_input.setMinimumHeight(100)
        header_instr_layout.addWidget(self.instructions_input, 5, 0, 1, 2)

        editor_area_layout.addLayout(header_instr_layout)


        # Questions List (Drag & Drop)
        editor_area_layout.addWidget(QLabel("Questions (0 Total)", editor_area_frame))
        self.add_from_bank_btn = PrimaryButton("+ Add from Question Bank", parent=editor_area_frame)
        self.add_from_bank_btn.clicked.connect(self.add_question_requested.emit)
        editor_area_layout.addWidget(self.add_from_bank_btn)

        self.questions_list_widget = QListWidget(editor_area_frame)
        self.questions_list_widget.setObjectName("exam_questions_list")
        self.questions_list_widget.setDragDropMode(QListWidget.DragDropMode.InternalMove)
        self.questions_list_widget.setSelectionMode(QListWidget.SelectionMode.SingleSelection)
        self.questions_list_widget.setAcceptDrops(True)
        self.questions_list_widget.setDropIndicatorShown(True)
        self._populate_questions_list() # Dummy questions
        editor_area_layout.addWidget(self.questions_list_widget)

        main_layout.addWidget(editor_area_frame, 2) # Takes more space


        # 3. Export Config Panel
        export_config_frame = QFrame(self)
        export_config_frame.setObjectName("export_config_panel")
        export_config_frame.setFixedWidth(200)
        export_config_frame.setStyleSheet(f"""
            QFrame#export_config_panel {{
                background-color: {Color.WHITE};
                border: 1px solid {Color.BORDER_LIGHT};
                border-radius: {Dimensions.BORDER_RADIUS_LG};
            }}
        """)
        export_config_layout = QVBoxLayout(export_config_frame)
        export_config_layout.setContentsMargins(Spacing.MD, Spacing.MD, Spacing.MD, Spacing.MD)
        export_config_layout.setSpacing(Spacing.LG)

        export_config_layout.addWidget(QLabel("Export Config", export_config_frame))

        # Column Layout
        export_config_layout.addWidget(QLabel("Columns:", export_config_frame))
        self.column_button_group = QButtonGroup(self)
        self.single_column_radio = QRadioButton("Single Column", export_config_frame)
        self.two_columns_radio = QRadioButton("Two Columns", export_config_frame)
        self.two_columns_radio.setChecked(True) # Default
        self.column_button_group.addButton(self.single_column_radio)
        self.column_button_group.addButton(self.two_columns_radio)
        export_config_layout.addWidget(self.single_column_radio)
        export_config_layout.addWidget(self.two_columns_radio)

        # Options
        export_config_layout.addWidget(QLabel("Options:", export_config_frame))
        self.answer_key_checkbox = QCheckBox("Answer Key", export_config_frame)
        export_config_layout.addWidget(self.answer_key_checkbox)

        self.point_values_checkbox = QCheckBox("Point Values", export_config_frame)
        export_config_layout.addWidget(self.point_values_checkbox)

        self.work_space_checkbox = QCheckBox("Work Space", export_config_frame)
        export_config_layout.addWidget(self.work_space_checkbox)

        export_config_layout.addStretch()

        # Summary
        summary_layout = QVBoxLayout()
        summary_layout.setSpacing(Spacing.XS)
        summary_layout.addWidget(QLabel("Total: 0 Q", export_config_frame))
        summary_layout.addWidget(QLabel("Points: 0/0", export_config_frame))
        summary_layout.addWidget(QLabel("Pages: ~0", export_config_frame))
        export_config_layout.addLayout(summary_layout)

        # Action Buttons
        generate_pdf_btn = PrimaryButton("Generate PDF", parent=export_config_frame)
        generate_pdf_btn.clicked.connect(self._on_generate_pdf)
        export_config_layout.addWidget(generate_pdf_btn)

        export_latex_btn = SecondaryButton("Export LaTeX", parent=export_config_frame)
        export_latex_btn.clicked.connect(self._on_export_latex)
        export_config_layout.addWidget(export_latex_btn)

        main_layout.addWidget(export_config_frame)

    def _populate_exam_list(self):
        # Dummy data
        self.exam_list_widget.addItem("• Calculus I")
        self.exam_list_widget.addItem("• Algebra Quiz")
        self.exam_list_widget.addItem("• Prob Final")

    def _populate_questions_list(self):
        # Dummy questions
        self.questions_list_widget.addItem(QuestionListItem("Q1", "Integration • Power Rule"))
        self.questions_list_widget.addItem(QuestionListItem("Q2", "Derivatives • Chain Rule"))
        self.questions_list_widget.addItem(QuestionListItem("Q3", "Limits • L'Hopital's Rule"))


    def _on_generate_pdf(self):
        config = self._get_export_config()
        self.generate_pdf_requested.emit(config)

    def _on_export_latex(self):
        config = self._get_export_config()
        self.export_latex_requested.emit(config)

    def _get_export_config(self):
        return {
            "columns": "single" if self.single_column_radio.isChecked() else "two",
            "include_answer_key": self.answer_key_checkbox.isChecked(),
            "include_point_values": self.point_values_checkbox.isChecked(),
            "include_work_space": self.work_space_checkbox.isChecked(),
        }

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
            self.setWindowTitle("Exam List Page Test")
            self.setGeometry(100, 100, 1200, 800)

            self.exam_list_page = ExamListPage(self)
            self.setCentralWidget(self.exam_list_page)

            self.exam_list_page.exam_selected.connect(lambda exam_id: print(f"Exam selected: {exam_id}"))
            self.exam_list_page.add_question_requested.connect(lambda: print("Add question requested!"))
            self.exam_list_page.generate_pdf_requested.connect(lambda config: print(f"Generate PDF with config: {config}"))
            self.exam_list_page.export_latex_requested.connect(lambda config: print(f"Export LaTeX with config: {config}"))

    window = TestMainWindow()
    window.show()
    sys.exit(app.exec())