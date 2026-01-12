"""
Value Object: Letra de Alternativa
DESCRIÇÃO: Representa letras válidas para alternativas (A, B, C, D, E)
REGRAS DE NEGÓCIO:
    - Apenas letras A, B, C, D, E são válidas
    - Questão objetiva deve ter exatamente 5 alternativas
    - Apenas uma alternativa pode ser correta
"""

from enum import Enum
from typing import List


class LetraAlternativa(Enum):
    """Enum para letras de alternativas"""

    A = "A"
    B = "B"
    C = "C"
    D = "D"
    E = "E"

    @classmethod
    def from_string(cls, letra: str) -> 'LetraAlternativa':
        """Converte string para LetraAlternativa

        Args:
            letra: String com a letra ('A', 'B', 'C', 'D', 'E')

        Returns:
            LetraAlternativa correspondente

        Raises:
            ValueError: Se a letra não for válida
        """
        letra_upper = letra.upper().strip()
        try:
            return cls(letra_upper)
        except ValueError:
            raise ValueError(
                f"Letra de alternativa inválida: '{letra}'. "
                f"Letras válidas: {', '.join([l.value for l in cls])}"
            )

    @classmethod
    def todas(cls) -> List['LetraAlternativa']:
        """Retorna lista com todas as letras válidas"""
        return list(cls)

    @classmethod
    def total_obrigatorio(cls) -> int:
        """Retorna número total de alternativas obrigatórias"""
        return len(cls)

    def proximo(self) -> 'LetraAlternativa':
        """Retorna a próxima letra na sequência

        Returns:
            Próxima letra ou None se for a última (E)

        Raises:
            ValueError: Se não houver próxima letra
        """
        letras = list(LetraAlternativa)
        index_atual = letras.index(self)
        if index_atual >= len(letras) - 1:
            raise ValueError(f"Letra {self.value} é a última, não há próxima")
        return letras[index_atual + 1]

    def anterior(self) -> 'LetraAlternativa':
        """Retorna a letra anterior na sequência

        Returns:
            Letra anterior ou None se for a primeira (A)

        Raises:
            ValueError: Se não houver letra anterior
        """
        letras = list(LetraAlternativa)
        index_atual = letras.index(self)
        if index_atual <= 0:
            raise ValueError(f"Letra {self.value} é a primeira, não há anterior")
        return letras[index_atual - 1]

    @property
    def indice(self) -> int:
        """Retorna índice da letra (A=0, B=1, C=2, D=3, E=4)"""
        return list(LetraAlternativa).index(self)

    def __str__(self) -> str:
        return self.value

    def __lt__(self, other: 'LetraAlternativa') -> bool:
        """Permite ordenação de letras"""
        if not isinstance(other, LetraAlternativa):
            return NotImplemented
        return self.indice < other.indice
