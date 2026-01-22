"""Repository para Fontes de Questões"""
from typing import Optional, List
from sqlalchemy.orm import Session
from models.orm import FonteQuestao
from .base_repository import BaseRepository

class FonteQuestaoRepository(BaseRepository[FonteQuestao]):
    def __init__(self, session: Session):
        super().__init__(FonteQuestao, session)
    
    def buscar_por_sigla(self, sigla: str) -> Optional[FonteQuestao]:
        """Busca fonte por sigla"""
        return self.session.query(FonteQuestao).filter_by(sigla=sigla, ativo=True).first()
    
    def listar_todas(self) -> List[FonteQuestao]:
        """Lista todas as fontes ativas ordenadas por sigla"""
        return self.session.query(FonteQuestao).filter_by(ativo=True).order_by(FonteQuestao.sigla).all()