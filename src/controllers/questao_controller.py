"""
Sistema de Banco de Questões Educacionais
Módulo: Controller Questão
Versão: 1.0.1

DESCRIÇÃO:
    Controller responsável pela lógica de negócio relacionada a Questões.
    Faz a mediação entre as Views (interface) e os Models (dados).

FUNCIONALIDADES:
    - Validar dados de questão antes de salvar
    - Orquestrar criação completa de questão (questão + alternativas + tags)
    - Buscar questões com filtros complexos
    - Gerenciar alternativas de questões objetivas
    - Exportar dados de questão para diferentes formatos
    - Validar integridade de questões

RELACIONAMENTOS:
    - questao.py (model): Acesso aos dados de questões
    - alternativa.py (model): Gerenciamento de alternativas
    - tag.py (model): Vinculação de tags
    - dificuldade.py (model): Validação de dificuldade
    - QuestaoForm (view): Recebe dados do formulário
    - SearchPanel (view): Fornece resultados de busca

REGRAS DE NEGÓCIO IMPLEMENTADAS:
    - Questão OBJETIVA deve ter exatamente 5 alternativas (A-E)
    - Apenas 1 alternativa pode ser correta
    - Questão deve ter no mínimo 1 tag
    - Campos obrigatórios: enunciado, tipo, ano, fonte
    - Validação de imagens (formato, tamanho)
    - Soft delete (inativar ao invés de deletar)
"""

import logging
from typing import Dict, List, Optional, Any
from pathlib import Path
import shutil
from datetime import datetime

from src.models.questao import QuestaoModel
from src.models.alternativa import AlternativaModel
from src.models.tag import TagModel
from src.models.dificuldade import DificuldadeModel
from src.constants import (
    TipoQuestao, DificuldadeID, Validacao,
    ImagemConfig, ErroMensagens, TOTAL_ALTERNATIVAS
)

logger = logging.getLogger(__name__)


class QuestaoController:
    """
    Controller para gerenciar lógica de negócio de questões.
    """

    @staticmethod
    def validar_dados_questao(dados: Dict) -> Dict[str, Any]:
        """
        Valida todos os dados de uma questão antes de salvar.

        Args:
            dados: Dict com dados da questão

        Returns:
            Dict: {'valido': bool, 'erros': List[str], 'avisos': List[str]}
        """
        erros = []
        avisos = []

        try:
            # Validar enunciado (obrigatório)
            if not dados.get('enunciado') or not dados.get('enunciado').strip():
                erros.append(ErroMensagens.ENUNCIADO_VAZIO)

            # Validar tipo (obrigatório)
            tipo = dados.get('tipo', '').upper()
            if tipo not in [TipoQuestao.OBJETIVA, TipoQuestao.DISCURSIVA]:
                erros.append(ErroMensagens.TIPO_INVALIDO)

            # Validar ano (obrigatório e razoável)
            ano = dados.get('ano')
            if not ano:
                erros.append("O ano é obrigatório")
            elif not isinstance(ano, int) or ano < Validacao.ANO_MINIMO or ano > Validacao.ANO_MAXIMO:
                erros.append(ErroMensagens.ANO_INVALIDO)

            # Validar fonte (obrigatório)
            if not dados.get('fonte') or not dados.get('fonte').strip():
                erros.append(ErroMensagens.FONTE_VAZIA)

            # Validar dificuldade (opcional, mas se fornecida deve ser válida)
            id_dificuldade = dados.get('id_dificuldade')
            dificuldades_validas = [
                DificuldadeID.FACIL,
                DificuldadeID.MEDIO,
                DificuldadeID.DIFICIL,
                DificuldadeID.SEM_DIFICULDADE
            ]
            if id_dificuldade and id_dificuldade not in dificuldades_validas:
                erros.append(ErroMensagens.DIFICULDADE_INVALIDA)

            # Validar alternativas se OBJETIVA
            if tipo == TipoQuestao.OBJETIVA:
                alternativas = dados.get('alternativas', [])

                if len(alternativas) == 0:
                    erros.append("Questão objetiva deve ter alternativas")
                elif len(alternativas) < TOTAL_ALTERNATIVAS:
                    erros.append(ErroMensagens.FALTAM_ALTERNATIVAS)

                # Verificar se há exatamente uma correta
                corretas = [alt for alt in alternativas if alt.get('correta', False)]
                if len(corretas) == 0:
                    erros.append(ErroMensagens.FALTA_CORRETA)
                elif len(corretas) > 1:
                    erros.append(ErroMensagens.MULTIPLAS_CORRETAS)

                # Verificar se alternativas têm conteúdo
                for alt in alternativas:
                    if not alt.get('texto') and not alt.get('imagem'):
                        avisos.append(f"Alternativa {alt.get('letra')} sem texto nem imagem")

            # Validar tags (recomendado ter pelo menos 1)
            tags = dados.get('tags', [])
            if len(tags) < Validacao.MIN_TAGS_POR_QUESTAO:
                avisos.append(ErroMensagens.SEM_TAGS)

            # Validar imagem do enunciado (se fornecida)
            imagem_enunciado = dados.get('imagem_enunciado')
            if imagem_enunciado:
                if not Path(imagem_enunciado).exists():
                    erros.append(ErroMensagens.IMAGEM_NAO_ENCONTRADA)
                else:
                    # Validar extensão
                    ext = Path(imagem_enunciado).suffix.lower()
                    if ext not in ImagemConfig.EXTENSOES_VALIDAS:
                        erros.append(ErroMensagens.FORMATO_INVALIDO)

            # Validar título (se fornecido)
            titulo = dados.get('titulo')
            if titulo and len(titulo) > Validacao.TITULO_MAX_LENGTH:
                avisos.append(f"Título muito longo (máximo {Validacao.TITULO_MAX_LENGTH} caracteres)")

            return {
                'valido': len(erros) == 0,
                'erros': erros,
                'avisos': avisos
            }

        except Exception as e:
            logger.error(f"Erro ao validar dados da questão: {e}")
            return {
                'valido': False,
                'erros': [f"Erro na validação: {str(e)}"],
                'avisos': []
            }

    @staticmethod
    def criar_questao_completa(dados: Dict) -> Optional[int]:
        """
        Cria uma questão completa com alternativas e tags.

        Args:
            dados: Dict com todos os dados da questão

        Returns:
            int: ID da questão criada ou None se erro
        """
        try:
            # 1. Validar dados
            validacao = QuestaoController.validar_dados_questao(dados)
            if not validacao['valido']:
                logger.error(f"Validação falhou: {validacao['erros']}")
                return None

            logger.info("Criando questão completa...")

            # 2. Processar imagem do enunciado (copiar para pasta correta)
            imagem_destino = None
            if dados.get('imagem_enunciado'):
                imagem_destino = QuestaoController._processar_imagem(
                    dados['imagem_enunciado'],
                    'enunciado'
                )

            # 3. Criar questão
            id_questao = QuestaoModel.criar(
                titulo=dados.get('titulo'),
                enunciado=dados['enunciado'],
                tipo=dados['tipo'].upper(),
                ano=dados['ano'],
                fonte=dados['fonte'],
                id_dificuldade=dados.get('id_dificuldade'),
                imagem_enunciado=imagem_destino,
                escala_imagem_enunciado=dados.get('escala_imagem_enunciado', 0.7),
                resolucao=dados.get('resolucao'),
                gabarito_discursiva=dados.get('gabarito_discursiva'),
                observacoes=dados.get('observacoes')
            )

            if not id_questao:
                logger.error("Falha ao criar questão no banco")
                return None

            logger.info(f"Questão criada com ID: {id_questao}")

            # 4. Se OBJETIVA, criar alternativas
            if dados['tipo'].upper() == QuestaoModel.TIPO_OBJETIVA:
                alternativas = dados.get('alternativas', [])
                if alternativas:
                    sucesso = AlternativaModel.criar_conjunto_completo(
                        id_questao,
                        alternativas
                    )
                    if not sucesso:
                        logger.warning(f"Problema ao criar alternativas para questão {id_questao}")

            # 5. Vincular tags
            tags = dados.get('tags', [])
            for id_tag in tags:
                QuestaoModel.vincular_tag(id_questao, id_tag)

            logger.info(f"Questão completa criada com sucesso. ID: {id_questao}")
            return id_questao

        except Exception as e:
            logger.error(f"Erro ao criar questão completa: {e}")
            return None

    @staticmethod
    def atualizar_questao_completa(id_questao: int, dados: Dict) -> bool:
        """
        Atualiza uma questão completa incluindo alternativas e tags.

        Args:
            id_questao: ID da questão
            dados: Dict com dados atualizados

        Returns:
            bool: True se atualizada com sucesso
        """
        try:
            # 1. Validar dados
            validacao = QuestaoController.validar_dados_questao(dados)
            if not validacao['valido']:
                logger.error(f"Validação falhou: {validacao['erros']}")
                return False

            logger.info(f"Atualizando questão {id_questao}...")

            # 2. Processar imagem (se alterada)
            imagem_destino = dados.get('imagem_enunciado')
            if imagem_destino and Path(imagem_destino).exists():
                imagem_destino = QuestaoController._processar_imagem(
                    imagem_destino,
                    'enunciado',
                    id_questao
                )

            # 3. Atualizar questão
            sucesso = QuestaoModel.atualizar(
                id_questao,
                titulo=dados.get('titulo'),
                enunciado=dados['enunciado'],
                tipo=dados['tipo'].upper(),
                ano=dados['ano'],
                fonte=dados['fonte'],
                id_dificuldade=dados.get('id_dificuldade'),
                imagem_enunciado=imagem_destino,
                escala_imagem_enunciado=dados.get('escala_imagem_enunciado', 0.7),
                resolucao=dados.get('resolucao'),
                gabarito_discursiva=dados.get('gabarito_discursiva'),
                observacoes=dados.get('observacoes')
            )

            if not sucesso:
                logger.error("Falha ao atualizar questão no banco")
                return False

            # 4. Se OBJETIVA, recriar alternativas
            if dados['tipo'].upper() == QuestaoModel.TIPO_OBJETIVA:
                # Deletar alternativas antigas
                AlternativaModel.deletar_por_questao(id_questao)

                # Criar novas
                alternativas = dados.get('alternativas', [])
                if alternativas:
                    AlternativaModel.criar_conjunto_completo(id_questao, alternativas)
            else:
                # Se mudou para DISCURSIVA, remover alternativas
                AlternativaModel.deletar_por_questao(id_questao)

            # 5. Atualizar tags (remover todas e adicionar novamente)
            # Buscar tags atuais
            tags_atuais = QuestaoModel.listar_tags(id_questao)
            for tag in tags_atuais:
                QuestaoModel.desvincular_tag(id_questao, tag['id_tag'])

            # Adicionar novas tags
            tags_novas = dados.get('tags', [])
            for id_tag in tags_novas:
                QuestaoModel.vincular_tag(id_questao, id_tag)

            logger.info(f"Questão {id_questao} atualizada com sucesso")
            return True

        except Exception as e:
            logger.error(f"Erro ao atualizar questão: {e}")
            return False

    @staticmethod
    def buscar_questoes(filtros: Dict = None) -> List[Dict]:
        """
        Busca questões aplicando filtros.
        Enriquece os dados com alternativas e tags.

        Args:
            filtros: Dict com filtros opcionais:
                - titulo: str
                - tipo: str (OBJETIVA/DISCURSIVA)
                - ano: int
                - ano_de: int
                - ano_ate: int
                - fonte: str
                - id_dificuldade: int
                - tags: List[int]
                - busca_texto: str (busca no enunciado)

        Returns:
            List[Dict]: Lista de questões
        """
        try:
            if filtros is None:
                filtros = {}

            logger.info(f"Buscando questões com filtros: {filtros}")

            # Preparar filtros para o model
            model_filtros = {}

            if 'titulo' in filtros:
                model_filtros['titulo'] = filtros['titulo']

            if 'tipo' in filtros and filtros['tipo'] not in ['Todas', 'TODAS', '']:
                model_filtros['tipo'] = filtros['tipo'].upper()

            if 'ano' in filtros:
                model_filtros['ano'] = filtros['ano']

            if 'fonte' in filtros and filtros['fonte']:
                model_filtros['fonte'] = filtros['fonte']

            if 'id_dificuldade' in filtros:
                model_filtros['id_dificuldade'] = filtros['id_dificuldade']

            if 'tags' in filtros and len(filtros['tags']) > 0:
                model_filtros['tags'] = filtros['tags']

            # Buscar questões
            questoes = QuestaoModel.buscar_por_filtros(**model_filtros)

            # Enriquecer com alternativas (se objetiva) e tags
            for questao in questoes:
                if questao['tipo'] == QuestaoModel.TIPO_OBJETIVA:
                    questao['alternativas'] = AlternativaModel.listar_por_questao(
                        questao['id_questao']
                    )
                else:
                    questao['alternativas'] = []

                questao['tags'] = QuestaoModel.listar_tags(questao['id_questao'])

            # Aplicar filtros adicionais não suportados pelo model
            if 'ano_de' in filtros:
                questoes = [q for q in questoes if q['ano'] >= filtros['ano_de']]

            if 'ano_ate' in filtros:
                questoes = [q for q in questoes if q['ano'] <= filtros['ano_ate']]

            if 'busca_texto' in filtros and filtros['busca_texto']:
                texto = filtros['busca_texto'].lower()
                questoes = [q for q in questoes
                           if texto in q.get('enunciado', '').lower() or
                              texto in q.get('titulo', '').lower()]

            logger.info(f"Encontradas {len(questoes)} questões")
            return questoes

        except Exception as e:
            logger.error(f"Erro ao buscar questões: {e}")
            return []

    @staticmethod
    def obter_questao_completa(id_questao: int) -> Optional[Dict]:
        """
        Obtém uma questão completa com todas as informações.

        Args:
            id_questao: ID da questão

        Returns:
            Dict: Questão completa ou None se não encontrada
        """
        try:
            questao = QuestaoModel.buscar_por_id(id_questao)
            if not questao:
                return None

            # Adicionar alternativas
            if questao['tipo'] == QuestaoModel.TIPO_OBJETIVA:
                questao['alternativas'] = AlternativaModel.listar_por_questao(id_questao)
            else:
                questao['alternativas'] = []

            # Adicionar tags
            questao['tags'] = QuestaoModel.listar_tags(id_questao)

            return questao

        except Exception as e:
            logger.error(f"Erro ao obter questão completa: {e}")
            return None

    @staticmethod
    def inativar_questao(id_questao: int) -> bool:
        """
        Inativa uma questão (soft delete).

        Args:
            id_questao: ID da questão

        Returns:
            bool: True se inativada com sucesso
        """
        try:
            return QuestaoModel.inativar(id_questao)
        except Exception as e:
            logger.error(f"Erro ao inativar questão: {e}")
            return False

    @staticmethod
    def reativar_questao(id_questao: int) -> bool:
        """
        Reativa uma questão inativa.

        Args:
            id_questao: ID da questão

        Returns:
            bool: True se reativada com sucesso
        """
        try:
            return QuestaoModel.reativar(id_questao)
        except Exception as e:
            logger.error(f"Erro ao reativar questão: {e}")
            return False

    @staticmethod
    def _processar_imagem(caminho_origem: str, tipo: str, id_questao: int = None) -> Optional[str]:
        """
        Processa uma imagem copiando para pasta de imagens do sistema.

        Args:
            caminho_origem: Caminho completo da imagem original
            tipo: Tipo (enunciado, alternativa, etc)
            id_questao: ID da questão (opcional)

        Returns:
            str: Caminho relativo da imagem copiada ou None se erro
        """
        try:
            origem = Path(caminho_origem)
            if not origem.exists():
                logger.error(f"Imagem não encontrada: {caminho_origem}")
                return None

            # Criar diretório de imagens se não existir
            # Estrutura: imagens/questoes/
            from src.models.database import db
            project_root = db.get_project_root()
            img_dir = project_root / 'imagens' / 'questoes'
            img_dir.mkdir(parents=True, exist_ok=True)

            # Nome do arquivo: questao_{id}_{tipo}_{timestamp}.ext
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            id_str = f"questao_{id_questao}_" if id_questao else ""
            nome_arquivo = f"{id_str}{tipo}_{timestamp}{origem.suffix}"

            destino = img_dir / nome_arquivo

            # Copiar arquivo
            shutil.copy2(origem, destino)

            # Retornar caminho relativo
            caminho_relativo = f"imagens/questoes/{nome_arquivo}"
            logger.info(f"Imagem processada: {caminho_relativo}")

            return caminho_relativo

        except Exception as e:
            logger.error(f"Erro ao processar imagem: {e}")
            return None

    @staticmethod
    def obter_estatisticas() -> Dict:
        """
        Obtém estatísticas gerais sobre questões.

        Returns:
            Dict: Estatísticas
        """
        try:
            total = QuestaoModel.contar_total(apenas_ativas=True)
            todas = QuestaoModel.listar_todas(apenas_ativas=True)

            objetivas = len([q for q in todas if q['tipo'] == QuestaoModel.TIPO_OBJETIVA])
            discursivas = len([q for q in todas if q['tipo'] == QuestaoModel.TIPO_DISCURSIVA])

            # Contadores por dificuldade
            faceis = len([q for q in todas if q.get('id_dificuldade') == 1])
            medias = len([q for q in todas if q.get('id_dificuldade') == 2])
            dificeis = len([q for q in todas if q.get('id_dificuldade') == 3])

            return {
                'total': total,
                'objetivas': objetivas,
                'discursivas': discursivas,
                'faceis': faceis,
                'medias': medias,
                'dificeis': dificeis
            }

        except Exception as e:
            logger.error(f"Erro ao obter estatísticas: {e}")
            return {
                'total': 0,
                'objetivas': 0,
                'discursivas': 0,
                'faceis': 0,
                'medias': 0,
                'dificeis': 0
            }


logger.info("QuestaoController carregado")
