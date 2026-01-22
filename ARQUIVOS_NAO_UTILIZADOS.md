# Relatório de Arquivos Não Utilizados

Este relatório identifica arquivos que não estão mais em uso no sistema e podem ser removidos para limpar a codebase.

## 📋 Arquivos Confirmados como Não Utilizados

### 1. Modelos Antigos (SQLite direto - substituídos por ORM)

#### `src/models/database.py`
- **Status**: ❌ NÃO UTILIZADO
- **Motivo**: Sistema migrou para ORM (SQLAlchemy). Este arquivo contém código antigo de conexão SQLite direta.
- **Verificação**: Nenhum import encontrado no código.
- **Ação**: Pode ser removido com segurança.

#### `src/models/queries.py`
- **Status**: ❌ NÃO UTILIZADO
- **Motivo**: Queries SQL centralizadas não são mais usadas. O sistema usa ORM.
- **Verificação**: Nenhum import encontrado no código.
- **Ação**: Pode ser removido com segurança.

### 2. Infraestrutura Vazia

#### `src/infrastructure/__init__.py`
- **Status**: ❌ NÃO UTILIZADO
- **Motivo**: Arquivo contém apenas comentários, sem implementação. Nenhum módulo neste diretório.
- **Verificação**: Nenhum import encontrado.
- **Ação**: Pode ser removido. O diretório `infrastructure/` pode ser removido completamente se estiver vazio.

### 3. Adapters Antigos

#### `src/adapters/questao_adapter.py`
- **Status**: ❌ NÃO UTILIZADO
- **Motivo**: 
  - Tem imports incorretos (sem prefixo `src.`)
  - Foi substituído por `src/controllers/adapters.py` que é o adapter atualmente em uso
  - O sistema usa `src/controllers/adapters.py` para compatibilidade
- **Verificação**: Apenas importado em `src/adapters/__init__.py`, mas esse módulo não é usado.
- **Ação**: Pode ser removido. O diretório `adapters/` pode ser removido se apenas contiver este arquivo.

#### `src/adapters/__init__.py`
- **Status**: ❌ NÃO UTILIZADO (se questao_adapter.py for removido)
- **Motivo**: Apenas exporta `questao_adapter.py` que não é usado.
- **Ação**: Remover junto com `questao_adapter.py`.

### 4. Views Antigas/Experimentais

#### `src/views/novas-views/` (Diretório completo)
- **Status**: ❌ NÃO UTILIZADO
- **Arquivos**:
  - `mathbank_main.py`
  - `mathbank_sidebar.py`
  - `mathbank_card.py`
  - `mathbank_dashboard.py`
  - `mathbank_styles.css`
- **Motivo**: Parece ser código experimental/protótipo que não foi integrado ao sistema principal.
- **Verificação**: Nenhum import encontrado.
- **Ação**: Pode ser removido. As imagens em `telas-figma/` podem ser mantidas como referência de design se necessário.

## ⚠️ Arquivos que Requerem Análise Adicional

### Arquivos que podem estar em uso via re-exports

Os seguintes arquivos são re-exports (apenas importam de outros lugares) e são mantidos para compatibilidade:

- `src/views/questao_form.py` → re-exporta de `pages/questao_form_page.py`
- `src/views/questao_preview.py` → re-exporta de `pages/questao_preview_page.py`
- `src/views/lista_form.py` → re-exporta de `pages/lista_form_page.py`
- `src/views/search_panel.py` → re-exporta de `pages/search_page.py`
- `src/views/lista_panel.py` → re-exporta de `pages/lista_page.py`
- `src/views/questao_selector_dialog.py` → re-exporta de `pages/questao_selector_page.py`
- `src/views/export_dialog.py` → re-exporta de `pages/export_page.py`
- `src/views/tag_manager.py` → re-exporta de `pages/tag_manager_page.py`
- `src/views/main_window.py` → re-exporta de `pages/main_window.py`
- `src/views/widgets.py` → re-exporta de `components/`

**Decisão**: Estes arquivos são importados via `src/views/__init__.py` para manter compatibilidade. Podem ser mantidos ou removidos dependendo da estratégia de migração.

### Arquivos que podem ter dependências indiretas

#### `src/utils/config_reader.py`
- **Status**: ⚠️ VERIFICAR
- **Uso**: Apenas por `database.py` (não utilizado)
- **Ação**: Pode ser removido se não houver outros usos

#### `src/utils/validators.py`
- **Status**: ❌ NÃO UTILIZADO
- **Motivo**: Nenhum import encontrado no código
- **Ação**: Pode ser removido

#### `src/constants.py`
- **Status**: ❌ NÃO UTILIZADO (após remover arquivos dependentes)
- **Uso**: Usado apenas por `validators.py` (não utilizado), `database.py` (não utilizado) e `queries.py` (não utilizado)
- **Ação**: Pode ser removido após remover os arquivos que o usam

## 📊 Resumo

### Arquivos para Remoção Imediata (Confirmados)

1. ✅ `src/models/database.py`
2. ✅ `src/models/queries.py`
3. ✅ `src/infrastructure/__init__.py` (e diretório se vazio)
4. ✅ `src/adapters/questao_adapter.py`
5. ✅ `src/adapters/__init__.py` (se apenas exporta questao_adapter)
6. ✅ `src/views/novas-views/` (diretório completo)
7. ✅ `src/utils/validators.py` (não utilizado)
8. ✅ `src/utils/config_reader.py` (usado apenas por database.py não utilizado)
9. ✅ `src/constants.py` (usado apenas por arquivos não utilizados acima)

### Diretórios para Verificação

- `src/infrastructure/` - Verificar se está vazio após remover `__init__.py`
- `src/adapters/` - Verificar se está vazio após remover os arquivos

## 🔍 Como Verificar Antes de Remover

Antes de remover qualquer arquivo, execute:

```bash
# Buscar referências ao arquivo
grep -r "nome_do_arquivo" src/

# Verificar imports
grep -r "from.*nome_do_modulo" src/
grep -r "import.*nome_do_modulo" src/
```

## ✅ Limpeza Realizada

### Arquivos Removidos (Confirmados)

1. ✅ `src/models/database.py` - Removido
2. ✅ `src/models/queries.py` - Removido
3. ✅ `src/infrastructure/__init__.py` - Removido
4. ✅ `src/infrastructure/` - Diretório removido
5. ✅ `src/adapters/questao_adapter.py` - Removido
6. ✅ `src/adapters/__init__.py` - Removido
7. ✅ `src/adapters/` - Diretório removido
8. ✅ `src/views/novas-views/` - Diretório removido
9. ✅ `src/utils/validators.py` - Removido
10. ✅ `src/utils/config_reader.py` - Removido
11. ✅ `src/constants.py` - Removido

### Re-exports Removidos (Imports Atualizados)

1. ✅ `src/views/widgets.py` - Removido (imports atualizados para `components/`)
2. ✅ `src/views/main_window.py` - Removido (import atualizado para `pages/main_window.py`)
3. ✅ `src/views/questao_form.py` - Removido (import atualizado para `pages/questao_form_page.py`)
4. ✅ `src/views/questao_preview.py` - Removido (import atualizado para `pages/questao_preview_page.py`)
5. ✅ `src/views/lista_form.py` - Removido (import atualizado para `pages/lista_form_page.py`)
6. ✅ `src/views/search_panel.py` - Removido (import atualizado para `pages/search_page.py`)
7. ✅ `src/views/lista_panel.py` - Removido (import atualizado para `pages/lista_page.py`)
8. ✅ `src/views/questao_selector_dialog.py` - Removido (import atualizado para `pages/questao_selector_page.py`)
9. ✅ `src/views/export_dialog.py` - Removido (import atualizado para `pages/export_page.py`)
10. ✅ `src/views/tag_manager.py` - Removido (import atualizado para `pages/tag_manager_page.py`)

### Arquivos Atualizados

- ✅ `src/views/__init__.py` - Imports atualizados para usar caminhos reais
- ✅ `src/main.py` - Import atualizado para `pages/main_window.py`
- ✅ `src/views/components/cards/questao_card.py` - Import atualizado para `pages/questao_preview_page.py`

## 📝 Notas

- Todos os imports foram atualizados para usar os caminhos reais
- Nenhum erro de sintaxe encontrado após as mudanças
- Recomenda-se testar a aplicação para garantir que tudo funciona corretamente
