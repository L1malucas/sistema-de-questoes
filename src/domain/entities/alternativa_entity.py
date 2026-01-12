"""
Entity: Alternativa
DESCRIÇÃO: Entidade representando uma alternativa de questão objetiva
RESPONSABILIDADES:
    - Encapsular dados da alternativa
    - Validar invariantes do domínio
    - Expor comportamentos relacionados à alternativa
"""

from typing import Optional
from dataclasses import dataclass

from ..value_objects import LetraAlternativa


@dataclass
class AlternativaEntity:
    """Entidade Alternativa com regras de negócio"""

    id: Optional[int]
    id_questao: int
    letra: LetraAlternativa
    texto: str
    correta: bool
    imagem: Optional[str]
    escala_imagem: Optional[float]

    def __post_init__(self):
        """Valida invariantes após criação"""
        self._validar_texto()
        self._validar_escala_imagem()

    def _validar_texto(self):
        """Valida que texto não está vazio"""
        if not self.texto or not self.texto.strip():
            raise ValueError(
                f"Texto da alternativa {self.letra.value} não pode ser vazio"
            )

    def _validar_escala_imagem(self):
        """Valida que escala está entre 0 e 1"""
        if self.escala_imagem is not None:
            if not (0 < self.escala_imagem <= 1):
                raise ValueError("Escala de imagem deve estar entre 0 e 1")

    @property
    def tem_imagem(self) -> bool:
        """Verifica se alternativa possui imagem"""
        return self.imagem is not None

    @property
    def label_completo(self) -> str:
        """Retorna label completo da alternativa (ex: 'A) Texto...')"""
        preview = self.texto[:50].strip()
        texto_exibicao = f"{preview}..." if len(self.texto) > 50 else preview
        return f"{self.letra.value}) {texto_exibicao}"

    def marcar_como_correta(self):
        """Marca alternativa como correta"""
        self.correta = True

    def marcar_como_incorreta(self):
        """Marca alternativa como incorreta"""
        self.correta = False

    def atualizar_texto(self, novo_texto: str):
        """Atualiza texto validando invariantes"""
        if not novo_texto or not novo_texto.strip():
            raise ValueError(
                f"Texto da alternativa {self.letra.value} não pode ser vazio"
            )
        self.texto = novo_texto

    def to_dict(self) -> dict:
        """Converte entidade para dicionário"""
        return {
            'id': self.id,
            'id_questao': self.id_questao,
            'letra': self.letra.value,
            'texto': self.texto,
            'correta': self.correta,
            'imagem': self.imagem,
            'escala_imagem': self.escala_imagem
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'AlternativaEntity':
        """Cria entidade a partir de dicionário"""
        return cls(
            id=data.get('id'),
            id_questao=data['id_questao'],
            letra=LetraAlternativa.from_string(data['letra']),
            texto=data['texto'],
            correta=data.get('correta', False),
            imagem=data.get('imagem'),
            escala_imagem=data.get('escala_imagem')
        )


@dataclass
class ConjuntoAlternativas:
    """Value Object representando conjunto completo de alternativas"""

    alternativas: list[AlternativaEntity]

    def __post_init__(self):
        """Valida invariantes do conjunto"""
        self._validar_quantidade()
        self._validar_letras_unicas()
        self._validar_apenas_uma_correta()

    def _validar_quantidade(self):
        """Valida que há exatamente 5 alternativas"""
        if len(self.alternativas) != LetraAlternativa.total_obrigatorio():
            raise ValueError(
                f"Conjunto deve ter exatamente {LetraAlternativa.total_obrigatorio()} alternativas, "
                f"mas tem {len(self.alternativas)}"
            )

    def _validar_letras_unicas(self):
        """Valida que não há letras duplicadas"""
        letras = [alt.letra for alt in self.alternativas]
        if len(letras) != len(set(letras)):
            raise ValueError("Alternativas com letras duplicadas")

    def _validar_apenas_uma_correta(self):
        """Valida que há exatamente uma alternativa correta"""
        corretas = [alt for alt in self.alternativas if alt.correta]
        if len(corretas) == 0:
            raise ValueError("Deve haver pelo menos uma alternativa correta")
        if len(corretas) > 1:
            letras_corretas = [alt.letra.value for alt in corretas]
            raise ValueError(
                f"Deve haver apenas uma alternativa correta, "
                f"mas {len(corretas)} estão marcadas como corretas: {', '.join(letras_corretas)}"
            )

    @property
    def alternativa_correta(self) -> AlternativaEntity:
        """Retorna a alternativa correta"""
        return next(alt for alt in self.alternativas if alt.correta)

    @property
    def letra_correta(self) -> LetraAlternativa:
        """Retorna a letra da alternativa correta"""
        return self.alternativa_correta.letra

    def obter_por_letra(self, letra: LetraAlternativa) -> Optional[AlternativaEntity]:
        """Obtém alternativa por letra"""
        return next(
            (alt for alt in self.alternativas if alt.letra == letra),
            None
        )

    def ordenadas(self) -> list[AlternativaEntity]:
        """Retorna alternativas ordenadas por letra (A, B, C, D, E)"""
        return sorted(self.alternativas, key=lambda alt: alt.letra)

    def to_dict_list(self) -> list[dict]:
        """Converte conjunto para lista de dicionários"""
        return [alt.to_dict() for alt in self.ordenadas()]

    @classmethod
    def from_dict_list(cls, data_list: list[dict]) -> 'ConjuntoAlternativas':
        """Cria conjunto a partir de lista de dicionários"""
        alternativas = [AlternativaEntity.from_dict(data) for data in data_list]
        return cls(alternativas=alternativas)
