"""
Interfaces (Protocols)
DESCRIÇÃO: Define contratos para implementação de repositórios e serviços
PRINCÍPIO: Dependency Inversion (DIP) - dependa de abstrações, não de implementações
"""

from .repositories import (
    IQuestaoRepository,
    IAlternativaRepository,
    ITagRepository,
    IListaRepository
)

__all__ = [
    'IQuestaoRepository',
    'IAlternativaRepository',
    'ITagRepository',
    'IListaRepository'
]
