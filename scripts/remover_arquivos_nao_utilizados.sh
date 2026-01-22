#!/bin/bash
# Script para remover arquivos não utilizados identificados na análise
# ATENÇÃO: Execute este script com cuidado e faça backup antes!

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"

echo "=========================================="
echo "REMOVENDO ARQUIVOS NÃO UTILIZADOS"
echo "=========================================="
echo ""

# Lista de arquivos para remover
FILES_TO_REMOVE=(
    "src/models/database.py"
    "src/models/queries.py"
    "src/infrastructure/__init__.py"
    "src/adapters/questao_adapter.py"
    "src/adapters/__init__.py"
    "src/utils/validators.py"
    "src/utils/config_reader.py"
    "src/constants.py"
)

# Diretórios para remover (após verificar se estão vazios)
DIRS_TO_REMOVE=(
    "src/infrastructure"
    "src/adapters"
    "src/views/novas-views"
)

echo "Arquivos a serem removidos:"
for file in "${FILES_TO_REMOVE[@]}"; do
    if [ -f "$file" ]; then
        echo "  - $file"
    else
        echo "  - $file (não encontrado)"
    fi
done

echo ""
echo "Diretórios a serem removidos:"
for dir in "${DIRS_TO_REMOVE[@]}"; do
    if [ -d "$dir" ]; then
        echo "  - $dir"
    else
        echo "  - $dir (não encontrado)"
    fi
done

echo ""
read -p "Deseja continuar? (s/N): " -n 1 -r
echo ""

if [[ ! $REPLY =~ ^[Ss]$ ]]; then
    echo "Operação cancelada."
    exit 0
fi

echo ""
echo "Removendo arquivos..."
for file in "${FILES_TO_REMOVE[@]}"; do
    if [ -f "$file" ]; then
        rm "$file"
        echo "  ✓ Removido: $file"
    fi
done

echo ""
echo "Removendo diretórios..."
for dir in "${DIRS_TO_REMOVE[@]}"; do
    if [ -d "$dir" ]; then
        # Verificar se diretório está vazio (exceto __pycache__)
        if [ -z "$(find "$dir" -type f -not -path '*/__pycache__/*' -not -name '__pycache__')" ]; then
            rm -rf "$dir"
            echo "  ✓ Removido: $dir"
        else
            echo "  ⚠ Diretório não está vazio: $dir"
        fi
    fi
done

echo ""
echo "=========================================="
echo "LIMPEZA CONCLUÍDA"
echo "=========================================="
echo ""
echo "⚠️  IMPORTANTE:"
echo "  1. Teste a aplicação para garantir que nada quebrou"
echo "  2. Execute: python3 -m py_compile src/**/*.py (se disponível)"
echo "  3. Verifique se há erros de importação"
