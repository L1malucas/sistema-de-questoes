"""
Model ORM para Nível Escolar
"""
from sqlalchemy import Column, String, Integer, Text
from sqlalchemy.orm import relationship
from .base import BaseModel


class NivelEscolar(BaseModel):
    """
    Nível Escolar (EF1, EF2, EM, EJA, TEC, SUP)
    """
    __tablename__ = 'nivel_escolar'

    codigo = Column(String(10), unique=True, nullable=False, index=True)
    nome = Column(String(100), nullable=False)
    descricao = Column(Text, nullable=True)
    ordem = Column(Integer, nullable=False)

    # Relationships
    questoes = relationship("Questao", secondary="questao_nivel", back_populates="niveis")

    def __repr__(self):
        return f"<NivelEscolar(codigo={self.codigo}, nome={self.nome})>"

    @classmethod
    def buscar_por_codigo(cls, session, codigo: str):
        """Busca nível por código"""
        return session.query(cls).filter_by(codigo=codigo, ativo=True).first()

    @classmethod
    def listar_todos(cls, session):
        """Lista todos os níveis ativos ordenados por ordem"""
        return session.query(cls).filter_by(ativo=True).order_by(cls.ordem).all()
