# src/infrastructure/logging/mongo_handler.py
"""Handler de logging para MongoDB Atlas."""

import logging
from datetime import datetime, timezone
from typing import Optional
from queue import Queue
from threading import Thread, Event
import time

try:
    from pymongo import MongoClient
    from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
    PYMONGO_AVAILABLE = True
except ImportError:
    PYMONGO_AVAILABLE = False

from .machine_id import get_machine_id, get_environment_info, get_app_version


class MongoDBHandler(logging.Handler):
    """Handler de logging que envia registros para MongoDB Atlas."""
    
    def __init__(
        self,
        connection_string: str,
        database: str,
        collection: str,
        batch_size: int = 10,
        flush_interval: float = 5.0,
        connection_timeout_ms: int = 5000
    ):
        super().__init__()
        
        if not PYMONGO_AVAILABLE:
            raise ImportError("pymongo não está instalado")
        
        self.connection_string = connection_string
        self.database_name = database
        self.collection_name = collection
        self.batch_size = batch_size
        self.flush_interval = flush_interval
        
        self.machine_id = get_machine_id()
        self.environment_info = get_environment_info()
        self.app_version = get_app_version()
        
        self._client: Optional[MongoClient] = None
        self._collection = None
        self._connection_timeout_ms = connection_timeout_ms
        
        self._queue: Queue = Queue()
        self._stop_event = Event()
        self._is_connected = False
        
        self._worker_thread = Thread(target=self._worker, daemon=True)
        self._worker_thread.start()
    
    def _get_collection(self):
        """Obtém a collection do MongoDB (lazy initialization)."""
        if self._collection is not None:
            return self._collection
            
        try:
            self._client = MongoClient(
                self.connection_string,
                serverSelectionTimeoutMS=self._connection_timeout_ms
            )
            self._client.admin.command('ping')
            
            db = self._client[self.database_name]
            self._collection = db[self.collection_name]
            self._is_connected = True
            return self._collection
        except Exception:
            self._is_connected = False
            return None
    
    def _worker(self):
        """Thread worker que processa a queue de logs."""
        buffer = []
        last_flush = time.time()
        
        while not self._stop_event.is_set():
            try:
                try:
                    record = self._queue.get(timeout=1.0)
                    doc = self._format_record(record)
                    if doc:
                        buffer.append(doc)
                    self._queue.task_done()
                except:
                    pass
                
                should_flush = (
                    len(buffer) >= self.batch_size or
                    (buffer and time.time() - last_flush >= self.flush_interval)
                )
                
                if should_flush and buffer:
                    self._flush_buffer(buffer)
                    buffer = []
                    last_flush = time.time()
            except Exception:
                pass
        
        if buffer:
            self._flush_buffer(buffer)
    
    def _flush_buffer(self, buffer: list):
        """Envia os logs do buffer para o MongoDB."""
        collection = self._get_collection()
        if collection is None or not buffer:
            return
        try:
            collection.insert_many(buffer, ordered=False)
        except Exception:
            for doc in buffer:
                try:
                    collection.insert_one(doc)
                except:
                    pass
    
    def _format_record(self, record: logging.LogRecord) -> Optional[dict]:
        """Formata um LogRecord para documento MongoDB."""
        try:
            exc_info = None
            if record.exc_info:
                exc_type, exc_value, _ = record.exc_info
                exc_info = {
                    "tipo": exc_type.__name__ if exc_type else None,
                    "mensagem": str(exc_value) if exc_value else None,
                    "stacktrace": self.format(record) if record.exc_info else None,
                }
            
            return {
                "timestamp": datetime.now(timezone.utc),
                "nivel": record.levelname,
                "maquina_id": self.machine_id,
                "app_version": self.app_version,
                "logger_name": record.name,
                "erro": {
                    "tipo": exc_info["tipo"] if exc_info else None,
                    "mensagem": record.getMessage(),
                    "stacktrace": exc_info["stacktrace"] if exc_info else None,
                    "arquivo": record.pathname,
                    "linha": record.lineno,
                    "funcao": record.funcName,
                },
                "ambiente": self.environment_info,
            }
        except Exception:
            return None
    
    def emit(self, record: logging.LogRecord):
        """Emite um registro de log."""
        try:
            self._queue.put_nowait(record)
        except Exception:
            pass
    
    def close(self):
        """Encerra o handler."""
        self._stop_event.set()
        self._worker_thread.join(timeout=10.0)
        if self._client:
            self._client.close()
        super().close()
    
    @property
    def is_connected(self) -> bool:
        return self._is_connected


def create_mongo_handler(
    connection_string: str,
    database: str = "mathbank_logs",
    collection: str = "errors",
    level: int = logging.ERROR
) -> Optional[MongoDBHandler]:
    """Factory function para criar um MongoDBHandler configurado."""
    try:
        handler = MongoDBHandler(connection_string, database, collection)
        handler.setLevel(level)
        handler.setFormatter(logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        ))
        return handler
    except Exception as e:
        logging.warning(f"Não foi possível criar MongoDBHandler: {e}")
        return None
