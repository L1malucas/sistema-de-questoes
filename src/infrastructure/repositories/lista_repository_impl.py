"""
Repository Implementation: Lista
DESCRIÇÃO: Implementação concreta do repositório de listas
PADRÃO: Adapter para ListaModel existente
"""

import logging
from typing import Optional, Dict, List, Any

from src.domain.interfaces import IListaRepository
from src.models.lista import ListaModel

logger = logging.getLogger(__name__)


class ListaRepositoryImpl(IListaRepository):
    """Implementação de repositório de listas"""

    def criar(
        self,
        titulo: str,
        tipo: Optional[str] = None,
        cabecalho: Optional[str] = None,
        instrucoes: Optional[str] = None
    ) -> Optional[int]:
        """Cria uma lista"""
        try:
            kwargs = {'titulo': titulo}

            if tipo is not None:
                kwargs['tipo'] = tipo

            if cabecalho is not None:
                kwargs['cabecalho'] = cabecalho

            if instrucoes is not None:
                kwargs['instrucoes'] = instrucoes

            id_lista = ListaModel.criar(**kwargs)

            if id_lista:
                logger.info(f"Lista criada: {titulo}")

            return id_lista

        except Exception as e:
            logger.error(f"Erro ao criar lista: {e}", exc_info=True)
            return None

    def buscar_por_id(self, id_lista: int) -> Optional[Dict[str, Any]]:
        """Busca lista por ID"""
        try:
            lista = ListaModel.buscar_por_id(id_lista)
            return lista

        except Exception as e:
            logger.error(f"Erro ao buscar lista: {e}", exc_info=True)
            return None

    def buscar_todas(self) -> List[Dict[str, Any]]:
        """Busca todas as listas"""
        try:
            listas = ListaModel.listar_todas()
            logger.debug(f"Listas obtidas: {len(listas)}")
            return listas

        except Exception as e:
            logger.error(f"Erro ao buscar listas: {e}", exc_info=True)
            return []

    def atualizar(
        self,
        id_lista: int,
        titulo: Optional[str] = None,
        tipo: Optional[str] = None,
        cabecalho: Optional[str] = None,
        instrucoes: Optional[str] = None
    ) -> bool:
        """Atualiza uma lista"""
        try:
            kwargs = {}

            if titulo is not None:
                kwargs['titulo'] = titulo

            if tipo is not None:
                kwargs['tipo'] = tipo

            if cabecalho is not None:
                kwargs['cabecalho'] = cabecalho

            if instrucoes is not None:
                kwargs['instrucoes'] = instrucoes

            sucesso = ListaModel.atualizar(id_lista, **kwargs)

            if sucesso:
                logger.info(f"Lista atualizada: ID {id_lista}")

            return sucesso

        except Exception as e:
            logger.error(f"Erro ao atualizar lista: {e}", exc_info=True)
            return False

    def deletar(self, id_lista: int) -> bool:
        """Deleta uma lista"""
        try:
            sucesso = ListaModel.deletar(id_lista)

            if sucesso:
                logger.info(f"Lista deletada: ID {id_lista}")

            return sucesso

        except Exception as e:
            logger.error(f"Erro ao deletar lista: {e}", exc_info=True)
            return False

    def adicionar_questao(
        self,
        id_lista: int,
        id_questao: int,
        ordem: int
    ) -> bool:
        """Adiciona questão a uma lista"""
        try:
            sucesso = ListaModel.adicionar_questao(id_lista, id_questao, ordem)

            if sucesso:
                logger.info(
                    f"Questão adicionada: lista {id_lista} <- questão {id_questao}"
                )

            return sucesso

        except Exception as e:
            logger.error(f"Erro ao adicionar questão à lista: {e}", exc_info=True)
            return False

    def remover_questao(self, id_lista: int, id_questao: int) -> bool:
        """Remove questão de uma lista"""
        try:
            sucesso = ListaModel.remover_questao(id_lista, id_questao)

            if sucesso:
                logger.info(
                    f"Questão removida: lista {id_lista} X questão {id_questao}"
                )

            return sucesso

        except Exception as e:
            logger.error(f"Erro ao remover questão da lista: {e}", exc_info=True)
            return False

    def obter_questoes(self, id_lista: int) -> List[Dict[str, Any]]:
        """Obtém questões de uma lista"""
        try:
            questoes = ListaModel.obter_questoes(id_lista)
            logger.debug(f"Questões da lista {id_lista}: {len(questoes)}")
            return questoes

        except Exception as e:
            logger.error(f"Erro ao obter questões da lista: {e}", exc_info=True)
            return []

    def reordenar_questoes(
        self,
        id_lista: int,
        questoes_ordem: List[tuple[int, int]]
    ) -> bool:
        """Reordena questões de uma lista"""
        try:
            sucesso = ListaModel.reordenar_questoes(id_lista, questoes_ordem)

            if sucesso:
                logger.info(
                    f"Questões reordenadas: lista {id_lista} "
                    f"({len(questoes_ordem)} questões)"
                )

            return sucesso

        except Exception as e:
            logger.error(f"Erro ao reordenar questões: {e}", exc_info=True)
            return False
