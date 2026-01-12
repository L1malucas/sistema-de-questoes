"""
Value Object: Dificuldade
DESCRIÇÃO: Representa o nível de dificuldade de uma questão
REGRAS DE NEGÓCIO:
    - Três níveis: FACIL (1), MEDIO (2), DIFICIL (3)
    - Deve corresponder aos IDs na tabela dificuldade do banco
"""

from enum import IntEnum
from typing import Optional


class Dificuldade(IntEnum):
    """Enum para níveis de dificuldade"""

    FACIL = 1
    MEDIO = 2
    DIFICIL = 3

    @classmethod
    def from_id(cls, id_dificuldade: int) -> 'Dificuldade':
        """Converte ID do banco para Dificuldade

        Args:
            id_dificuldade: ID da dificuldade (1, 2 ou 3)

        Returns:
            Dificuldade correspondente

        Raises:
            ValueError: Se o ID não for válido
        """
        try:
            return cls(id_dificuldade)
        except ValueError:
            raise ValueError(
                f"ID de dificuldade inválido: {id_dificuldade}. "
                f"IDs válidos: {', '.join([str(d.value) for d in cls])}"
            )

    @classmethod
    def from_nome(cls, nome: str) -> Optional['Dificuldade']:
        """Converte nome para Dificuldade

        Args:
            nome: Nome da dificuldade ('FACIL', 'MEDIO', 'DIFICIL')

        Returns:
            Dificuldade correspondente ou None se não encontrado
        """
        nome_upper = nome.upper().strip()
        for dificuldade in cls:
            if dificuldade.name == nome_upper:
                return dificuldade
        return None

    @property
    def nome(self) -> str:
        """Retorna o nome da dificuldade"""
        return self.name

    @property
    def descricao(self) -> str:
        """Retorna descrição amigável da dificuldade"""
        descricoes = {
            Dificuldade.FACIL: "Fácil",
            Dificuldade.MEDIO: "Médio",
            Dificuldade.DIFICIL: "Difícil"
        }
        return descricoes[self]

    @property
    def cor(self) -> str:
        """Retorna cor para UI (código hex)"""
        cores = {
            Dificuldade.FACIL: "#4caf50",    # Verde
            Dificuldade.MEDIO: "#ff9800",    # Laranja
            Dificuldade.DIFICIL: "#f44336"   # Vermelho
        }
        return cores[self]

    def __str__(self) -> str:
        return self.descricao
