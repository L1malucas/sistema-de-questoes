#!/usr/bin/env python3
"""
Script para análise completa de código não utilizado.
Identifica arquivos órfãos e código morto.
"""

import os
import ast
import re
from pathlib import Path
from typing import Set, Dict, List, Tuple
from collections import defaultdict

PROJECT_ROOT = Path(__file__).parent.parent
SRC_DIR = PROJECT_ROOT / "src"


def get_all_python_files(directory: Path) -> Set[Path]:
    """Retorna todos os arquivos Python no diretório"""
    python_files = set()
    for root, dirs, files in os.walk(directory):
        dirs[:] = [d for d in dirs if d not in ['__pycache__', 'venv', '.git', 'novas-views']]
        for file in files:
            if file.endswith('.py'):
                python_files.add(Path(root) / file)
    return python_files


def get_module_name(file_path: Path) -> str:
    """Converte caminho de arquivo para nome de módulo"""
    rel_path = file_path.relative_to(SRC_DIR)
    parts = list(rel_path.parts[:-1]) + [rel_path.stem]
    return '.'.join(parts)


def extract_all_imports(file_path: Path) -> Set[str]:
    """Extrai todos os imports de um arquivo Python"""
    imports = set()
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Parse AST
        try:
            tree = ast.parse(content, filename=str(file_path))
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        module = alias.name.split('.')[0]
                        imports.add(module)
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        module = node.module.split('.')[0]
                        imports.add(module)
        except SyntaxError:
            pass
        
        # Buscar imports dinâmicos
        patterns = [
            r'from\s+src\.([a-zA-Z_][a-zA-Z0-9_.]*)',
            r'import\s+src\.([a-zA-Z_][a-zA-Z0-9_.]*)',
        ]
        for pattern in patterns:
            matches = re.findall(pattern, content)
            for match in matches:
                imports.add('src.' + match.split('.')[0])
        
    except Exception:
        pass
    
    return imports


def find_unused_files():
    """Encontra arquivos não utilizados"""
    print("=" * 80)
    print("ANÁLISE COMPLETA DE CÓDIGO NÃO UTILIZADO")
    print("=" * 80)
    print()
    
    # Obter todos os arquivos
    all_files = get_all_python_files(SRC_DIR)
    print(f"Total de arquivos Python: {len(all_files)}")
    
    # Mapear módulos para arquivos
    module_to_file: Dict[str, Path] = {}
    file_to_module: Dict[Path, str] = {}
    
    for file_path in all_files:
        module_name = get_module_name(file_path)
        module_to_file[module_name] = file_path
        file_to_module[file_path] = module_name
    
    # Coletar todos os imports
    all_imports: Set[str] = set()
    imports_by_file: Dict[Path, Set[str]] = {}
    
    print("Analisando imports...")
    for file_path in all_files:
        imports = extract_all_imports(file_path)
        imports_by_file[file_path] = imports
        all_imports.update(imports)
    
    # Encontrar arquivos importados
    imported_modules: Set[str] = set()
    for imports in imports_by_file.values():
        for imp in imports:
            if imp.startswith('src.'):
                imported_modules.add(imp)
            elif imp in module_to_file:
                imported_modules.add(imp)
    
    # Verificar se módulos são importados
    unused_files: List[Path] = []
    entry_points = {'main', '__main__', '__init__'}
    
    for file_path in all_files:
        module_name = file_to_module[file_path]
        module_base = module_name.split('.')[-1]
        
        # Pular pontos de entrada
        if module_base in entry_points:
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
        
        # Verificar se está em __init__.py
        if not is_imported:
            for init_file in all_files:
                if init_file.name == '__init__.py':
                    init_imports = extract_all_imports(init_file)
                    for imp in init_imports:
                        if module_name in imp or imp in module_name:
                            is_imported = True
                            break
                    if is_imported:
                        break
        
        if not is_imported:
            unused_files.append(file_path)
    
    # Ordenar
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
    
    return unused_files


if __name__ == "__main__":
    unused = find_unused_files()
    print()
    print("=" * 80)
    print("ANÁLISE CONCLUÍDA")
    print("=" * 80)
