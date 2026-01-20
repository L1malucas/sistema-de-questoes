# src/views/components/layout/sidebar.py
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame,
    QTreeWidget, QTreeWidgetItem, QApplication,
    QSpacerItem, QSizePolicy
)
from PyQt6.QtCore import Qt, QSize, pyqtSignal
from PyQt6.QtGui import QIcon
from src.views.design.constants import Color, Spacing, Typography, Dimensions
from src.views.design.enums import ActionEnum
from src.views.components.common.buttons import IconButton, PrimaryButton, SecondaryButton # Reusing buttons

class TagTreeItem(QTreeWidgetItem):
    """
    Custom tree widget item for a tag, supporting expansion and an optional checkbox.
    """
    def __init__(self, parent, name, uuid, level=0, selectable=True, is_checked=False):
        super().__init__(parent, [name])
        self.uuid = uuid
        self.name = name
        self.level = level
        self.selectable = selectable

        if selectable:
            self.setFlags(self.flags() | Qt.ItemFlag.ItemIsUserCheckable | Qt.ItemFlag.ItemIsSelectable)
            self.setCheckState(0, Qt.CheckState.Checked if is_checked else Qt.CheckState.Unchecked)
        else:
            self.setFlags(self.flags() | Qt.ItemFlag.ItemIsSelectable) # Can still select the item, but no checkbox

        # Set font based on level
        font = self.font(0)
        if level == 0:
            font.setPointSize(font.pointSize() + 2) # Larger for top-level
            font.setBold(True)
        elif level == 1:
            font.setBold(True)
        self.setFont(0, font)

        # Apply styles via objectName if possible, or directly for padding/indentation
        # self.treeWidget().setStyleSheet(f"""
        #     QTreeWidget::item {{
        #         padding-left: {level * Spacing.MD}px;
        #     }}
        # """) # This applies to all items. Better to handle through custom delegate or tree config


class TagTreeView(QTreeWidget):
    """
    Hierarchical tree view for tags.
    """
    tag_selected = pyqtSignal(str, bool) # Emits (tag_uuid, is_checked)
    item_expanded = pyqtSignal(str) # Emits (tag_uuid)
    item_collapsed = pyqtSignal(str) # Emits (tag_uuid)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("tag_tree_view")
        self.setHeaderHidden(True)
        self.setRootIsDecorated(False) # Hide root handles
        self.setIndentation(Spacing.LG)
        self.setAnimated(True) # Smooth expansion/collapse

        self.itemChanged.connect(self._on_item_changed)
        self.itemClicked.connect(self._on_item_clicked)
        self.itemExpanded.connect(lambda item: self.item_expanded.emit(item.uuid))
        self.itemCollapsed.connect(lambda item: self.item_collapsed.emit(item.uuid))

        # Placeholder data - replace with actual data fetching logic
        self._load_placeholder_tags()

        self.setStyleSheet(f"""
            QTreeWidget#tag_tree_view {{
                background-color: transparent;
                border: none;
                font-size: {Typography.FONT_SIZE_MD};
                color: {Color.DARK_TEXT};
                show-decoration-selected: 1; /* Make selection visible */
            }}
            QTreeWidget#tag_tree_view::item {{
                padding: {Spacing.XS}px 0;
                margin: {Spacing.XXS}px 0;
                border-radius: {Dimensions.BORDER_RADIUS_SM};
            }}
            QTreeWidget#tag_tree_view::item:selected {{
                background-color: {Color.LIGHT_BLUE_BG_2};
                color: {Color.PRIMARY_BLUE};
            }}
            QTreeWidget#tag_tree_view::item:hover {{
                background-color: {Color.BORDER_LIGHT};
            }}
            QTreeWidget#tag_tree_view::branch {{
                background: transparent;
            }}
            QTreeWidget#tag_tree_view::branch:open {{
                image: url(resources/icons/arrow_down.png); /* Placeholder */
            }}
            QTreeWidget#tag_tree_view::branch:closed,
            QTreeWidget#tag_tree_view::branch:has-children:!open {{
                image: url(resources/icons/arrow_right.png); /* Placeholder */
            }}
        """)

    def _load_placeholder_tags(self):
        # Example hierarchical data
        algebra = TagTreeItem(self, "1. Algebra", "uuid-algebra", level=0, selectable=True, is_checked=True)
        functions = TagTreeItem(algebra, "1.1 Functions", "uuid-functions", level=1, selectable=True)
        TagTreeItem(functions, "1.1.1 Linear", "uuid-linear", level=2, selectable=True)
        TagTreeItem(functions, "1.1.1 Quadratic", "uuid-quadratic", level=2, selectable=True)
        equations = TagTreeItem(algebra, "1.2 Equations", "uuid-equations", level=1, selectable=True)
        TagTreeItem(equations, "1.2.1 Polynomial", "uuid-polynomial", level=2, selectable=True)
        TagTreeItem(equations, "1.2.2 Trigonometric", "uuid-trigonometric", level=2, selectable=True)

        geometry = TagTreeItem(self, "2. Geometry", "uuid-geometry", level=0, selectable=True)
        euclidean = TagTreeItem(geometry, "2.1 Euclidean", "uuid-euclidean", level=1, selectable=True)
        TagTreeItem(euclidean, "2.1.1 Triangles", "uuid-triangles", level=2, selectable=True)

        calculus = TagTreeItem(self, "3. Calculus", "uuid-calculus", level=0, selectable=True)
        differential = TagTreeItem(calculus, "3.1 Differential", "uuid-differential", level=1, selectable=True)
        integral = TagTreeItem(calculus, "3.2 Integral", "uuid-integral", level=1, selectable=True)

        self.expandItem(algebra) # Expand Algebra by default

    def _on_item_changed(self, item: TagTreeItem, column: int):
        if item.selectable and column == 0:
            is_checked = item.checkState(column) == Qt.CheckState.Checked
            self.tag_selected.emit(item.uuid, is_checked)

    def _on_item_clicked(self, item: TagTreeItem, column: int):
        if not item.selectable: # If not selectable, toggle expansion
            if item.isExpanded():
                self.collapseItem(item)
            else:
                self.expandItem(item)
        # If selectable, itemChanged handles the checkbox click.
        # This click handler can be used for other actions like opening a tag edit view.


class Sidebar(QFrame):
    """
    Main sidebar component for navigation and filtering.
    """
    export_clicked = pyqtSignal()
    help_clicked = pyqtSignal()
    tag_filter_changed = pyqtSignal(str, bool) # Emits (tag_uuid, is_checked)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("sidebar")
        self.setFixedWidth(Dimensions.SIDEBAR_WIDTH)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(Spacing.LG, Spacing.LG, Spacing.LG, Spacing.LG)
        main_layout.setSpacing(Spacing.LG)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Header
        header_layout = QHBoxLayout()
        header_title = QLabel("MATH CONTENT", self)
        header_title.setObjectName("sidebar_title")
        header_title.setStyleSheet(f"""
            QLabel#sidebar_title {{
                font-size: {Typography.FONT_SIZE_SM};
                font-weight: {Typography.FONT_WEIGHT_BOLD};
                color: {Color.DARK_TEXT};
                letter-spacing: 1px;
            }}
        """)
        header_layout.addWidget(header_title)
        header_layout.addStretch()
        # Expand/Collapse button (placeholder icon)
        expand_button = IconButton(icon_path="images/icons/collapse.png", size=QSize(16,16), parent=self)
        expand_button.setToolTip("Expand/Collapse Sidebar")
        header_layout.addWidget(expand_button)
        main_layout.addLayout(header_layout)

        # Hierarchical Tags
        tags_subtitle = QLabel("Hierarchical Tags", self)
        tags_subtitle.setObjectName("sidebar_subtitle")
        tags_subtitle.setStyleSheet(f"""
            QLabel#sidebar_subtitle {{
                font-size: {Typography.FONT_SIZE_XS};
                color: {Color.GRAY_TEXT};
            }}
        """)
        main_layout.addWidget(tags_subtitle)

        self.tag_tree_view = TagTreeView(self)
        self.tag_tree_view.tag_selected.connect(self.tag_filter_changed.emit)
        main_layout.addWidget(self.tag_tree_view)

        # Footer Actions
        footer_frame = QFrame(self)
        footer_frame.setObjectName("sidebar_footer")
        footer_frame.setStyleSheet(f"""
            QFrame#sidebar_footer {{
                border-top: 1px solid {Color.BORDER_LIGHT};
                padding-top: {Spacing.MD}px;
            }}
        """)
        footer_layout = QVBoxLayout(footer_frame)
        footer_layout.setContentsMargins(0, Spacing.MD, 0, 0)
        footer_layout.setSpacing(Spacing.SM)
        footer_layout.setAlignment(Qt.AlignmentFlag.AlignBottom)

        export_button = PrimaryButton("Export to PDF", icon="images/icons/pdf.png", parent=self) # Placeholder icon
        export_button.setObjectName("export_button") # Use existing style from mathbank_styles.css
        export_button.clicked.connect(self.export_clicked.emit)
        footer_layout.addWidget(export_button)

        help_button = SecondaryButton("Help Center", icon="images/icons/help.png", parent=self) # Placeholder icon
        help_button.clicked.connect(self.help_clicked.emit)
        footer_layout.addWidget(help_button)

        footer_frame.setLayout(footer_layout)
        main_layout.addWidget(footer_frame)
        main_layout.addStretch() # Push footer to bottom

        self.setLayout(main_layout)

    def set_tags(self, tags_data: list):
        """
        Sets the data for the tag tree view.
        `tags_data` should be a list of dictionaries representing hierarchical tags.
        """
        self.tag_tree_view.clear()
        self._add_tags_to_tree(self.tag_tree_view, tags_data)

    def _add_tags_to_tree(self, parent_item, tags_data, level=0):
        for tag in tags_data:
            item = TagTreeItem(parent_item, tag['name'], tag['uuid'], level, selectable=tag.get('selectable', True), is_checked=tag.get('is_checked', False))
            if 'children' in tag and tag['children']:
                self._add_tags_to_tree(item, tag['children'], level + 1)


if __name__ == '__main__':
    import sys
    from PyQt6.QtWidgets import QMainWindow

    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    from src.views.design.theme import ThemeManager
    ThemeManager.apply_global_theme(app)

    class TestMainWindow(QMainWindow):
        def __init__(self):
            super().__init__()
            self.setWindowTitle("Sidebar Test")
            self.setGeometry(100, 100, 400, 800)

            self.sidebar = Sidebar(self)
            self.setCentralWidget(self.sidebar)

            self.sidebar.export_clicked.connect(lambda: print("Export button clicked!"))
            self.sidebar.help_clicked.connect(lambda: print("Help button clicked!"))
            self.sidebar.tag_filter_changed.connect(lambda uuid, checked: print(f"Tag filter changed: {uuid}, Checked: {checked}"))

            # Example of dynamic tag data
            sample_tags_data = [
                {'name': 'Science', 'uuid': 'sci-uuid', 'selectable': False, 'children': [
                    {'name': 'Physics', 'uuid': 'phy-uuid', 'is_checked': True, 'children': [
                        {'name': 'Mechanics', 'uuid': 'mech-uuid'},
                        {'name': 'Thermodynamics', 'uuid': 'thermo-uuid'}
                    ]},
                    {'name': 'Chemistry', 'uuid': 'chem-uuid'}
                ]},
                {'name': 'History', 'uuid': 'hist-uuid', 'is_checked': False, 'children': []}
            ]
            self.sidebar.set_tags(sample_tags_data)

    window = TestMainWindow()
    window.show()
    sys.exit(app.exec())