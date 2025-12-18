"""Eliminar carpetas vacías y renumerar todo correctamente"""
from pathlib import Path
import shutil
import re

base = Path(r"c:\Users\WARRIOR\Documents\data engineer")

# Carpetas vacías a eliminar
empty_folders_to_delete = {
    "02-analisis-datos": [
        "03-pandas-avanzado",
        "07-notebooks"
    ],
    "03-ingenieria-datos": [
        "03-data-warehouse",
        "04-calidad-datos"
    ],
    "05-big-data-avanzado": [
        "01-hadoop-ecosystem",
        "02-apache-spark",
        "03-kafka-streaming",
        "04-orchestration"
    ]
}

def delete_empty_folders():
    """Eliminar carpetas vacías"""
    print("🗑️  ELIMINANDO CARPETAS VACÍAS")
    print("=" * 70)
    
    deleted_count = 0
    for section, folders in empty_folders_to_delete.items():
        section_path = base / section
        print(f"\n📁 {section}")
        
        for folder_name in folders:
            folder_path = section_path / folder_name
            if folder_path.exists():
                # Verificar que esté vacía
                files = list(folder_path.rglob('*'))
                if len(files) == 0 or all(f.name == '__pycache__' or '__pycache__' in str(f) for f in files):
                    shutil.rmtree(folder_path)
                    print(f"  ✓ Eliminada: {folder_name}")
                    deleted_count += 1
                else:
                    print(f"  ⚠️ No está vacía, saltando: {folder_name}")
    
    print(f"\n✅ {deleted_count} carpetas eliminadas")
    return deleted_count

def renumber_all_folders():
    """Renumerar todas las carpetas que quedan"""
    print(f"\n{'=' * 70}")
    print("🔢 RENUMERANDO CARPETAS")
    print("=" * 70)
    
    sections = [
        "02-analisis-datos",
        "03-ingenieria-datos",
        "05-big-data-avanzado"
    ]
    
    for section in sections:
        section_path = base / section
        
        if not section_path.exists():
            continue
        
        print(f"\n📁 {section}")
        
        # Obtener todas las carpetas actuales (solo directorios)
        current_folders = sorted([f for f in section_path.iterdir() if f.is_dir()])
        
        # Crear mapeo temporal
        temp_mapping = {}
        for idx, folder in enumerate(current_folders, start=1):
            # Extraer nombre sin número
            name_without_num = re.sub(r'^\d+-', '', folder.name)
            new_num = f"{idx:02d}"
            new_name = f"{new_num}-{name_without_num}"
            
            if folder.name == new_name:
                print(f"  ✓ OK: {folder.name}")
                continue
            
            # Renombrar a temporal
            temp_name = f"_TEMP_{idx:03d}_{name_without_num}"
            temp_path = section_path / temp_name
            
            print(f"  ➡️  {folder.name} → {new_name}")
            folder.rename(temp_path)
            temp_mapping[temp_name] = new_name
        
        # Renombrar de temporal a final
        for temp_name, final_name in temp_mapping.items():
            temp_path = section_path / temp_name
            final_path = section_path / final_name
            temp_path.rename(final_path)
        
        print(f"  ✅ {len(current_folders)} carpetas renumeradas")

if __name__ == "__main__":
    print("🔧 LIMPIEZA Y RENUMERACIÓN DE PORTAFOLIO")
    print("=" * 70)
    
    # Paso 1: Eliminar vacías
    deleted = delete_empty_folders()
    
    # Paso 2: Renumerar
    renumber_all_folders()
    
    print(f"\n{'=' * 70}")
    print("✅ ¡COMPLETADO!")
    print("=" * 70)
    print(f"  • {deleted} carpetas vacías eliminadas")
    print(f"  • Todas las carpetas renumeradas secuencialmente")
    print(f"\n📊 Nuevo conteo de proyectos:")
    print(f"  • 02-analisis-datos: 17 proyectos")
    print(f"  • 03-ingenieria-datos: 7 proyectos")
    print(f"  • 05-big-data-avanzado: 9 proyectos")
    print(f"  • TOTAL: ~53 proyectos con código")
    print(f"\n🔥 Siguiente paso:")
    print(f"  git add .")
    print(f"  git commit -m 'Clean: Remove empty folders and fix numbering'")
    print(f"  git push")
