"""
Repository Implementation: Tag
DESCRIÇÃO: Implementação concreta do repositório de tags
PADRÃO: Adapter para TagModel existente
"""

import logging
from typing import Optional, Dict, List, Any

from src.domain.interfaces import ITagRepository
from src.models.tag import TagModel

logger = logging.getLogger(__name__)


class TagRepositoryImpl(ITagRepository):
    """Implementação de repositório de tags"""

    def criar(
        self,
        nome: str,
        nivel: int,
        id_pai: Optional[int] = None
    ) -> Optional[int]:
        """Cria uma tag"""
        try:
            id_tag = TagModel.criar(
                nome=nome,
                nivel=nivel,
                id_pai=id_pai
            )

            if id_tag:
                logger.info(f"Tag criada: {nome} (nível {nivel})")

            return id_tag

        except Exception as e:
            logger.error(f"Erro ao criar tag: {e}", exc_info=True)
            return None

    def buscar_por_id(self, id_tag: int) -> Optional[Dict[str, Any]]:
        """Busca tag por ID"""
        try:
            tag = TagModel.buscar_por_id(id_tag)
            return tag

        except Exception as e:
            logger.error(f"Erro ao buscar tag: {e}", exc_info=True)
            return None

    def buscar_todas(self, nivel: Optional[int] = None) -> List[Dict[str, Any]]:
        """Busca todas as tags"""
        try:
            if nivel is not None:
                tags = TagModel.buscar_por_nivel(nivel)
            else:
                tags = TagModel.listar_todas()

            logger.debug(f"Tags obtidas: {len(tags)}")
            return tags

        except Exception as e:
            logger.error(f"Erro ao buscar tags: {e}", exc_info=True)
            return []

    def buscar_filhas(self, id_tag: int) -> List[Dict[str, Any]]:
        """Busca tags filhas de uma tag pai"""
        try:
            tags = TagModel.buscar_filhas(id_tag)
            logger.debug(f"Tags filhas: {len(tags)} (pai: {id_tag})")
            return tags

        except Exception as e:
            logger.error(f"Erro ao buscar tags filhas: {e}", exc_info=True)
            return []

    def buscar_hierarquia_completa(self) -> List[Dict[str, Any]]:
        """Busca toda hierarquia de tags"""
        try:
            hierarquia = TagModel.obter_hierarquia_completa()
            logger.debug("Hierarquia de tags obtida")
            return hierarquia

        except Exception as e:
            logger.error(f"Erro ao buscar hierarquia: {e}", exc_info=True)
            return []

    def atualizar(
        self,
        id_tag: int,
        nome: Optional[str] = None,
        nivel: Optional[int] = None,
        id_pai: Optional[int] = None
    ) -> bool:
        """Atualiza uma tag"""
        try:
            kwargs = {}

            if nome is not None:
                kwargs['nome'] = nome

            if nivel is not None:
                kwargs['nivel'] = nivel

            if id_pai is not None:
                kwargs['id_pai'] = id_pai

            sucesso = TagModel.atualizar(id_tag, **kwargs)

            if sucesso:
                logger.info(f"Tag atualizada: ID {id_tag}")

            return sucesso

        except Exception as e:
            logger.error(f"Erro ao atualizar tag: {e}", exc_info=True)
            return False

    def deletar(self, id_tag: int) -> bool:
        """Deleta uma tag"""
        try:
            sucesso = TagModel.deletar(id_tag)

            if sucesso:
                logger.info(f"Tag deletada: ID {id_tag}")

            return sucesso

        except Exception as e:
            logger.error(f"Erro ao deletar tag: {e}", exc_info=True)
            return False
