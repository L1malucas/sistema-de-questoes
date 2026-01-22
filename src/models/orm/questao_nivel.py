"""
Tabela de relacionamento Questão-Nível Escolar (N:N)
"""
from sqlalchemy import Table, Column, Text, ForeignKey, DateTime
from datetime import datetime
from .base import Base


QuestaoNivel = Table(
    'questao_nivel',
    Base.metadata,
    Column('uuid_questao', Text, ForeignKey('questao.uuid'), primary_key=True),
    Column('uuid_nivel', Text, ForeignKey('nivel_escolar.uuid'), primary_key=True),
    Column('data_associacao', DateTime, default=datetime.utcnow, nullable=False)
)
