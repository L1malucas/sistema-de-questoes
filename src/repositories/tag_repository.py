"""Repository para Tags"""
import logging
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session

from src.infrastructure.logging import get_audit_logger, get_metrics_collector
from src.models.orm import Tag
from .base_repository import BaseRepository

class TagRepository(BaseRepository[Tag]):
    def __init__(self, session: Session):
        super().__init__(Tag, session)
        self._audit = get_audit_logger()
        self._metrics = get_metrics_collector()
        self._logger = logging.getLogger(__name__)
    
    def criar(self, **kwargs) -> Optional[Tag]:
        """Cria uma nova tag com auditoria e métricas."""
        try:
            tag = super().criar(**kwargs)
            if tag and self._audit:
                self._audit.tag_criada(
                    tag_id=str(tag.uuid),
                    nome=tag.nome,
                    numeracao=tag.numeracao
                )
            if self._metrics:
                self._metrics.increment("tags_criadas")
            return tag
        except Exception as e:
            self._logger.error(f"Erro ao criar tag: {e}", exc_info=True)
            if self._metrics:
                self._metrics.increment("erros_criar_tag")
            return None

    def atualizar(self, uuid: str, **kwargs) -> Optional[Tag]:
        """Atualiza uma tag com auditoria e métricas."""
        try:
            tag_antiga = self.buscar_por_uuid(uuid)
            tag_atualizada = super().atualizar(uuid, **kwargs)
            if tag_atualizada and self._audit:
                campos_alterados = [k for k in kwargs if getattr(tag_antiga, k) != kwargs[k]]
                if campos_alterados:
                    self._audit.tag_editada(
                        tag_id=str(tag_atualizada.uuid),
                        campos_alterados=campos_alterados
                    )
            if self._metrics:
                self._metrics.increment("tags_atualizadas")
            return tag_atualizada
        except Exception as e:
            self._logger.error(f"Erro ao atualizar tag {uuid}: {e}", exc_info=True)
            if self._metrics:
                self._metrics.increment("erros_atualizar_tag")
            return None
    
    def desativar(self, uuid: str) -> bool:
        """Desativa uma tag (soft delete) com auditoria e métricas."""
        try:
            tag = self.buscar_por_uuid(uuid)
            if tag and tag.ativo:
                resultado = super().desativar(uuid)
                if resultado and self._audit:
                    self._audit.tag_deletada(
                        tag_id=str(tag.uuid),
                        nome=tag.nome
                    )
                if self._metrics:
                    self._metrics.increment("tags_desativadas")
                return resultado
            return False
        except Exception as e:
            self._logger.error(f"Erro ao desativar tag {uuid}: {e}", exc_info=True)
            if self._metrics:
                self._metrics.increment("erros_desativar_tag")
            return False

    def buscar_por_nome(self, nome: str) -> Optional[Tag]:
        return self.session.query(Tag).filter_by(nome=nome, ativo=True).first()
    
    def buscar_por_numeracao(self, numeracao: str) -> Optional[Tag]:
        return self.session.query(Tag).filter_by(numeracao=numeracao, ativo=True).first()
    
    def listar_raizes(self) -> List[Tag]:
        return self.session.query(Tag).filter_by(uuid_tag_pai=None, ativo=True).order_by(Tag.ordem).all()
    
    def listar_filhas(self, numeracao_pai: str) -> List[Tag]:
        tag_pai = self.buscar_por_numeracao(numeracao_pai)
        if not tag_pai:
            return []
        return self.session.query(Tag).filter_by(uuid_tag_pai=tag_pai.uuid, ativo=True).order_by(Tag.ordem).all()
    
    def obter_caminho_completo(self, numeracao: str) -> str:
        tag = self.buscar_por_numeracao(numeracao)
        return tag.obter_caminho_completo() if tag else ""

    def obter_maior_numeracao_raiz(self, prefixo: str = '') -> int:
        """
        Obtém o maior número usado em tags raiz (incluindo inativas).

        Args:
            prefixo: 'V' para vestibular, 'N' para série, '' para conteúdo

        Returns:
            Maior número encontrado ou 0 se nenhum
        """
        query = self.session.query(Tag.numeracao).filter(Tag.uuid_tag_pai == None)

        if prefixo:
            query = query.filter(Tag.numeracao.like(f'{prefixo}%'))

        numeracoes = [row[0] for row in query.all() if row[0]]

        if not numeracoes:
            return 0

        # Extrair números
        numeros = []
        for num in numeracoes:
            try:
                if prefixo:
                    # Ex: "V1" -> 1
                    numeros.append(int(num[len(prefixo):]))
                elif num and num[0].isdigit():
                    # Tags de conteúdo começam com dígito, ex: "1", "2", "10"
                    numeros.append(int(num.split('.')[0]))
            except (ValueError, IndexError):
                pass

        return max(numeros) if numeros else 0

    def obter_maior_numeracao_filha(self, uuid_pai: str) -> int:
        """
        Obtém o maior número usado em tags filhas (incluindo inativas).

        Args:
            uuid_pai: UUID da tag pai

        Returns:
            Maior número encontrado ou 0 se nenhum
        """
        query = self.session.query(Tag.numeracao).filter(Tag.uuid_tag_pai == uuid_pai)
        numeracoes = [row[0] for row in query.all() if row[0]]

        if not numeracoes:
            return 0

        # Extrair o último número da numeração (ex: "1.2.3" -> 3)
        numeros = []
        for num in numeracoes:
            try:
                ultimo = num.split('.')[-1]
                numeros.append(int(ultimo))
            except (ValueError, IndexError):
                pass

        return max(numeros) if numeros else 0

