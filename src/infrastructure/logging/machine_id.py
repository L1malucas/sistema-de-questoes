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
