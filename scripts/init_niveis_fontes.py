#!/usr/bin/env python3
"""
Script para inicializar níveis escolares e fontes padrão no banco de dados
Executa após criar as tabelas
"""

import sys
from pathlib import Path

# Adicionar src ao path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / 'src'))

from database.session_manager import session_manager
from models.orm import NivelEscolar, FonteQuestao
import uuid as uuid_lib
from datetime import datetime


def criar_niveis_iniciais(session):
    """Cria níveis escolares iniciais"""
    print("📚 Criando níveis escolares iniciais...")
    
    niveis_data = [
        ('EF1', 'Ensino Fundamental I', 'Primeiro ao quinto ano do ensino fundamental', 1),
        ('EF2', 'Ensino Fundamental II', 'Sexto ao nono ano do ensino fundamental', 2),
        ('EM', 'Ensino Médio', 'Ensino médio completo', 3),
        ('EJA', 'Educação de Jovens e Adultos', 'Educação para jovens e adultos', 4),
        ('TEC', 'Ensino Técnico', 'Ensino técnico profissionalizante', 5),
        ('SUP', 'Ensino Superior', 'Ensino superior (graduação)', 6),
    ]
    
    criados = 0
    for codigo, nome, descricao, ordem in niveis_data:
        nivel_existente = session.query(NivelEscolar).filter_by(codigo=codigo).first()
        if not nivel_existente:
            nivel = NivelEscolar(
                uuid=str(uuid_lib.uuid4()),
                codigo=codigo,
                nome=nome,
                descricao=descricao,
                ordem=ordem,
                ativo=True
            )
            session.add(nivel)
            criados += 1
            print(f"  ✓ Criado: {codigo} - {nome}")
        else:
            print(f"  ℹ Já existe: {codigo} - {nome}")
    
    session.commit()
    print(f"✅ {criados} níveis criados\n")
    return criados


def criar_fontes_iniciais(session):
    """Cria fontes de questões iniciais"""
    print("📄 Criando fontes de questões iniciais...")
    
    fontes_data = [
        ('ENEM', 'Exame Nacional do Ensino Médio', 'VESTIBULAR', None, 1998, None, None),
        ('FUVEST', 'Fundação Universitária para o Vestibular', 'VESTIBULAR', 'SP', 1976, None, 'https://www.fuvest.br'),
        ('UNICAMP', 'Universidade Estadual de Campinas', 'VESTIBULAR', 'SP', 1987, None, 'https://www.comvest.unicamp.br'),
        ('UNESP', 'Universidade Estadual Paulista', 'VESTIBULAR', 'SP', 1983, None, 'https://www.vunesp.com.br'),
        ('IME', 'Instituto Militar de Engenharia', 'VESTIBULAR', None, 1959, None, 'https://www.ime.eb.br'),
        ('ITA', 'Instituto Tecnológico de Aeronáutica', 'VESTIBULAR', None, 1950, None, 'https://www.ita.br'),
        ('OBMEP', 'Olimpíada Brasileira de Matemática das Escolas Públicas', 'OLIMPIADA', None, 2005, None, 'https://www.obmep.org.br'),
        ('OBM', 'Olimpíada Brasileira de Matemática', 'OLIMPIADA', None, 1979, None, 'https://www.obm.org.br'),
        ('AUTORAL', 'Questão Autoral', 'AUTORAL', None, None, None, None),
    ]
    
    criadas = 0
    for sigla, nome_completo, tipo_instituicao, estado, ano_inicio, ano_fim, url_oficial in fontes_data:
        fonte_existente = session.query(FonteQuestao).filter_by(sigla=sigla).first()
        if not fonte_existente:
            fonte = FonteQuestao(
                uuid=str(uuid_lib.uuid4()),
                sigla=sigla,
                nome_completo=nome_completo,
                tipo_instituicao=tipo_instituicao,
                estado=estado,
                ano_inicio=ano_inicio,
                ano_fim=ano_fim,
                url_oficial=url_oficial,
                ativo=True
            )
            session.add(fonte)
            criadas += 1
            print(f"  ✓ Criada: {sigla} - {nome_completo}")
        else:
            print(f"  ℹ Já existe: {sigla} - {nome_completo}")
    
    session.commit()
    print(f"✅ {criadas} fontes criadas\n")
    return criadas


def main():
    """Função principal"""
    print("=" * 80)
    print("INICIALIZAÇÃO: Níveis Escolares e Fontes de Questões")
    print("=" * 80)
    print()
    
    try:
        # Criar todas as tabelas primeiro
        print("📦 Criando tabelas no banco de dados...")
        session_manager.create_all_tables()
        print("✅ Tabelas criadas\n")
        
        # Popular dados iniciais
        with session_manager.session_scope() as session:
            niveis_criados = criar_niveis_iniciais(session)
            fontes_criadas = criar_fontes_iniciais(session)
            
            print("=" * 80)
            print("✅ INICIALIZAÇÃO CONCLUÍDA!")
            print("=" * 80)
            print(f"📊 Resumo:")
            print(f"   - Níveis escolares: {niveis_criados} criados")
            print(f"   - Fontes de questões: {fontes_criadas} criadas")
            print()
            
    except Exception as e:
        print(f"\n❌ ERRO durante inicialização: {e}")
        import traceback
        traceback.print_exc()
        raise


if __name__ == "__main__":
    main()
