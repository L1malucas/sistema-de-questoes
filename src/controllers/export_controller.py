"""
Controller para gerenciar a exportação de listas e outros dados.
"""
import logging
import re
from pathlib import Path
from typing import List

# Corrigindo a importação para o DTO
from src.application.dtos.export_dto import ExportOptionsDTO
# Corrigindo a importação para o Service
from src.application.services.export_service import ExportService, escape_latex
from src.services import services # Usando a fachada de serviços para buscar dados

logger = logging.getLogger(__name__)

class ExportController:
    def __init__(self):
        # O ExportService não depende de sessão, então pode ser instanciado diretamente
        self.export_service = ExportService()

    def listar_templates_disponiveis(self) -> List[str]:
        """
        Lista os arquivos de template LaTeX (.tex) disponíveis na pasta de templates.
        """
        template_dir = Path('templates/latex')
        if not template_dir.exists():
            logger.warning(f"Diretório de templates não encontrado: {template_dir.resolve()}")
            return []
        
        templates = [f.name for f in template_dir.glob('*.tex')] 
        logger.info(f"Templates LaTeX encontrados: {templates}")
        return templates

    def _carregar_template(self, nome_template: str) -> str:
        """Carrega o conteúdo de um arquivo de template."""
        template_path = Path('templates/latex') / nome_template
        if not template_path.exists():
            raise FileNotFoundError(f"Template LaTeX '{nome_template}' não encontrado.")
        
        return template_path.read_text(encoding='utf-8')

    def _gerar_conteudo_latex(self, opcoes: ExportOptionsDTO) -> str:
        """
        Gera o conteudo LaTeX completo para a lista, aplicando as opcoes de exportacao.
        """
        # 1. Buscar dados da lista
        lista_dados = services.lista.buscar_lista(opcoes.id_lista)
        if not lista_dados:
            raise ValueError(f"Lista com codigo {opcoes.id_lista} nao encontrada.")

        # 2. Carregar o template base
        template_content = self._carregar_template(opcoes.template_latex)

        # 3. Substituir placeholders do cabecalho
        template_content = template_content.replace("[TITULO_LISTA]", escape_latex(lista_dados['titulo']))
        template_content = template_content.replace("[NOME_ESCOLA]", escape_latex(lista_dados.get('cabecalho', '') or ''))
        template_content = template_content.replace("[NOME_PROFESSOR]", "")
        template_content = template_content.replace("[DATA]", "")
        template_content = template_content.replace("[TURMA]", "")
        template_content = template_content.replace("[INSTRUCOES]", escape_latex(lista_dados.get('instrucoes', '') or ''))

        # 4. Gerar o bloco de questoes
        questoes_latex = []
        for i, questao in enumerate(lista_dados['questoes'], 1):
            enunciado = escape_latex(questao.get('enunciado', ''))
            fonte = escape_latex(questao.get('fonte') or '')
            ano = escape_latex(str(questao.get('ano') or ''))

            # Cabecalho da questao
            if fonte or ano:
                item = f"\\item \\textbf{{({ano} - {fonte})}}\n\n"
            else:
                item = "\\item "

            item += f"{enunciado}\n\n"

            # Adicionar alternativas (se objetiva)
            alternativas = questao.get('alternativas', [])
            if alternativas:
                item += "\\begin{enumerate}[label=\\Alph*)]\n"
                for alt in alternativas:
                    texto_alt = escape_latex(alt.get('texto', ''))
                    item += f"    \\item {texto_alt}\n"
                item += "\\end{enumerate}\n"

            item += "\\vspace{0.5cm}\n"
            questoes_latex.append(item)

        # Substituir placeholder de questoes
        questoes_block = "\n".join(questoes_latex)
        template_content = template_content.replace("% [QUESTOES_AQUI]", questoes_block)

        # 5. Gerar o bloco de gabarito ou remover secao inteira
        if opcoes.incluir_gabarito:
            gabarito_latex = []
            for i, questao in enumerate(lista_dados['questoes'], 1):
                resposta = questao.get('resposta') or 'N/A'
                gabarito_latex.append(f"\\item Questao {i}: {escape_latex(str(resposta))}")
            gabarito_block = "\n".join(gabarito_latex)
            template_content = template_content.replace("% [GABARITO_AQUI]", gabarito_block)
        else:
            # Remover secao inteira de gabarito
            template_content = re.sub(
                r'% ={10,}\s*\n% GABARITO \(opcional\)\s*\n% ={10,}\s*\n.*?\\end\{enumerate\}',
                '',
                template_content,
                flags=re.DOTALL
            )

        # 6. Remover secao inteira de resolucoes (nao implementada ainda)
        template_content = re.sub(
            r'% ={10,}\s*\n% RESOLU[ÇC][ÕO]ES \(opcional\)\s*\n% ={10,}\s*\n.*?\\end\{enumerate\}',
            '',
            template_content,
            flags=re.DOTALL
        )

        return template_content

    def exportar_lista(self, opcoes: ExportOptionsDTO) -> Path:
        """
        Orquestra a exportação de uma lista para LaTeX ou PDF.

        Args:
            opcoes: DTO com todas as configurações de exportação.

        Returns:
            Caminho do arquivo gerado (.tex ou .pdf).
        """
        logger.info(f"Iniciando exportação para lista ID {opcoes.id_lista} com opções: {opcoes}")

        # Gerar o conteúdo LaTeX dinamicamente
        # NOTE: A lógica de geração de conteúdo está agora no controller para acessar outros services
        latex_content = self._gerar_conteudo_latex(opcoes)

        output_dir = Path(opcoes.output_dir)
        lista_dados = services.lista.buscar_lista(opcoes.id_lista)
        base_filename = f"{lista_dados['titulo'].replace(' ', '_')}_{opcoes.template_latex.replace('.tex', '')}"

        if opcoes.tipo_exportacao == 'direta':
            logger.info(f"Compilando LaTeX para PDF para lista ID {opcoes.id_lista}...")
            pdf_path = self.export_service.compilar_latex_para_pdf(latex_content, output_dir, base_filename)
            return pdf_path
        else: # 'manual'
            tex_path = output_dir / f"{base_filename}.tex"
            logger.info(f"Escrevendo arquivo .tex manual para: {tex_path}")
            tex_path.write_text(latex_content, encoding='utf-8')
            return tex_path
