#!/usr/bin/env python3
"""
Script para adicionar novas colunas à tabela fonte_questao
SQLite não suporta ALTER TABLE ADD COLUMN IF NOT EXISTS, então verificamos antes
"""

import sys
import sqlite3
from pathlib import Path

# Adicionar src ao path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / 'src'))

def verificar_coluna_existe(cursor, tabela, coluna):
    """Verifica se uma coluna existe na tabela"""
    cursor.execute(f"PRAGMA table_info({tabela})")
    colunas = [row[1] for row in cursor.fetchall()]
    return coluna in colunas

def migrar_fonte_questao():
    """Adiciona novas colunas à tabela fonte_questao se não existirem"""
    db_path = Path('database/sistema_questoes_v2.db')
    
    if not db_path.exists():
        print(f"❌ Banco de dados não encontrado: {db_path}")
        return False
    
    print("=" * 80)
    print("MIGRAÇÃO: Adicionar colunas à tabela fonte_questao")
    print("=" * 80)
    print()
    
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()
    
    try:
        colunas_para_adicionar = [
            ('estado', 'VARCHAR(2)'),
            ('ano_inicio', 'INTEGER'),
            ('ano_fim', 'INTEGER'),
            ('url_oficial', 'VARCHAR(500)'),
        ]
        
        for coluna, tipo in colunas_para_adicionar:
            if verificar_coluna_existe(cursor, 'fonte_questao', coluna):
                print(f"  ℹ Coluna '{coluna}' já existe")
            else:
                print(f"  + Adicionando coluna '{coluna}'...")
                cursor.execute(f"ALTER TABLE fonte_questao ADD COLUMN {coluna} {tipo}")
                print(f"  ✓ Coluna '{coluna}' adicionada")
        
        conn.commit()
        print()
        print("✅ Migração concluída com sucesso!")
        return True
        
    except Exception as e:
        print(f"\n❌ ERRO durante migração: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()

if __name__ == "__main__":
    sucesso = migrar_fonte_questao()
    sys.exit(0 if sucesso else 1)
