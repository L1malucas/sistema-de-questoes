# test_logging_manual.py
import time

CONNECTION_STRING = "mongodb+srv://mathbank_logger:MathBank2026@mathbankcluster.4lqsue0.mongodb.net/?appName=MathBankCluster"
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