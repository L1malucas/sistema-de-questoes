# src/views/design/constants.py

# Cores
class Color:
    PRIMARY_BLUE = "#1258e2"
    HOVER_BLUE = "#0d47b8"
    LIGHT_BLUE_BG_1 = "rgba(18, 88, 226, 0.1)"
    LIGHT_BLUE_BG_2 = "rgba(18, 88, 226, 0.05)"
    LIGHT_BLUE_BORDER = "rgba(18, 88, 226, 0.2)"

    WHITE = "#ffffff"
    BLACK = "#000000"
    DARK_TEXT = "#111318"
    GRAY_TEXT = "#616f89"
    LIGHT_BACKGROUND = "#f6f6f8"
    BORDER_LIGHT = "#f0f2f4"
    BORDER_MEDIUM = "#e0e0e0"
    LIGHT_GRAY_BACKGROUND = "#f8f9fa" # Formula box background

    # Tag Colors
    TAG_BLUE = "#2563eb"
    TAG_GREEN = "#16a34a"
    TAG_RED = "#dc2626"
    TAG_YELLOW = "#ca8a04"
    TAG_PURPLE = "#9333ea"
    TAG_ORANGE = "#ea580c"
    TAG_GRAY = "#616f89"

# Espaçamentos (Padding, Margin, Gap)
class Spacing:
    NONE = 0
    XXS = 2
    XS = 4
    SM = 8
    MD = 12
    LG = 16
    XL = 24
    XXL = 32

# Tipografia
class Typography:
    FONT_FAMILY = "Segoe UI, Arial, sans-serif"
    FONT_SIZE_XS = "10px"
    FONT_SIZE_SM = "12px"
    FONT_SIZE_MD = "14px"
    FONT_SIZE_LG = "16px"
    FONT_SIZE_XL = "18px"
    FONT_SIZE_XXL = "20px"
    FONT_SIZE_PAGE_TITLE = "24px"

    FONT_WEIGHT_LIGHT = 300
    FONT_WEIGHT_REGULAR = 400
    FONT_WEIGHT_MEDIUM = 500
    FONT_WEIGHT_SEMIBOLD = 600
    FONT_WEIGHT_BOLD = 700

# Dimensões
class Dimensions:
    NAVBAR_HEIGHT = 60  # Placeholder
    SIDEBAR_WIDTH = 250 # Placeholder
    BORDER_RADIUS_SM = "4px"
    BORDER_RADIUS_MD = "8px"
    BORDER_RADIUS_LG = "12px"
    BORDER_RADIUS_CIRCLE = "50%"

# Textos/Labels da interface (i18n-ready - placeholders for now)
class Text:
    APP_TITLE = "MathBank"
    NAV_DASHBOARD = "Dashboard"
    NAV_QUESTION_BANK = "Banco de Questões"
    NAV_LISTS = "Listas"
    NAV_TAXONOMY = "Taxonomia"
    BUTTON_CREATE = "Criar Nova"
    SEARCH_PLACEHOLDER = "Pesquisar..."
    # Add more as needed

# Rotas/Páginas disponíveis (placeholders for now, will be enums later)
class Page:
    DASHBOARD = "dashboard"
    QUESTION_BANK = "question_bank"
    LISTS = "lists"
    TAXONOMY = "taxonomy"
    QUESTION_EDITOR = "question_editor"

# Outros
class IconSize:
    SM = "16px"
    MD = "18px"
    LG = "24px"
