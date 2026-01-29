#!/usr/bin/env python3
"""
Script para preparar o pacote de entrega do trabalho do MBA.
Copia apenas os arquivos obrigatórios para uma pasta de entrega.
"""

import os
import shutil
from pathlib import Path
from datetime import datetime

# Configuração
PROJECT_ROOT = Path(__file__).parent
DELIVERY_DIR = PROJECT_ROOT / "entrega"
TIMESTAMP = datetime.now().strftime("%Y%m%d_%H%M%S")

# Arquivos e pastas obrigatórios
REQUIRED_FILES = {
    "README.md": "README.md",
}

REQUIRED_DIRS = {
    "prompts": {
        "v1-baseline.md": "prompts/v1-baseline.md",
        "v2-structured.md": "prompts/v2-structured.md",
        "v3-schema.md": "prompts/v3-schema.md",
    },
    "resultados": {
        # v1
        "v1-PR1.jpg": "resultados/v1-PR1.jpg",
        "v1-PR2.jpg": "resultados/v1-PR2.jpg",
        "v1-PR3.jpg": "resultados/v1-PR3.jpg",
        "v1-PR4.jpg": "resultados/v1-PR4.jpg",
        "v1-PR5.jpg": "resultados/v1-PR5.jpg",
        "v1-PR6.jpg": "resultados/v1-PR6.jpg",
        # v2
        "v2-PR1.jpg": "resultados/v2-PR1.jpg",
        "v2-PR2.jpg": "resultados/v2-PR2.jpg",
        "v2-PR3.jpg": "resultados/v2-PR3.jpg",
        "v2-PR4.jpg": "resultados/v2-PR4.jpg",
        "v2-PR5.jpg": "resultados/v2-PR5.jpg",
        "v2-PR6.jpg": "resultados/v2-PR6.jpg",
        # v3
        "v3-PR1.jpg": "resultados/v3-PR1.jpg",
        "v3-PR2.jpg": "resultados/v3-PR2.jpg",
        "v3-PR3.jpg": "resultados/v3-PR3.jpg",
        "v3-PR4.jpg": "resultados/v3-PR4.jpg",
        "v3-PR5.jpg": "resultados/v3-PR5.jpg",
        "v3-PR6.jpg": "resultados/v3-PR6.jpg",
    }
}


def check_file_exists(filepath: Path) -> bool:
    """Verifica se um arquivo existe."""
    if not filepath.exists():
        print(f"  ⚠️  AVISO: Arquivo não encontrado: {filepath}")
        return False
    return True


def prepare_delivery():
    """Prepara a pasta de entrega com apenas os arquivos obrigatórios."""
    print("📦 Preparando pacote de entrega...\n")
    
    # Remove pasta de entrega anterior se existir
    if DELIVERY_DIR.exists():
        print(f"🗑️  Removendo pasta de entrega anterior: {DELIVERY_DIR}")
        shutil.rmtree(DELIVERY_DIR)
    
    # Cria nova pasta de entrega
    DELIVERY_DIR.mkdir(exist_ok=True)
    print(f"✅ Pasta criada: {DELIVERY_DIR}\n")
    
    # Contadores
    copied = 0
    missing = 0
    
    # Copia arquivos da raiz
    print("📄 Copiando arquivos da raiz...")
    for dest_name, source_path in REQUIRED_FILES.items():
        source = PROJECT_ROOT / source_path
        dest = DELIVERY_DIR / dest_name
        
        if check_file_exists(source):
            shutil.copy2(source, dest)
            print(f"  ✓ {dest_name}")
            copied += 1
        else:
            missing += 1
    
    # Copia arquivos das pastas
    print("\n📁 Copiando arquivos das pastas...")
    for dir_name, files in REQUIRED_DIRS.items():
        dir_path = DELIVERY_DIR / dir_name
        dir_path.mkdir(exist_ok=True)
        print(f"\n  📂 {dir_name}/")
        
        for dest_name, source_path in files.items():
            source = PROJECT_ROOT / source_path
            dest = dir_path / dest_name
            
            if check_file_exists(source):
                shutil.copy2(source, dest)
                print(f"    ✓ {dest_name}")
                copied += 1
            else:
                missing += 1
    
    # Resumo
    print("\n" + "="*60)
    print("📊 RESUMO")
    print("="*60)
    print(f"✅ Arquivos copiados: {copied}")
    if missing > 0:
        print(f"⚠️  Arquivos faltando: {missing}")
    print(f"📁 Pasta de entrega: {DELIVERY_DIR.absolute()}")
    print("\n" + "="*60)
    
    # Lista estrutura final
    print("\n📋 Estrutura da pasta de entrega:")
    print_tree(DELIVERY_DIR)
    
    # Pergunta se quer criar zip
    print("\n💡 Dica: Para criar um arquivo ZIP, execute:")
    print(f"   cd {DELIVERY_DIR.parent}")
    print(f"   zip -r entrega_{TIMESTAMP}.zip {DELIVERY_DIR.name}/")
    print(f"\n   Ou use: python prepare_delivery.py --zip")


def print_tree(directory: Path, prefix: str = "", is_last: bool = True):
    """Imprime a estrutura de diretórios em formato de árvore."""
    items = sorted(directory.iterdir(), key=lambda x: (x.is_file(), x.name))
    
    for i, item in enumerate(items):
        is_last_item = i == len(items) - 1
        current_prefix = "└── " if is_last_item else "├── "
        
        if item.is_file():
            size = item.stat().st_size
            size_str = format_size(size)
            print(f"{prefix}{current_prefix}{item.name} ({size_str})")
        else:
            print(f"{prefix}{current_prefix}{item.name}/")
            extension = "    " if is_last_item else "│   "
            print_tree(item, prefix + extension, is_last_item)


def format_size(size_bytes: int) -> str:
    """Formata tamanho de arquivo em formato legível."""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} TB"


if __name__ == "__main__":
    import sys
    
    prepare_delivery()
    
    # Se passar --zip, cria o arquivo zip também
    if "--zip" in sys.argv:
        import zipfile
        
        zip_path = PROJECT_ROOT / f"entrega_{TIMESTAMP}.zip"
        print(f"\n📦 Criando arquivo ZIP: {zip_path}")
        
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(DELIVERY_DIR):
                for file in files:
                    file_path = Path(root) / file
                    arcname = file_path.relative_to(DELIVERY_DIR.parent)
                    zipf.write(file_path, arcname)
        
        zip_size = format_size(zip_path.stat().st_size)
        print(f"✅ ZIP criado: {zip_path.name} ({zip_size})")
