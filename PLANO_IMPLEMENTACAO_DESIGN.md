# Plano de Implementação do Design MathBank

## Objetivo
Implementar o design conforme especificado no `FORMALIZACAO-DESIGN.MD`, componentizando e evitando hardcode/magic strings.

---

## Fase 0: Estrutura Base e Constantes

### 0.1 Criar arquivo de constantes de design
**Arquivo:** `src/views/design/constants.py`

```
- Cores (primária, sucesso, atenção, perigo, etc.)
- Espaçamentos (padding, margin, gap)
- Tipografia (tamanhos de fonte, pesos)
- Dimensões (largura sidebar, altura navbar)
- Textos/Labels da interface (i18n-ready)
- Rotas/Páginas disponíveis
```

### 0.2 Criar arquivo de estilos base
**Arquivo:** `src/views/design/styles.py`

```
- Funções para gerar QSS dinâmico
- Classes de estilo reutilizáveis
- Mixins para botões, cards, inputs
```

### 0.3 Criar enums de navegação
**Arquivo:** `src/views/design/enums.py`

```
- Enum de páginas (ESTATISTICAS, BANCO_QUESTOES, LISTAS, TAXONOMIA)
- Enum de ações contextuais
- Enum de tipos de botão
- Enum de níveis de dificuldade (cores)
```

**Entregáveis Fase 0:**
- [ ] `src/views/design/__init__.py`
- [ ] `src/views/design/constants.py`
- [ ] `src/views/design/styles.py`
- [ ] `src/views/design/enums.py`
- [ ] `src/views/design/theme.py` (gerenciador de tema)

---

## Fase 1: Componentes Base Reutilizáveis

### 1.1 Botões
**Arquivo:** `src/views/components/common/buttons.py`

| Componente | Descrição |
|------------|-----------|
| `PrimaryButton` | Botão azul principal (#2563EB) |
| `SecondaryButton` | Botão outline azul |
| `DangerButton` | Botão vermelho para exclusão |
| `IconButton` | Botão apenas com ícone |
| `ContextualActionButton` | Botão que muda conforme página |

### 1.2 Inputs
**Arquivo:** `src/views/components/common/inputs.py`

| Componente | Descrição |
|------------|-----------|
| `TextInput` | Input de texto padrão |
| `SearchInput` | Input com ícone de busca |
| `TextAreaInput` | Área de texto multilinha |
| `LatexTextArea` | Área com suporte LaTeX |
| `SelectInput` | Dropdown/Combobox |
| `DateInput` | Seletor de data |

### 1.3 Badges/Tags
**Arquivo:** `src/views/components/common/badges.py`

| Componente | Descrição |
|------------|-----------|
| `Badge` | Badge genérico com cor customizável |
| `DifficultyBadge` | Badge de dificuldade (Fácil/Médio/Difícil) |
| `SourceBadge` | Badge de fonte (ENEM, FUVEST, etc.) |
| `RemovableBadge` | Badge com botão X para remover |

### 1.4 Cards
**Arquivo:** `src/views/components/common/cards.py`

| Componente | Descrição |
|------------|-----------|
| `BaseCard` | Card base com sombra e bordas |
| `StatCard` | Card de estatística (número + label + variação) |
| `QuestionCard` | Card de questão (código, título, fórmula, tags) |

### 1.5 Feedback
**Arquivo:** `src/views/components/common/feedback.py`

| Componente | Descrição |
|------------|-----------|
| `Toast` | Notificação temporária (sucesso/erro/aviso/info) |
| `LoadingSpinner` | Indicador de carregamento |
| `EmptyState` | Estado vazio com ícone e mensagem |
| `ConfirmDialog` | Diálogo de confirmação |

**Entregáveis Fase 1:**
- [ ] `src/views/components/common/__init__.py`
- [ ] `src/views/components/common/buttons.py`
- [ ] `src/views/components/common/inputs.py`
- [ ] `src/views/components/common/badges.py`
- [ ] `src/views/components/common/cards.py`
- [ ] `src/views/components/common/feedback.py`

---

## Fase 2: Navbar (Componente Principal)

### 2.1 Estrutura da Navbar
**Arquivo:** `src/views/components/layout/navbar.py`

```
┌─────────────────────────────────────────────────────────────────────┐
│  [Logo]  │  Nav1 | Nav2 | Nav3 | Nav4  │  [CtxBtn] [🔔] [⚙] [👤]  │
└─────────────────────────────────────────────────────────────────────┘
```

### 2.2 Subcomponentes da Navbar

| Componente | Arquivo | Descrição |
|------------|---------|-----------|
| `Logo` | `navbar.py` | Ícone Σ + texto "MathBank" |
| `NavMenu` | `navbar.py` | Menu de navegação horizontal |
| `NavItem` | `navbar.py` | Item individual do menu (ativo/inativo) |
| `ActionArea` | `navbar.py` | Área direita com botões |
| `NotificationIcon` | `navbar.py` | Ícone de notificações |
| `SettingsIcon` | `navbar.py` | Ícone de configurações |
| `UserAvatar` | `navbar.py` | Avatar do usuário |

### 2.3 Comportamentos da Navbar

1. **Navegação:**
   - Clique em item → emite sinal `pageChanged(PageEnum)`
   - Item ativo destacado visualmente

2. **Botão Contextual:**
   - Recebe `current_page` e exibe botão apropriado
   - Emite sinal `actionClicked(ActionEnum)`

3. **Sinais emitidos:**
   - `pageChanged(PageEnum)` - Mudança de página
   - `actionClicked(ActionEnum)` - Ação do botão contextual
   - `notificationsClicked()` - Clique em notificações
   - `settingsClicked()` - Clique em configurações
   - `profileClicked()` - Clique no avatar

**Entregáveis Fase 2:**
- [ ] `src/views/components/layout/navbar.py` (reescrito)
- [ ] Testes de navegação entre páginas
- [ ] Botão contextual funcionando

---

## Fase 3: Sidebar (Componente de Navegação Secundária)

### 3.1 Estrutura da Sidebar
**Arquivo:** `src/views/components/layout/sidebar.py`

```
┌──────────────────────┐
│ MATH CONTENT    [^v] │
│ Hierarchical Tags    │
├──────────────────────┤
│ ▼ 1. Algebra    [✓]  │
│   ├─ 1.1 Functions   │
│   │  ├─ 1.1.1 Linear │
│   │  └─ 1.1.2 Quad.. │
│   └─ 1.2 Equations   │
│ ▶ 2. Geometry        │
│ ▶ 3. Calculus        │
├──────────────────────┤
│ [📄 Export to PDF]   │
│ [❓ Help Center]     │
└──────────────────────┘
```

### 3.2 Subcomponentes da Sidebar

| Componente | Descrição |
|------------|-----------|
| `SidebarHeader` | Título + botão expandir/colapsar |
| `TagTreeView` | Árvore hierárquica de tags |
| `TagTreeItem` | Item da árvore (expansível, com checkbox) |
| `SidebarFooter` | Botões de ação (Export, Help) |

### 3.3 Comportamentos

1. **Árvore de Tags:**
   - Expansão/colapso de nós
   - Seleção de tag → filtra questões
   - Checkbox para seleção múltipla (quando aplicável)

2. **Sinais emitidos:**
   - `tagSelected(tag_uuid)` - Tag selecionada
   - `exportClicked()` - Botão exportar
   - `helpClicked()` - Botão ajuda

**Entregáveis Fase 3:**
- [ ] `src/views/components/layout/sidebar.py` (reescrito)
- [ ] Árvore de tags funcional
- [ ] Integração com filtros

---

## Fase 4: MainWindow (Shell da Aplicação)

### 4.1 Estrutura
**Arquivo:** `src/views/pages/main_window.py`

```
┌─────────────────────────────────────────────────────────────────┐
│                         NAVBAR                                  │
├────────────────┬────────────────────────────────────────────────┤
│                │                                                │
│    SIDEBAR     │              CONTENT AREA                      │
│                │            (QStackedWidget)                    │
│                │                                                │
│                │    ┌────────────────────────────────────┐     │
│                │    │  Página atual (lazy loading)       │     │
│                │    └────────────────────────────────────┘     │
│                │                                                │
├────────────────┴────────────────────────────────────────────────┤
│                         STATUS BAR                              │
└─────────────────────────────────────────────────────────────────┘
```

### 4.2 Responsabilidades

1. **Gerenciar navegação** entre páginas
2. **Lazy loading** de páginas (carregar sob demanda)
3. **Atualizar navbar** com página atual
4. **Mostrar/ocultar sidebar** conforme página
5. **Gerenciar estado global** da aplicação

### 4.3 Páginas Gerenciadas

| Página | Classe | Sidebar? |
|--------|--------|----------|
| Estatísticas | `DashboardPage` | Não |
| Banco de Questões | `QuestionBankPage` | Sim |
| Listas | `ExamListPage` | Sim |
| Taxonomia | `TaxonomyPage` | Sim |

**Entregáveis Fase 4:**
- [ ] `src/views/pages/main_window.py` (reescrito)
- [ ] Navegação funcional entre todas as páginas
- [ ] Sidebar condicional

---

## Fase 5: Página Banco de Questões

### 5.1 Estrutura
**Arquivo:** `src/views/pages/question_bank_page.py`

```
┌─────────────────────────────────────────────────────────────────┐
│ Breadcrumb: Algebra / Functions                                 │
├─────────────────────────────────────────────────────────────────┤
│ Question Explorer                    Showing 24 of 1,240 results│
├─────────────────────────────────────────────────────────────────┤
│ [🔍 Search...                    ] [ENEM▼] [Easy×] [Type▼] [⚙] │
├─────────────────────────────────────────────────────────────────┤
│ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐                │
│ │ #Q-1042     │ │ #Q-2051     │ │ #Q-4592     │                │
│ │ Title...    │ │ Title...    │ │ Title...    │                │
│ │ f(x) = ...  │ │ ax² + ...   │ │ ∫ x² dx     │                │
│ │ [ENEM][EASY]│ │ [HARD][UTF] │ │ [CALC][HARD]│                │
│ └─────────────┘ └─────────────┘ └─────────────┘                │
│ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐                │
│ │ ...         │ │ ...         │ │ ...         │                │
│ └─────────────┘ └─────────────┘ └─────────────┘                │
└─────────────────────────────────────────────────────────────────┘
```

### 5.2 Subcomponentes

| Componente | Descrição |
|------------|-----------|
| `Breadcrumb` | Navegação hierárquica |
| `PageHeader` | Título + contador de resultados |
| `FilterBar` | Barra de busca + filtros |
| `QuestionGrid` | Grid responsivo de cards |
| `QuestionCard` | Card individual de questão |
| `Pagination` | Controles de paginação |

**Entregáveis Fase 5:**
- [ ] `src/views/pages/question_bank_page.py`
- [ ] Grid de cards funcional
- [ ] Filtros funcionais
- [ ] Integração com sidebar

---

## Fase 6: Página de Estatísticas (Dashboard)

### 6.1 Estrutura
**Arquivo:** `src/views/pages/dashboard_page.py`

```
┌─────────────────────────────────────────────────────────────────┐
│ [Period: Last 30 Days ▼] [Tags: All ▼] [Difficulty: All ▼]     │
├─────────────────────────────────────────────────────────────────┤
│ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐            │
│ │ 1,234    │ │ +87      │ │ 68.5%    │ │ 4m 32s   │            │
│ │ Total    │ │ New      │ │ Success  │ │ Avg Time │            │
│ └──────────┘ └──────────┘ └──────────┘ └──────────┘            │
├─────────────────────────────────────────────────────────────────┤
│ ┌─────────────────────┐ ┌─────────────────────┐                │
│ │ Questions Over Time │ │ Difficulty Distrib. │                │
│ │ [Gráfico de linha]  │ │ [Gráfico de donut]  │                │
│ └─────────────────────┘ └─────────────────────┘                │
├─────────────────────────────────────────────────────────────────┤
│ Taxa de Acerto por Tópico                                       │
│ [Barras horizontais com percentuais]                            │
├─────────────────────────────────────────────────────────────────┤
│ Top 10 Hardest Questions                         [Export CSV]   │
│ [Tabela com ID, Topic, Tag, Success Rate, Actions]              │
└─────────────────────────────────────────────────────────────────┘
```

### 6.2 Subcomponentes

| Componente | Descrição |
|------------|-----------|
| `FilterRow` | Linha de filtros do dashboard |
| `StatCard` | Card de métrica principal |
| `LineChart` | Gráfico de linha (questões ao longo do tempo) |
| `DonutChart` | Gráfico de rosca (distribuição de dificuldade) |
| `HorizontalBarChart` | Barras horizontais (taxa por tópico) |
| `DataTable` | Tabela de dados (top 10 difíceis) |

**Entregáveis Fase 6:**
- [ ] `src/views/pages/dashboard_page.py` (reescrito)
- [ ] Cards de métricas
- [ ] Gráficos (pode usar matplotlib ou pyqtgraph)
- [ ] Tabela de questões difíceis

---

## Fase 7: Fluxo de Criação de Questão (3 Abas)

### 7.1 Estrutura Geral
**Arquivo:** `src/views/pages/question_editor_page.py`

```
┌─────────────────────────────────────────────────────────────────┐
│ ← Back  │  MathBank  │  [Editor View] [Dual Pane]  │ Cancel │ Save │
├─────────────────────────────────────────────────────────────────┤
│   📝 Editor   │   👁 Preview   │   🏷 Tags                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│                    [Conteúdo da aba atual]                      │
│                                                                 │
├─────────────────────────────────────────────────────────────────┤
│                                          [👁 View Preview]      │
├─────────────────────────────────────────────────────────────────┤
│ 💾 Auto-saved 2 mins ago              QUESTION LANGUAGE: EN-US │
└─────────────────────────────────────────────────────────────────┘
```

### 7.2 Aba Editor
**Arquivo:** `src/views/components/question/editor_tab.py`

| Campo | Tipo | Obrigatório |
|-------|------|-------------|
| Metadata & Mode | Toggle (Objetiva/Discursiva) | Sim |
| Academic Year | TextInput | Sim |
| Origin/Source | TextInput | Sim |
| Question Statement | LatexTextArea + Image | Sim |
| Alternatives (Objetiva) | 5x (TextInput + Radio + Image) | Sim |
| Answer Key (Discursiva) | LatexTextArea + Image | Sim |

### 7.3 Aba Preview
**Arquivo:** `src/views/components/question/preview_tab.py`

- Renderização formatada da questão
- Controles de zoom (100%)
- Botões imprimir/download
- Seção de resolução (visão professor)

### 7.4 Aba Tags
**Arquivo:** `src/views/components/question/tags_tab.py`

- Tags selecionadas (chips removíveis)
- Busca de tags
- Tags mais usadas (sidebar)
- Árvore de taxonomia com checkboxes

**Entregáveis Fase 7:**
- [ ] `src/views/pages/question_editor_page.py`
- [ ] `src/views/components/question/editor_tab.py`
- [ ] `src/views/components/question/preview_tab.py`
- [ ] `src/views/components/question/tags_tab.py`
- [ ] Navegação entre abas
- [ ] Validações conforme MD
- [ ] Botão Save habilitado só com tags

---

## Fase 8: Página de Listas/Provas

### 8.1 Estrutura
**Arquivo:** `src/views/pages/exam_list_page.py`

```
┌────────────────┬─────────────────────────────┬──────────────────┐
│ MY EXAMS       │ EXAM HEADER & INSTRUCTIONS  │ Export Config    │
│ [+ Create New] │                             │                  │
│                │ School Name: [___________]  │ ○ Single Column  │
│ • Calculus I   │ Professor: [___________]    │ ● Two Columns    │
│ • Algebra Quiz │ Exam Date: [___________]    │                  │
│ • Prob Final   │ Department: [___________]   │ ☑ Answer Key     │
│                │                             │ ☑ Point Values   │
│                │ Instructions (LaTeX):       │ ☐ Work Space     │
│                │ [_____________________]     │                  │
│                │                             │ Total: 12 Q      │
│                │ Questions (12 Total)        │ Points: 100/100  │
│                │ [+ Add from Question Bank]  │ Pages: ~4        │
│                │                             │                  │
│                │ Q1 Integration • Power Rule │ [Generate PDF]   │
│                │ Q2 Derivatives • Chain Rule │ [Export LaTeX]   │
└────────────────┴─────────────────────────────┴──────────────────┘
```

**Entregáveis Fase 8:**
- [ ] `src/views/pages/exam_list_page.py`
- [ ] Lista de provas na sidebar
- [ ] Editor de cabeçalho/instruções
- [ ] Lista de questões com drag-and-drop
- [ ] Painel de configuração de exportação

---

## Fase 9: Página de Taxonomia

### 9.1 Estrutura
**Arquivo:** `src/views/pages/taxonomy_page.py`

```
┌────────────────┬─────────────────────────────┬──────────────────┐
│ Math Taxonomy  │ Edit Tag: Quadratics        │ Tag Statistics   │
│ 1,402 tags     │                             │                  │
│                │ ℹ Basic Information         │ 📊 Questions: 12 │
│ [Collapse]     │ Name: [Quadratics____]      │ ✅ Avg Success:68│
│ [Filter]       │ Slug: [algebra-quadratics]  │ 📈 Difficulty:Med│
│                │ Description: [__________]   │                  │
│ ▼ Algebra (120)│                             │ Quick Actions    │
│   ▼ Equations  │ 🎨 Visual Identity          │ [Merge with...]  │
│     ● Quadratic│ Color: ○●○○○○○              │ [Delete Tag]     │
│     ○ Linear   │ Icon: [Σ][📊][📐][%]       │                  │
│ ▶ Calculus (85)│                             │ [💾 Save Changes]│
│ ▶ Geometry (42)│ Associated Exams            │                  │
│                │ [Tabela de provas]          │                  │
└────────────────┴─────────────────────────────┴──────────────────┘
```

**Entregáveis Fase 9:**
- [ ] `src/views/pages/taxonomy_page.py`
- [ ] Árvore de tags editável
- [ ] Formulário de edição de tag
- [ ] Estatísticas da tag
- [ ] Ações rápidas (merge, delete)

---

## Fase 10: Integração e Polimento

### 10.1 Tarefas

- [ ] Revisar todos os sinais e slots
- [ ] Implementar feedback visual (toasts)
- [ ] Adicionar estados de loading
- [ ] Implementar atalhos de teclado
- [ ] Testar navegação completa
- [ ] Ajustar responsividade
- [ ] Revisar acessibilidade

### 10.2 Testes

- [ ] Testar criação de questão (objetiva e discursiva)
- [ ] Testar filtros do banco de questões
- [ ] Testar criação e edição de listas
- [ ] Testar gerenciamento de tags
- [ ] Testar exportação PDF/LaTeX

---

## Estrutura Final de Arquivos

```
src/views/
├── design/                          # NOVO - Fase 0
│   ├── __init__.py
│   ├── constants.py                 # Cores, espaçamentos, textos
│   ├── styles.py                    # Funções de estilo QSS
│   ├── enums.py                     # Enums de páginas, ações
│   └── theme.py                     # Gerenciador de tema
│
├── components/
│   ├── common/                      # NOVO - Fase 1
│   │   ├── __init__.py
│   │   ├── buttons.py               # Botões reutilizáveis
│   │   ├── inputs.py                # Inputs reutilizáveis
│   │   ├── badges.py                # Badges/tags
│   │   ├── cards.py                 # Cards base
│   │   └── feedback.py              # Toast, loading, dialogs
│   │
│   ├── layout/                      # REESCRITO - Fases 2-3
│   │   ├── __init__.py
│   │   ├── navbar.py                # Navbar principal
│   │   └── sidebar.py               # Sidebar com árvore
│   │
│   ├── question/                    # NOVO - Fase 7
│   │   ├── __init__.py
│   │   ├── editor_tab.py            # Aba de edição
│   │   ├── preview_tab.py           # Aba de preview
│   │   └── tags_tab.py              # Aba de tags
│   │
│   └── ... (outros existentes)
│
├── pages/                           # REESCRITO - Fases 4-9
│   ├── __init__.py
│   ├── main_window.py               # Shell principal
│   ├── dashboard_page.py            # Estatísticas
│   ├── question_bank_page.py        # Banco de questões
│   ├── question_editor_page.py      # Criar/editar questão
│   ├── exam_list_page.py            # Listas/provas
│   └── taxonomy_page.py             # Gerenciador de taxonomia
│
└── styles/
    └── mathbank.qss                 # Atualizado com novos estilos
```

---

## Cronograma Sugerido

| Fase | Descrição | Dependências |
|------|-----------|--------------|
| 0 | Estrutura Base e Constantes | Nenhuma |
| 1 | Componentes Base | Fase 0 |
| 2 | Navbar | Fases 0, 1 |
| 3 | Sidebar | Fases 0, 1 |
| 4 | MainWindow | Fases 2, 3 |
| 5 | Banco de Questões | Fase 4 |
| 6 | Dashboard | Fase 4 |
| 7 | Editor de Questão | Fases 4, 1 |
| 8 | Listas/Provas | Fase 4 |
| 9 | Taxonomia | Fase 4 |
| 10 | Integração | Todas |

---

## Observações Importantes

1. **Evitar Hardcode:**
   - Todas as strings em `constants.py`
   - Todas as cores em `constants.py`
   - Usar enums para valores fixos

2. **Componentização:**
   - Componentes pequenos e focados
   - Reutilização máxima
   - Props/parâmetros para customização

3. **Sinais e Slots:**
   - Comunicação via pyqtSignal
   - Desacoplamento entre componentes

4. **Compatibilidade:**
   - Manter re-exports para imports existentes
   - Migração gradual

---

*Documento criado em: 2026-01-20*
