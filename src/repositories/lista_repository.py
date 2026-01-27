"""Repository para Listas"""
import logging
from typing import List, Optional
from sqlalchemy.orm import Session

from src.infrastructure.logging import get_audit_logger, get_metrics_collector
from src.models.orm import Lista, Questao, Tag, CodigoGenerator
from .base_repository import BaseRepository

class ListaRepository(BaseRepository[Lista]):
    def __init__(self, session: Session):
        super().__init__(Lista, session)
        self._audit = get_audit_logger()
        self._metrics = get_metrics_collector()
        self._logger = logging.getLogger(__name__)
    
    def buscar_por_codigo(self, codigo: str) -> Optional[Lista]:
        return self.session.query(Lista).filter_by(codigo=codigo, ativo=True).first()
    
    def buscar_por_titulo(self, titulo: str) -> List[Lista]:
        return self.session.query(Lista).filter(Lista.titulo.ilike(f"%{titulo}%"), Lista.ativo == True).all()
    
    def buscar_por_tipo(self, tipo: str) -> List[Lista]:
        return self.session.query(Lista).filter_by(tipo=tipo, ativo=True).order_by(Lista.data_criacao.desc()).all()
    
    def criar_lista(self, titulo: str, tipo: str = 'LISTA', formulas: str = None) -> Optional[Lista]:
        try:
            codigo = None
            if self._metrics:
                with self._metrics.time_operation("criar_lista"):
                    codigo = CodigoGenerator.gerar_codigo_lista(self.session)
                    lista = Lista(codigo=codigo, titulo=titulo, tipo=tipo, formulas=formulas)
                    self.session.add(lista)
                    self.session.flush()
            else:
                codigo = CodigoGenerator.gerar_codigo_lista(self.session)
                lista = Lista(codigo=codigo, titulo=titulo, tipo=tipo, formulas=formulas)
                self.session.add(lista)
                self.session.flush()

            if lista and self._audit:
                self._audit.lista_criada(
                    lista_id=str(lista.uuid),
                    titulo=lista.titulo,
                    qtd_questoes=0 # No momento da criação, a lista está vazia
                )
            if self._metrics:
                self._metrics.increment("listas_criadas")
            return lista
        except Exception as e:
            self._logger.error(f"Erro ao criar lista: {e}", exc_info=True)
            if self._metrics:
                self._metrics.increment("erros_criar_lista")
            return None
    
    def adicionar_questao(self, codigo_lista: str, codigo_questao: str, ordem: int = None) -> bool:
        try:
            lista = self.buscar_por_codigo(codigo_lista)
            questao = self.session.query(Questao).filter_by(codigo=codigo_questao, ativo=True).first()
            if lista and questao:
                lista.adicionar_questao(self.session, questao, ordem)
                if self._audit:
                    self._audit.lista_editada(
                        lista_id=str(lista.uuid),
                        campos_alterados=[f"add_questao_{questao.codigo}"]
                    )
                if self._metrics:
                    self._metrics.increment("lista_questoes_adicionadas")
                return True
            return False
        except Exception as e:
            self._logger.error(f"Erro ao adicionar questão à lista: {e}", exc_info=True)
            if self._metrics:
                self._metrics.increment("erros_lista_questoes_adicionadas")
            return False
    
    def remover_questao(self, codigo_lista: str, codigo_questao: str) -> bool:
        try:
            lista = self.buscar_por_codigo(codigo_lista)
            questao = self.session.query(Questao).filter_by(codigo=codigo_questao).first()
            if lista and questao:
                lista.remover_questao(self.session, questao)
                if self._audit:
                    self._audit.lista_editada(
                        lista_id=str(lista.uuid),
                        campos_alterados=[f"remove_questao_{questao.codigo}"]
                    )
                if self._metrics:
                    self._metrics.increment("lista_questoes_removidas")
                return True
            return False
        except Exception as e:
            self._logger.error(f"Erro ao remover questão da lista: {e}", exc_info=True)
            if self._metrics:
                self._metrics.increment("erros_lista_questoes_removidas")
            return False
    
    def reordenar_questoes(self, codigo_lista: str, codigos_questoes_ordenados: List[str]) -> bool:
        try:
            lista = self.buscar_por_codigo(codigo_lista)
            if lista:
                lista.reordenar_questoes(self.session, codigos_questoes_ordenados)
                if self._audit:
                    self._audit.lista_editada(
                        lista_id=str(lista.uuid),
                        campos_alterados=["reordenar_questoes"]
                    )
                if self._metrics:
                    self._metrics.increment("lista_questoes_reordenadas")
                return True
            return False
        except Exception as e:
            self._logger.error(f"Erro ao reordenar questões da lista: {e}", exc_info=True)
            if self._metrics:
                self._metrics.increment("erros_lista_questoes_reordenadas")
            return False
    
    def remover(self, uuid: str) -> bool:
        """
        Remove uma lista por UUID e registra na auditoria.
        Sobrescreve o método da BaseRepository.
        """
        try:
            lista = self.buscar_por_uuid(uuid)
            if lista:
                super().remover(uuid) # Chama o remover da BaseRepository
                if self._audit:
                    self._audit.lista_deletada(lista_id=str(lista.uuid), titulo=lista.titulo)
                if self._metrics:
                    self._metrics.increment("listas_deletadas")
                return True
            return False
        except Exception as e:
            self._logger.error(f"Erro ao remover lista por UUID: {e}", exc_info=True)
            if self._metrics:
                self._metrics.increment("erros_listas_deletadas")
            return False
    
    def buscar_tags_relacionadas(self, codigo_lista: str) -> List[Tag]:
        lista = self.buscar_por_codigo(codigo_lista)
        return lista.buscar_tags_relacionadas(self.session) if lista else []
    
    def contar_questoes(self, codigo_lista: str) -> int:
        lista = self.buscar_por_codigo(codigo_lista)
        return lista.contar_questoes() if lista else 0
