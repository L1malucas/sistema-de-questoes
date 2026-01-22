"""
View: Painel de Estatísticas
DESCRIÇÃO: Exibe estatísticas do banco de dados
"""
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QScrollArea,
    QGridLayout, QFrame
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from typing import Dict, Any
import logging

from src.controllers.questao_controller_orm import QuestaoControllerORM
from src.controllers.lista_controller_orm import ListaControllerORM
from src.controllers.tag_controller_orm import TagControllerORM
from src.database import session_manager
from src.models.orm import (
    Questao, Lista, Tag, Alternativa, Imagem, TipoQuestao,
    Dificuldade, FonteQuestao, AnoReferencia, ListaQuestao, QuestaoTag
)

logger = logging.getLogger(__name__)


class EstatisticasPanel(QWidget):
    """
    Painel de estatísticas do banco de dados
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.carregar_estatisticas()

    def setup_ui(self):
        """Configura a interface"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        # Título
        title = QLabel("Estatísticas")
        title.setStyleSheet("""
            font-size: 28px;
            font-weight: bold;
            color: #2c3e50;
            padding: 10px;
        """)
        layout.addWidget(title)

        # Scroll area para conteúdo
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: #f8f9fa;
            }
        """)

        # Widget de conteúdo
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setSpacing(20)
        content_layout.setContentsMargins(10, 10, 10, 10)

        # Cards de estatísticas
        self.cards_container = QWidget()
        self.cards_layout = QGridLayout(self.cards_container)
        self.cards_layout.setSpacing(15)
        self.cards_layout.setContentsMargins(0, 0, 0, 0)

        content_layout.addWidget(self.cards_container)
        content_layout.addStretch()

        scroll.setWidget(content_widget)
        layout.addWidget(scroll)

    def carregar_estatisticas(self):
        """Carrega e exibe estatísticas do banco"""
        try:
            with session_manager.session_scope() as session:
                # Estatísticas de Questões
                stats_questoes = self._obter_stats_questoes(session)
                self._criar_card(
                    "Questões",
                    stats_questoes,
                    row=0, col=0
                )

                # Estatísticas de Listas
                stats_listas = self._obter_stats_listas(session)
                self._criar_card(
                    "Listas",
                    stats_listas,
                    row=0, col=1
                )

                # Estatísticas de Tags
                stats_tags = self._obter_stats_tags(session)
                self._criar_card(
                    "Tags",
                    stats_tags,
                    row=1, col=0
                )

                # Estatísticas de Alternativas
                stats_alternativas = self._obter_stats_alternativas(session)
                self._criar_card(
                    "Alternativas",
                    stats_alternativas,
                    row=1, col=1
                )

                # Estatísticas de Imagens
                stats_imagens = self._obter_stats_imagens(session)
                self._criar_card(
                    "Imagens",
                    stats_imagens,
                    row=2, col=0
                )

                # Estatísticas Gerais
                stats_gerais = self._obter_stats_gerais(session)
                self._criar_card(
                    "Visão Geral",
                    stats_gerais,
                    row=2, col=1
                )

        except Exception as e:
            logger.error(f"Erro ao carregar estatísticas: {e}", exc_info=True)
            error_label = QLabel(f"Erro ao carregar estatísticas: {str(e)}")
            error_label.setStyleSheet("color: red; padding: 20px;")
            self.cards_layout.addWidget(error_label, 0, 0)

    def _obter_stats_questoes(self, session) -> Dict[str, Any]:
        """Obtém estatísticas de questões"""
        try:
            # Usar o método existente do controller
            stats = QuestaoControllerORM.obter_estatisticas()
            
            # Adicionar mais informações
            total_ativas = session.query(Questao).filter_by(ativo=True).count()
            total_inativas = session.query(Questao).filter_by(ativo=False).count()
            
            # Questões com imagens
            questoes_com_imagem = session.query(Questao).filter(
                Questao.uuid_imagem_enunciado.isnot(None),
                Questao.ativo == True
            ).count()
            
            # Questões com tags
            questoes_com_tags = session.query(Questao).join(
                Questao.tags
            ).filter(Questao.ativo == True).distinct().count()
            
            return {
                'Total Ativas': total_ativas,
                'Total Inativas': total_inativas,
                'Com Imagens': questoes_com_imagem,
                'Com Tags': questoes_com_tags,
                'Por Tipo': stats.get('por_tipo', {}),
                'Por Dificuldade': stats.get('por_dificuldade', {}),
                'Por Fonte': stats.get('por_fonte', {}),
                'Por Ano': stats.get('por_ano', {})
            }
        except Exception as e:
            logger.error(f"Erro ao obter stats de questões: {e}")
            return {'Erro': str(e)}

    def _obter_stats_listas(self, session) -> Dict[str, Any]:
        """Obtém estatísticas de listas"""
        try:
            total = session.query(Lista).filter_by(ativo=True).count()
            
            # Por tipo
            por_tipo = {}
            tipos = ['PROVA', 'LISTA', 'SIMULADO']
            for tipo in tipos:
                count = session.query(Lista).filter_by(
                    tipo=tipo, ativo=True
                ).count()
                if count > 0:
                    por_tipo[tipo] = count
            
            # Total de questões em listas
            total_questoes_em_listas = session.query(ListaQuestao).count()
            
            # Listas com mais questões
            listas_com_questoes = session.query(
                Lista.codigo,
                Lista.titulo
            ).join(
                ListaQuestao, Lista.uuid == ListaQuestao.uuid_lista
            ).filter(
                Lista.ativo == True
            ).group_by(
                Lista.uuid
            ).all()
            
            return {
                'Total': total,
                'Por Tipo': por_tipo,
                'Questões em Listas': total_questoes_em_listas,
                'Listas com Questões': len(listas_com_questoes)
            }
        except Exception as e:
            logger.error(f"Erro ao obter stats de listas: {e}")
            return {'Erro': str(e)}

    def _obter_stats_tags(self, session) -> Dict[str, Any]:
        """Obtém estatísticas de tags"""
        try:
            total = session.query(Tag).filter_by(ativo=True).count()
            
            # Tags raiz
            tags_raiz = session.query(Tag).filter_by(
                uuid_tag_pai=None, ativo=True
            ).count()
            
            # Tags mais usadas (top 5)
            from sqlalchemy import func
            from src.models.orm import QuestaoTag
            
            tags_mais_usadas = session.query(
                Tag.nome,
                func.count(QuestaoTag.c.uuid_tag).label('uso')
            ).join(
                QuestaoTag, Tag.uuid == QuestaoTag.c.uuid_tag
            ).filter(
                Tag.ativo == True
            ).group_by(
                Tag.uuid
            ).order_by(
                func.count(QuestaoTag.c.uuid_tag).desc()
            ).limit(5).all()
            
            top_tags = {nome: uso for nome, uso in tags_mais_usadas}
            
            return {
                'Total': total,
                'Tags Raiz': tags_raiz,
                'Tags Filhas': total - tags_raiz,
                'Top 5 Mais Usadas': top_tags
            }
        except Exception as e:
            logger.error(f"Erro ao obter stats de tags: {e}")
            return {'Erro': str(e)}

    def _obter_stats_alternativas(self, session) -> Dict[str, Any]:
        """Obtém estatísticas de alternativas"""
        try:
            total = session.query(Alternativa).count()
            
            # Alternativas com imagens
            com_imagem = session.query(Alternativa).filter(
                Alternativa.uuid_imagem.isnot(None)
            ).count()
            
            # Questões objetivas
            questoes_objetivas = session.query(Questao).join(
                TipoQuestao, Questao.uuid_tipo_questao == TipoQuestao.uuid
            ).filter(
                TipoQuestao.codigo == 'OBJETIVA',
                Questao.ativo == True
            ).count()
            
            media_por_questao = total / questoes_objetivas if questoes_objetivas > 0 else 0
            
            return {
                'Total': total,
                'Com Imagens': com_imagem,
                'Questões Objetivas': questoes_objetivas,
                'Média por Questão': f"{media_por_questao:.2f}"
            }
        except Exception as e:
            logger.error(f"Erro ao obter stats de alternativas: {e}")
            return {'Erro': str(e)}

    def _obter_stats_imagens(self, session) -> Dict[str, Any]:
        """Obtém estatísticas de imagens"""
        try:
            total = session.query(Imagem).filter_by(ativo=True).count()
            
            # Imagens em uso (em questões)
            imagens_em_questoes = session.query(Imagem.uuid).join(
                Questao, Questao.uuid_imagem_enunciado == Imagem.uuid
            ).filter(Questao.ativo == True).distinct().count()
            
            # Imagens em alternativas
            imagens_em_alternativas = session.query(Imagem.uuid).join(
                Alternativa, Alternativa.uuid_imagem == Imagem.uuid
            ).distinct().count()
            
            # Total de imagens únicas em uso
            from sqlalchemy import func
            imagens_uso_questoes = session.query(Questao.uuid_imagem_enunciado).filter(
                Questao.uuid_imagem_enunciado.isnot(None),
                Questao.ativo == True
            ).distinct().count()
            
            imagens_uso_alternativas = session.query(Alternativa.uuid_imagem).filter(
                Alternativa.uuid_imagem.isnot(None)
            ).distinct().count()
            
            # Aproximação: soma simples (pode haver sobreposição, mas é aceitável)
            imagens_em_uso = imagens_uso_questoes + imagens_uso_alternativas
            
            # Imagens não utilizadas (aproximação)
            nao_utilizadas = max(0, total - imagens_em_uso)
            
            return {
                'Total': total,
                'Em Questões': imagens_uso_questoes,
                'Em Alternativas': imagens_uso_alternativas,
                'Não Utilizadas': nao_utilizadas
            }
        except Exception as e:
            logger.error(f"Erro ao obter stats de imagens: {e}")
            return {'Erro': str(e)}

    def _obter_stats_gerais(self, session) -> Dict[str, Any]:
        """Obtém estatísticas gerais"""
        try:
            total_questoes = session.query(Questao).filter_by(ativo=True).count()
            total_listas = session.query(Lista).filter_by(ativo=True).count()
            total_tags = session.query(Tag).filter_by(ativo=True).count()
            total_imagens = session.query(Imagem).filter_by(ativo=True).count()
            
            # Taxa de utilização
            questoes_em_listas = session.query(ListaQuestao).count()
            taxa_uso = (questoes_em_listas / total_questoes * 100) if total_questoes > 0 else 0
            
            return {
                'Total Questões': total_questoes,
                'Total Listas': total_listas,
                'Total Tags': total_tags,
                'Total Imagens': total_imagens,
                'Taxa de Uso': f"{taxa_uso:.1f}%"
            }
        except Exception as e:
            logger.error(f"Erro ao obter stats gerais: {e}")
            return {'Erro': str(e)}

    def _criar_card(self, titulo: str, dados: Dict[str, Any], row: int, col: int):
        """Cria um card de estatísticas"""
        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 8px;
                border: 1px solid #e0e0e0;
                padding: 15px;
            }
        """)
        
        layout = QVBoxLayout(card)
        layout.setSpacing(10)
        
        # Título do card
        title_label = QLabel(titulo)
        title_label.setStyleSheet("""
            font-size: 18px;
            font-weight: bold;
            color: #2c3e50;
            padding-bottom: 10px;
            border-bottom: 2px solid #3498db;
        """)
        layout.addWidget(title_label)
        
        # Dados
        for chave, valor in dados.items():
            if isinstance(valor, dict):
                # Se for um dicionário, criar subseção
                sub_label = QLabel(f"<b>{chave}:</b>")
                sub_label.setStyleSheet("font-size: 12px; color: #34495e; margin-top: 5px;")
                layout.addWidget(sub_label)
                
                for sub_chave, sub_valor in valor.items():
                    item_layout = QHBoxLayout()
                    item_layout.setContentsMargins(15, 0, 0, 0)
                    
                    key_label = QLabel(f"  • {sub_chave}:")
                    key_label.setStyleSheet("font-size: 11px; color: #7f8c8d;")
                    
                    value_label = QLabel(str(sub_valor))
                    value_label.setStyleSheet("font-size: 11px; font-weight: bold; color: #2c3e50;")
                    
                    item_layout.addWidget(key_label)
                    item_layout.addStretch()
                    item_layout.addWidget(value_label)
                    
                    item_widget = QWidget()
                    item_widget.setLayout(item_layout)
                    layout.addWidget(item_widget)
            else:
                # Item simples
                item_layout = QHBoxLayout()
                
                key_label = QLabel(f"<b>{chave}:</b>")
                key_label.setStyleSheet("font-size: 13px; color: #34495e;")
                
                value_label = QLabel(str(valor))
                value_label.setStyleSheet("font-size: 13px; font-weight: bold; color: #2c3e50;")
                
                item_layout.addWidget(key_label)
                item_layout.addStretch()
                item_layout.addWidget(value_label)
                
                item_widget = QWidget()
                item_widget.setLayout(item_layout)
                layout.addWidget(item_widget)
        
        layout.addStretch()
        self.cards_layout.addWidget(card, row, col)
