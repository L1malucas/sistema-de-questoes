"""
Entity: Questão
DESCRIÇÃO: Entidade central do domínio representando uma questão
RESPONSABILIDADES:
    - Encapsular dados da questão
    - Validar invariantes do domínio
    - Expor comportamentos relacionados à questão
"""

from typing import Optional, List
from datetime import datetime
from dataclasses import dataclass

from ..value_objects import TipoQuestao, Dificuldade


@dataclass
class QuestaoEntity:
    """Entidade Questão com regras de negócio"""

    id: Optional[int]
    titulo: Optional[str]
    enunciado: str
    tipo: TipoQuestao
    ano: Optional[int]
    fonte: Optional[str]
    dificuldade: Dificuldade
    resolucao: Optional[str]
    imagem_enunciado: Optional[str]
    escala_imagem_enunciado: Optional[float]
    ativa: bool
    data_criacao: datetime
    data_atualizacao: Optional[datetime]

    def __post_init__(self):
        """Valida invariantes após criação"""
        self._validar_enunciado()
        self._validar_ano()
        self._validar_escala_imagem()

    def _validar_enunciado(self):
        """Valida que enunciado não está vazio"""
        if not self.enunciado or not self.enunciado.strip():
            raise ValueError("Enunciado não pode ser vazio")

    def _validar_ano(self):
        """Valida que ano está em range válido"""
        if self.ano is not None:
            ano_atual = datetime.now().year
            if self.ano < 1900 or self.ano > ano_atual + 1:
                raise ValueError(
                    f"Ano deve estar entre 1900 e {ano_atual + 1}"
                )

    def _validar_escala_imagem(self):
        """Valida que escala está entre 0 e 1"""
        if self.escala_imagem_enunciado is not None:
            if not (0 < self.escala_imagem_enunciado <= 1):
                raise ValueError("Escala de imagem deve estar entre 0 e 1")

    @property
    def tem_imagem(self) -> bool:
        """Verifica se questão possui imagem"""
        return self.imagem_enunciado is not None

    @property
    def tem_resolucao(self) -> bool:
        """Verifica se questão possui resolução"""
        return bool(self.resolucao and self.resolucao.strip())

    @property
    def eh_objetiva(self) -> bool:
        """Verifica se questão é objetiva"""
        return self.tipo == TipoQuestao.OBJETIVA

    @property
    def eh_discursiva(self) -> bool:
        """Verifica se questão é discursiva"""
        return self.tipo == TipoQuestao.DISCURSIVA

    @property
    def titulo_ou_preview(self) -> str:
        """Retorna título ou preview do enunciado"""
        if self.titulo and self.titulo.strip():
            return self.titulo
        # Preview: primeiros 50 caracteres do enunciado
        preview = self.enunciado[:50].strip()
        return f"{preview}..." if len(self.enunciado) > 50 else preview

    def inativar(self):
        """Inativa a questão"""
        self.ativa = False
        self.data_atualizacao = datetime.now()

    def reativar(self):
        """Reativa a questão"""
        self.ativa = True
        self.data_atualizacao = datetime.now()

    def atualizar_enunciado(self, novo_enunciado: str):
        """Atualiza enunciado validando invariantes"""
        if not novo_enunciado or not novo_enunciado.strip():
            raise ValueError("Enunciado não pode ser vazio")
        self.enunciado = novo_enunciado
        self.data_atualizacao = datetime.now()

    def atualizar_resolucao(self, nova_resolucao: Optional[str]):
        """Atualiza resolução"""
        self.resolucao = nova_resolucao
        self.data_atualizacao = datetime.now()

    def to_dict(self) -> dict:
        """Converte entidade para dicionário"""
        return {
            'id': self.id,
            'titulo': self.titulo,
            'enunciado': self.enunciado,
            'tipo': self.tipo.value,
            'ano': self.ano,
            'fonte': self.fonte,
            'id_dificuldade': self.dificuldade.value,
            'dificuldade_nome': self.dificuldade.nome,
            'resolucao': self.resolucao,
            'imagem_enunciado': self.imagem_enunciado,
            'escala_imagem_enunciado': self.escala_imagem_enunciado,
            'ativa': self.ativa,
            'data_criacao': self.data_criacao.isoformat(),
            'data_atualizacao': self.data_atualizacao.isoformat() if self.data_atualizacao else None
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'QuestaoEntity':
        """Cria entidade a partir de dicionário"""
        return cls(
            id=data.get('id'),
            titulo=data.get('titulo'),
            enunciado=data['enunciado'],
            tipo=TipoQuestao.from_string(data['tipo']),
            ano=data.get('ano'),
            fonte=data.get('fonte'),
            dificuldade=Dificuldade.from_id(data['id_dificuldade']),
            resolucao=data.get('resolucao'),
            imagem_enunciado=data.get('imagem_enunciado'),
            escala_imagem_enunciado=data.get('escala_imagem_enunciado'),
            ativa=data.get('ativa', True),
            data_criacao=datetime.fromisoformat(data['data_criacao']) if isinstance(data.get('data_criacao'), str) else data.get('data_criacao', datetime.now()),
            data_atualizacao=datetime.fromisoformat(data['data_atualizacao']) if isinstance(data.get('data_atualizacao'), str) and data.get('data_atualizacao') else None
        )
