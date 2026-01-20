# src/views/pages/taxonomy_page.py
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame,
    QGridLayout, QScrollArea, QTableWidget, QTableWidgetItem,
    QHeaderView, QPushButton, QSizePolicy, QSpacerItem
)
from PyQt6.QtCore import Qt, pyqtSignal, QSize
from PyQt6.QtGui import QIcon, QColor
from src.views.design.constants import Color, Spacing, Typography, Dimensions, Text
from src.views.components.common.inputs import TextInput
from src.views.components.common.buttons import PrimaryButton, SecondaryButton
from src.views.components.layout.sidebar import TagTreeView

class TaxonomyPage(QWidget):
    """
    Page for managing the hierarchical taxonomy of tags.
    Allows editing tags, viewing statistics, and performing quick actions.
    """
    tag_selected = pyqtSignal(str) # Emits UUID of selected tag for editing
    save_tag_requested = pyqtSignal(dict) # Emits tag data to save
    delete_tag_requested = pyqtSignal(str) # Emits UUID of tag to delete
    merge_tag_requested = pyqtSignal(str, str) # Emits (source_tag_uuid, target_tag_uuid)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("taxonomy_page")

        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(Spacing.XL, Spacing.LG, Spacing.XL, Spacing.LG)
        main_layout.setSpacing(Spacing.LG)

        # 1. Math Taxonomy Tree (Left Panel)
        taxonomy_tree_frame = QFrame(self)
        taxonomy_tree_frame.setObjectName("taxonomy_tree_frame")
        taxonomy_tree_frame.setFixedWidth(300)
        taxonomy_tree_frame.setStyleSheet(f"""
            QFrame#taxonomy_tree_frame {{
                background-color: {Color.WHITE};
                border: 1px solid {Color.BORDER_LIGHT};
                border-radius: {Dimensions.BORDER_RADIUS_LG};
            }}
        """)
        taxonomy_tree_layout = QVBoxLayout(taxonomy_tree_frame)
        taxonomy_tree_layout.setContentsMargins(Spacing.MD, Spacing.MD, Spacing.MD, Spacing.MD)
        taxonomy_tree_layout.setSpacing(Spacing.SM)

        taxonomy_header_layout = QHBoxLayout()
        taxonomy_header_layout.addWidget(QLabel("Math Taxonomy", taxonomy_tree_frame))
        taxonomy_header_layout.addStretch()
        taxonomy_header_layout.addWidget(QLabel("1,402 tags", taxonomy_tree_frame)) # Placeholder count
        taxonomy_tree_layout.addLayout(taxonomy_header_layout)

        taxonomy_tree_layout.addWidget(SecondaryButton("Collapse All", parent=taxonomy_tree_frame))
        taxonomy_tree_layout.addWidget(SecondaryButton("Filter...", parent=taxonomy_tree_frame))

        self.tag_tree_view = TagTreeView(taxonomy_tree_frame) # Reusing TagTreeView
        self.tag_tree_view.tag_selected.connect(self._on_tree_tag_selected)
        taxonomy_tree_layout.addWidget(self.tag_tree_view)
        main_layout.addWidget(taxonomy_tree_frame)

        # 2. Edit Tag & Tag Statistics (Right Panels)
        right_panel_layout = QVBoxLayout()
        right_panel_layout.setSpacing(Spacing.LG)

        # Edit Tag Form
        edit_tag_frame = QFrame(self)
        edit_tag_frame.setObjectName("edit_tag_frame")
        edit_tag_frame.setStyleSheet(f"""
            QFrame#edit_tag_frame {{
                background-color: {Color.WHITE};
                border: 1px solid {Color.BORDER_LIGHT};
                border-radius: {Dimensions.BORDER_RADIUS_LG};
                padding: {Spacing.LG}px;
            }}
        """)
        edit_tag_layout = QVBoxLayout(edit_tag_frame)
        edit_tag_layout.setContentsMargins(0,0,0,0)
        edit_tag_layout.setSpacing(Spacing.MD)

        edit_tag_header_layout = QHBoxLayout()
        edit_tag_header_layout.addWidget(QLabel("Edit Tag: Quadratics", edit_tag_frame))
        edit_tag_header_layout.addStretch()
        edit_tag_layout.addLayout(edit_tag_header_layout)

        # Basic Information
        edit_tag_layout.addWidget(QLabel("ℹ Basic Information", edit_tag_frame))
        basic_info_grid = QGridLayout()
        basic_info_grid.setSpacing(Spacing.SM)

        basic_info_grid.addWidget(QLabel("Name:", edit_tag_frame), 0, 0)
        self.tag_name_input = TextInput(parent=edit_tag_frame)
        basic_info_grid.addWidget(self.tag_name_input, 0, 1)

        basic_info_grid.addWidget(QLabel("Slug:", edit_tag_frame), 1, 0)
        self.tag_slug_input = TextInput(parent=edit_tag_frame)
        basic_info_grid.addWidget(self.tag_slug_input, 1, 1)

        basic_info_grid.addWidget(QLabel("Description:", edit_tag_frame), 2, 0)
        self.tag_description_input = TextInput(parent=edit_tag_frame) # Using TextInput for simplicity
        basic_info_grid.addWidget(self.tag_description_input, 2, 1)

        edit_tag_layout.addLayout(basic_info_grid)

        # Visual Identity
        edit_tag_layout.addWidget(QLabel("🎨 Visual Identity", edit_tag_frame))
        visual_identity_layout = QGridLayout()
        visual_identity_layout.setSpacing(Spacing.SM)

        visual_identity_layout.addWidget(QLabel("Color:", edit_tag_frame), 0, 0)
        # Placeholder for color picker
        color_picker_btn = SecondaryButton("○●○○○○○", parent=edit_tag_frame)
        visual_identity_layout.addWidget(color_picker_btn, 0, 1)

        visual_identity_layout.addWidget(QLabel("Icon:", edit_tag_frame), 1, 0)
        # Placeholder for icon picker
        icon_picker_btn = SecondaryButton("[Σ][📊][📐][%]", parent=edit_tag_frame)
        visual_identity_layout.addWidget(icon_picker_btn, 1, 1)

        edit_tag_layout.addLayout(visual_identity_layout)

        # Associated Exams (Placeholder)
        edit_tag_layout.addWidget(QLabel("Associated Exams", edit_tag_frame))
        associated_exams_table = QTableWidget(edit_tag_frame)
        associated_exams_table.setColumnCount(2)
        associated_exams_table.setHorizontalHeaderLabels(["Exam Name", "Count"])
        associated_exams_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        associated_exams_table.setRowCount(2)
        associated_exams_table.setItem(0,0, QTableWidgetItem("Calculus Midterm"))
        associated_exams_table.setItem(0,1, QTableWidgetItem("12"))
        associated_exams_table.setItem(1,0, QTableWidgetItem("Algebra Final"))
        associated_exams_table.setItem(1,1, QTableWidgetItem("8"))
        edit_tag_layout.addWidget(associated_exams_table)

        save_changes_btn = PrimaryButton("💾 Save Changes", parent=edit_tag_frame)
        save_changes_btn.clicked.connect(self._on_save_tag_clicked)
        edit_tag_layout.addWidget(save_changes_btn)

        right_panel_layout.addWidget(edit_tag_frame)

        # Tag Statistics & Quick Actions
        stats_actions_frame = QFrame(self)
        stats_actions_frame.setObjectName("stats_actions_frame")
        stats_actions_frame.setStyleSheet(f"""
            QFrame#stats_actions_frame {{
                background-color: {Color.WHITE};
                border: 1px solid {Color.BORDER_LIGHT};
                border-radius: {Dimensions.BORDER_RADIUS_LG};
                padding: {Spacing.LG}px;
            }}
        """)
        stats_actions_layout = QVBoxLayout(stats_actions_frame)
        stats_actions_layout.setContentsMargins(0,0,0,0)
        stats_actions_layout.setSpacing(Spacing.MD)

        stats_actions_layout.addWidget(QLabel("Tag Statistics", stats_actions_frame))
        stats_layout = QGridLayout()
        stats_layout.setSpacing(Spacing.SM)
        stats_layout.addWidget(QLabel("📊 Questions:", stats_actions_frame), 0, 0)
        stats_layout.addWidget(QLabel("12", stats_actions_frame), 0, 1) # Placeholder
        stats_layout.addWidget(QLabel("✅ Avg Success:", stats_actions_frame), 1, 0)
        stats_layout.addWidget(QLabel("68%", stats_actions_frame), 1, 1) # Placeholder
        stats_layout.addWidget(QLabel("📈 Difficulty:", stats_actions_frame), 2, 0)
        stats_layout.addWidget(QLabel("Medium", stats_actions_frame), 2, 1) # Placeholder
        stats_actions_layout.addLayout(stats_layout)

        stats_actions_layout.addWidget(QLabel("Quick Actions", stats_actions_frame))
        quick_actions_layout = QVBoxLayout()
        merge_btn = SecondaryButton("Merge with...", parent=stats_actions_frame)
        merge_btn.clicked.connect(lambda: self.merge_tag_requested.emit(self.current_tag_uuid, "another_uuid")) # Placeholder
        quick_actions_layout.addWidget(merge_btn)
        delete_btn = SecondaryButton("Delete Tag", parent=stats_actions_frame)
        delete_btn.clicked.connect(lambda: self.delete_tag_requested.emit(self.current_tag_uuid)) # Placeholder
        quick_actions_layout.addWidget(delete_btn)
        stats_actions_layout.addLayout(quick_actions_layout)

        stats_actions_layout.addStretch() # Push content to top
        right_panel_layout.addWidget(stats_actions_frame)
        main_layout.addLayout(right_panel_layout, 3) # Give more horizontal space


        self.current_tag_uuid = None # Store currently selected tag UUID

    def _on_tree_tag_selected(self, tag_uuid: str, is_checked: bool):
        # We only care about selection here, not checkbox state change for editing
        # The `TagTreeView` emits `tag_selected` with checkbox state, but here we ignore `is_checked`
        self.current_tag_uuid = tag_uuid
        print(f"Tag selected for editing: {tag_uuid}")
        # In a real application, fetch tag details and populate the form
        self._populate_edit_form_with_tag_data(tag_uuid)

    def _populate_edit_form_with_tag_data(self, tag_uuid: str):
        # Dummy data for populating the form
        if tag_uuid == "uuid-algebra":
            self.tag_name_input.setText("Algebra")
            self.tag_slug_input.setText("algebra")
            self.tag_description_input.setText("Concepts related to algebra.")
        elif tag_uuid == "uuid-geometry":
            self.tag_name_input.setText("Geometry")
            self.tag_slug_input.setText("geometry")
            self.tag_description_input.setText("Geometric shapes and properties.")
        else:
            self.tag_name_input.setText(f"Selected Tag: {tag_uuid}")
            self.tag_slug_input.setText("")
            self.tag_description_input.setText("")

    def _on_save_tag_clicked(self):
        if self.current_tag_uuid:
            tag_data = {
                "uuid": self.current_tag_uuid,
                "name": self.tag_name_input.text(),
                "slug": self.tag_slug_input.text(),
                "description": self.tag_description_input.text(),
                # Add color, icon etc.
            }
            self.save_tag_requested.emit(tag_data)
            print(f"Saving tag: {tag_data}")


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
            self.setWindowTitle("Taxonomy Page Test")
            self.setGeometry(100, 100, 1200, 900)

            self.taxonomy_page = TaxonomyPage(self)
            self.setCentralWidget(self.taxonomy_page)

            self.taxonomy_page.tag_selected.connect(lambda uuid: print(f"Tag selected for edit: {uuid}"))
            self.taxonomy_page.save_tag_requested.connect(lambda data: print(f"Save tag requested: {data}"))
            self.taxonomy_page.delete_tag_requested.connect(lambda uuid: print(f"Delete tag requested: {uuid}"))
            self.taxonomy_page.merge_tag_requested.connect(lambda src, target: print(f"Merge tag {src} into {target} requested"))

            # Example of dynamic tag data for TagTreeView in sidebar
            sample_tags_data = [
                {'name': 'Algebra', 'uuid': 'uuid-algebra', 'selectable': True, 'children': [
                    {'name': 'Functions', 'uuid': 'uuid-functions'},
                    {'name': 'Equations', 'uuid': 'uuid-equations'}
                ]},
                {'name': 'Calculus', 'uuid': 'uuid-calculus', 'selectable': True, 'children': [
                    {'name': 'Differential', 'uuid': 'uuid-differential'},
                    {'name': 'Integral', 'uuid': 'uuid-integral'}
                ]},
                {'name': 'Geometry', 'uuid': 'uuid-geometry', 'selectable': True, 'children': [
                    {'name': 'Euclidean', 'uuid': 'uuid-euclidean'}
                ]}
            ]
            self.taxonomy_page.tag_tree_view.set_tags(sample_tags_data)

    window = TestMainWindow()
    window.show()
    sys.exit(app.exec())