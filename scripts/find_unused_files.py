#!/usr/bin/env python3
"""
Script para identificar arquivos Python não utilizados no projeto.
Analisa imports e referências para encontrar arquivos órfãos.
"""

import os
import ast
import re
from pathlib import Path
from typing import Set, Dict, List
from collections import defaultdict

# Diretório raiz do projeto
PROJECT_ROOT = Path(__file__).parent.parent
SRC_DIR = PROJECT_ROOT / "src"


def get_all_python_files(directory: Path) -> Set[Path]:
    """Retorna todos os arquivos Python no diretório"""
    python_files = set()
    for root, dirs, files in os.walk(directory):
        # Ignorar __pycache__ e venv
        dirs[:] = [d for d in dirs if d not in ['__pycache__', 'venv', '.git']]
        for file in files:
            if file.endswith('.py'):
                python_files.add(Path(root) / file)
    return python_files


def get_module_path(file_path: Path) -> str:
    """Converte caminho de arquivo para nome de módulo"""
    # Relativo ao src/
    rel_path = file_path.relative_to(SRC_DIR)
    # Remove extensão .py
    module_parts = list(rel_path.parts[:-1]) + [rel_path.stem]
    # Converte para formato de import
    return '.'.join(module_parts)


def extract_imports(file_path: Path) -> Set[str]:
    """Extrai todos os imports de um arquivo Python"""
    imports = set()
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Parse AST para imports formais
        try:
            tree = ast.parse(content, filename=str(file_path))
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        imports.add(alias.name.split('.')[0])
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        imports.add(node.module.split('.')[0])
        except SyntaxError:
            pass
        
        # Buscar imports dinâmicos (importlib, __import__, etc)
        # Buscar padrões como: from src.xxx import, import src.xxx
        patterns = [
            r'from\s+src\.([a-zA-Z_][a-zA-Z0-9_.]*)',
            r'import\s+src\.([a-zA-Z_][a-zA-Z0-9_.]*)',
        ]
        for pattern in patterns:
            matches = re.findall(pattern, content)
            for match in matches:
                imports.add('src.' + match.split('.')[0])
        
    except Exception as e:
        print(f"Erro ao processar {file_path}: {e}")
    
    return imports


def find_unused_files():
    """Encontra arquivos não utilizados"""
    print("=" * 80)
    print("ANÁLISE DE ARQUIVOS NÃO UTILIZADOS")
    print("=" * 80)
    print()
    
    # Obter todos os arquivos Python
    all_files = get_all_python_files(SRC_DIR)
    print(f"Total de arquivos Python encontrados: {len(all_files)}")
    print()
    
    # Mapear módulos para arquivos
    module_to_file: Dict[str, Path] = {}
    file_to_module: Dict[Path, str] = {}
    
    for file_path in all_files:
        module_name = get_module_path(file_path)
        module_to_file[module_name] = file_path
        file_to_module[file_path] = module_name
    
    # Coletar todos os imports
    all_imports: Set[str] = set()
    imports_by_file: Dict[Path, Set[str]] = {}
    
    print("Analisando imports...")
    for file_path in all_files:
        imports = extract_imports(file_path)
        imports_by_file[file_path] = imports
        all_imports.update(imports)
    
    # Arquivos que são importados
    imported_modules: Set[str] = set()
    for imports in imports_by_file.values():
        for imp in imports:
            # Normalizar imports
            if imp.startswith('src.'):
                imported_modules.add(imp)
            elif imp in module_to_file:
                imported_modules.add(imp)
    
    # Encontrar arquivos não importados
    unused_files: List[Path] = []
    
    # Exceções: arquivos que são pontos de entrada ou devem ser mantidos
    exceptions = {
        'main',  # main.py é ponto de entrada
        '__init__',  # __init__.py são necessários
    }
    
    for file_path in all_files:
        module_name = file_to_module[file_path]
        module_base = module_name.split('.')[-1]
        
        # Pular exceções
        if module_base in exceptions:
            continue
        
        # Verificar se é importado
        is_imported = False
        
        # Verificar import direto
        if module_name in imported_modules:
            is_imported = True
        
        # Verificar se algum import referencia este módulo
        for imp in all_imports:
            if imp.startswith(module_name) or module_name.startswith(imp):
                is_imported = True
                break
        
        # Verificar se está em __init__.py (re-export)
        if not is_imported:
            # Verificar se algum __init__.py importa este arquivo
            for init_file in all_files:
                if init_file.name == '__init__.py':
                    init_imports = extract_imports(init_file)
                    for imp in init_imports:
                        if module_name in imp or imp in module_name:
                            is_imported = True
                            break
                    if is_imported:
                        break
        
        if not is_imported:
            unused_files.append(file_path)
    
    # Ordenar por caminho
    unused_files.sort()
    
    print()
    print("=" * 80)
    print(f"ARQUIVOS POTENCIALMENTE NÃO UTILIZADOS: {len(unused_files)}")
    print("=" * 80)
    print()
    
    # Agrupar por diretório
    by_directory = defaultdict(list)
    for file_path in unused_files:
        rel_path = file_path.relative_to(PROJECT_ROOT)
        by_directory[rel_path.parent].append(rel_path)
    
    for directory in sorted(by_directory.keys()):
        print(f"\n📁 {directory}/")
        for file_path in sorted(by_directory[directory]):
            print(f"   - {file_path.name}")
    
    # Análise detalhada de arquivos específicos
    print()
    print("=" * 80)
    print("ANÁLISE DETALHADA DE ARQUIVOS SUSPEITOS")
    print("=" * 80)
    print()
    
    suspicious_files = [
        'src/models/database.py',
        'src/models/queries.py',
        'src/infrastructure/__init__.py',
        'src/adapters/questao_adapter.py',
    ]
    
    for file_path_str in suspicious_files:
        file_path = PROJECT_ROOT / file_path_str
        if file_path.exists():
            print(f"\n📄 {file_path_str}")
            # Verificar se é importado
            module_name = get_module_path(file_path)
            found_imports = []
            for other_file, imports in imports_by_file.items():
                if module_name in str(imports) or any(module_name in imp for imp in imports):
                    found_imports.append(other_file.relative_to(PROJECT_ROOT))
            
            if found_imports:
                print(f"   ✓ Encontrado em {len(found_imports)} arquivo(s):")
                for imp_file in found_imports[:5]:  # Mostrar apenas os 5 primeiros
                    print(f"     - {imp_file}")
            else:
                print(f"   ✗ NÃO ENCONTRADO em nenhum import")
    
    # Verificar diretório novas-views
    print()
    print("=" * 80)
    print("ANÁLISE DO DIRETÓRIO novas-views/")
    print("=" * 80)
    print()
    
    novas_views_dir = PROJECT_ROOT / "src/views/novas-views"
    if novas_views_dir.exists():
        novas_views_files = list(novas_views_dir.glob("*.py"))
        print(f"Arquivos Python encontrados: {len(novas_views_files)}")
        for file_path in novas_views_files:
            rel_path = file_path.relative_to(PROJECT_ROOT)
            module_name = get_module_path(file_path)
            found = False
            for other_file, imports in imports_by_file.items():
                if any(module_name in imp or imp in module_name for imp in imports):
                    found = True
                    break
            status = "✓ USADO" if found else "✗ NÃO USADO"
            print(f"   {status}: {rel_path}")
    
    return unused_files


if __name__ == "__main__":
    unused = find_unused_files()
    print()
    print("=" * 80)
    print("ANÁLISE CONCLUÍDA")
    print("=" * 80)
    print(f"\nTotal de arquivos potencialmente não utilizados: {len(unused)}")
    print("\n⚠️  ATENÇÃO: Revise manualmente antes de deletar!")
    print("   Alguns arquivos podem ser:")
    print("   - Pontos de entrada não detectados")
    print("   - Usados via importação dinâmica")
    print("   - Mantidos para compatibilidade")
