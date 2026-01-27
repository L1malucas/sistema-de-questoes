# src/infrastructure/logging/setup_indexes.py
"""Script para criar índices no MongoDB Atlas para otimização de consultas."""

import os
from typing import Optional

try:
    from pymongo import MongoClient, ASCENDING, DESCENDING
    from pymongo.errors import OperationFailure
    PYMONGO_AVAILABLE = True
except ImportError:
    PYMONGO_AVAILABLE = False


def setup_mongodb_indexes(
    connection_string: Optional[str] = None,
    database: str = "mathbank_logs"
) -> dict:
    """
    Cria índices otimizados nas collections do MongoDB.

    Args:
        connection_string: String de conexão do MongoDB.
                          Se None, usa variável de ambiente MONGODB_CONNECTION_STRING.
        database: Nome do banco de dados.

    Returns:
        dict: Resultado da criação dos índices por collection.
    """
    if not PYMONGO_AVAILABLE:
        return {"error": "pymongo não está instalado"}

    # Obter connection string
    if connection_string is None:
        connection_string = os.environ.get(
            "MONGODB_CONNECTION_STRING",
            "mongodb+srv://mathbank_logger:MathBank2026@mathbankcluster.4lqsue0.mongodb.net/?appName=MathBankCluster"
        )

    results = {
        "errors": [],
        "audit": [],
        "metrics": [],
        "success": True,
        "message": ""
    }

    try:
        client = MongoClient(connection_string, serverSelectionTimeoutMS=10000)

        # Testar conexão
        client.admin.command('ping')
        print("Conectado ao MongoDB Atlas com sucesso!")

        db = client[database]

        # ========================================
        # Índices para collection: errors
        # ========================================
        print("\nCriando índices para 'errors'...")
        errors_collection = db["errors"]

        errors_indexes = [
            # Índice por timestamp (consultas recentes)
            ({"keys": [("timestamp", DESCENDING)], "name": "idx_timestamp_desc"}),
            # Índice composto: máquina + timestamp (erros por instância)
            ({"keys": [("maquina_id", ASCENDING), ("timestamp", DESCENDING)], "name": "idx_maquina_timestamp"}),
            # Índice por tipo de erro (agrupamento por tipo)
            ({"keys": [("erro.tipo", ASCENDING)], "name": "idx_erro_tipo"}),
            # Índice por nível (filtrar por severidade)
            ({"keys": [("nivel", ASCENDING)], "name": "idx_nivel"}),
            # Índice por versão do app (rastrear erros por versão)
            ({"keys": [("app_version", ASCENDING), ("timestamp", DESCENDING)], "name": "idx_version_timestamp"}),
        ]

        for idx in errors_indexes:
            try:
                result = errors_collection.create_index(idx["keys"], name=idx["name"])
                results["errors"].append(f"OK: {idx['name']}")
                print(f"   Criado: {idx['name']}")
            except OperationFailure as e:
                if "already exists" in str(e):
                    results["errors"].append(f"JÁ EXISTE: {idx['name']}")
                    print(f"   Já existe: {idx['name']}")
                else:
                    results["errors"].append(f"ERRO: {idx['name']} - {e}")
                    print(f"   Erro: {idx['name']} - {e}")

        # ========================================
        # Índices para collection: audit
        # ========================================
        print("\nCriando índices para 'audit'...")
        audit_collection = db["audit"]

        audit_indexes = [
            # Índice por timestamp (eventos recentes)
            ({"keys": [("timestamp", DESCENDING)], "name": "idx_timestamp_desc"}),
            # Índice por ação + timestamp (filtrar por tipo de ação)
            ({"keys": [("acao", ASCENDING), ("timestamp", DESCENDING)], "name": "idx_acao_timestamp"}),
            # Índice por entidade (filtrar por tipo de entidade)
            ({"keys": [("entidade", ASCENDING), ("timestamp", DESCENDING)], "name": "idx_entidade_timestamp"}),
            # Índice por máquina (rastrear ações por instância)
            ({"keys": [("maquina_id", ASCENDING), ("timestamp", DESCENDING)], "name": "idx_maquina_timestamp"}),
            # Índice por entidade_id (buscar histórico de uma entidade específica)
            ({"keys": [("entidade_id", ASCENDING), ("timestamp", DESCENDING)], "name": "idx_entidade_id_timestamp"}),
        ]

        for idx in audit_indexes:
            try:
                result = audit_collection.create_index(idx["keys"], name=idx["name"])
                results["audit"].append(f"OK: {idx['name']}")
                print(f"   Criado: {idx['name']}")
            except OperationFailure as e:
                if "already exists" in str(e):
                    results["audit"].append(f"JÁ EXISTE: {idx['name']}")
                    print(f"   Já existe: {idx['name']}")
                else:
                    results["audit"].append(f"ERRO: {idx['name']} - {e}")
                    print(f"   Erro: {idx['name']} - {e}")

        # ========================================
        # Índices para collection: metrics
        # ========================================
        print("\nCriando índices para 'metrics'...")
        metrics_collection = db["metrics"]

        metrics_indexes = [
            # Índice por timestamp (métricas recentes)
            ({"keys": [("timestamp", DESCENDING)], "name": "idx_timestamp_desc"}),
            # Índice por máquina + timestamp (métricas por instância)
            ({"keys": [("maquina_id", ASCENDING), ("timestamp", DESCENDING)], "name": "idx_maquina_timestamp"}),
            # Índice por tipo de métrica
            ({"keys": [("tipo", ASCENDING), ("timestamp", DESCENDING)], "name": "idx_tipo_timestamp"}),
            # Índice por versão do app (comparar métricas entre versões)
            ({"keys": [("app_version", ASCENDING), ("timestamp", DESCENDING)], "name": "idx_version_timestamp"}),
        ]

        for idx in metrics_indexes:
            try:
                result = metrics_collection.create_index(idx["keys"], name=idx["name"])
                results["metrics"].append(f"OK: {idx['name']}")
                print(f"   Criado: {idx['name']}")
            except OperationFailure as e:
                if "already exists" in str(e):
                    results["metrics"].append(f"JÁ EXISTE: {idx['name']}")
                    print(f"   Já existe: {idx['name']}")
                else:
                    results["metrics"].append(f"ERRO: {idx['name']} - {e}")
                    print(f"   Erro: {idx['name']} - {e}")

        # Resumo
        print("\n" + "=" * 50)
        print("RESUMO DOS ÍNDICES CRIADOS")
        print("=" * 50)
        print(f"errors: {len([r for r in results['errors'] if r.startswith('OK')])} criados, "
              f"{len([r for r in results['errors'] if r.startswith('JÁ')])} já existiam")
        print(f"audit:  {len([r for r in results['audit'] if r.startswith('OK')])} criados, "
              f"{len([r for r in results['audit'] if r.startswith('JÁ')])} já existiam")
        print(f"metrics: {len([r for r in results['metrics'] if r.startswith('OK')])} criados, "
              f"{len([r for r in results['metrics'] if r.startswith('JÁ')])} já existiam")

        results["message"] = "Índices configurados com sucesso!"
        client.close()

    except Exception as e:
        results["success"] = False
        results["message"] = f"Erro ao configurar índices: {e}"
        print(f"\nERRO: {e}")

    return results


def list_indexes(
    connection_string: Optional[str] = None,
    database: str = "mathbank_logs"
) -> dict:
    """
    Lista todos os índices existentes nas collections.

    Returns:
        dict: Índices por collection.
    """
    if not PYMONGO_AVAILABLE:
        return {"error": "pymongo não está instalado"}

    if connection_string is None:
        connection_string = os.environ.get(
            "MONGODB_CONNECTION_STRING",
            "mongodb+srv://mathbank_logger:MathBank2026@mathbankcluster.4lqsue0.mongodb.net/?appName=MathBankCluster"
        )

    try:
        client = MongoClient(connection_string, serverSelectionTimeoutMS=10000)
        db = client[database]

        result = {}
        for collection_name in ["errors", "audit", "metrics"]:
            collection = db[collection_name]
            indexes = list(collection.list_indexes())
            result[collection_name] = [
                {"name": idx["name"], "keys": dict(idx["key"])}
                for idx in indexes
            ]

        client.close()
        return result

    except Exception as e:
        return {"error": str(e)}


if __name__ == "__main__":
    print("=" * 60)
    print("CONFIGURAÇÃO DE ÍNDICES DO MONGODB ATLAS")
    print("=" * 60)

    result = setup_mongodb_indexes()

    if result["success"]:
        print(f"\n{result['message']}")
    else:
        print(f"\nFALHA: {result['message']}")

    print("\n" + "=" * 60)
    print("ÍNDICES ATUAIS NO BANCO")
    print("=" * 60)

    indexes = list_indexes()
    if "error" not in indexes:
        for collection, idx_list in indexes.items():
            print(f"\n{collection}:")
            for idx in idx_list:
                print(f"   - {idx['name']}: {idx['keys']}")
    else:
        print(f"Erro ao listar: {indexes['error']}")
