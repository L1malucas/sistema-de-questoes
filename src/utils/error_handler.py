"""
Error Handler
DESCRIÇÃO: Sistema centralizado de tratamento de erros e notificações
BENEFÍCIOS:
    - Mensagens consistentes em todo o sistema
    - Logging automático de erros
    - Popups automáticos para o usuário
    - Decorador para simplificar tratamento em métodos
"""

import logging
import traceback
from functools import wraps
from typing import Optional, Callable, Any
from PyQt6.QtWidgets import QMessageBox, QWidget

logger = logging.getLogger(__name__)


class ErrorHandler:
    """Handler centralizado de erros com notificações ao usuário"""

    @staticmethod
    def show_error(
        parent: Optional[QWidget],
        title: str,
        message: str,
        details: Optional[str] = None
    ):
        """Exibe popup de erro ao usuário

        Args:
            parent: Widget pai do dialog
            title: Título do popup
            message: Mensagem principal
            details: Detalhes técnicos (opcional)
        """
        msg_box = QMessageBox(parent)
        msg_box.setIcon(QMessageBox.Icon.Critical)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)

        if details:
            msg_box.setDetailedText(details)

        msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg_box.exec()

        logger.error(f"{title}: {message}")
        if details:
            logger.error(f"Detalhes: {details}")

    @staticmethod
    def show_warning(
        parent: Optional[QWidget],
        title: str,
        message: str,
        details: Optional[str] = None
    ):
        """Exibe popup de aviso ao usuário

        Args:
            parent: Widget pai do dialog
            title: Título do popup
            message: Mensagem principal
            details: Detalhes adicionais (opcional)
        """
        msg_box = QMessageBox(parent)
        msg_box.setIcon(QMessageBox.Icon.Warning)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)

        if details:
            msg_box.setInformativeText(details)

        msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg_box.exec()

        logger.warning(f"{title}: {message}")

    @staticmethod
    def show_info(
        parent: Optional[QWidget],
        title: str,
        message: str
    ):
        """Exibe popup informativo ao usuário

        Args:
            parent: Widget pai do dialog
            title: Título do popup
            message: Mensagem
        """
        QMessageBox.information(parent, title, message)
        logger.info(f"{title}: {message}")

    @staticmethod
    def show_success(
        parent: Optional[QWidget],
        title: str,
        message: str
    ):
        """Exibe popup de sucesso ao usuário

        Args:
            parent: Widget pai do dialog
            title: Título do popup
            message: Mensagem
        """
        msg_box = QMessageBox(parent)
        msg_box.setIcon(QMessageBox.Icon.Information)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg_box.exec()

        logger.info(f"{title}: {message}")

    @staticmethod
    def show_validation_errors(
        parent: Optional[QWidget],
        errors: list[str]
    ):
        """Exibe erros de validação em formato de lista

        Args:
            parent: Widget pai do dialog
            errors: Lista de erros de validação
        """
        if not errors:
            return

        message = "Corrija os seguintes erros:\n\n" + "\n".join(f"• {erro}" for erro in errors)

        ErrorHandler.show_warning(
            parent,
            "Validação",
            message
        )

    @staticmethod
    def handle_exception(
        parent: Optional[QWidget],
        exception: Exception,
        user_message: str = "Ocorreu um erro inesperado",
        title: str = "Erro"
    ):
        """Trata exceção mostrando mensagem amigável ao usuário

        Args:
            parent: Widget pai do dialog
            exception: Exceção capturada
            user_message: Mensagem amigável para o usuário
            title: Título do popup
        """
        # Mensagem técnica com traceback
        technical_details = f"{type(exception).__name__}: {str(exception)}\n\n"
        technical_details += traceback.format_exc()

        # Mensagem amigável baseada no tipo de exceção
        if isinstance(exception, ValueError):
            # Erros de validação - mostrar mensagem da exceção
            ErrorHandler.show_warning(
                parent,
                "Validação",
                str(exception)
            )
        elif isinstance(exception, IOError):
            # Erros de I/O (arquivos, imagens, etc)
            ErrorHandler.show_error(
                parent,
                "Erro de Arquivo",
                f"Erro ao processar arquivo:\n\n{str(exception)}",
                technical_details
            )
        elif isinstance(exception, RuntimeError):
            # Erros de runtime (banco de dados, etc)
            ErrorHandler.show_error(
                parent,
                "Erro de Sistema",
                f"Erro ao executar operação:\n\n{str(exception)}",
                technical_details
            )
        else:
            # Erro genérico
            ErrorHandler.show_error(
                parent,
                title,
                f"{user_message}\n\n{str(exception)}",
                technical_details
            )


def handle_errors(
    parent_attr: str = 'parent',
    success_message: Optional[str] = None,
    success_title: str = "Sucesso",
    error_title: str = "Erro"
):
    """Decorador para tratamento automático de erros em métodos de Views

    Captura exceções, mostra popups ao usuário e loga erros automaticamente.

    Args:
        parent_attr: Nome do atributo que contém o widget pai (padrão: 'parent')
        success_message: Se fornecido, mostra popup de sucesso se método retornar True ou valor válido
        success_title: Título do popup de sucesso
        error_title: Título do popup de erro

    Uso:
        @handle_errors(success_message="Questão salva com sucesso!")
        def save_questao(self):
            # código que pode lançar exceções
            return True

    Comportamento:
        - ValueError: Mostra como aviso de validação
        - IOError: Mostra como erro de arquivo
        - RuntimeError: Mostra como erro de sistema
        - Outras exceções: Mostra como erro genérico com detalhes técnicos
        - Se método retorna valor e success_message definido, mostra sucesso
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(self, *args, **kwargs) -> Any:
            try:
                # Executar método
                result = func(self, *args, **kwargs)

                # Se tem mensagem de sucesso e resultado válido, mostrar
                if success_message and result not in [None, False]:
                    parent = getattr(self, parent_attr, None)
                    ErrorHandler.show_success(
                        parent,
                        success_title,
                        success_message
                    )

                return result

            except ValueError as e:
                # Erro de validação - mostrar aviso
                parent = getattr(self, parent_attr, None)
                ErrorHandler.show_warning(
                    parent,
                    "Validação",
                    str(e)
                )
                return None

            except IOError as e:
                # Erro de I/O
                parent = getattr(self, parent_attr, None)
                technical_details = traceback.format_exc()
                ErrorHandler.show_error(
                    parent,
                    "Erro de Arquivo",
                    f"Erro ao processar arquivo:\n\n{str(e)}",
                    technical_details
                )
                return None

            except RuntimeError as e:
                # Erro de runtime
                parent = getattr(self, parent_attr, None)
                technical_details = traceback.format_exc()
                ErrorHandler.show_error(
                    parent,
                    "Erro de Sistema",
                    f"Erro ao executar operação:\n\n{str(e)}",
                    technical_details
                )
                return None

            except Exception as e:
                # Erro genérico
                parent = getattr(self, parent_attr, None)
                technical_details = traceback.format_exc()
                ErrorHandler.show_error(
                    parent,
                    error_title,
                    f"Erro inesperado:\n\n{str(e)}",
                    technical_details
                )
                return None

        return wrapper
    return decorator


logger.info("ErrorHandler carregado")
