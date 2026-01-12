"""
Sistema de Banco de Questões Educacionais
Módulo: Main
Descrição: Ponto de entrada da aplicação
Versão: 1.0.1
Data: Janeiro 2026
"""

import sys
import os
from pathlib import Path

# Adicionar diretório raiz ao PYTHONPATH
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from PyQt6.QtWidgets import QApplication, QMessageBox
from PyQt6.QtCore import Qt
import logging

# Importar módulo de banco de dados
from src.models.database import db, initialize_db, verify_db

# Configuração de logging
log_dir = project_root / 'logs'
log_dir.mkdir(exist_ok=True)
log_file = log_dir / 'app.log'

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file, encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


def setup_database() -> bool:
    """
    Configura o banco de dados na primeira execução.
    Verifica se o banco existe, se não, inicializa.

    Returns:
        bool: True se banco está pronto, False caso contrário
    """
    try:
        db_path = db.get_db_path()

        # Se banco não existe, inicializar
        if not db_path.exists():
            logger.info("Banco de dados não encontrado. Inicializando...")
            if not initialize_db():
                logger.error("Falha ao inicializar banco de dados")
                return False
            logger.info("Banco de dados inicializado com sucesso")
        else:
            logger.info(f"Banco de dados encontrado: {db_path}")

        # Verificar integridade
        if not verify_db():
            logger.warning("Problemas de integridade detectados")
            # Tentar reinicializar
            logger.info("Tentando reinicializar banco de dados...")
            if not initialize_db():
                logger.error("Falha ao reinicializar banco")
                return False

        return True

    except Exception as e:
        logger.error(f"Erro ao configurar banco de dados: {e}")
        return False


def show_error_dialog(title: str, message: str):
    """
    Exibe diálogo de erro para o usuário.

    Args:
        title: Título da janela
        message: Mensagem de erro
    """
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Icon.Critical)
    msg.setWindowTitle(title)
    msg.setText(message)
    msg.setStandardButtons(QMessageBox.StandardButton.Ok)
    msg.exec()


def main():
    """
    Função principal da aplicação.
    Inicializa a aplicação Qt e exibe a janela principal.
    """
    logger.info("=" * 60)
    logger.info("INICIANDO SISTEMA DE BANCO DE QUESTÕES EDUCACIONAIS")
    logger.info("Versão: 1.0.1")
    logger.info("=" * 60)

    # Criar aplicação Qt
    app = QApplication(sys.argv)
    app.setApplicationName("Sistema de Banco de Questões")
    app.setApplicationVersion("1.0.1")
    app.setOrganizationName("Sistema Educacional")

    # Configurar estilo
    app.setStyle("Fusion")  # Estilo moderno cross-platform

    try:
        # Configurar banco de dados
        logger.info("Configurando banco de dados...")
        if not setup_database():
            show_error_dialog(
                "Erro de Inicialização",
                "Não foi possível inicializar o banco de dados.\n"
                "Verifique os logs em 'logs/app.log' para mais detalhes."
            )
            logger.error("Falha na inicialização do banco de dados")
            return 1

        logger.info("Banco de dados configurado com sucesso")

        # Importar e criar janela principal
        from src.views.main_window import MainWindow
        window = MainWindow()
        window.show()

        logger.info("Sistema inicializado com sucesso!")
        logger.info("Entrando no loop de eventos da aplicação")

        # Entrar no loop de eventos
        return app.exec()

    except Exception as e:
        logger.error(f"Erro crítico na aplicação: {e}", exc_info=True)
        show_error_dialog(
            "Erro Crítico",
            f"Ocorreu um erro inesperado:\n\n{str(e)}\n\n"
            "Verifique os logs para mais detalhes."
        )
        return 1

    finally:
        # Fechar conexão com banco
        try:
            db.disconnect()
            logger.info("Conexão com banco de dados fechada")
        except:
            pass


if __name__ == "__main__":
    """
    Ponto de entrada quando o script é executado diretamente.
    """
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        logger.info("Aplicação interrompida pelo usuário (Ctrl+C)")
        sys.exit(0)
    except Exception as e:
        logger.critical(f"Erro fatal: {e}", exc_info=True)
        sys.exit(1)
