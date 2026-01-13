"""
Sistema de Banco de Questões Educacionais
Módulo: Exceptions
Versão: 1.0.1

DESCRIÇÃO:
    Exceções customizadas para tratamento de erros padronizado.
    Facilita debugging e fornece mensagens claras para o usuário.

BENEFÍCIOS:
    - Tratamento de erros consistente
    - Mensagens de erro claras e acionáveis
    - Facilita logging e debugging
    - Separação entre erros de sistema e de negócio
"""

from typing import Optional, Dict, Any


class BaseQuestaoException(Exception):
    """Classe base para todas as exceções do sistema"""

    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        """
        Args:
            message: Mensagem de erro para o usuário
            details: Detalhes adicionais para debugging
        """
        self.message = message
        self.details = details or {}
        super().__init__(self.message)

    def to_dict(self) -> Dict[str, Any]:
        """Converte exceção para dicionário"""
        return {
            'error': self.__class__.__name__,
            'message': self.message,
            'details': self.details
        }


# ============================================
# EXCEÇÕES DE VALIDAÇÃO
# ============================================

class ValidationError(BaseQuestaoException):
    """Erro de validação de dados"""
    pass


class EnunciadoVazioError(ValidationError):
    """Enunciado da questão está vazio"""

    def __init__(self):
        super().__init__("O enunciado é obrigatório e não pode estar vazio")


class TipoInvalidoError(ValidationError):
    """Tipo de questão inválido"""

    def __init__(self, tipo: str):
        super().__init__(
            "Tipo de questão inválido. Deve ser OBJETIVA ou DISCURSIVA",
            details={'tipo_fornecido': tipo}
        )


class AnoInvalidoError(ValidationError):
    """Ano da questão inválido"""

    def __init__(self, ano: int, ano_min: int, ano_max: int):
        super().__init__(
            f"Ano inválido. Deve estar entre {ano_min} e {ano_max}",
            details={'ano_fornecido': ano, 'ano_min': ano_min, 'ano_max': ano_max}
        )


class AlternativasInvalidasError(ValidationError):
    """Número ou conteúdo de alternativas inválido"""

    def __init__(self, total: int, esperado: int):
        super().__init__(
            f"Questão objetiva deve ter {esperado} alternativas (encontradas: {total})",
            details={'total_encontrado': total, 'total_esperado': esperado}
        )


class AlternativaCorretaInvalidaError(ValidationError):
    """Problema com alternativa correta"""

    def __init__(self, total_corretas: int):
        if total_corretas == 0:
            message = "Nenhuma alternativa foi marcada como correta"
        else:
            message = f"Apenas uma alternativa pode ser correta (encontradas: {total_corretas})"

        super().__init__(message, details={'total_corretas': total_corretas})


class ImagemInvalidaError(ValidationError):
    """Imagem inválida ou não encontrada"""

    def __init__(self, caminho: str, motivo: str):
        super().__init__(
            f"Imagem inválida: {motivo}",
            details={'caminho': caminho, 'motivo': motivo}
        )


# ============================================
# EXCEÇÕES DE BANCO DE DADOS
# ============================================

class DatabaseError(BaseQuestaoException):
    """Erro genérico de banco de dados"""
    pass


class RecordNotFoundError(DatabaseError):
    """Registro não encontrado"""

    def __init__(self, entidade: str, id_valor: Any):
        super().__init__(
            f"{entidade} não encontrada",
            details={'entidade': entidade, 'id': id_valor}
        )


class DuplicateRecordError(DatabaseError):
    """Tentativa de criar registro duplicado"""

    def __init__(self, entidade: str, campo: str, valor: Any):
        super().__init__(
            f"{entidade} já existe com {campo} = {valor}",
            details={'entidade': entidade, 'campo': campo, 'valor': valor}
        )


class ForeignKeyError(DatabaseError):
    """Erro de chave estrangeira"""

    def __init__(self, entidade: str, relacionamento: str):
        super().__init__(
            f"Não é possível remover {entidade} porque existem {relacionamento} relacionados",
            details={'entidade': entidade, 'relacionamento': relacionamento}
        )


class ConnectionError(DatabaseError):
    """Erro de conexão com banco de dados"""

    def __init__(self, detalhes: str):
        super().__init__(
            "Erro ao conectar ao banco de dados",
            details={'detalhes': detalhes}
        )


# ============================================
# EXCEÇÕES DE NEGÓCIO
# ============================================

class BusinessRuleError(BaseQuestaoException):
    """Erro de regra de negócio"""
    pass


class QuestaoInativaError(BusinessRuleError):
    """Tentativa de usar questão inativa"""

    def __init__(self, id_questao: int):
        super().__init__(
            "Esta questão está inativa e não pode ser utilizada",
            details={'id_questao': id_questao}
        )


class TagInativaError(BusinessRuleError):
    """Tentativa de usar tag inativa"""

    def __init__(self, id_tag: int):
        super().__init__(
            "Esta tag está inativa e não pode ser utilizada",
            details={'id_tag': id_tag}
        )


class ListaVaziaError(BusinessRuleError):
    """Lista sem questões"""

    def __init__(self, id_lista: int):
        super().__init__(
            "A lista não contém questões",
            details={'id_lista': id_lista}
        )


# ============================================
# EXCEÇÕES DE ARQUIVO
# ============================================

class FileError(BaseQuestaoException):
    """Erro relacionado a arquivos"""
    pass


class FileNotFoundError(FileError):
    """Arquivo não encontrado"""

    def __init__(self, caminho: str):
        super().__init__(
            f"Arquivo não encontrado: {caminho}",
            details={'caminho': caminho}
        )


class InvalidFileFormatError(FileError):
    """Formato de arquivo inválido"""

    def __init__(self, formato_encontrado: str, formatos_validos: list):
        super().__init__(
            f"Formato de arquivo inválido: {formato_encontrado}. " +
            f"Formatos válidos: {', '.join(formatos_validos)}",
            details={
                'formato_encontrado': formato_encontrado,
                'formatos_validos': formatos_validos
            }
        )


class FileSizeExceededError(FileError):
    """Arquivo excede tamanho máximo"""

    def __init__(self, tamanho_mb: float, max_mb: float):
        super().__init__(
            f"Arquivo muito grande ({tamanho_mb:.2f}MB). Tamanho máximo: {max_mb}MB",
            details={'tamanho_mb': tamanho_mb, 'max_mb': max_mb}
        )


# ============================================
# EXCEÇÕES DE EXPORTAÇÃO
# ============================================

class ExportError(BaseQuestaoException):
    """Erro durante exportação"""
    pass


class LatexCompilationError(ExportError):
    """Erro na compilação LaTeX"""

    def __init__(self, detalhes: str):
        super().__init__(
            "Erro ao compilar documento LaTeX",
            details={'detalhes': detalhes}
        )


class TemplateNotFoundError(ExportError):
    """Template LaTeX não encontrado"""

    def __init__(self, template_name: str):
        super().__init__(
            f"Template LaTeX não encontrado: {template_name}",
            details={'template': template_name}
        )


# ============================================
# EXCEÇÕES DE SEGURANÇA
# ============================================

class SecurityError(BaseQuestaoException):
    """Erro de segurança"""
    pass


class PathTraversalError(SecurityError):
    """Tentativa de path traversal"""

    def __init__(self, caminho: str):
        super().__init__(
            "Acesso negado: caminho inválido",
            details={'caminho': caminho}
        )


class DangerousLatexCommandError(SecurityError):
    """Comando LaTeX perigoso detectado"""

    def __init__(self, comando: str):
        super().__init__(
            f"Comando LaTeX não permitido: {comando}",
            details={'comando': comando}
        )


# ============================================
# HELPER FUNCTIONS
# ============================================

def handle_exception(exception: Exception, logger=None) -> Dict[str, Any]:
    """
    Trata uma exceção e retorna resposta padronizada.

    Args:
        exception: Exceção capturada
        logger: Logger para registrar erro (opcional)

    Returns:
        Dict com informações do erro
    """
    if isinstance(exception, BaseQuestaoException):
        error_dict = exception.to_dict()
    else:
        error_dict = {
            'error': 'UnexpectedError',
            'message': str(exception),
            'details': {}
        }

    if logger:
        logger.error(f"Erro capturado: {error_dict['error']} - {error_dict['message']}")
        if error_dict['details']:
            logger.debug(f"Detalhes: {error_dict['details']}")

    return error_dict


def raise_validation_error(field: str, value: Any, message: str):
    """
    Helper para lançar erro de validação genérico.

    Args:
        field: Nome do campo
        value: Valor fornecido
        message: Mensagem de erro
    """
    raise ValidationError(
        message,
        details={'field': field, 'value': value}
    )


# ============================================
# RESULTADO PADRONIZADO
# ============================================

class Result:
    """
    Classe para retorno padronizado de operações.
    Evita exceções em situações esperadas.
    """

    def __init__(self, success: bool, data: Any = None, error: str = None, details: dict = None):
        self.success = success
        self.data = data
        self.error = error
        self.details = details or {}

    @classmethod
    def ok(cls, data: Any = None) -> 'Result':
        """Cria resultado de sucesso"""
        return cls(success=True, data=data)

    @classmethod
    def fail(cls, error: str, details: dict = None) -> 'Result':
        """Cria resultado de falha"""
        return cls(success=False, error=error, details=details)

    def to_dict(self) -> Dict[str, Any]:
        """Converte para dicionário"""
        result = {'success': self.success}

        if self.success:
            result['data'] = self.data
        else:
            result['error'] = self.error
            if self.details:
                result['details'] = self.details

        return result

    def __bool__(self) -> bool:
        """Permite usar Result em if statements"""
        return self.success

    def __repr__(self) -> str:
        if self.success:
            return f"Result(success=True, data={self.data})"
        return f"Result(success=False, error={self.error})"
