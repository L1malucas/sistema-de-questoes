"""
Repository para Nível Escolar
"""
from typing import Optional, List
from sqlalchemy.orm import Session
from src.models.orm import NivelEscolar
from .base_repository import BaseRepository


class NivelEscolarRepository(BaseRepository[NivelEscolar]):
    """Repository para operações com Nível Escolar"""
    
    def __init__(self, session: Session):
        super().__init__(NivelEscolar, session)
    
    def buscar_por_codigo(self, codigo: str) -> Optional[NivelEscolar]:
        """Busca nível por código"""
        return self.session.query(NivelEscolar).filter_by(
            codigo=codigo,
            ativo=True
        ).first()
    
    def listar_todos(self) -> List[NivelEscolar]:
        """Lista todos os níveis ativos ordenados por ordem"""
        return self.session.query(NivelEscolar).filter_by(
            ativo=True
        ).order_by(NivelEscolar.ordem).all()
    
    def buscar_por_ordem(self, ordem: int) -> Optional[NivelEscolar]:
        """Busca nível por ordem"""
        return self.session.query(NivelEscolar).filter_by(
            ordem=ordem,
            ativo=True
        ).first()
