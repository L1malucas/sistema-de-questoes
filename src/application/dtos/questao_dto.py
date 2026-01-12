"""
DTOs: Questão
DESCRIÇÃO: Data Transfer Objects para operações com questões
"""

from typing import Optional, List
from dataclasses import dataclass, field


@dataclass
class AlternativaDTO:
    """DTO para alternativa de questão objetiva"""

    letra: str
    texto: str
    correta: bool = False
    imagem: Optional[str] = None
    escala_imagem: Optional[float] = None

    def to_dict(self) -> dict:
        """Converte para dicionário"""
        return {
            'letra': self.letra,
            'texto': self.texto,
            'correta': self.correta,
            'imagem': self.imagem,
            'escala_imagem': self.escala_imagem
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'AlternativaDTO':
        """Cria DTO a partir de dicionário"""
        return cls(
            letra=data['letra'],
            texto=data['texto'],
            correta=data.get('correta', False),
            imagem=data.get('imagem'),
            escala_imagem=data.get('escala_imagem')
        )


@dataclass
class QuestaoCreateDTO:
    """DTO para criação de questão"""

    enunciado: str
    tipo: str  # 'OBJETIVA' ou 'DISCURSIVA'
    id_dificuldade: int
    titulo: Optional[str] = None
    ano: Optional[int] = None
    fonte: Optional[str] = None
    resolucao: Optional[str] = None
    imagem_enunciado: Optional[str] = None
    escala_imagem_enunciado: Optional[float] = None
    alternativas: List[AlternativaDTO] = field(default_factory=list)
    tags: List[int] = field(default_factory=list)

    def to_dict(self) -> dict:
        """Converte para dicionário"""
        return {
            'titulo': self.titulo,
            'enunciado': self.enunciado,
            'tipo': self.tipo,
            'ano': self.ano,
            'fonte': self.fonte,
            'id_dificuldade': self.id_dificuldade,
            'resolucao': self.resolucao,
            'imagem_enunciado': self.imagem_enunciado,
            'escala_imagem_enunciado': self.escala_imagem_enunciado,
            'alternativas': [alt.to_dict() for alt in self.alternativas],
            'tags': self.tags
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'QuestaoCreateDTO':
        """Cria DTO a partir de dicionário"""
        alternativas_data = data.get('alternativas', [])
        alternativas = [
            AlternativaDTO.from_dict(alt) for alt in alternativas_data
        ]

        return cls(
            titulo=data.get('titulo'),
            enunciado=data['enunciado'],
            tipo=data['tipo'],
            ano=data.get('ano'),
            fonte=data.get('fonte'),
            id_dificuldade=data['id_dificuldade'],
            resolucao=data.get('resolucao'),
            imagem_enunciado=data.get('imagem_enunciado'),
            escala_imagem_enunciado=data.get('escala_imagem_enunciado'),
            alternativas=alternativas,
            tags=data.get('tags', [])
        )


@dataclass
class QuestaoUpdateDTO:
    """DTO para atualização de questão"""

    id_questao: int
    titulo: Optional[str] = None
    enunciado: Optional[str] = None
    tipo: Optional[str] = None
    ano: Optional[int] = None
    fonte: Optional[str] = None
    id_dificuldade: Optional[int] = None
    resolucao: Optional[str] = None
    imagem_enunciado: Optional[str] = None
    escala_imagem_enunciado: Optional[float] = None
    alternativas: Optional[List[AlternativaDTO]] = None
    tags: Optional[List[int]] = None

    def to_dict(self) -> dict:
        """Converte para dicionário (apenas campos não-None)"""
        dados = {'id_questao': self.id_questao}

        if self.titulo is not None:
            dados['titulo'] = self.titulo

        if self.enunciado is not None:
            dados['enunciado'] = self.enunciado

        if self.tipo is not None:
            dados['tipo'] = self.tipo

        if self.ano is not None:
            dados['ano'] = self.ano

        if self.fonte is not None:
            dados['fonte'] = self.fonte

        if self.id_dificuldade is not None:
            dados['id_dificuldade'] = self.id_dificuldade

        if self.resolucao is not None:
            dados['resolucao'] = self.resolucao

        if self.imagem_enunciado is not None:
            dados['imagem_enunciado'] = self.imagem_enunciado

        if self.escala_imagem_enunciado is not None:
            dados['escala_imagem_enunciado'] = self.escala_imagem_enunciado

        if self.alternativas is not None:
            dados['alternativas'] = [alt.to_dict() for alt in self.alternativas]

        if self.tags is not None:
            dados['tags'] = self.tags

        return dados


@dataclass
class QuestaoResponseDTO:
    """DTO para resposta de questão (com dados completos)"""

    id: int
    titulo: Optional[str]
    enunciado: str
    tipo: str
    ano: Optional[int]
    fonte: Optional[str]
    id_dificuldade: int
    dificuldade_nome: str
    resolucao: Optional[str]
    imagem_enunciado: Optional[str]
    escala_imagem_enunciado: Optional[float]
    ativa: bool
    data_criacao: str
    data_atualizacao: Optional[str]
    alternativas: List[AlternativaDTO] = field(default_factory=list)
    tags: List[dict] = field(default_factory=list)

    def to_dict(self) -> dict:
        """Converte para dicionário"""
        return {
            'id': self.id,
            'titulo': self.titulo,
            'enunciado': self.enunciado,
            'tipo': self.tipo,
            'ano': self.ano,
            'fonte': self.fonte,
            'id_dificuldade': self.id_dificuldade,
            'dificuldade_nome': self.dificuldade_nome,
            'resolucao': self.resolucao,
            'imagem_enunciado': self.imagem_enunciado,
            'escala_imagem_enunciado': self.escala_imagem_enunciado,
            'ativa': self.ativa,
            'data_criacao': self.data_criacao,
            'data_atualizacao': self.data_atualizacao,
            'alternativas': [alt.to_dict() for alt in self.alternativas],
            'tags': self.tags
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'QuestaoResponseDTO':
        """Cria DTO a partir de dicionário"""
        alternativas_data = data.get('alternativas', [])
        alternativas = [
            AlternativaDTO.from_dict(alt) for alt in alternativas_data
        ]

        return cls(
            id=data['id'],
            titulo=data.get('titulo'),
            enunciado=data['enunciado'],
            tipo=data['tipo'],
            ano=data.get('ano'),
            fonte=data.get('fonte'),
            id_dificuldade=data['id_dificuldade'],
            dificuldade_nome=data.get('dificuldade_nome', ''),
            resolucao=data.get('resolucao'),
            imagem_enunciado=data.get('imagem_enunciado'),
            escala_imagem_enunciado=data.get('escala_imagem_enunciado'),
            ativa=data.get('ativa', True),
            data_criacao=data.get('data_criacao', ''),
            data_atualizacao=data.get('data_atualizacao'),
            alternativas=alternativas,
            tags=data.get('tags', [])
        )
