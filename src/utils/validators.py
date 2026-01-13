"""
Util: Validators
DESCRIÇÃO: Funções de validação de dados
RELACIONAMENTOS: Todos os controllers
FUNCIONALIDADES:
    - Validar formato de imagens (PNG, JPG, JPEG, SVG)
    - Validar tamanho de arquivos
    - Validar sintaxe LaTeX
    - Validar campos obrigatórios
    - Validar tipos de dados
"""
import logging
import os
from pathlib import Path

from src.constants import ImagemConfig

logger = logging.getLogger(__name__)

# ATUALIZADO: Usar constantes centralizadas
FORMATOS_IMAGEM_PERMITIDOS = ImagemConfig.EXTENSOES_VALIDAS
TAMANHO_MAX_IMAGEM_MB = ImagemConfig.MAX_SIZE_MB

def validar_imagem(caminho: str) -> dict:
    """Valida se arquivo é uma imagem válida"""
    # TODO: Implementar validação completa
    pass

def validar_latex(codigo: str) -> dict:
    """Valida sintaxe básica de LaTeX"""
    # TODO: Implementar validação
    pass

logger.info("Validators carregado")
