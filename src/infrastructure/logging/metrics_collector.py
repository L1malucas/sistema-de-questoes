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
