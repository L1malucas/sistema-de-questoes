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
