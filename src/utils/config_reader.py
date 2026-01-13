"""
Util: Config Reader
DESCRIÇÃO: Lê e gerencia configurações do config.ini
RELACIONAMENTOS: config.ini
FUNCIONALIDADES:
    - Ler configurações do arquivo config.ini
    - Salvar alterações de configurações
    - Fornecer valores padrão
    - Validar configurações
"""
import logging
import configparser
from pathlib import Path
from typing import Any, Optional, List

logger = logging.getLogger(__name__)


class ConfigReader:
    """
    Gerencia leitura e escrita de configurações do arquivo config.ini.
    Implementa padrão Singleton para garantir configurações consistentes.
    """

    _instance: Optional['ConfigReader'] = None
    _initialized: bool = False

    def __new__(cls):
        """Implementa padrão Singleton"""
        if cls._instance is None:
            cls._instance = super(ConfigReader, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        """Inicializa o ConfigReader (apenas uma vez devido ao Singleton)"""
        if not ConfigReader._initialized:
            self.config = configparser.ConfigParser()
            self.config_path: Optional[Path] = None
            ConfigReader._initialized = True

    def _get_default_config_path(self) -> Path:
        """
        Retorna o caminho padrão para o arquivo config.ini.
        Assume que config_reader.py está em src/utils/
        """
        current_file = Path(__file__)
        project_root = current_file.parent.parent.parent
        return project_root / 'config.ini'

    def load(self, config_path: Optional[str] = None) -> bool:
        """
        Carrega configurações do arquivo config.ini.

        Args:
            config_path: Caminho para o arquivo config.ini (opcional)

        Returns:
            bool: True se carregado com sucesso, False caso contrário
        """
        try:
            if config_path:
                self.config_path = Path(config_path)
            else:
                self.config_path = self._get_default_config_path()

            if not self.config_path.exists():
                logger.error(f"Arquivo de configuração não encontrado: {self.config_path}")
                return False

            self.config.read(self.config_path, encoding='utf-8')
            logger.info(f"Configurações carregadas de: {self.config_path}")
            return True

        except Exception as e:
            logger.error(f"Erro ao carregar configurações: {e}")
            return False

    def get(self, section: str, key: str, default: Any = None) -> Any:
        """
        Obtém valor de configuração.

        Args:
            section: Seção do arquivo INI
            key: Chave da configuração
            default: Valor padrão se não encontrado

        Returns:
            Valor da configuração ou default
        """
        try:
            if not self.config.has_section(section):
                logger.warning(f"Seção '{section}' não encontrada no config.ini")
                return default

            if not self.config.has_option(section, key):
                logger.warning(f"Chave '{key}' não encontrada na seção '{section}'")
                return default

            return self.config.get(section, key)

        except Exception as e:
            logger.error(f"Erro ao obter configuração [{section}]{key}: {e}")
            return default

    def get_int(self, section: str, key: str, default: int = 0) -> int:
        """Obtém valor inteiro de configuração"""
        try:
            return self.config.getint(section, key)
        except (ValueError, configparser.NoSectionError, configparser.NoOptionError):
            return default

    def get_float(self, section: str, key: str, default: float = 0.0) -> float:
        """Obtém valor float de configuração"""
        try:
            return self.config.getfloat(section, key)
        except (ValueError, configparser.NoSectionError, configparser.NoOptionError):
            return default

    def get_bool(self, section: str, key: str, default: bool = False) -> bool:
        """Obtém valor booleano de configuração"""
        try:
            return self.config.getboolean(section, key)
        except (ValueError, configparser.NoSectionError, configparser.NoOptionError):
            return default

    def get_list(self, section: str, key: str, separator: str = ',', default: Optional[List[str]] = None) -> List[str]:
        """
        Obtém lista de valores de configuração.

        Args:
            section: Seção do arquivo INI
            key: Chave da configuração
            separator: Separador de itens (padrão: vírgula)
            default: Lista padrão se não encontrado

        Returns:
            Lista de valores
        """
        try:
            value = self.get(section, key)
            if value is None:
                return default if default is not None else []
            return [item.strip() for item in value.split(separator)]
        except Exception as e:
            logger.error(f"Erro ao obter lista [{section}]{key}: {e}")
            return default if default is not None else []

    def get_path(self, section: str, key: str, default: Optional[Path] = None) -> Optional[Path]:
        """
        Obtém caminho de arquivo/diretório de configuração.
        Resolve caminhos relativos em relação ao diretório do projeto.

        Args:
            section: Seção do arquivo INI
            key: Chave da configuração
            default: Caminho padrão se não encontrado

        Returns:
            Path object ou default
        """
        try:
            value = self.get(section, key)
            if value is None:
                return default

            path = Path(value)

            # Se for caminho relativo, resolver em relação ao projeto
            if not path.is_absolute():
                project_root = self.config_path.parent if self.config_path else Path.cwd()
                path = project_root / path

            return path

        except Exception as e:
            logger.error(f"Erro ao obter caminho [{section}]{key}: {e}")
            return default

    def set(self, section: str, key: str, value: Any) -> bool:
        """
        Define valor de configuração.

        Args:
            section: Seção do arquivo INI
            key: Chave da configuração
            value: Valor a ser definido

        Returns:
            bool: True se definido com sucesso
        """
        try:
            if not self.config.has_section(section):
                self.config.add_section(section)

            self.config.set(section, key, str(value))
            logger.debug(f"Configuração definida: [{section}]{key} = {value}")
            return True

        except Exception as e:
            logger.error(f"Erro ao definir configuração [{section}]{key}: {e}")
            return False

    def save(self) -> bool:
        """
        Salva configurações no arquivo config.ini.

        Returns:
            bool: True se salvo com sucesso
        """
        try:
            if self.config_path is None:
                logger.error("Caminho do arquivo de configuração não definido")
                return False

            with open(self.config_path, 'w', encoding='utf-8') as f:
                self.config.write(f)

            logger.info(f"Configurações salvas em: {self.config_path}")
            return True

        except Exception as e:
            logger.error(f"Erro ao salvar configurações: {e}")
            return False

    def reload(self) -> bool:
        """
        Recarrega configurações do arquivo.

        Returns:
            bool: True se recarregado com sucesso
        """
        if self.config_path:
            return self.load(str(self.config_path))
        return False

    def get_all_sections(self) -> List[str]:
        """Retorna todas as seções disponíveis"""
        return self.config.sections()

    def get_all_options(self, section: str) -> List[str]:
        """Retorna todas as opções de uma seção"""
        try:
            return self.config.options(section)
        except configparser.NoSectionError:
            return []


# Instância global do ConfigReader (Singleton)
config_reader = ConfigReader()

# Carregar configurações automaticamente ao importar o módulo
if not config_reader.load():
    logger.warning("Falha ao carregar configurações. Usando valores padrão.")

logger.info("ConfigReader carregado e inicializado")
