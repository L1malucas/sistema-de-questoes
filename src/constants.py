"""
Sistema de Banco de Questões Educacionais
Módulo: Constants
Descrição: Constantes centralizadas do sistema
Versão: 1.0.1

IMPORTANTE:
    Este arquivo centraliza todas as constantes usadas no sistema.
    Evita magic strings e hardcoded values espalhados pelo código.
"""

from enum import IntEnum, Enum
from typing import List


# ============================================
# TIPOS DE QUESTÃO
# ============================================
class TipoQuestao(str, Enum):
    """Tipos de questão suportados"""
    OBJETIVA = 'OBJETIVA'
    DISCURSIVA = 'DISCURSIVA'


# ============================================
# DIFICULDADES
# ============================================
class DificuldadeID(IntEnum):
    """IDs das dificuldades no banco de dados"""
    FACIL = 1
    MEDIO = 2
    DIFICIL = 3
    SEM_DIFICULDADE = -1


class DificuldadeNome(str, Enum):
    """Nomes das dificuldades"""
    FACIL = 'Fácil'
    MEDIO = 'Médio'
    DIFICIL = 'Difícil'


# ============================================
# ALTERNATIVAS
# ============================================
class LetraAlternativa(str, Enum):
    """Letras válidas para alternativas"""
    A = 'A'
    B = 'B'
    C = 'C'
    D = 'D'
    E = 'E'


# Constantes de alternativas
LETRAS_ALTERNATIVAS: List[str] = ['A', 'B', 'C', 'D', 'E']
TOTAL_ALTERNATIVAS: int = 5


# ============================================
# VALIDAÇÕES
# ============================================
class Validacao:
    """Regras de validação do sistema"""

    # Questões
    MIN_TAGS_POR_QUESTAO = 1
    ANO_MINIMO = 1900
    ANO_MAXIMO = 2100
    TITULO_MAX_LENGTH = 200

    # Alternativas
    NUM_ALTERNATIVAS_OBJETIVA = 5
    NUM_ALTERNATIVAS_CORRETAS = 1

    # Tags
    TAG_MAX_LENGTH = 100
    TAG_NIVEL_MAX = 3  # Máximo 3 níveis hierárquicos


# ============================================
# IMAGENS
# ============================================
class ImagemConfig:
    """Configurações de imagens"""

    # Formatos suportados (sem o ponto)
    FORMATOS_SUPORTADOS = ['png', 'jpg', 'jpeg', 'svg', 'gif', 'bmp']

    # Extensões com ponto (para validação)
    EXTENSOES_VALIDAS = ['.png', '.jpg', '.jpeg', '.svg', '.gif', '.bmp']

    # Tamanhos
    MAX_SIZE_MB = 10
    MAX_SIZE_BYTES = MAX_SIZE_MB * 1024 * 1024

    # Escala padrão para LaTeX
    ESCALA_PADRAO = 0.7
    ESCALA_MINIMA = 0.1
    ESCALA_MAXIMA = 2.0


# ============================================
# CAMINHOS E DIRETÓRIOS
# ============================================
class Paths:
    """Nomes de diretórios (relativos ao projeto root)"""

    # Diretórios principais
    DATABASE_DIR = 'database'
    IMAGES_DIR = 'imagens'
    TEMPLATES_DIR = 'templates'
    EXPORTS_DIR = 'exports'
    BACKUPS_DIR = 'backups'
    LOGS_DIR = 'logs'

    # Subdiretórios de imagens
    IMAGES_ENUNCIADOS = 'imagens/enunciados'
    IMAGES_ALTERNATIVAS = 'imagens/alternativas'
    IMAGES_QUESTOES = 'imagens/questoes'

    # Templates LaTeX
    TEMPLATES_LATEX = 'templates/latex'

    # Nome do banco de dados
    DATABASE_FILE = 'questoes.db'


# ============================================
# LATEX
# ============================================
class LatexConfig:
    """Configurações de LaTeX"""

    # Templates
    TEMPLATE_PADRAO = 'default.tex'

    # Layouts
    LAYOUT_UMA_COLUNA = 1
    LAYOUT_DUAS_COLUNAS = 2

    # Comandos perigosos que devem ser removidos/escapados
    COMANDOS_PERIGOSOS = [
        r'\write18',
        r'\input',
        r'\include',
        r'\openin',
        r'\openout',
        r'\immediate',
        r'\newread',
        r'\newwrite',
        r'\csname',
        r'\expandafter',
        r'\def',
        r'\let',
        r'\catcode',
    ]

    # Flags de segurança para pdflatex
    PDFLATEX_SECURITY_FLAGS = [
        '-no-shell-escape',
        '-interaction=nonstopmode',
    ]


# ============================================
# DATABASE
# ============================================
class DatabaseConfig:
    """Configurações do banco de dados"""

    TIMEOUT_SECONDS = 10.0
    CHECK_SAME_THREAD = False
    FOREIGN_KEYS_ENABLED = True

    # Tabelas do sistema
    TABELA_TAG = 'tag'
    TABELA_DIFICULDADE = 'dificuldade'
    TABELA_QUESTAO = 'questao'
    TABELA_ALTERNATIVA = 'alternativa'
    TABELA_QUESTAO_TAG = 'questao_tag'
    TABELA_LISTA = 'lista'
    TABELA_LISTA_QUESTAO = 'lista_questao'
    TABELA_QUESTAO_VERSAO = 'questao_versao'
    TABELA_CONFIGURACAO = 'configuracao'


# ============================================
# BUSCA E PAGINAÇÃO
# ============================================
class SearchConfig:
    """Configurações de busca"""

    MAX_RESULTS = 1000
    TIMEOUT_SECONDS = 5.0
    QUESTOES_POR_PAGINA = 20
    CASE_SENSITIVE = False


# ============================================
# LOGGING
# ============================================
class LogLevel(str, Enum):
    """Níveis de log"""
    DEBUG = 'DEBUG'
    INFO = 'INFO'
    WARNING = 'WARNING'
    ERROR = 'ERROR'
    CRITICAL = 'CRITICAL'


class LogConfig:
    """Configurações de logging"""

    DEFAULT_LEVEL = LogLevel.INFO
    FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    MAX_LOG_SIZE_MB = 10
    BACKUP_COUNT = 5


# ============================================
# INTERFACE
# ============================================
class InterfaceConfig:
    """Configurações de interface"""

    # Temas
    THEME_LIGHT = 'light'
    THEME_DARK = 'dark'
    THEME_AUTO = 'auto'

    # Idiomas
    LANG_PT_BR = 'pt-BR'
    LANG_EN_US = 'en-US'

    # Tamanhos
    FONT_SIZE_DEFAULT = 10
    WINDOW_MIN_WIDTH = 1000
    WINDOW_MIN_HEIGHT = 600
    SIDEBAR_MIN_WIDTH = 200
    SIDEBAR_MAX_WIDTH = 250


# ============================================
# BACKUP
# ============================================
class BackupConfig:
    """Configurações de backup"""

    AUTO_BACKUP_ENABLED = False
    PERIODICIDADE_DIAS = 7
    MANTER_BACKUPS = 5
    FORMATO_NOME = 'backup_questoes_%Y%m%d_%H%M%S.zip'


# ============================================
# FONTES/BANCAS PADRÃO
# ============================================
class FontePadrao:
    """Fontes/bancas comuns de questões"""

    AUTORAL = 'AUTORAL'
    ENEM = 'ENEM'
    FUVEST = 'FUVEST'
    UNICAMP = 'UNICAMP'
    UNESP = 'UNESP'
    IME = 'IME'
    ITA = 'ITA'
    OBMEP = 'OBMEP'
    OBM = 'OBM'


# ============================================
# MENSAGENS DE ERRO PADRÃO
# ============================================
class ErroMensagens:
    """Mensagens de erro padronizadas"""

    # Validação
    ENUNCIADO_VAZIO = "O enunciado é obrigatório"
    TIPO_INVALIDO = "Tipo deve ser OBJETIVA ou DISCURSIVA"
    ANO_INVALIDO = f"Ano deve estar entre {Validacao.ANO_MINIMO} e {Validacao.ANO_MAXIMO}"
    FONTE_VAZIA = "A fonte/banca é obrigatória"
    DIFICULDADE_INVALIDA = "Dificuldade inválida"

    # Alternativas
    FALTAM_ALTERNATIVAS = f"Questão objetiva deve ter {TOTAL_ALTERNATIVAS} alternativas"
    FALTA_CORRETA = "Marque qual alternativa é a correta"
    MULTIPLAS_CORRETAS = "Apenas uma alternativa pode ser correta"

    # Tags
    SEM_TAGS = "Recomendado adicionar pelo menos uma tag para facilitar a busca"

    # Imagens
    IMAGEM_NAO_ENCONTRADA = "Arquivo de imagem não encontrado"
    FORMATO_INVALIDO = "Formato de imagem inválido"
    TAMANHO_EXCEDIDO = f"Imagem excede tamanho máximo de {ImagemConfig.MAX_SIZE_MB}MB"

    # Banco de dados
    ERRO_CONEXAO_DB = "Erro ao conectar ao banco de dados"
    ERRO_QUERY = "Erro ao executar query no banco de dados"

    # LaTeX
    ERRO_COMPILACAO_LATEX = "Erro na compilação LaTeX"
    PDFLATEX_NAO_ENCONTRADO = "Comando 'pdflatex' não encontrado. Instale TeX Live ou MiKTeX."


# ============================================
# VERSÃO DO SISTEMA
# ============================================
class SystemInfo:
    """Informações do sistema"""

    VERSAO = '1.0.1'
    DATA = 'Janeiro 2026'
    NOME = 'Sistema de Banco de Questões Educacionais'
    NOME_CURTO = 'Banco de Questões'
