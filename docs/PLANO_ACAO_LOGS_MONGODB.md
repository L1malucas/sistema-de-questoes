# Plano de Ação Completo: Sistema de Logs/Auditoria com MongoDB Atlas

## Visão Geral

Este documento fornece um guia passo a passo para implementar um sistema de logging centralizado usando MongoDB Atlas. O sistema permitirá rastrear erros em múltiplas instâncias, auditoria de ações, debugging remoto e métricas de uso.

**Tempo estimado:** 2-3 dias de trabalho  
**Nível de dificuldade:** Médio  
**Pré-requisitos:** Conhecimento básico de Python, MongoDB e logging

---

## Índice

1. [Fase 1: Configuração do MongoDB Atlas](#fase-1-configuração-do-mongodb-atlas)
2. [Fase 2: Preparação do Ambiente Local](#fase-2-preparação-do-ambiente-local)
3. [Fase 3: Criação da Estrutura de Arquivos](#fase-3-criação-da-estrutura-de-arquivos)
4. [Fase 4: Implementação do Identificador de Máquina](#fase-4-implementação-do-identificador-de-máquina)
5. [Fase 5: Implementação do Handler MongoDB](#fase-5-implementação-do-handler-mongodb)
6. [Fase 6: Implementação do Logger de Auditoria](#fase-6-implementação-do-logger-de-auditoria)
7. [Fase 7: Implementação do Error Reporter](#fase-7-implementação-do-error-reporter)
8. [Fase 8: Implementação do Metrics Collector](#fase-8-implementação-do-metrics-collector)
9. [Fase 9: Configuração do Arquivo config.ini](#fase-9-configuração-do-arquivo-configini)
10. [Fase 10: Integração com main.py](#fase-10-integração-com-mainpy)
11. [Fase 11: Integração com Repositories](#fase-11-integração-com-repositories)
12. [Fase 12: Testes e Validação](#fase-12-testes-e-validação)
13. [Fase 13: Dashboard no MongoDB Atlas](#fase-13-dashboard-no-mongodb-atlas)

---

## Fase 1: Configuração do MongoDB Atlas

### 1.1 Criar Conta no MongoDB Atlas

1. Acesse https://www.mongodb.com/atlas
2. Clique em "Try Free"
3. Preencha o cadastro com email e senha
4. Confirme o email recebido

### 1.2 Criar um Cluster Gratuito

1. Após o login, clique em "Build a Database"
2. Selecione "M0 FREE" (tier gratuito)
3. Escolha o provedor de nuvem:
   - Recomendado: AWS
   - Região: São Paulo (sa-east-1) ou a mais próxima
4. Nome do cluster: `MathBankCluster`
5. Clique em "Create"

> Aguarde: A criação do cluster leva aproximadamente 3-5 minutos.

### 1.3 Criar Usuário do Banco de Dados

1. No menu lateral, vá em "Database Access"
2. Clique em "Add New Database User"
3. Configure:
   - Authentication Method: Password
   - Username: `mathbank_logger`
   - Password: Gere uma senha forte (anote-a!)
   - Database User Privileges: Selecione "Read and write to any database"
4. Clique em "Add User"

### 1.4 Configurar Acesso de Rede (IP Whitelist)

1. No menu lateral, vá em "Network Access"
2. Clique em "Add IP Address"
3. Para desenvolvimento: Clique em "Allow Access from Anywhere" (0.0.0.0/0)
4. Clique em "Confirm"

> SEGURANÇA: Em produção, sempre restrinja os IPs permitidos.

### 1.5 Obter a Connection String

1. No menu lateral, vá em "Database"
2. Clique em "Connect" no seu cluster
3. Selecione "Connect your application"
4. Escolha Driver: Python, Version: 3.6 or later
5. Copie a connection string:
   ```
   mongodb+srv://mathbank_logger:<password>@mathbankcluster.xxxxx.mongodb.net/?retryWrites=true&w=majority
   ```
6. Substitua `<password>` pela senha criada

### 1.6 Criar o Banco de Dados e Collections

1. No cluster, clique em "Browse Collections"
2. Clique em "Add My Own Data"
3. Database name: `mathbank_logs`
4. Collection name: `errors`
5. Adicione mais collections: `audit` e `metrics`

---

## Fase 2: Preparação do Ambiente Local

### 2.1 Instalar Dependências Python

```bash
pip install pymongo>=4.6.0 dnspython>=2.4.0
```

### 2.2 Atualizar requirements.txt

```txt
# MongoDB para logging remoto
pymongo>=4.6.0
dnspython>=2.4.0
```

### 2.3 Criar Arquivo .env

```env
MONGODB_CONNECTION_STRING=mongodb+srv://mathbank_logger:SENHA@cluster.mongodb.net/?retryWrites=true&w=majority
MONGODB_DATABASE=mathbank_logs
```

> IMPORTANTE: Adicione `.env` ao `.gitignore`!

### 2.4 Verificar Conexão (Teste Rápido)

```python
# test_mongo.py
from pymongo import MongoClient

connection_string = "mongodb+srv://mathbank_logger:MathBank2026@mathbankcluster.4lqsue0.mongodb.net/?appName=MathBankCluster"

try:
    client = MongoClient(connection_string)
    db = client["mathbank_logs"]
    result = db["errors"].insert_one({"test": "conexão OK"})
    print(f"Conexão bem-sucedida! ID: {result.inserted_id}")
    db["errors"].delete_one({"_id": result.inserted_id})
except Exception as e:
    print(f"Erro: {e}")
finally:
    client.close()
```

---

## Fase 3: Criação da Estrutura de Arquivos

### 3.1 Criar Diretórios

```bash
mkdir -p src/infrastructure/logging
```

### 3.2 Estrutura Final

```
src/
├── infrastructure/
│   └── logging/
│       ├── __init__.py
│       ├── machine_id.py
│       ├── mongo_handler.py
│       ├── audit_logger.py
│       ├── error_reporter.py
│       └── metrics_collector.py
```

### 3.3 Criar __init__.py

```python
# src/infrastructure/logging/__init__.py
"""Módulo de Logging e Auditoria com MongoDB Atlas."""

from .machine_id import get_machine_id
from .mongo_handler import MongoDBHandler, create_mongo_handler
from .audit_logger import AuditLogger, AcaoAuditoria, EventoAuditoria, init_audit_logger, get_audit_logger
from .error_reporter import ErrorReporter, init_error_reporter, get_error_reporter
from .metrics_collector import MetricsCollector, init_metrics_collector, get_metrics_collector

__all__ = [
    "get_machine_id",
    "MongoDBHandler",
    "create_mongo_handler",
    "AuditLogger",
    "AcaoAuditoria",
    "EventoAuditoria",
    "init_audit_logger",
    "get_audit_logger",
    "ErrorReporter",
    "init_error_reporter",
    "get_error_reporter",
    "MetricsCollector",
    "init_metrics_collector",
    "get_metrics_collector",
]
```

---

## Fase 4: Implementação do Identificador de Máquina

### 4.1 Criar machine_id.py

```python
# src/infrastructure/logging/machine_id.py
"""Módulo para geração de identificador único de máquina."""

import platform
import socket
import uuid
import hashlib
from functools import lru_cache


@lru_cache(maxsize=1)
def get_machine_id() -> str:
    """
    Gera um ID único e anônimo para a máquina atual.
    
    Returns:
        str: Hash SHA-256 truncado (16 caracteres).
    """
    try:
        hostname = socket.gethostname()
        node_name = platform.node()
        mac_address = uuid.getnode()
        
        data = f"{hostname}-{node_name}-{mac_address}"
        hash_object = hashlib.sha256(data.encode())
        return hash_object.hexdigest()[:16]
    except Exception:
        return hashlib.sha256(str(uuid.uuid4()).encode()).hexdigest()[:16]


def get_environment_info() -> dict:
    """Coleta informações do ambiente de execução."""
    return {
        "os": f"{platform.system()} {platform.release()}",
        "os_version": platform.version(),
        "python_version": platform.python_version(),
        "architecture": platform.machine(),
    }


def get_app_version() -> str:
    """Retorna a versão atual da aplicação."""
    return "1.0.0"  # TODO: Ler de arquivo de versão
```

---

## Fase 5: Implementação do Handler MongoDB

### 5.1 Criar mongo_handler.py

```python
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
```

---

## Fase 6: Implementação do Logger de Auditoria

### 6.1 Criar audit_logger.py

```python
# src/infrastructure/logging/audit_logger.py
"""Sistema de auditoria para rastreamento de ações do usuário."""

from enum import Enum
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional, Dict, Any
from threading import Lock

try:
    from pymongo import MongoClient
    PYMONGO_AVAILABLE = True
except ImportError:
    PYMONGO_AVAILABLE = False

from .machine_id import get_machine_id, get_app_version


class AcaoAuditoria(Enum):
    """Enum com todas as ações auditáveis do sistema."""
    # Questões
    QUESTAO_CRIADA = "questao.criada"
    QUESTAO_EDITADA = "questao.editada"
    QUESTAO_INATIVADA = "questao.inativada"
    QUESTAO_REATIVADA = "questao.reativada"
    
    # Listas
    LISTA_CRIADA = "lista.criada"
    LISTA_EDITADA = "lista.editada"
    LISTA_DELETADA = "lista.deletada"
    LISTA_EXPORTADA = "lista.exportada"
    
    # Tags
    TAG_CRIADA = "tag.criada"
    TAG_EDITADA = "tag.editada"
    TAG_DELETADA = "tag.deletada"
    
    # Sistema
    SESSAO_INICIADA = "sessao.iniciada"
    SESSAO_ENCERRADA = "sessao.encerrada"
    BACKUP_CRIADO = "backup.criado"
    BACKUP_RESTAURADO = "backup.restaurado"


@dataclass
class EventoAuditoria:
    """Representa um evento de auditoria."""
    acao: AcaoAuditoria
    entidade: str
    entidade_id: str
    detalhes: Optional[Dict[str, Any]] = None
    usuario_id: Optional[str] = None
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    
    def to_dict(self) -> dict:
        return {
            "timestamp": self.timestamp,
            "acao": self.acao.value,
            "entidade": self.entidade,
            "entidade_id": str(self.entidade_id),
            "detalhes": self.detalhes or {},
            "usuario_id": self.usuario_id,
        }


class AuditLogger:
    """Logger de auditoria para MongoDB."""
    
    _instance: Optional['AuditLogger'] = None
    _lock = Lock()
    
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self, connection_string: str, database: str, collection: str, enabled: bool = True):
        if hasattr(self, '_initialized') and self._initialized:
            return
            
        self.connection_string = connection_string
        self.database_name = database
        self.collection_name = collection
        self.enabled = enabled
        
        self.machine_id = get_machine_id()
        self.app_version = get_app_version()
        
        self._client: Optional[MongoClient] = None
        self._collection = None
        self._is_connected = False
        self._initialized = True
    
    def _get_collection(self):
        if not self.enabled or not PYMONGO_AVAILABLE:
            return None
        if self._collection is not None:
            return self._collection
        try:
            self._client = MongoClient(self.connection_string, serverSelectionTimeoutMS=5000)
            self._client.admin.command('ping')
            self._collection = self._client[self.database_name][self.collection_name]
            self._is_connected = True
            return self._collection
        except Exception:
            self._is_connected = False
            return None
    
    def log(self, evento: EventoAuditoria) -> bool:
        if not self.enabled:
            return False
        collection = self._get_collection()
        if collection is None:
            return False
        try:
            doc = evento.to_dict()
            doc["maquina_id"] = self.machine_id
            doc["app_version"] = self.app_version
            collection.insert_one(doc)
            return True
        except Exception:
            return False
    
    # Atalhos para questões
    def questao_criada(self, questao_id: str, titulo: str, tipo: str, tags: list = None) -> bool:
        return self.log(EventoAuditoria(
            acao=AcaoAuditoria.QUESTAO_CRIADA,
            entidade="questao",
            entidade_id=questao_id,
            detalhes={"titulo": titulo[:100], "tipo": tipo, "tags": tags or []}
        ))
    
    def questao_editada(self, questao_id: str, campos_alterados: list) -> bool:
        return self.log(EventoAuditoria(
            acao=AcaoAuditoria.QUESTAO_EDITADA,
            entidade="questao",
            entidade_id=questao_id,
            detalhes={"campos_alterados": campos_alterados}
        ))
    
    def questao_inativada(self, questao_id: str, motivo: str = None) -> bool:
        return self.log(EventoAuditoria(
            acao=AcaoAuditoria.QUESTAO_INATIVADA,
            entidade="questao",
            entidade_id=questao_id,
            detalhes={"motivo": motivo}
        ))
    
    # Atalhos para listas
    def lista_criada(self, lista_id: str, titulo: str, qtd_questoes: int) -> bool:
        return self.log(EventoAuditoria(
            acao=AcaoAuditoria.LISTA_CRIADA,
            entidade="lista",
            entidade_id=lista_id,
            detalhes={"titulo": titulo[:100], "qtd_questoes": qtd_questoes}
        ))
    
    def lista_exportada(self, lista_id: str, formato: str, qtd_questoes: int) -> bool:
        return self.log(EventoAuditoria(
            acao=AcaoAuditoria.LISTA_EXPORTADA,
            entidade="lista",
            entidade_id=lista_id,
            detalhes={"formato": formato, "qtd_questoes": qtd_questoes}
        ))
    
    # Atalhos para sistema
    def sessao_iniciada(self) -> bool:
        return self.log(EventoAuditoria(
            acao=AcaoAuditoria.SESSAO_INICIADA,
            entidade="sistema",
            entidade_id=self.machine_id
        ))
    
    def sessao_encerrada(self, duracao_segundos: int) -> bool:
        return self.log(EventoAuditoria(
            acao=AcaoAuditoria.SESSAO_ENCERRADA,
            entidade="sistema",
            entidade_id=self.machine_id,
            detalhes={"duracao_segundos": duracao_segundos}
        ))
    
    def close(self):
        if self._client:
            self._client.close()
            self._client = None
            self._collection = None


# Instância global
_audit_logger: Optional[AuditLogger] = None

def get_audit_logger() -> Optional[AuditLogger]:
    return _audit_logger

def init_audit_logger(connection_string: str, database: str = "mathbank_logs", 
                      collection: str = "audit", enabled: bool = True) -> AuditLogger:
    global _audit_logger
    _audit_logger = AuditLogger(connection_string, database, collection, enabled)
    return _audit_logger
```

---

## Fase 7: Implementação do Error Reporter

### 7.1 Criar error_reporter.py

```python
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
```

---

## Fase 8: Implementação do Metrics Collector

### 8.1 Criar metrics_collector.py

```python
# src/infrastructure/logging/metrics_collector.py
"""Coletor de métricas de uso da aplicação."""

from datetime import datetime, timezone
from typing import Optional, Dict, Any
from threading import Lock
import time

try:
    from pymongo import MongoClient
    PYMONGO_AVAILABLE = True
except ImportError:
    PYMONGO_AVAILABLE = False

from .machine_id import get_machine_id, get_app_version


class MetricsCollector:
    """Coletor de métricas de uso."""
    
    def __init__(self, connection_string: str, database: str, collection: str, enabled: bool = True):
        self.connection_string = connection_string
        self.database_name = database
        self.collection_name = collection
        self.enabled = enabled
        
        self.machine_id = get_machine_id()
        self.app_version = get_app_version()
        
        self._client: Optional[MongoClient] = None
        self._collection = None
        
        self._session_start: Optional[datetime] = None
        self._counters: Dict[str, int] = {}
        self._timings: Dict[str, list] = {}
        self._lock = Lock()
    
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
    
    def start_session(self):
        """Inicia uma nova sessão de métricas."""
        with self._lock:
            self._session_start = datetime.now(timezone.utc)
            self._counters = {}
            self._timings = {}
    
    def increment(self, metric_name: str, value: int = 1):
        """Incrementa um contador de métrica."""
        if not self.enabled:
            return
        with self._lock:
            if metric_name not in self._counters:
                self._counters[metric_name] = 0
            self._counters[metric_name] += value
    
    def record_timing(self, operation: str, duration_ms: float):
        """Registra tempo de uma operação."""
        if not self.enabled:
            return
        with self._lock:
            if operation not in self._timings:
                self._timings[operation] = []
            self._timings[operation].append(duration_ms)
    
    class TimingContext:
        def __init__(self, collector, operation: str):
            self.collector = collector
            self.operation = operation
            self.start_time = None
        
        def __enter__(self):
            self.start_time = time.perf_counter()
            return self
        
        def __exit__(self, *args):
            if self.start_time:
                duration_ms = (time.perf_counter() - self.start_time) * 1000
                self.collector.record_timing(self.operation, duration_ms)
    
    def time_operation(self, operation: str):
        """Context manager para medir tempo de uma operação."""
        return self.TimingContext(self, operation)
    
    def end_session(self) -> bool:
        """Encerra a sessão e envia métricas para MongoDB."""
        if not self.enabled or self._session_start is None:
            return False
        
        collection = self._get_collection()
        if collection is None:
            return False
        
        try:
            with self._lock:
                session_end = datetime.now(timezone.utc)
                duration = (session_end - self._session_start).total_seconds()
                
                timing_stats = {}
                for op, times in self._timings.items():
                    if times:
                        timing_stats[op] = {
                            "count": len(times),
                            "min_ms": round(min(times), 2),
                            "max_ms": round(max(times), 2),
                            "avg_ms": round(sum(times) / len(times), 2),
                        }
                
                doc = {
                    "timestamp": session_end,
                    "maquina_id": self.machine_id,
                    "app_version": self.app_version,
                    "tipo": "SESSAO",
                    "sessao": {
                        "inicio": self._session_start,
                        "fim": session_end,
                        "duracao_segundos": int(duration),
                    },
                    "contadores": self._counters.copy(),
                    "timings": timing_stats,
                }
                
                collection.insert_one(doc)
                
                self._session_start = None
                self._counters = {}
                self._timings = {}
                return True
        except Exception:
            return False
    
    def close(self):
        if self._session_start:
            self.end_session()
        if self._client:
            self._client.close()


# Instância global
_metrics_collector: Optional[MetricsCollector] = None

def get_metrics_collector() -> Optional[MetricsCollector]:
    return _metrics_collector

def init_metrics_collector(connection_string: str, database: str = "mathbank_logs",
                           collection: str = "metrics", enabled: bool = True) -> MetricsCollector:
    global _metrics_collector
    _metrics_collector = MetricsCollector(connection_string, database, collection, enabled)
    return _metrics_collector
```

---

## Fase 9: Configuração do Arquivo config.ini

### 9.1 Adicionar Seções ao config.ini

```ini
[LOGGING]
nivel_console = INFO
nivel_arquivo = DEBUG
nivel_remoto = ERROR
remote_logging_enabled = true

[MONGODB]
# ATENÇÃO: Use variáveis de ambiente em produção!
connection_string = mongodb+srv://mathbank_logger:SENHA@cluster.mongodb.net/?retryWrites=true&w=majority
database = mathbank_logs
collection_errors = errors
collection_audit = audit
collection_metrics = metrics
connection_timeout_ms = 5000

[AUDIT]
auditar_questoes = true
auditar_listas = true
auditar_tags = true
auditar_exportacoes = true
auditar_sessoes = true

[METRICS]
enabled = true
enviar_ao_encerrar = true
```

---

## Fase 10: Integração com main.py

### 10.1 Modificar main.py

```python
# src/main.py
"""Ponto de entrada principal da aplicação."""

import sys
import logging
import atexit
import os


def setup_logging():
    """Configura o sistema de logging completo."""
    
    # Carrega connection string (prioriza variável de ambiente)
    connection_string = os.environ.get(
        "MONGODB_CONNECTION_STRING",
        "mongodb+srv://mathbank_logger:SENHA@cluster.mongodb.net/?retryWrites=true&w=majority"
    )
    database = "mathbank_logs"
    
    # Configuração do logger raiz
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)
    
    # Handler de Console
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(logging.Formatter(log_format))
    root_logger.addHandler(console_handler)
    
    # Handler de Arquivo
    try:
        os.makedirs("logs", exist_ok=True)
        file_handler = logging.FileHandler("logs/mathbank.log", encoding="utf-8")
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(logging.Formatter(log_format))
        root_logger.addHandler(file_handler)
    except Exception as e:
        logging.warning(f"Não foi possível criar arquivo de log: {e}")
    
    # Logging remoto (MongoDB)
    try:
        from src.infrastructure.logging import (
            create_mongo_handler,
            init_audit_logger,
            init_error_reporter,
            init_metrics_collector,
        )
        
        # Handler MongoDB para erros
        mongo_handler = create_mongo_handler(connection_string, database, "errors", logging.ERROR)
        if mongo_handler:
            root_logger.addHandler(mongo_handler)
            logging.info("Logging remoto configurado")
        
        # Error Reporter
        init_error_reporter(connection_string, database, "errors", install_global=True)
        
        # Audit Logger
        audit = init_audit_logger(connection_string, database, "audit")
        
        # Metrics Collector
        metrics = init_metrics_collector(connection_string, database, "metrics")
        metrics.start_session()
        audit.sessao_iniciada()
        
        # Handler de encerramento
        def on_exit():
            try:
                if metrics:
                    metrics.end_session()
            except Exception:
                pass
        
        atexit.register(on_exit)
        
    except Exception as e:
        logging.warning(f"Logging remoto não configurado: {e}")
    
    logging.info("Sistema de logging inicializado")


# Configura logging ANTES de outros imports
setup_logging()

# Imports da aplicação
from PyQt6.QtWidgets import QApplication

logger = logging.getLogger(__name__)


def main():
    logger.info("Iniciando aplicação...")
    
    try:
        app = QApplication(sys.argv)
        # ... seu código existente ...
        logger.info("Aplicação iniciada com sucesso")
        sys.exit(app.exec())
    except Exception as e:
        logger.critical(f"Erro fatal: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
```

---

## Fase 11: Integração com Repositories

### 11.1 Exemplo: QuestaoRepository

```python
# src/repositories/questao_repository.py
import logging
from src.infrastructure.logging import get_audit_logger, get_metrics_collector

logger = logging.getLogger(__name__)


class QuestaoRepository:
    def __init__(self, session):
        self.session = session
        self._audit = get_audit_logger()
        self._metrics = get_metrics_collector()
    
    def criar(self, questao_data: dict):
        try:
            # Mede tempo da operação
            if self._metrics:
                with self._metrics.time_operation("criar_questao"):
                    questao_id = self._criar_interno(questao_data)
            else:
                questao_id = self._criar_interno(questao_data)
            
            # Registra na auditoria
            if questao_id and self._audit:
                self._audit.questao_criada(
                    questao_id=questao_id,
                    titulo=questao_data.get("titulo", ""),
                    tipo=questao_data.get("tipo", "")
                )
            
            # Incrementa contador
            if self._metrics:
                self._metrics.increment("questoes_criadas")
            
            return questao_id
            
        except Exception as e:
            logger.error(f"Erro ao criar questão: {e}", exc_info=True)
            if self._metrics:
                self._metrics.increment("erros_criar_questao")
            return None
```

### 11.2 Padrão para Outros Repositories

```python
# No __init__
self._audit = get_audit_logger()
self._metrics = get_metrics_collector()

# Após operação bem-sucedida
if self._audit:
    self._audit.metodo_apropriado(...)

# Para métricas
if self._metrics:
    self._metrics.increment("nome_contador")
```

---

## Fase 12: Testes e Validação

### 12.1 Script de Teste Manual

```python
# test_logging_manual.py
import time

CONNECTION_STRING = "sua_connection_string"
DATABASE = "mathbank_logs"

def test_completo():
    print("=" * 60)
    print("TESTE DO SISTEMA DE LOGGING")
    print("=" * 60)
    
    # 1. Machine ID
    print("\n1. Machine ID...")
    from src.infrastructure.logging.machine_id import get_machine_id
    print(f"   ID: {get_machine_id()}")
    
    # 2. Audit Logger
    print("\n2. Audit Logger...")
    from src.infrastructure.logging.audit_logger import init_audit_logger
    audit = init_audit_logger(CONNECTION_STRING, DATABASE, "audit")
    result = audit.questao_criada("test-001", "Questão Teste", "OBJETIVA")
    print(f"   Resultado: {'OK' if result else 'FALHOU'}")
    
    # 3. Metrics
    print("\n3. Metrics Collector...")
    from src.infrastructure.logging.metrics_collector import init_metrics_collector
    metrics = init_metrics_collector(CONNECTION_STRING, DATABASE, "metrics")
    metrics.start_session()
    metrics.increment("teste", 5)
    with metrics.time_operation("operacao_teste"):
        time.sleep(0.1)
    result = metrics.end_session()
    print(f"   Resultado: {'OK' if result else 'FALHOU'}")
    
    # 4. Error Reporter
    print("\n4. Error Reporter...")
    from src.infrastructure.logging.error_reporter import init_error_reporter
    import sys
    reporter = init_error_reporter(CONNECTION_STRING, DATABASE, "errors", install_global=False)
    try:
        raise ValueError("Erro de teste")
    except:
        result = reporter.report(*sys.exc_info())
    print(f"   Resultado: {'OK' if result else 'FALHOU'}")
    
    print("\n" + "=" * 60)
    print("TESTE CONCLUÍDO - Verifique o MongoDB Atlas!")
    print("=" * 60)

if __name__ == "__main__":
    test_completo()
```

---

## Fase 13: Dashboard no MongoDB Atlas

### 13.1 Criar Índices

Execute no MongoDB Atlas Shell:

```javascript
// Collection: errors
db.errors.createIndex({ "timestamp": -1 });
db.errors.createIndex({ "maquina_id": 1, "timestamp": -1 });
db.errors.createIndex({ "erro.tipo": 1 });

// Collection: audit
db.audit.createIndex({ "timestamp": -1 });
db.audit.createIndex({ "acao": 1, "timestamp": -1 });

// Collection: metrics
db.metrics.createIndex({ "timestamp": -1 });
db.metrics.createIndex({ "maquina_id": 1, "timestamp": -1 });
```

---

## Checklist Final

### Preparação MongoDB Atlas
- [ ] Conta criada no MongoDB Atlas
- [ ] Cluster M0 (gratuito) criado
- [ ] Usuário `mathbank_logger` criado
- [ ] IP adicionado à whitelist
- [ ] Connection string obtida
- [ ] Banco `mathbank_logs` com collections: `errors`, `audit`, `metrics`

### Dependências
- [ ] `pymongo>=4.6.0` instalado
- [ ] `dnspython>=2.4.0` instalado
- [ ] `requirements.txt` atualizado

### Arquivos Criados
- [ ] `src/infrastructure/logging/__init__.py`
- [ ] `src/infrastructure/logging/machine_id.py`
- [ ] `src/infrastructure/logging/mongo_handler.py`
- [ ] `src/infrastructure/logging/audit_logger.py`
- [ ] `src/infrastructure/logging/error_reporter.py`
- [ ] `src/infrastructure/logging/metrics_collector.py`

### Configuração
- [ ] `config.ini` atualizado
- [ ] Connection string configurada (variável de ambiente ou .env)
- [ ] Diretório `logs/` criado

### Integração
- [ ] `main.py` modificado com `setup_logging()`
- [ ] Repositories atualizados com auditoria
- [ ] Handler de encerramento registrado

### Testes
- [ ] Script de teste executado com sucesso
- [ ] Dados verificados no MongoDB Atlas

### Segurança
- [ ] `.env` no `.gitignore`
- [ ] Connection string NÃO em código versionado

---

## Troubleshooting

### "ServerSelectionTimeoutError"
- Verifique IP na whitelist
- Verifique connection string
- Teste conexão isoladamente

### "Authentication failed"
- Verifique usuário e senha
- Escape caracteres especiais na senha (@ → %40)

### Logs não aparecem no MongoDB
- Verifique `handler.is_connected`
- Ajuste `nivel_remoto` para ERROR
- Aguarde flush ou chame `handler.close()`

### Aplicação lenta
- Aumente `batch_size` e `flush_interval`
- Reduza nível de log remoto para ERROR

---

## Referências

- [MongoDB Atlas Documentation](https://www.mongodb.com/docs/atlas/)
- [PyMongo Documentation](https://pymongo.readthedocs.io/)
- [Python Logging HOWTO](https://docs.python.org/3/howto/logging.html)

---

*Documento criado em: 2026-01-21*
*Baseado no PLANO 3 do arquivo PLANOS_IMPLEMENTACAO.md*
