# src/infrastructure/logging/error_reporter.py
"""Reporter de erros não tratados."""

import sys
import traceback
import logging
from datetime import datetime, timezone
from typing import Optional, Callable
from functools import wraps

try:
    from pymongo import MongoClient
    PYMONGO_AVAILABLE = True
except ImportError:
    PYMONGO_AVAILABLE = False

from .machine_id import get_machine_id, get_environment_info, get_app_version


class ErrorReporter:
    """Reporter de erros não tratados para MongoDB."""
    
    def __init__(self, connection_string: str, database: str, collection: str,
                 enabled: bool = True, also_log_locally: bool = True):
        self.connection_string = connection_string
        self.database_name = database
        self.collection_name = collection
        self.enabled = enabled
        self.also_log_locally = also_log_locally
        
        self.machine_id = get_machine_id()
        self.environment_info = get_environment_info()
        self.app_version = get_app_version()
        
        self._client: Optional[MongoClient] = None
        self._collection = None
        self._original_excepthook = None
        self._logger = logging.getLogger(__name__)
    
    def _get_collection(self):
        if not self.enabled or not PYMONGO_AVAILABLE:
            return None
        if self._collection is not None:
            return self._collection
        try:
            self._client = MongoClient(self.connection_string, serverSelectionTimeoutMS=5000)
            self._collection = self._client[self.database_name][self.collection_name]
            return self._collection
        except Exception:
            return None
    
    def report(self, exc_type: type, exc_value: Exception, exc_traceback, context: dict = None) -> bool:
        if self.also_log_locally:
            self._logger.error(f"Exceção: {exc_type.__name__}: {exc_value}", 
                             exc_info=(exc_type, exc_value, exc_traceback))
        
        collection = self._get_collection()
        if collection is None:
            return False
        
        try:
            tb_lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
            stacktrace = ''.join(tb_lines)
            
            if exc_traceback:
                tb = traceback.extract_tb(exc_traceback)
                last_frame = tb[-1] if tb else None
                arquivo = last_frame.filename if last_frame else None
                linha = last_frame.lineno if last_frame else None
                funcao = last_frame.name if last_frame else None
            else:
                arquivo = linha = funcao = None
            
            doc = {
                "timestamp": datetime.now(timezone.utc),
                "nivel": "CRITICAL",
                "maquina_id": self.machine_id,
                "app_version": self.app_version,
                "erro": {
                    "tipo": exc_type.__name__,
                    "mensagem": str(exc_value),
                    "stacktrace": stacktrace,
                    "arquivo": arquivo,
                    "linha": linha,
                    "funcao": funcao,
                },
                "contexto": context or {},
                "ambiente": self.environment_info,
                "nao_tratada": True,
            }
            
            collection.insert_one(doc)
            return True
        except Exception:
            return False
    
    def install_global_hook(self):
        """Instala o reporter como hook global para exceções não tratadas."""
        self._original_excepthook = sys.excepthook
        
        def exception_hook(exc_type, exc_value, exc_traceback):
            self.report(exc_type, exc_value, exc_traceback)
            if self._original_excepthook:
                self._original_excepthook(exc_type, exc_value, exc_traceback)
        
        sys.excepthook = exception_hook
    
    def catch(self, func: Callable) -> Callable:
        """Decorador para capturar exceções em funções específicas."""
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception:
                self.report(*sys.exc_info(), context={"funcao_decorada": func.__name__})
                raise
        return wrapper
    
    def close(self):
        if self._original_excepthook:
            sys.excepthook = self._original_excepthook
        if self._client:
            self._client.close()


# Instância global
_error_reporter: Optional[ErrorReporter] = None

def get_error_reporter() -> Optional[ErrorReporter]:
    return _error_reporter

def init_error_reporter(connection_string: str, database: str = "mathbank_logs",
                        collection: str = "errors", install_global: bool = True,
                        enabled: bool = True) -> ErrorReporter:
    global _error_reporter
    _error_reporter = ErrorReporter(connection_string, database, collection, enabled)
    if install_global:
        _error_reporter.install_global_hook()
    return _error_reporter
