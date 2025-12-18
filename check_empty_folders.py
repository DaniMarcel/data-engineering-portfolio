"""Analizar cuáles carpetas tienen contenido y cuáles están vacías"""
from pathlib import Path

base = Path(r"c:\Users\WARRIOR\Documents\data engineer")

sections = [
    "02-analisis-datos",
    "03-ingenieria-datos", 
    "05-big-data-avanzado"
]

def analyze_folders():
    total_empty = 0
    total_with_content = 0
    
    for section in sections:
        section_path = base / section
        
        if not section_path.exists():
            continue
        
        print(f"\n{'='*70}")
        print(f"📁 {section}")
        print('='*70)
        
        # Obtener todas las subcarpetas
        folders = sorted([f for f in section_path.iterdir() if f.is_dir()])
        
        empty_folders = []
        content_folders = []
        
        for folder in folders:
            # Contar archivos (recursivamente, excluyendo __pycache__)
            files = [f for f in folder.rglob('*') 
                    if f.is_file() and '__pycache__' not in str(f)]
            
            if len(files) == 0:
                empty_folders.append(folder.name)
                print(f"  ❌ VACÍA: {folder.name}")
            else:
                content_folders.append((folder.name, len(files)))
                print(f"  ✅ {len(files):3d} archivos: {folder.name}")
        
        total_empty += len(empty_folders)
        total_with_content += len(content_folders)
        
        print(f"\n  Total: {len(content_folders)} con contenido, {len(empty_folders)} vacías")
    
    print(f"\n{'='*70}")
    print(f"📊 RESUMEN GENERAL")
    print('='*70)
    print(f"  ✅ Carpetas con contenido: {total_with_content}")
    print(f"  ❌ Carpetas vacías: {total_empty}")
    
    return total_empty

if __name__ == "__main__":
    print("🔍 ANALIZANDO CONTENIDO DE CARPETAS\n")
    empty_count = analyze_folders()
    
    if empty_count > 0:
        print(f"\n⚠️  Encontré {empty_count} carpetas vacías")
        print("    Opciones:")
        print("    1. Eliminarlas y renumerar")
        print("    2. Llenarlas con código placeholder")
        print("    3. Dejarlas como están")
    else:
        print("\n✅ ¡Todas las carpetas tienen contenido!")
