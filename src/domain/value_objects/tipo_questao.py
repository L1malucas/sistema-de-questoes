"""
Value Object: Tipo de Questão
DESCRIÇÃO: Representa os tipos válidos de questão no sistema
REGRAS DE NEGÓCIO:
    - Apenas OBJETIVA ou DISCURSIVA são válidos
    - Questão objetiva requer exatamente 5 alternativas
    - Questão discursiva não possui alternativas
"""

from enum import Enum


class TipoQuestao(Enum):
    """Enum para tipos de questão"""

    OBJETIVA = "OBJETIVA"
    DISCURSIVA = "DISCURSIVA"

    @classmethod
    def from_string(cls, valor: str) -> 'TipoQuestao':
        """Converte string para TipoQuestao

        Args:
            valor: String com o tipo ('OBJETIVA' ou 'DISCURSIVA')

        Returns:
            TipoQuestao correspondente

        Raises:
            ValueError: Se o tipo não for válido
        """
        valor_upper = valor.upper().strip()
        try:
            return cls(valor_upper)
        except ValueError:
            raise ValueError(
                f"Tipo de questão inválido: '{valor}'. "
                f"Tipos válidos: {', '.join([t.value for t in cls])}"
            )

    @property
    def requer_alternativas(self) -> bool:
        """Retorna se este tipo requer alternativas"""
        return self == TipoQuestao.OBJETIVA

    @property
    def numero_alternativas_obrigatorio(self) -> int:
        """Retorna número de alternativas obrigatórias para este tipo"""
        return 5 if self == TipoQuestao.OBJETIVA else 0

    def __str__(self) -> str:
        return self.value
