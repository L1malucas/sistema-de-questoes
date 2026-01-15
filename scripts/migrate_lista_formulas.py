"""
Script de migração: Adiciona coluna 'formulas' na tabela 'lista'
e remove colunas 'cabecalho' e 'instrucoes'

Execute este script uma vez para atualizar o banco de dados.
"""
import sqlite3
import os
import sys

# Adicionar o diretório raiz ao path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def migrate():
    db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'database', 'sistema_questoes_v2.db')

    if not os.path.exists(db_path):
        print(f"Banco de dados não encontrado: {db_path}")
        return False

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        # Verificar se a coluna 'formulas' já existe
        cursor.execute("PRAGMA table_info(lista)")
        columns = [col[1] for col in cursor.fetchall()]

        if 'formulas' not in columns:
            print("Adicionando coluna 'formulas' à tabela 'lista'...")
            cursor.execute("ALTER TABLE lista ADD COLUMN formulas TEXT")
            print("Coluna 'formulas' adicionada com sucesso!")
        else:
            print("Coluna 'formulas' já existe.")

        # SQLite não suporta DROP COLUMN diretamente em versões antigas
        # Vamos apenas deixar as colunas antigas (cabecalho, instrucoes) como estão
        # Elas serão ignoradas pelo ORM

        conn.commit()
        print("Migração concluída com sucesso!")
        return True

    except Exception as e:
        conn.rollback()
        print(f"Erro na migração: {e}")
        return False
    finally:
        conn.close()

if __name__ == "__main__":
    migrate()
