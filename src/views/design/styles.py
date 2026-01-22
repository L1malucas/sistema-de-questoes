# src/views/design/styles.py
from src.views.design.constants import Color, Typography, Spacing, Dimensions

class StyleSheet:
    @staticmethod
    def get_global_stylesheet():
        return f"""
        * {{
            font-family: "{Typography.FONT_FAMILY}";
        }}

        QMainWindow {{
            background-color: {Color.LIGHT_BACKGROUND};
        }}

        /* Add more global styles here */
        """

    @staticmethod
    def get_navbar_stylesheet():
        return f"""
        #header {{
            background-color: {Color.WHITE};
            border-bottom: 1px solid {Color.BORDER_LIGHT};
            min-height: {Dimensions.NAVBAR_HEIGHT}px;
        }}

        #logo {{
            background-color: {Color.PRIMARY_BLUE};
            color: {Color.WHITE};
            font-size: {Typography.FONT_SIZE_XL};
            font-weight: {Typography.FONT_WEIGHT_BOLD};
            border-radius: {Dimensions.BORDER_RADIUS_SM};
            padding: {Spacing.XS}px {Spacing.SM}px;
        }}

        #title {{
            font-size: {Typography.FONT_SIZE_XXL};
            font-weight: {Typography.FONT_WEIGHT_BOLD};
            color: {Color.DARK_TEXT};
        }}

        #nav_active {{
            color: {Color.PRIMARY_BLUE};
            font-size: {Typography.FONT_SIZE_MD};
            font-weight: {Typography.FONT_WEIGHT_SEMIBOLD};
            border: none;
            border-bottom: 2px solid {Color.PRIMARY_BLUE};
            background: transparent;
            padding: {Spacing.XS}px {Spacing.NONE}px;
        }}

        #nav_link {{
            color: {Color.GRAY_TEXT};
            font-size: {Typography.FONT_SIZE_MD};
            font-weight: {Typography.FONT_WEIGHT_MEDIUM};
            border: none;
            background: transparent;
            padding: {Spacing.XS}px {Spacing.NONE}px;
        }}

        #nav_link:hover {{
            color: {Color.PRIMARY_BLUE};
        }}

        #create_button {{
            background-color: {Color.PRIMARY_BLUE};
            color: {Color.WHITE};
            font-size: {Typography.FONT_SIZE_MD};
            font-weight: {Typography.FONT_WEIGHT_BOLD};
            border: none;
            border-radius: {Dimensions.BORDER_RADIUS_MD};
            padding: {Spacing.SM}px {Spacing.LG}px;
            min-height: 40px; /* Specific from CSS */
        }}

        #create_button:hover {{
            background-color: {Color.HOVER_BLUE};
        }}

        #avatar {{
            border-radius: {Dimensions.BORDER_RADIUS_CIRCLE};
            border: 1px solid {Color.BORDER_MEDIUM};
            background-color: {Color.BORDER_MEDIUM};
        }}
        """

    @staticmethod
    def get_sidebar_stylesheet():
        return f"""
        #sidebar {{
            background-color: {Color.WHITE};
            border-right: 1px solid {Color.BORDER_LIGHT};
            min-width: {Dimensions.SIDEBAR_WIDTH}px;
            max-width: {Dimensions.SIDEBAR_WIDTH}px;
        }}

        #sidebar_title {{
            font-size: {Typography.FONT_SIZE_SM};
            font-weight: {Typography.FONT_WEIGHT_BOLD};
            color: {Color.DARK_TEXT};
            letter-spacing: 1px;
        }}

        #sidebar_subtitle {{
            font-size: {Typography.FONT_SIZE_XS};
            color: {Color.GRAY_TEXT};
        }}

        #sidebar_icon {{
            color: {Color.GRAY_TEXT};
            font-size: {Typography.FONT_SIZE_XL};
        }}

        #tree_item_active {{
            background-color: {Color.LIGHT_BLUE_BG_1};
            border-radius: {Dimensions.BORDER_RADIUS_MD};
        }}

        #tree_item_text {{
            font-size: {Typography.FONT_SIZE_MD};
            font-weight: {Typography.FONT_WEIGHT_SEMIBOLD};
            color: {Color.PRIMARY_BLUE};
        }}

        #tree_item {{
            background-color: transparent;
            border-radius: {Dimensions.BORDER_RADIUS_MD};
        }}

        #tree_item:hover {{
            background-color: {Color.LIGHT_GRAY_BACKGROUND};
        }}

        #tree_item_text_inactive {{
            font-size: {Typography.FONT_SIZE_MD};
            font-weight: {Typography.FONT_WEIGHT_MEDIUM};
            color: {Color.DARK_TEXT};
        }}

        #tree_subitem_active {{
            background-color: {Color.LIGHT_BLUE_BG_2};
            border-radius: {Dimensions.BORDER_RADIUS_MD};
            border-left: 2px solid {Color.LIGHT_BLUE_BORDER};
        }}

        #tree_subitem_text {{
            font-size: {Typography.FONT_SIZE_SM};
            font-weight: {Typography.FONT_WEIGHT_MEDIUM};
            color: {Color.PRIMARY_BLUE};
        }}

        #tree_subitem {{
            background-color: transparent;
            border-radius: {Dimensions.BORDER_RADIUS_MD};
        }}

        #tree_subitem:hover {{
            background-color: {Color.LIGHT_GRAY_BACKGROUND};
        }}

        #tree_subitem_text_inactive {{
            font-size: {Typography.FONT_SIZE_SM};
            font-weight: {Typography.FONT_WEIGHT_MEDIUM};
            color: {Color.GRAY_TEXT};
        }}

        #export_button {{
            background-color: {Color.WHITE};
            color: {Color.PRIMARY_BLUE};
            border: 2px solid {Color.PRIMARY_BLUE};
            border-radius: {Dimensions.BORDER_RADIUS_MD};
            font-size: {Typography.FONT_SIZE_MD};
            font-weight: {Typography.FONT_WEIGHT_BOLD};
            padding: {Spacing.SM}px;
        }}

        #export_button:hover {{
            background-color: {Color.LIGHT_BLUE_BG_2};
        }}
        """

    @staticmethod
    def get_main_content_stylesheet():
        return f"""
        #main_scroll {{
            background-color: {Color.LIGHT_BACKGROUND};
            border: none;
        }}

        #main_content {{
            background-color: {Color.LIGHT_BACKGROUND};
        }}

        #page_title {{
            font-size: {Typography.FONT_SIZE_PAGE_TITLE};
            font-weight: {Typography.FONT_WEIGHT_BOLD};
            color: {Color.DARK_TEXT};
        }}

        #results_count {{
            font-size: {Typography.FONT_SIZE_MD};
            color: {Color.GRAY_TEXT};
        }}
        """

    @staticmethod
    def get_filter_bar_stylesheet():
        return f"""
        #filters {{
            background-color: {Color.WHITE};
            border: 1px solid {Color.BORDER_LIGHT};
            border-radius: {Dimensions.BORDER_RADIUS_LG};
        }}

        #search_bar {{
            background-color: {Color.BORDER_LIGHT};
            border: none;
            border-radius: {Dimensions.BORDER_RADIUS_MD};
            padding: {Spacing.SM}px {Spacing.SM}px {Spacing.SM}px {Spacing.XL}px; /* Adjust padding for icon */
            font-size: {Typography.FONT_SIZE_MD};
            color: {Color.DARK_TEXT};
        }}

        #search_bar::placeholder {{
            color: {Color.GRAY_TEXT};
        }}

        #filter_button {{
            background-color: {Color.BORDER_LIGHT};
            border: none;
            border-radius: {Dimensions.BORDER_RADIUS_MD};
            padding: {Spacing.SM}px {Spacing.LG}px;
            font-size: {Typography.FONT_SIZE_MD};
            font-weight: {Typography.FONT_WEIGHT_MEDIUM};
            color: {Color.DARK_TEXT};
            min-height: 40px;
        }}

        #filter_button:hover {{
            background-color: {Color.BORDER_MEDIUM};
        }}

        #filter_button_active {{
            background-color: {Color.LIGHT_BLUE_BG_1};
            border: 1px solid {Color.LIGHT_BLUE_BORDER};
            border-radius: {Dimensions.BORDER_RADIUS_MD};
            padding: {Spacing.SM}px {Spacing.LG}px;
            font-size: {Typography.FONT_SIZE_MD};
            font-weight: {Typography.FONT_WEIGHT_MEDIUM};
            color: {Color.PRIMARY_BLUE};
            min-height: 40px;
        }}

        #filter_button_dark {{
            background-color: {Color.DARK_TEXT};
            border: none;
            border-radius: {Dimensions.BORDER_RADIUS_MD};
            padding: {Spacing.SM}px {Spacing.LG}px;
            font-size: {Typography.FONT_SIZE_MD};
            font-weight: {Typography.FONT_WEIGHT_MEDIUM};
            color: {Color.WHITE};
            min-height: 40px;
        }}

        #filter_button_dark:hover {{
            background-color: {Color.BLACK};
        }}
        """

    @staticmethod
    def get_question_card_stylesheet():
        return f"""
        #question_card {{
            background-color: {Color.WHITE};
            border: 1px solid {Color.BORDER_LIGHT};
            border-radius: {Dimensions.BORDER_RADIUS_LG};
        }}

        /* Shadow is now handled via QGraphicsDropShadowEffect in Python code */

        #card_id {{
            color: {Color.PRIMARY_BLUE};
            font-size: {Typography.FONT_SIZE_MD};
            font-weight: {Typography.FONT_WEIGHT_BOLD};
            letter-spacing: 0.5px;
        }}

        #card_type, #card_menu {{
            color: {Color.GRAY_TEXT};
            font-size: {Typography.FONT_SIZE_LG};
        }}

        #card_title {{
            font-size: {Typography.FONT_SIZE_LG};
            font-weight: {Typography.FONT_WEIGHT_SEMIBOLD};
            color: {Color.DARK_TEXT};
        }}

        #formula_box {{
            background-color: {Color.LIGHT_GRAY_BACKGROUND};
            border: 1px dashed {Color.BORDER_MEDIUM};
            border-radius: {Dimensions.BORDER_RADIUS_MD};
            padding: {Spacing.LG}px;
        }}

        #formula_text {{
            font-family: "Times New Roman", serif;
            font-style: italic;
            font-size: {Typography.FONT_SIZE_LG};
            color: {Color.DARK_TEXT};
        }}
        """

    @staticmethod
    def get_tag_stylesheet(tag_color_name):
        color_map = {
            "blue": (Color.TAG_BLUE, "rgba(59, 130, 246, 0.1)"),
            "green": (Color.TAG_GREEN, "rgba(34, 197, 94, 0.1)"),
            "red": (Color.TAG_RED, "rgba(239, 68, 68, 0.1)"),
            "yellow": (Color.TAG_YELLOW, "rgba(234, 179, 8, 0.1)"),
            "purple": (Color.TAG_PURPLE, "rgba(168, 85, 247, 0.1)"),
            "orange": (Color.TAG_ORANGE, "rgba(249, 115, 22, 0.1)"),
            "gray": (Color.TAG_GRAY, "#f1f5f9"),
        }
        text_color, bg_color = color_map.get(tag_color_name.lower(), (Color.TAG_GRAY, "#f1f5f9")) # Default to gray

        return f"""
        .tag-{tag_color_name.lower()} {{
            background-color: {bg_color};
            color: {text_color};
            font-size: {Typography.FONT_SIZE_XS};
            font-weight: {Typography.FONT_WEIGHT_BOLD};
            padding: {Spacing.XXS}px {Spacing.XS}px;
            border-radius: {Dimensions.BORDER_RADIUS_SM};
        }}
        """
    @staticmethod
    def get_scrollbar_stylesheet():
        return f"""
        QScrollArea {{
            border: none;
        }}

        QScrollBar:vertical {{
            border: none;
            background: transparent;
            width: {Spacing.SM}px;
            margin: {Spacing.NONE};
        }}

        QScrollBar::handle:vertical {{
            background: #dbdfe6; /* Specific color from CSS */
            border-radius: {Spacing.XS}px;
            min-height: {Spacing.XL}px;
        }}

        QScrollBar::handle:vertical:hover {{
            background: #c0c4cc; /* Specific color from CSS */
        }}

        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
            height: {Spacing.NONE};
        }}

        QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{
            background: none;
        }}
        """