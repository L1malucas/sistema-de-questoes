"""
Entities
DESCRIÇÃO: Entidades do domínio com identidade única
DIFERENÇA DE VALUE OBJECTS:
    - Entidades têm ID único e ciclo de vida
    - Value Objects são imutáveis e definidos apenas por seus atributos
"""

from .questao_entity import QuestaoEntity
from .alternativa_entity import AlternativaEntity

__all__ = ['QuestaoEntity', 'AlternativaEntity']
