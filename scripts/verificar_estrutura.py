#!/usr/bin/env python3
"""
Script para verificar se a estrutura do banco está correta
"""

import sys
from pathlib import Path

# Adicionar src ao path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / 'src'))

from database.session_manager import session_manager
from models.orm import NivelEscolar, FonteQuestao, Questao, QuestaoNivel
from sqlalchemy import inspect


def verificar_estrutura():
    """Verifica se todas as tabelas e relacionamentos estão corretos"""
    print("=" * 80)
    print("VERIFICAÇÃO DA ESTRUTURA DO BANCO DE DADOS")
    print("=" * 80)
    print()
    
    try:
        with session_manager.session_scope() as session:
            # Verificar tabela nivel_escolar
            print("📚 Verificando tabela nivel_escolar...")
            niveis = session.query(NivelEscolar).filter_by(ativo=True).all()
            print(f"  ✓ {len(niveis)} níveis encontrados:")
            for nivel in niveis:
                print(f"     - {nivel.codigo}: {nivel.nome}")
            print()
            
            # Verificar tabela fonte_questao
            print("📄 Verificando tabela fonte_questao...")
            fontes = session.query(FonteQuestao).filter_by(ativo=True).all()
            print(f"  ✓ {len(fontes)} fontes encontradas:")
            for fonte in fontes[:5]:  # Mostrar apenas as primeiras 5
                print(f"     - {fonte.sigla}: {fonte.nome_completo} ({fonte.tipo_instituicao})")
            if len(fontes) > 5:
                print(f"     ... e mais {len(fontes) - 5} fontes")
            print()
            
            # Verificar tabela questao_nivel
            print("🔗 Verificando tabela questao_nivel...")
            inspector = inspect(session_manager.engine)
            tabelas = inspector.get_table_names()
            if 'questao_nivel' in tabelas:
                print("  ✓ Tabela questao_nivel existe")
                # Contar relacionamentos
                relacionamentos = session.query(QuestaoNivel).count()
                print(f"  ✓ {relacionamentos} relacionamentos questao_nivel encontrados")
            else:
                print("  ❌ Tabela questao_nivel NÃO existe")
            print()
            
            # Verificar colunas de fonte_questao
            print("🔍 Verificando colunas de fonte_questao...")
            colunas_esperadas = ['estado', 'ano_inicio', 'ano_fim', 'url_oficial']
            colunas_tabela = [col['name'] for col in inspector.get_columns('fonte_questao')]
            for coluna in colunas_esperadas:
                if coluna in colunas_tabela:
                    print(f"  ✓ Coluna '{coluna}' existe")
                else:
                    print(f"  ❌ Coluna '{coluna}' NÃO existe")
            print()
            
            # Verificar questões existentes
            print("📝 Verificando questões existentes...")
            questoes = session.query(Questao).filter_by(ativo=True).limit(5).all()
            print(f"  ✓ {len(questoes)} questões ativas encontradas (mostrando até 5):")
            for questao in questoes:
                niveis_questao = [n.codigo for n in questao.niveis if n.ativo]
                fonte_sigla = questao.fonte.sigla if questao.fonte else "N/A"
                print(f"     - {questao.codigo}: {questao.titulo or 'Sem título'}")
                print(f"       Fonte: {fonte_sigla}, Níveis: {', '.join(niveis_questao) if niveis_questao else 'Nenhum'}")
            print()
            
            print("=" * 80)
            print("✅ VERIFICAÇÃO CONCLUÍDA!")
            print("=" * 80)
            
    except Exception as e:
        print(f"\n❌ ERRO durante verificação: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True


if __name__ == "__main__":
    sucesso = verificar_estrutura()
    sys.exit(0 if sucesso else 1)
