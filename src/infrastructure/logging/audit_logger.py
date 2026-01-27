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

    def questao_reativada(self, questao_id: str) -> bool:
        return self.log(EventoAuditoria(
            acao=AcaoAuditoria.QUESTAO_REATIVADA,
            entidade="questao",
            entidade_id=questao_id
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

    def lista_editada(self, lista_id: str, campos_alterados: list) -> bool:
        return self.log(EventoAuditoria(
            acao=AcaoAuditoria.LISTA_EDITADA,
            entidade="lista",
            entidade_id=lista_id,
            detalhes={"campos_alterados": campos_alterados}
        ))

    def lista_deletada(self, lista_id: str, titulo: str = None) -> bool:
        return self.log(EventoAuditoria(
            acao=AcaoAuditoria.LISTA_DELETADA,
            entidade="lista",
            entidade_id=lista_id,
            detalhes={"titulo": titulo}
        ))

    # Atalhos para tags
    def tag_criada(self, tag_id: str, nome: str, numeracao: str = None) -> bool:
        return self.log(EventoAuditoria(
            acao=AcaoAuditoria.TAG_CRIADA,
            entidade="tag",
            entidade_id=tag_id,
            detalhes={"nome": nome, "numeracao": numeracao}
        ))

    def tag_editada(self, tag_id: str, campos_alterados: list) -> bool:
        return self.log(EventoAuditoria(
            acao=AcaoAuditoria.TAG_EDITADA,
            entidade="tag",
            entidade_id=tag_id,
            detalhes={"campos_alterados": campos_alterados}
        ))

    def tag_deletada(self, tag_id: str, nome: str = None) -> bool:
        return self.log(EventoAuditoria(
            acao=AcaoAuditoria.TAG_DELETADA,
            entidade="tag",
            entidade_id=tag_id,
            detalhes={"nome": nome}
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
