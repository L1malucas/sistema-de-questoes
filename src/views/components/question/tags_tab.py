# src/views/components/question/tags_tab.py
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame,
    QScrollArea, QSizePolicy
)
from PyQt6.QtCore import Qt, pyqtSignal
from src.views.design.constants import Color, Spacing, Typography, Dimensions
from src.views.components.common.inputs import SearchInput
from src.views.components.common.badges import RemovableBadge, Badge
from src.views.components.layout.sidebar import TagTreeView # Reusing TagTreeView

class TagsTab(QWidget):
    """
    Tab for managing tags associated with a question.
    Allows searching, selecting from a taxonomy tree, and displaying selected tags.
    """
    tags_changed = pyqtSignal(list) # Emits a list of selected tag UUIDs

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("tags_tab")
        self.selected_tag_uuids = [] # List to store UUIDs of selected tags

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(Spacing.LG, Spacing.LG, Spacing.LG, Spacing.LG)
        main_layout.setSpacing(Spacing.LG)

        # 1. Selected Tags (Chips removíveis)
        selected_tags_frame = QFrame(self)
        selected_tags_frame.setObjectName("selected_tags_frame")
        selected_tags_frame.setStyleSheet(f"QFrame#selected_tags_frame {{ border: 1px solid {Color.BORDER_LIGHT}; border-radius: {Dimensions.BORDER_RADIUS_MD}; padding: {Spacing.MD}px; background-color: {Color.LIGHT_BACKGROUND}; }}")
        selected_tags_layout = QVBoxLayout(selected_tags_frame)
        selected_tags_layout.setContentsMargins(Spacing.SM, Spacing.SM, Spacing.SM, Spacing.SM)
        selected_tags_layout.setSpacing(Spacing.SM)

        selected_tags_label = QLabel("Tags Selecionadas:", selected_tags_frame)
        selected_tags_label.setStyleSheet(f"font-weight: {Typography.FONT_WEIGHT_SEMIBOLD}; color: {Color.DARK_TEXT};")
        selected_tags_layout.addWidget(selected_tags_label)

        self.selected_tags_flow_layout = QHBoxLayout() # For flowing removable badges
        self.selected_tags_flow_layout.setContentsMargins(0,0,0,0)
        self.selected_tags_flow_layout.setSpacing(Spacing.SM)
        self.selected_tags_flow_layout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        selected_tags_layout.addLayout(self.selected_tags_flow_layout)

        selected_tags_layout.addStretch() # Push tags to the top left
        main_layout.addWidget(selected_tags_frame)


        # 2. Tag Search
        tag_search_frame = QFrame(self)
        tag_search_frame.setObjectName("tag_search_frame")
        tag_search_frame.setStyleSheet(f"QFrame#tag_search_frame {{ border: 1px solid {Color.BORDER_LIGHT}; border-radius: {Dimensions.BORDER_RADIUS_MD}; padding: {Spacing.MD}px; }}")
        tag_search_layout = QVBoxLayout(tag_search_frame)
        tag_search_layout.setContentsMargins(Spacing.SM, Spacing.SM, Spacing.SM, Spacing.SM)
        tag_search_layout.setSpacing(Spacing.SM)

        tag_search_label = QLabel("Buscar Tags:", tag_search_frame)
        tag_search_label.setStyleSheet(f"font-weight: {Typography.FONT_WEIGHT_SEMIBOLD}; color: {Color.DARK_TEXT};")
        tag_search_layout.addWidget(tag_search_label)

        self.tag_search_input = SearchInput(placeholder_text="Pesquisar tags...", parent=tag_search_frame)
        self.tag_search_input.textChanged.connect(self._on_tag_search_changed)
        tag_search_layout.addWidget(self.tag_search_input)
        main_layout.addWidget(tag_search_frame)


        # 3. Tags and Taxonomy Tree
        taxonomy_frame = QFrame(self)
        taxonomy_frame.setObjectName("taxonomy_frame")
        taxonomy_frame.setStyleSheet(f"QFrame#taxonomy_frame {{ border: 1px solid {Color.BORDER_LIGHT}; border-radius: {Dimensions.BORDER_RADIUS_MD}; padding: {Spacing.MD}px; }}")
        taxonomy_layout = QHBoxLayout(taxonomy_frame)
        taxonomy_layout.setContentsMargins(Spacing.SM, Spacing.SM, Spacing.SM, Spacing.SM)
        taxonomy_layout.setSpacing(Spacing.LG)

        # Most Used Tags (Sidebar-like)
        most_used_frame = QFrame(taxonomy_frame)
        most_used_layout = QVBoxLayout(most_used_frame)
        most_used_layout.setContentsMargins(0,0,0,0)
        most_used_layout.setSpacing(Spacing.SM)

        most_used_label = QLabel("Tags Mais Usadas:", most_used_frame)
        most_used_label.setStyleSheet(f"font-weight: {Typography.FONT_WEIGHT_SEMIBOLD}; color: {Color.DARK_TEXT};")
        most_used_layout.addWidget(most_used_label)

        self.most_used_tags_layout = QVBoxLayout()
        self.most_used_tags_layout.setContentsMargins(0,0,0,0)
        self.most_used_tags_layout.setSpacing(Spacing.XS)
        self._add_most_used_tags_placeholders() # Add some dummy tags
        most_used_layout.addLayout(self.most_used_tags_layout)
        most_used_layout.addStretch() # Push most used tags to top

        taxonomy_layout.addWidget(most_used_frame, 1)

        # Taxonomy Tree
        self.tag_tree_view = TagTreeView(taxonomy_frame)
        self.tag_tree_view.tag_selected.connect(self._on_tag_selected_from_tree)
        taxonomy_layout.addWidget(self.tag_tree_view, 2)

        main_layout.addWidget(taxonomy_frame, 1) # Occupy remaining space

        self.setLayout(main_layout)

    def _add_most_used_tags_placeholders(self):
        # Dummy data for most used tags
        tags_data = [
            ("Algebra", Color.TAG_BLUE),
            ("Calculus", Color.TAG_GREEN),
            ("Geometry", Color.TAG_PURPLE),
            ("ENEM", Color.TAG_ORANGE),
        ]
        for tag_text, tag_color in tags_data:
            tag_widget = Badge(tag_text, tag_color, Color.WHITE)
            self.most_used_tags_layout.addWidget(tag_widget)


    def _on_tag_search_changed(self, text: str):
        # In a real application, this would filter the TagTreeView
        print(f"Tag search: {text}")

    def _on_tag_selected_from_tree(self, tag_uuid: str, is_checked: bool):
        if is_checked and tag_uuid not in self.selected_tag_uuids:
            self.selected_tag_uuids.append(tag_uuid)
            self._add_removable_badge(tag_uuid)
        elif not is_checked and tag_uuid in self.selected_tag_uuids:
            self.selected_tag_uuids.remove(tag_uuid)
            self._remove_removable_badge(tag_uuid)
        self.tags_changed.emit(self.selected_tag_uuids)

    def _add_removable_badge(self, tag_uuid: str):
        # For demonstration, map UUID back to a name and assign a color
        # In a real app, you'd fetch tag details from a service
        name_map = {
            "uuid-algebra": "Algebra", "uuid-functions": "Functions",
            "uuid-linear": "Linear", "uuid-quadratic": "Quadratic",
            "uuid-equations": "Equations", "uuid-polynomial": "Polynomial",
            "uuid-trigonometric": "Trigonometric", "uuid-geometry": "Geometry",
            "uuid-euclidean": "Euclidean", "uuid-triangles": "Triangles",
            "uuid-calculus": "Calculus", "uuid-differential": "Differential",
            "uuid-integral": "Integral",
        }
        color_map = {
            "Algebra": Color.TAG_BLUE, "Calculus": Color.TAG_GREEN,
            "Geometry": Color.TAG_PURPLE, "Functions": Color.TAG_YELLOW,
            "Equations": Color.TAG_RED, "Linear": Color.TAG_ORANGE,
            "Quadratic": Color.TAG_GRAY, "Euclidean": Color.TAG_BLUE,
            "Triangles": Color.TAG_GREEN, "Differential": Color.TAG_RED,
            "Integral": Color.TAG_PURPLE, "Polynomial": Color.TAG_ORANGE,
            "Trigonometric": Color.TAG_YELLOW,
        }
        tag_name = name_map.get(tag_uuid, f"Tag-{tag_uuid[:4]}")
        tag_color = color_map.get(tag_name, Color.TAG_GRAY)

        badge = RemovableBadge(tag_name, color=tag_color, text_color=Color.WHITE, parent=self)
        badge.tag_uuid = tag_uuid # Store UUID for removal
        badge.removed.connect(self._on_removable_badge_removed)
        self.selected_tags_flow_layout.addWidget(badge)

    def _remove_removable_badge(self, tag_uuid: str):
        for i in range(self.selected_tags_flow_layout.count()):
            widget = self.selected_tags_flow_layout.itemAt(i).widget()
            if hasattr(widget, 'tag_uuid') and widget.tag_uuid == tag_uuid:
                widget.setParent(None) # Remove from layout
                widget.deleteLater()
                break

    def _on_removable_badge_removed(self, tag_name: str):
        # Find UUID by tag_name (simplified for demo, in real app use UUID)
        # Assuming unique names for now.
        name_map_reverse = {
            "Algebra": "uuid-algebra", "Functions": "uuid-functions",
            "Linear": "uuid-linear", "Quadratic": "uuid-quadratic",
            "Equations": "uuid-equations", "Polynomial": "uuid-polynomial",
            "Trigonometric": "uuid-trigonometric", "Geometry": "uuid-geometry",
            "Euclidean": "uuid-euclidean", "Triangles": "uuid-triangles",
            "Calculus": "uuid-calculus", "Differential": "uuid-differential",
            "Integral": "uuid-integral",
        }
        tag_uuid = name_map_reverse.get(tag_name)
        if tag_uuid and tag_uuid in self.selected_tag_uuids:
            self.selected_tag_uuids.remove(tag_uuid)
            self.tags_changed.emit(self.selected_tag_uuids)

        # Uncheck item in tree view
        # This requires traversing the tree to find the item
        # Simplified: for demo, assume treeview items are directly manageable
        root = self.tag_tree_view.invisibleRootItem()
        self._uncheck_tree_item(root, tag_uuid)


    def _uncheck_tree_item(self, parent_item, tag_uuid):
        for i in range(parent_item.childCount()):
            child = parent_item.child(i)
            if hasattr(child, 'uuid') and child.uuid == tag_uuid:
                child.setCheckState(0, Qt.CheckState.Unchecked)
                return
            self._uncheck_tree_item(child, tag_uuid)


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
            self.setWindowTitle("Tags Tab Test")
            self.setGeometry(100, 100, 800, 900)

            self.tags_tab = TagsTab(self)
            self.setCentralWidget(self.tags_tab)

            self.tags_tab.tags_changed.connect(lambda tags: print(f"Selected Tags UUIDs: {tags}"))

    window = TestMainWindow()
    window.show()
    sys.exit(app.exec())
