#!/usr/bin/env python3
"""
Script de Migração: Separar Níveis e Fontes
Migra tags V* (vestibular) para fonte_questao e tags N* (nível) para nivel_escolar

Uso:
    python scripts/migration/migrar_niveis_fontes.py
"""

import sys
from pathlib import Path

# Adicionar src ao path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'src'))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.database.session_manager import session_manager
from src.models.orm import Base, Tag, FonteQuestao, NivelEscolar, Questao, QuestaoTag
from src.models.orm.questao_nivel import QuestaoNivel
import uuid as uuid_lib
from datetime import datetime


def criar_niveis_iniciais(session):
    """Cria níveis escolares iniciais se não existirem"""
    niveis_data = [
        ('EF1', 'Ensino Fundamental I', 1),
        ('EF2', 'Ensino Fundamental II', 2),
        ('EM', 'Ensino Médio', 3),
        ('EJA', 'Educação de Jovens e Adultos', 4),
        ('TEC', 'Ensino Técnico', 5),
        ('SUP', 'Ensino Superior', 6),
    ]
    
    for codigo, nome, ordem in niveis_data:
        nivel_existente = session.query(NivelEscolar).filter_by(codigo=codigo).first()
        if not nivel_existente:
            nivel = NivelEscolar(
                uuid=str(uuid_lib.uuid4()),
                codigo=codigo,
                nome=nome,
                ordem=ordem,
                ativo=True
            )
            session.add(nivel)
            print(f"  ✓ Criado nível: {codigo} - {nome}")
    
    session.commit()


def migrar_tags_vestibular(session):
    """Migra tags V* para fonte_questao"""
    print("\n📋 Migrando tags de vestibular (V*) para fonte_questao...")
    
    tags_vestibular = session.query(Tag).filter(Tag.numeracao.like('V%')).all()
    
    if not tags_vestibular:
        print("  ℹ Nenhuma tag V* encontrada")
        return
    
    map_tag_fonte = {}  # uuid_tag -> uuid_fonte
    
    for tag in tags_vestibular:
        # Verificar se já existe fonte com essa sigla
        sigla = tag.numeracao.replace('V', '')  # Remove o prefixo V
        nome_fonte = tag.nome
        
        # Buscar ou criar fonte
        fonte = session.query(FonteQuestao).filter_by(sigla=sigla).first()
        
        if not fonte:
            fonte = FonteQuestao(
                uuid=str(uuid_lib.uuid4()),
                sigla=sigla,
                nome_completo=nome_fonte,
                tipo_instituicao='VESTIBULAR',
                ativo=True
            )
            session.add(fonte)
            session.flush()
            print(f"  ✓ Criada fonte: {sigla} - {nome_fonte}")
        else:
            print(f"  ℹ Fonte já existe: {sigla} - {nome_fonte}")
        
        map_tag_fonte[tag.uuid] = fonte.uuid
    
    session.commit()
    
    # Atualizar questões que usavam tags V*
    print("\n📋 Atualizando questões que usavam tags V*...")
    
    questoes_atualizadas = 0
    for tag_uuid, fonte_uuid in map_tag_fonte.items():
        # Buscar questões que têm essa tag
        questoes_com_tag = session.query(Questao).join(QuestaoTag).filter(
            QuestaoTag.c.uuid_tag == tag_uuid
        ).all()
        
        for questao in questoes_com_tag:
            # Se questão não tem fonte, atribuir a fonte migrada
            if not questao.uuid_fonte:
                questao.uuid_fonte = fonte_uuid
                questoes_atualizadas += 1
    
    session.commit()
    print(f"  ✓ {questoes_atualizadas} questões atualizadas com fontes")
    
    return map_tag_fonte


def migrar_tags_nivel(session):
    """Migra tags N* para nivel_escolar e cria relacionamentos"""
    print("\n📋 Migrando tags de nível escolar (N*) para nivel_escolar...")
    
    tags_nivel = session.query(Tag).filter(Tag.numeracao.like('N%')).all()
    
    if not tags_nivel:
        print("  ℹ Nenhuma tag N* encontrada")
        return
    
    # Mapeamento N1->EF2, N2->EM, N3->EJA (ajustar conforme necessário)
    map_n_tag_nivel = {
        'N1': 'EF2',
        'N2': 'EM',
        'N3': 'EJA',
    }
    
    map_tag_nivel = {}  # uuid_tag -> uuid_nivel
    
    for tag in tags_nivel:
        # Buscar nível correspondente
        codigo_nivel = map_n_tag_nivel.get(tag.numeracao)
        
        if codigo_nivel:
            nivel = session.query(NivelEscolar).filter_by(codigo=codigo_nivel).first()
            
            if nivel:
                map_tag_nivel[tag.uuid] = nivel.uuid
                print(f"  ✓ Mapeada tag {tag.numeracao} ({tag.nome}) → {codigo_nivel}")
            else:
                print(f"  ⚠ Nível {codigo_nivel} não encontrado para tag {tag.numeracao}")
        else:
            print(f"  ⚠ Tag {tag.numeracao} não tem mapeamento definido")
    
    # Criar relacionamentos questao_nivel
    print("\n📋 Criando relacionamentos questao_nivel...")
    
    relacionamentos_criados = 0
    for tag_uuid, nivel_uuid in map_tag_nivel.items():
        # Buscar questões que têm essa tag
        questoes_com_tag = session.query(Questao).join(QuestaoTag).filter(
            QuestaoTag.c.uuid_tag == tag_uuid
        ).all()
        
        for questao in questoes_com_tag:
            # Verificar se relacionamento já existe
            from sqlalchemy import select, insert
            relacionamento_existente = session.execute(
                select(QuestaoNivel).where(
                    (QuestaoNivel.c.uuid_questao == questao.uuid) &
                    (QuestaoNivel.c.uuid_nivel == nivel_uuid)
                )
            ).first()
            
            if not relacionamento_existente:
                session.execute(
                    insert(QuestaoNivel).values(
                        uuid_questao=questao.uuid,
                        uuid_nivel=nivel_uuid,
                        data_associacao=datetime.utcnow()
                    )
                )
                relacionamentos_criados += 1
    
    session.commit()
    print(f"  ✓ {relacionamentos_criados} relacionamentos questao_nivel criados")
    
    return map_tag_nivel


def remover_tags_migradas(session, tags_vestibular_uuids, tags_nivel_uuids):
    """Remove tags V* e N* da tabela tag"""
    print("\n📋 Removendo tags migradas da tabela tag...")
    
    tags_para_remover = tags_vestibular_uuids + tags_nivel_uuids
    
    if not tags_para_remover:
        print("  ℹ Nenhuma tag para remover")
        return
    
    # Desativar tags (não deletar para manter histórico)
    tags_removidas = session.query(Tag).filter(Tag.uuid.in_(tags_para_remover)).all()
    
    for tag in tags_removidas:
        tag.ativo = False
        print(f"  ✓ Tag desativada: {tag.numeracao} - {tag.nome}")
    
    session.commit()
    print(f"  ✓ {len(tags_removidas)} tags desativadas")


def main():
    """Função principal"""
    print("=" * 80)
    print("MIGRAÇÃO: Separar Níveis e Fontes")
    print("=" * 80)
    
    try:
        with session_manager.session_scope() as session:
            # 1. Criar níveis iniciais
            print("\n1️⃣ Criando níveis escolares iniciais...")
            criar_niveis_iniciais(session)
            
            # 2. Migrar tags V* para fonte_questao
            print("\n2️⃣ Migrando tags de vestibular...")
            map_tag_fonte = migrar_tags_vestibular(session)
            tags_vestibular_uuids = list(map_tag_fonte.keys()) if map_tag_fonte else []
            
            # 3. Migrar tags N* para nivel_escolar
            print("\n3️⃣ Migrando tags de nível escolar...")
            map_tag_nivel = migrar_tags_nivel(session)
            tags_nivel_uuids = list(map_tag_nivel.keys()) if map_tag_nivel else []
            
            # 4. Remover tags migradas
            print("\n4️⃣ Removendo tags migradas...")
            remover_tags_migradas(session, tags_vestibular_uuids, tags_nivel_uuids)
            
            print("\n" + "=" * 80)
            print("✅ MIGRAÇÃO CONCLUÍDA COM SUCESSO!")
            print("=" * 80)
            
    except Exception as e:
        print(f"\n❌ ERRO durante migração: {e}")
        import traceback
        traceback.print_exc()
        raise


if __name__ == "__main__":
    main()
