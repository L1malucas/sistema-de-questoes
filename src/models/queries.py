"""
Sistema de Banco de Questões Educacionais
Módulo: SQL Queries
Versão: 1.0.1

DESCRIÇÃO:
    Centralização de queries SQL reutilizáveis.
    Facilita manutenção e evita duplicação de código SQL.

BENEFÍCIOS:
    - Queries em um único lugar
    - Fácil de manter e atualizar
    - Previne inconsistências
    - Facilita otimizações futuras
"""

from src.constants import DatabaseConfig


class QuestaoQueries:
    """Queries SQL relacionadas à tabela questao"""

    # SELECT queries
    SELECT_BASE = """
        SELECT
            q.*,
            d.nome as dificuldade_nome
        FROM questao q
        LEFT JOIN dificuldade d ON q.id_dificuldade = d.id_dificuldade
    """

    SELECT_BY_ID = SELECT_BASE + """
        WHERE q.id_questao = ?
    """

    SELECT_BY_ID_ATIVAS = SELECT_BASE + """
        WHERE q.id_questao = ? AND q.ativo = 1
    """

    SELECT_ALL = SELECT_BASE + """
        WHERE q.ativo = 1
        ORDER BY q.data_criacao DESC
    """

    SELECT_ALL_WITH_INATIVAS = SELECT_BASE + """
        ORDER BY q.data_criacao DESC
    """

    # INSERT queries
    INSERT = """
        INSERT INTO questao (
            titulo, enunciado, tipo, ano, fonte, id_dificuldade,
            imagem_enunciado, escala_imagem_enunciado, resolucao,
            gabarito_discursiva, observacoes, ativo
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 1)
    """

    # UPDATE queries
    UPDATE_BASE = """
        UPDATE questao
        SET data_modificacao = CURRENT_TIMESTAMP
    """

    UPDATE_STATUS = """
        UPDATE questao
        SET ativo = ?
        WHERE id_questao = ?
    """

    # COUNT queries
    COUNT_TOTAL = """
        SELECT COUNT(*) as total
        FROM questao
        WHERE ativo = 1
    """

    COUNT_TOTAL_WITH_INATIVAS = """
        SELECT COUNT(*) as total
        FROM questao
    """


class AlternativaQueries:
    """Queries SQL relacionadas à tabela alternativa"""

    # SELECT queries
    SELECT_BY_QUESTAO = """
        SELECT *
        FROM alternativa
        WHERE id_questao = ?
        ORDER BY letra
    """

    SELECT_CORRETA = """
        SELECT *
        FROM alternativa
        WHERE id_questao = ? AND correta = 1
        LIMIT 1
    """

    SELECT_BY_ID = """
        SELECT *
        FROM alternativa
        WHERE id_alternativa = ?
    """

    # INSERT queries
    INSERT = """
        INSERT INTO alternativa (
            id_questao, letra, texto, imagem, escala_imagem, correta
        )
        VALUES (?, ?, ?, ?, ?, ?)
    """

    # UPDATE queries
    UPDATE = """
        UPDATE alternativa
        SET texto = ?, imagem = ?, escala_imagem = ?, correta = ?
        WHERE id_alternativa = ?
    """

    # DELETE queries
    DELETE_BY_ID = """
        DELETE FROM alternativa
        WHERE id_alternativa = ?
    """

    DELETE_BY_QUESTAO = """
        DELETE FROM alternativa
        WHERE id_questao = ?
    """

    # Validação
    CHECK_ALTERNATIVA_CORRETA_EXISTS = """
        SELECT COUNT(*) as total
        FROM alternativa
        WHERE id_questao = ? AND correta = 1
    """


class TagQueries:
    """Queries SQL relacionadas à tabela tag"""

    # SELECT queries
    SELECT_ALL = """
        SELECT *
        FROM tag
        WHERE ativo = 1
        ORDER BY ordem, numeracao
    """

    SELECT_BY_ID = """
        SELECT *
        FROM tag
        WHERE id_tag = ?
    """

    SELECT_BY_ID_ATIVAS = """
        SELECT *
        FROM tag
        WHERE id_tag = ? AND ativo = 1
    """

    SELECT_BY_PAI = """
        SELECT *
        FROM tag
        WHERE id_tag_pai = ? AND ativo = 1
        ORDER BY ordem
    """

    SELECT_RAIZES = """
        SELECT *
        FROM tag
        WHERE id_tag_pai IS NULL AND ativo = 1
        ORDER BY ordem
    """

    # INSERT queries
    INSERT = """
        INSERT INTO tag (
            nome, numeracao, nivel, id_tag_pai, ordem, ativo
        )
        VALUES (?, ?, ?, ?, ?, 1)
    """

    # UPDATE queries
    UPDATE = """
        UPDATE tag
        SET nome = ?, numeracao = ?, nivel = ?, id_tag_pai = ?, ordem = ?
        WHERE id_tag = ?
    """

    UPDATE_STATUS = """
        UPDATE tag
        SET ativo = ?
        WHERE id_tag = ?
    """

    # Relacionamentos
    SELECT_TAGS_BY_QUESTAO = """
        SELECT t.*
        FROM tag t
        JOIN questao_tag qt ON t.id_tag = qt.id_tag
        WHERE qt.id_questao = ? AND t.ativo = 1
        ORDER BY t.ordem
    """


class QuestaoTagQueries:
    """Queries SQL relacionadas à tabela questao_tag (N:N)"""

    # INSERT queries
    INSERT = """
        INSERT OR IGNORE INTO questao_tag (id_questao, id_tag)
        VALUES (?, ?)
    """

    # DELETE queries
    DELETE = """
        DELETE FROM questao_tag
        WHERE id_questao = ? AND id_tag = ?
    """

    DELETE_ALL_BY_QUESTAO = """
        DELETE FROM questao_tag
        WHERE id_questao = ?
    """

    # SELECT queries
    SELECT_QUESTOES_BY_TAG = """
        SELECT q.*, d.nome as dificuldade_nome
        FROM questao q
        LEFT JOIN dificuldade d ON q.id_dificuldade = d.id_dificuldade
        JOIN questao_tag qt ON q.id_questao = qt.id_questao
        WHERE qt.id_tag = ? AND q.ativo = 1
        ORDER BY q.data_criacao DESC
    """


class ListaQueries:
    """Queries SQL relacionadas à tabela lista"""

    # SELECT queries
    SELECT_ALL = """
        SELECT *
        FROM lista
        ORDER BY data_criacao DESC
    """

    SELECT_BY_ID = """
        SELECT *
        FROM lista
        WHERE id_lista = ?
    """

    # INSERT queries
    INSERT = """
        INSERT INTO lista (
            titulo, tipo, cabecalho, instrucoes
        )
        VALUES (?, ?, ?, ?)
    """

    # UPDATE queries
    UPDATE = """
        UPDATE lista
        SET titulo = ?, tipo = ?, cabecalho = ?, instrucoes = ?
        WHERE id_lista = ?
    """

    # DELETE queries
    DELETE = """
        DELETE FROM lista
        WHERE id_lista = ?
    """


class ListaQuestaoQueries:
    """Queries SQL relacionadas à tabela lista_questao (N:N)"""

    # INSERT queries
    INSERT = """
        INSERT INTO lista_questao (
            id_lista, id_questao, ordem
        )
        VALUES (?, ?, ?)
    """

    # DELETE queries
    DELETE = """
        DELETE FROM lista_questao
        WHERE id_lista = ? AND id_questao = ?
    """

    DELETE_ALL_BY_LISTA = """
        DELETE FROM lista_questao
        WHERE id_lista = ?
    """

    # SELECT queries
    SELECT_QUESTOES_BY_LISTA = """
        SELECT q.*, lq.ordem, d.nome as dificuldade_nome
        FROM questao q
        LEFT JOIN dificuldade d ON q.id_dificuldade = d.id_dificuldade
        JOIN lista_questao lq ON q.id_questao = lq.id_questao
        WHERE lq.id_lista = ?
        ORDER BY lq.ordem
    """

    COUNT_QUESTOES_BY_LISTA = """
        SELECT COUNT(*) as total
        FROM lista_questao
        WHERE id_lista = ?
    """


class DificuldadeQueries:
    """Queries SQL relacionadas à tabela dificuldade"""

    # SELECT queries
    SELECT_ALL = """
        SELECT *
        FROM dificuldade
        ORDER BY ordem
    """

    SELECT_BY_ID = """
        SELECT *
        FROM dificuldade
        WHERE id_dificuldade = ?
    """

    SELECT_BY_NOME = """
        SELECT *
        FROM dificuldade
        WHERE nome = ?
    """


class QuestaoVersaoQueries:
    """Queries SQL relacionadas à tabela questao_versao"""

    # INSERT queries
    INSERT = """
        INSERT OR IGNORE INTO questao_versao (
            id_questao_original, id_questao_versao, observacao
        )
        VALUES (?, ?, ?)
    """

    # SELECT queries
    SELECT_VERSOES = """
        SELECT q.*, qv.observacao
        FROM questao q
        JOIN questao_versao qv ON q.id_questao = qv.id_questao_versao
        WHERE qv.id_questao_original = ? AND q.ativo = 1
    """

    SELECT_ORIGINAL = """
        SELECT q.*
        FROM questao q
        JOIN questao_versao qv ON q.id_questao = qv.id_questao_original
        WHERE qv.id_questao_versao = ?
    """


class CommonQueries:
    """Queries SQL comuns usadas em múltiplas tabelas"""

    @staticmethod
    def build_where_clause(filters: dict) -> tuple[str, list]:
        """
        Constrói cláusula WHERE dinamicamente de forma segura.

        Args:
            filters: Dict com filtros {campo: valor}

        Returns:
            tuple: (where_clause, params)
        """
        conditions = []
        params = []

        for field, value in filters.items():
            if value is not None:
                conditions.append(f"{field} = ?")
                params.append(value)

        where_clause = " AND ".join(conditions) if conditions else ""
        return where_clause, params

    @staticmethod
    def build_in_clause(field: str, values: list) -> tuple[str, list]:
        """
        Constrói cláusula IN de forma segura.

        Args:
            field: Nome do campo
            values: Lista de valores

        Returns:
            tuple: (in_clause, params)
        """
        if not values:
            return "", []

        placeholders = ','.join(['?' for _ in values])
        in_clause = f"{field} IN ({placeholders})"
        return in_clause, values

    @staticmethod
    def build_pagination(limit: int = None, offset: int = 0) -> str:
        """
        Constrói cláusula de paginação.

        Args:
            limit: Número máximo de resultados
            offset: Deslocamento

        Returns:
            str: Cláusula SQL de paginação
        """
        pagination = ""

        if limit is not None and limit > 0:
            pagination += f" LIMIT {int(limit)}"

        if offset > 0:
            pagination += f" OFFSET {int(offset)}"

        return pagination

    # Campos de ordenação válidos (whitelist)
    VALID_ORDER_BY_QUESTAO = {
        "data_criacao DESC", "data_criacao ASC",
        "titulo ASC", "titulo DESC",
        "ano DESC", "ano ASC",
        "fonte ASC", "fonte DESC",
        "tipo ASC", "tipo DESC",
        "id_dificuldade ASC", "id_dificuldade DESC"
    }

    VALID_ORDER_BY_TAG = {
        "ordem ASC", "ordem DESC",
        "nome ASC", "nome DESC",
        "numeracao ASC", "numeracao DESC"
    }

    VALID_ORDER_BY_LISTA = {
        "data_criacao DESC", "data_criacao ASC",
        "titulo ASC", "titulo DESC"
    }


# Constantes de tabelas (para referência)
TABELAS = {
    'QUESTAO': DatabaseConfig.TABELA_QUESTAO,
    'ALTERNATIVA': DatabaseConfig.TABELA_ALTERNATIVA,
    'TAG': DatabaseConfig.TABELA_TAG,
    'DIFICULDADE': DatabaseConfig.TABELA_DIFICULDADE,
    'QUESTAO_TAG': DatabaseConfig.TABELA_QUESTAO_TAG,
    'LISTA': DatabaseConfig.TABELA_LISTA,
    'LISTA_QUESTAO': DatabaseConfig.TABELA_LISTA_QUESTAO,
    'QUESTAO_VERSAO': DatabaseConfig.TABELA_QUESTAO_VERSAO,
    'CONFIGURACAO': DatabaseConfig.TABELA_CONFIGURACAO
}
