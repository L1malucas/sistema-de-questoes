# Documentação de Regras de Interface Gráfica - MathBank

## 1. Estrutura de Navegação Principal

### 1.1 Navbar (Barra de Navegação)
- **Posição**: Fixa no topo da aplicação
- **Componentes**:
  - **Logo** (esquerda): "MathBank" com ícone Σ
  - **Menu de Navegação** (centro):
    - Estatísticas
    - Banco de Questões
    - Listas
    - Taxonomia
  - **Área de Ação** (direita):
    - Botão contextual (varia por página)
    - Ícone de notificações
    - Ícone de configurações
    - Avatar do usuário (vindo do banco de dados)

### 1.2 Botão de Ação Contextual (Canto Superior Direito)
O botão muda conforme a página ativa:

| Página | Botão | Ícone | Cor |
|--------|-------|-------|-----|
| Estatísticas | Nenhum | - | - |
| Banco de Questões | "Criar Questão" | + | Azul primário |
| Listas | "Criar Nova Lista" | + | Azul primário |
| Taxonomia | "Nova Tag" | + | Azul primário |

---

## 2. Fluxo de Criação de Questões

### 2.1 Estrutura de Abas
O fluxo possui 3 abas sequenciais:
1. **Editor** (Criação)
2. **Visualizar** (Pré-visualização)
3. **Tags** (Classificação)

### 2.2 Navegação Entre Abas
- **Permitido**: Usuário pode clicar em qualquer aba para navegar
- **Restrição de Salvamento**: Só pode salvar após completar:
  - ✓ Criar questão (Editor)
  - ✓ Associar pelo menos 1 tag (Tags)

### 2.3 Botão "Visualizar Prévia"
- **Posição**: Flutuante, canto inferior direito
- **Função**: Avançar para próxima etapa
- **Comportamento por Aba**:
  - Editor → "Visualizar Prévia" (vai para aba Visualizar)
  - Visualizar → "Continuar para Tags" (vai para aba Tags)
  - Tags → "Salvar Questão" (salva e finaliza)

### 2.4 Botão "Salvar Questão"
- **Posição**: Canto superior direito (fixo na navbar)
- **Estados**:
  - **Desabilitado**: Quando tags não foram associadas
  - **Habilitado**: Quando pelo menos 1 tag foi associada
- **Ação**: Salva questão e retorna ao Banco de Questões

---

## 3. Tela 1: Editor (Criação de Questão)

### 3.1 Seletor de Tipo de Questão
- **Metadados e Modo**: Seletor com 2 opções
  - Objetiva
  - Discursiva

### 3.2 Campos Comuns (Ambos os Tipos)
- **Ano Acadêmico**: Campo de texto 
  - *Exemplo de valor do BD*: "2024"
- **Origem/Fonte**: Fonte da questão 
  - *Exemplo de valor do BD*: "Olimpíada Brasileira de Matemática"
- **Enunciado da Questão**: Área de texto para enunciado
  - Suporta LaTeX (botões Σ e B)
  - Opção "Adicionar Imagem"
  - *Valor do BD*: texto do enunciado com possível marcação LaTeX

### 3.3 Questões Objetivas
**Campos Adicionais**:
- **Alternativas de Múltipla Escolha**: 5 opções (A-E)
  - Campo de texto/LaTeX para cada alternativa
  - Radio button "Correta" para marcar resposta
  - Botão de imagem por alternativa
  - Contador "5 Opções"
  - *Valores do BD*: array de alternativas, cada uma com campos: texto, correta (boolean), imagem_url

**Validações**:
- ✓ Pelo menos 1 alternativa deve ser marcada como correta
- ✓ Todas as alternativas devem ter conteúdo

### 3.4 Questões Discursivas
**Campos Adicionais**:
- **Gabarito / Solução Esperada**: Área de texto expandida
  - Suporta LaTeX
  - Tag "GABARITO" (badge verde)
  - Botão de imagem
  - *Valor do BD*: texto da solução esperada com marcação LaTeX

**Validações**:
- ✓ Campo de resposta esperada deve estar preenchido

---

## 4. Tela 2: Visualizar

### 4.1 Estrutura da Pré-visualização
- **Cabeçalho**:
  - Título: *valor do BD*: nome_evento (ex: "OLIMPÍADA BRASILEIRA DE MATEMÁTICA")
  - Subtítulo: *valor do BD*: fase + " - " + ano_academico (ex: "Sessão de Álgebra Avançada - Ano Acadêmico 2024")
  - ID de Referência (canto superior direito): *valor do BD*: codigo_referencia (ex: "REF: #Q-4B2-D24")

- **Corpo da Questão**:
  - Numeração (ex: "01.")
  - Enunciado formatado: *valor do BD*: enunciado
  - Equações LaTeX renderizadas
  - Imagens: *valor do BD*: imagens_urls (se houver)

### 4.2 Pré-visualização de Questão Objetiva
- Lista de alternativas (A-E): *valor do BD*: alternativas[]
- Marcação visual da alternativa correta (ícone ✓ verde)
- Badges de identificação: "CORRETA"

### 4.3 Pré-visualização de Questão Discursiva
- **Resolução e Explicação**: Seção expandível
  - Passos da resolução: *valor do BD*: passos_resolucao[]
  - Equações formatadas
  - Explicações detalhadas: *valor do BD*: explicacao_detalhada

### 4.4 Controles da Pré-visualização
- **Zoom**: 100% (controles +/-)
- **Imprimir**: Botão de impressão
- **Baixar**: Botão de download

### 4.5 Seção de Referência (Rodapé)
- "SOLUÇÃO DE REFERÊNCIA (VISÃO DO PROFESSOR)"
- Resolução Detalhada: *valor do BD*: resolucao_detalhada
- "GERADOR AUTOMÁTICO DE PROVAS MATHBANK"
- Paginação: "PÁGINA 1 / 1"

---

## 5. Tela 3: Tags

### 5.1 Estrutura da Tela
- **Título**: "Árvore de Taxonomia Matemática"
- **Controles**: "Expandir Tudo" | "Colapsar Tudo"

### 5.2 Tags Selecionadas (Topo)
- "SELECIONADAS PARA ESTA QUESTÃO:"
- Tags em formato de chips com ícone X para remover
- *Valores do BD*: tags_selecionadas[] (ex: ["Equações Quadráticas", "Álgebra"])

### 5.3 Árvore de Taxonomia (Hierárquica)
**Estrutura de 3 níveis**:
1. **Área Principal** 
   - *Valor do BD*: areas[] (ex: "1. Álgebra")
   - Checkbox para seleção
   - Ícone de expansão (▼/▶)
2. **Subcategoria**
   - *Valor do BD*: subcategorias[] (ex: "1.1 Funções")
   - Checkbox para seleção
3. **Tópico Específico**
   - *Valor do BD*: topicos[] (ex: "1.1.2 Equações Quadráticas")
   - Checkbox para seleção
   - Cor azul quando selecionado

**Áreas Disponíveis** (estrutura de exemplo - dados do BD):
- 1. Álgebra
  - 1.1 Funções
    - 1.1.1 Funções Lineares
    - 1.1.2 Equações Quadráticas ✓
    - 1.1.3 Funções Exponenciais
- 2. Geometria
- 3. Trigonometria
- 4. Cálculo
- 5. Probabilidade e Estatística

### 5.4 Barra Lateral Esquerda
**Seção "Mais Usadas"**:
- Lista de tags mais usadas
- Contador de usos ao lado
- *Valores do BD*: tags_frequentes[] com campos: nome, quantidade_usos
- Exemplos:
  - Cálculo I (42 usos)
  - Logaritmos (38 usos)
  - Trigonometria (29 usos)
  - Geometria Espacial (25 usos)

### 5.5 Validação de Tags
- **Mínimo**: 1 tag obrigatória
- **Recomendado**: Tags específicas (nível 3)
- **Comportamento**: Botão "Salvar Questão" só ativa com tags

---

## 6. Estatísticas/Dashboard

### 6.1 Métricas Principais (Cards no Topo)
- **Total de Questões**: 
  - *Valor do BD*: total_questoes (ex: "1.234")
  - Variação percentual: *valor do BD*: variacao_mensal (ex: "+2.4% vs mês passado")
  
- **Novas Este Mês**: 
  - *Valor do BD*: novas_questoes_mes (ex: "+87")
  - Taxa de crescimento: *valor do BD*: taxa_crescimento (ex: "+12.5% taxa de crescimento")
  
- **Taxa de Sucesso**: 
  - *Valor do BD*: taxa_acerto_geral (ex: "68.5%")
  - Indicador: *valor do BD*: variacao_taxa_acerto (ex: "-1.2% precisão")
  
- **Tempo Médio de Resolução**: 
  - *Valor do BD*: tempo_medio_resolucao (ex: "4m 32s")
  - Comparação: *valor do BD*: variacao_tempo (ex: "+0.5% mais rápido")

### 6.2 Gráficos
**Questões Adicionadas ao Longo do Tempo**:
- Gráfico de linha
- Tendência mensal
- *Dados do BD*: questoes_por_mes[] com campos: mes, quantidade
- Comparação: *valor do BD*: variacao_anual (ex: "+15% vs ano anterior")

**Distribuição de Dificuldade**:
- Gráfico de donut
- *Dados do BD*: distribuicao_dificuldade[] com campos:
  - Fácil: percentual (ex: 25%)
  - Médio: percentual (ex: 40%)
  - Difícil: percentual (ex: 20%)
  - Muito Difícil: percentual (ex: 15%)

### 6.3 Taxa de Acerto por Tópico
- Título: "Taxa de Acerto por Tópico"
- Barras horizontais com percentuais
- Ordenação por performance
- *Dados do BD*: taxa_acerto_topicos[] com campos: nome_topico, percentual_acerto
- Exemplos:
  - Álgebra Linear: 82.4%
  - Cálculo Diferencial: 64.1%
  - Geometria Analítica: 58.7%
  - Trigonometria: 45.2%
  - Estatística & Probabilidade: 38.9%

### 6.4 Top 10 Questões Mais Difíceis
- Tabela com colunas:
  - ID: *valor do BD*: codigo_questao (ex: "#Q-8821")
  - Tópico: *valor do BD*: nome_topico (ex: "Números Complexos")
  - Tag: *valor do BD*: nivel_dificuldade (badge colorido - ex: "MUITO DIFÍCIL")
  - Taxa de Acerto: *valor do BD*: taxa_acerto (ex: "4.2%")
  - Ações: ícone de visualização
- Link "VER TODAS AS QUESTÕES DIFÍCEIS"

### 6.5 Filtros (Topo da Dashboard)
- **Período**: Dropdown com valor padrão "Últimos 30 Dias"
- **Tags**: Dropdown com valor padrão "Todas"
- **Dificuldade**: Dropdown com valor padrão "Todas"

---

## 7. Banco de Questões / Explorador de Questões

### 7.1 Estrutura da Página
**Sidebar Esquerda**:
- **Conteúdo Matemático** (Hierárquico)
  - Árvore de navegação colapsável
  - Contador de questões por categoria
  - *Dados do BD*: taxonomia_completa[] (estrutura idêntica à aba Tags)

**Área Principal**:
- **Breadcrumb**: *valor do BD*: caminho_navegacao (ex: "Álgebra / Funções")
- **Título**: "Explorador de Questões"
- **Contador**: *valor do BD*: "Mostrando " + questoes_visiveis + " de " + total_questoes + " resultados" (ex: "Mostrando 24 de 1.240 resultados")

### 7.2 Barra de Pesquisa e Filtros
- **Pesquisar**: Placeholder "Pesquisar por ID, trecho do enunciado ou tags..."
- **Filtros Rápidos**:
  - Fonte: *valor do BD*: fonte_selecionada (ex: "ENEM" - removível com X)
  - Dificuldade: *valor do BD*: dificuldade_selecionada (ex: "Fácil" - removível com X)
  - Tipo: Dropdown
- **Botão "Filtros"**: Abre filtros avançados

### 7.3 Cards de Questões
**Estrutura de cada Card**:
- **ID**: *valor do BD*: codigo_questao (ex: "#Q-1042" - link clicável)
- **Título**: *valor do BD*: titulo_questao (ex: "Limites de Funções e Comportamento Assintótico no Infinito")
- **Preview**: Snippet LaTeX da questão - *valor do BD*: preview_enunciado
- **Tags** (badges coloridos):
  - Fonte: *valor do BD*: fonte (ex: "ENEM")
  - Dificuldade: *valor do BD*: dificuldade (ex: "FÁCIL")
  - Categoria: *valor do BD*: categoria (ex: "FUNÇÕES")
- **Ícones de Ação**:
  - Alvo/Visualizar
  - Menu de opções (⋮)

### 7.4 Tipos de Ícones por Questão
- **🎯 Alvo**: Questões objetivas
- **✏️ Lápis**: Questões discursivas
- **📊 Gráfico**: Questões com dados/gráficos

### 7.5 Página de Detalhes da Questão

**Cabeçalho**:
- Breadcrumb: *valor do BD*: "Explorador de Questões / " + codigo_questao
- Botões: "Editar Questão" | "Excluir" | "Adicionar à Lista"

**Conteúdo Principal**:
- ID: *valor do BD*: "QUESTÃO " + codigo_questao
- Título completo: *valor do BD*: titulo_completo
- Enunciado: *valor do BD*: enunciado (com LaTeX renderizado)
- Imagem: *valor do BD*: imagem_url (se houver)
- Alternativas: *valor do BD*: alternativas[] com indicador de resposta correta

**Sidebar Direita - METADADOS**:
- **Fonte**: *valor do BD*: fonte + " - " + descricao_fonte (ex: "ENEM 2022 - Exame Nacional")
- **Dificuldade**: *valor do BD*: nivel_dificuldade (barra visual colorida)
- **Categoria**: *valor do BD*: categoria_hierarquica (ex: "1.1 Funções")
- **Data de Criação**: *valor do BD*: data_criacao (ex: "12 de Agosto de 2023")
- **Tags**: *valor do BD*: tags[] (badges - ex: "CÁLCULO", "LIMITES", "ASSÍNTOTAS", "FUNÇÕES RACIONAIS")

**Seção de Resolução**:
- "📝 Resolução e Explicação"
- Passos numerados: *valor do BD*: passos_resolucao[]
- Equações LaTeX
- Explicação detalhada: *valor do BD*: explicacao_completa

**Estatísticas de Uso**:
- **Listas**: *valor do BD*: quantidade_listas (ex: "12")
- **Taxa de Acerto**: *valor do BD*: taxa_acerto (ex: "84%")

---

## 8. Listas/Provas

### 8.1 Sidebar - MINHAS LISTAS
- **Botão**: "+ Criar Nova Lista"
- **Lista de Listas**:
  - *Valores do BD*: listas_usuario[] com campos: nome, data_modificacao, ativo
  - Exemplos:
    - Cálculo I - Prova Intermediária (ativo)
    - Álgebra Linear Quiz 2
    - Prova Final de Probabilidade
    - Geometria - Unidade 3

### 8.2 Área Central - Cabeçalho e Instruções da Lista
**Campos do Cabeçalho**:
- **Nome da Escola**: *valor do BD*: nome_escola (ex: "Universidade de Matemática e Ciências")
- **Nome do Professor**: *valor do BD*: nome_professor (ex: "Dra. Elena Rodriguez")
- **Data da Prova**: Seletor de data - *valor do BD*: data_prova
- **Departamento**: *valor do BD*: departamento (ex: "Matemática - Depto. de Cálculo")

**Instruções** (Suporte LaTeX Habilitado):
- Área de texto para instruções
- *Valor do BD*: instrucoes_prova
- Exemplo: "Mostre todo o seu trabalho. Não é permitido o uso de calculadoras, exceto científicas não programáveis. Tempo limite: 120 minutos..."

### 8.3 Seção de Questões
- **Título**: *valor do BD*: "Questões (" + total_questoes + " Total)"
- **Botão**: "🔵 Adicionar do Banco de Questões"
- **Lista de Questões**:
  - Arraste (⋮⋮)
  - Número da questão: *valor do BD*: numero_ordem (Q1, Q2...)
  - Tópico e subtópico: *valor do BD*: topico + " • " + subtopico
  - Nível de dificuldade: *valor do BD*: nivel_dificuldade
  - Pontuação: *valor do BD*: pontos + " pts"
  - Menu de ações (⋮)

**Exemplo de Questão** (dados do BD):
- **Q1**: *topico*: "Integração" • *subtopico*: "Regra da Potência" • Nível: *nivel*: "Médio"
- **5 pts**
- Preview: *preview_latex*: "$\int (3x^2 - 5x + 2) \, dx$"

### 8.4 Configuração de Exportação (Sidebar Direita)

**Layout da Página**:
- Coluna Única (selecionado)
- Duas Colunas

**Incluir na Exportação**:
- ✓ Gabarito (toggle azul)
- ✓ Valores de Pontos (toggle azul)
- ○ Espaço de Trabalho (Linhas em branco) (toggle cinza)

**Estilo LaTeX**:
- Dropdown: "Classe de Prova (Padrão)"

**Resumo do Documento**:
- Total de Questões: *valor do BD*: total_questoes (ex: "12")
- Total de Pontos: *valor do BD*: pontos_obtidos + " / " + pontos_totais (ex: "100 / 100")
- Páginas Estimadas: *valor do BD*: paginas_estimadas (ex: "4")

**Botões de Ação**:
- **Gerar PDF** (azul primário)
- **Exportar Código LaTeX** (outline azul)

---

## 9. Gerenciador de Taxonomia

### 9.1 Cabeçalho
- Logo: Ícone de taxonomia
- Título: "Gerenciador de Taxonomia"
- **Pesquisar**: "Pesquisa global..."
- **Botão**: "+ Nova Tag"
- Avatar do usuário: *valor do BD*: avatar_url

### 9.2 Sidebar - Taxonomia Matemática
- **Contador**: *valor do BD*: total_tags + " tags ativas em todos os níveis" (ex: "1.402 tags ativas em todos os níveis")
- **Controles**: "⚡ Colapsar" | "🔽 Filtrar"

**Árvore Hierárquica** (colapsável):
- *Dados do BD*: taxonomia_completa[] com campos: nome, total_tags, nivel
- Exemplos:
  - **📊 Álgebra** (120 tags)
    - Equações (45)
      - **● Quadráticas** (12) ← Selecionado
      - ○ Sistemas Lineares (33)
  - **ƒₓ Cálculo** (85)
  - **▲ Geometria** (42)

### 9.3 Área Central - Editar Tag: Quadráticas

**ℹ️ Informações Básicas**:
- **Nome da Tag**: *valor do BD*: nome_tag (ex: "Quadráticas")
- **Slug**: *valor do BD*: slug (ex: "algebra-quadraticas")
- **Descrição**: *valor do BD*: descricao (ex: "Foca em equações polinomiais de segundo grau, incluindo fatoração, completar o quadrado e a fórmula quadrática.")

**🎨 Identidade Visual**:
- **Cor da Tag**: Paleta de cores (vermelho, azul ✓, verde, amarelo, roxo, rosa, laranja, +)
  - *Valor do BD*: cor_tag
- **Seleção de Ícone**: Conjunto de ícones (Σ, 📊, 📐, %, ⊕, ∞)
  - *Valor do BD*: icone_tag

**Listas Associadas**:
- Tabela com colunas:
  - Nome da Lista: *valor do BD*: nome_lista
  - Peso: *valor do BD*: peso_percentual
  - Data de Adição: *valor do BD*: data_adicao
  - Ações
- Exemplo: "Prática SAT Matemática 1" | 15,0% | 12 de Out, 2023 | ✏️
- Link: "Ver Todas"

### 9.4 Sidebar Direita - Estatísticas da Tag

**📊 Questões**: *valor do BD*: total_questoes (ex: "12")
**✅ Sucesso Médio**: *valor do BD*: taxa_acerto_media (ex: "68%")
**📈 Dificuldade**: *valor do BD*: nivel_dificuldade (ex: "Médio")

**Ações Rápidas**:
- "Mesclar com outra..." (com ícone ↗)
- "Excluir Tag" (vermelho, com ícone 🗑️)

**Botão Principal**:
- **💾 Salvar Alterações** (azul primário)

---

## 10. Paleta de Cores e Estilos

### 10.1 Cores Principais
- **Primária (Azul)**: #2563EB (botões principais, links)
- **Sucesso (Verde)**: #10B981 (correto, métricas positivas)
- **Atenção (Laranja)**: #F59E0B (avisos)
- **Perigo (Vermelho)**: #EF4444 (exclusão, erros)
- **Informação (Azul claro)**: #3B82F6 (informações)

### 10.2 Cores de Dificuldade
- **Fácil**: Verde (#10B981)
- **Médio**: Laranja (#F59E0B)
- **Difícil**: Vermelho (#EF4444)
- **Muito Difícil**: Roxo (#8B5CF6)

### 10.3 Badges/Tags
- Cantos arredondados (rounded-full ou rounded-md)
- Tamanho de texto pequeno (text-xs ou text-sm)
- Padding: px-2 py-1 ou px-3 py-1.5

### 10.4 Tipografia
- **Títulos**: Font weight bold (font-bold)
- **Subtítulos**: Font weight semibold (font-semibold)
- **Corpo**: Font weight normal (font-normal)
- **LaTeX**: Fonte matemática renderizada

---

## 11. Componentes Reutilizáveis

### 11.1 Botões
**Primário (Azul)**:
- Background: bg-blue-600
- Hover: hover:bg-blue-700
- Texto branco
- Padding: px-4 py-2
- Border radius: rounded-md

**Secundário (Outline)**:
- Border: border-2 border-blue-600
- Texto: text-blue-600
- Background: transparente
- Hover: hover:bg-blue-50

**Perigo (Vermelho)**:
- Background: bg-red-600
- Hover: hover:bg-red-700
- Uso: exclusão, ações destrutivas

### 11.2 Cards
- Background: bg-white
- Border: border border-gray-200
- Shadow: shadow-sm
- Border radius: rounded-lg
- Padding: p-4 ou p-6

### 11.3 Inputs/Formulários
- Border: border border-gray-300
- Focus: focus:ring-2 focus:ring-blue-500
- Border radius: rounded-md
- Padding: px-3 py-2

### 11.4 Dropdowns/Selects
- Ícone de dropdown: ▼
- Border: igual aos inputs
- Opções: lista com hover:bg-gray-100

### 11.5 Toggles/Switches
- Estado ativo: bg-blue-600
- Estado inativo: bg-gray-300
- Animação de transição suave

### 11.6 Modals/Diálogos
- Overlay: bg-black/50 (semi-transparente)
- Container: bg-white, rounded-lg, shadow-xl
- Posição: centralizado na tela
- Max width: max-w-2xl ou max-w-4xl

---

## 12. Responsividade


### 12.1 Comportamento Mobile
- Sidebar lateral: transforma em menu hambúrguer
- Cards: empilhamento vertical
- Tabelas: scroll horizontal com cards
- Navbar: itens colapsáveis

---

## 13. Estados e Feedback

### 13.1 Estados de Botões
- **Padrão**: Cor padrão
- **Hover**: Escurecimento leve
- **Ativo/Pressionado**: Escurecimento maior
- **Desabilitado**: Opacidade 50%, cursor not-allowed
- **Carregando**: Spinner + texto "Carregando..."

### 13.2 Estados de Formulário
- **Vazio**: Border cinza
- **Preenchido**: Border cinza
- **Foco**: Border azul + ring
- **Erro**: Border vermelho + mensagem
- **Sucesso**: Border verde + ícone ✓

### 13.3 Feedback de Ações
- **Sucesso**: Toast verde no topo direito (ex: "Questão salva com sucesso!")
- **Erro**: Toast vermelho no topo direito (ex: "Erro ao salvar questão")
- **Atenção**: Toast amarelo no topo direito (ex: "Associe pelo menos uma tag")
- **Informação**: Toast azul no topo direito (ex: "Prévia atualizada")

### 13.4 Estados de Carregamento
- **Página completa**: Spinner centralizado
- **Seção**: Skeleton screens
- **Botão**: Spinner pequeno + desabilitado

---

## 14. Validações e Regras de Negócio

### 14.1 Criação de Questão
**Campos obrigatórios**:
- ✓ Ano Acadêmico
- ✓ Origem/Fonte
- ✓ Enunciado da Questão
- ✓ Para objetivas: pelo menos 1 alternativa marcada como correta
- ✓ Para discursivas: gabarito/solução esperada preenchido

**Regras de salvamento**:
- ✓ Todos os campos obrigatórios preenchidos
- ✓ Pelo menos 1 tag associada
- ✓ Botão "Salvar Questão" só ativo quando válido

### 14.2 Criação de Lista
**Validações**:
- ✓ Pelo menos 1 questão adicionada
- ✓ Campos de cabeçalho preenchidos (nome da escola, professor, data, departamento)
- ✓ Total de pontos configurado

### 14.3 Gerenciamento de Tags
**Regras**:
- ✓ Nome de tag único
- ✓ Slug gerado automaticamente a partir do nome
- ✓ Cor obrigatória
- ✓ Não pode excluir tag com questões associadas (ou confirmarexclusão em cascata)

---

## 15. Acessibilidade

### 15.1 Navegação por Teclado
- Tab: navega entre elementos interativos
- Enter/Space: ativa botões e checkboxes
- Esc: fecha modals e dropdowns
- Setas: navega em listas e árvores

### 15.2 Labels e ARIA
- Todos os inputs têm labels visíveis ou aria-label
- Botões com ícones têm aria-label descritivo
- Estados anunciados para leitores de tela

### 15.3 Contraste
- Texto: contraste mínimo 4.5:1
- Elementos interativos: contraste mínimo 3:1
- Estados de foco claramente visíveis

---

## 16. Animações e Transições

### 16.1 Transições Padrão
- Duração: 150ms-300ms
- Easing: ease-in-out
- Propriedades: opacity, transform, background-color

### 16.2 Animações Específicas
- **Modals**: Fade in + scale
- **Toasts**: Slide in from top
- **Dropdowns**: Fade + slide down
- **Tabs**: Underline slide
- **Collapses**: Max-height transition

---

## 17. Mensagens do Sistema (Exemplos de Textos)

### 17.1 Mensagens de Sucesso
- "Questão criada com sucesso!"
- "Lista salva com sucesso!"
- "Tag atualizada com sucesso!"
- "Questão adicionada à lista"
- "Alterações salvas"

### 17.2 Mensagens de Erro
- "Erro ao salvar questão. Tente novamente."
- "Preencha todos os campos obrigatórios"
- "Selecione pelo menos uma alternativa correta"
- "Associe pelo menos uma tag à questão"
- "Este nome de tag já existe"

### 17.3 Mensagens de Confirmação
- "Tem certeza que deseja excluir esta questão?"
- "Esta ação não pode ser desfeita"
- "Deseja remover esta questão da lista?"
- "Excluir tag permanentemente?"

### 17.4 Placeholders
- "Digite o enunciado da questão..."
- "Descreva a solução esperada..."
- "Pesquisar questões..."
- "Nome da lista..."
- "Instruções para os alunos..."
