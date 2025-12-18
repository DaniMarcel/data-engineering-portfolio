"""Script para renumerar todas las carpetas secuencialmente (sin eliminar nada)"""
from pathlib import Path
import re

base = Path(r"c:\Users\WARRIOR\Documents\data engineer")

# Renumeración completa en cascada
renumbering = {
    "02-analisis-datos": [
        "01-eda-exploratorio",
        "02-visualizacion",
        "03-pandas-avanzado",
        "03-matplotlib-seaborn",  # → 04
        "04-polars",  # → 05
        "05-automatizacion",  # → 06
        "06-streamlit-apps",  # → 07
        "07-notebooks",  # → 08
        "08-series-temporales",  # → 09
        "09-machine-learning",  # → 10
        "10-dashboards-avanzados",  # → 11
        "11-optimizacion",  # → 12
        "12-statistical-analysis",  # → 13
        "13-clustering",  # → 14
        "14-nlp",  # → 15
        "15-geospatial",  # → 16
        "16-web-analytics",  # → 17
        "17-ab-testing",  # → 18
        "18-recommendation",  # → 19
    ],
    
    "03-ingenieria-datos": [
        "01-etl-python-puro",
        "02-bases-datos",
        "03-calidad-datos",
        "03-data-warehouse",  # → 04
        "04-calidad-datos",  # → 05
        "04-infraestructura",  # → 06
        "05-orquestacion",  # → 07
        "06-api-data",  # → 08
        "07-logging-monitoring",  # → 09
    ],
    
    "05-big-data-avanzado": [
        "01-apache-spark",
        "01-hadoop-ecosystem",  # → 02
        "02-apache-spark",  # → 03
        "02-kafka",  # → 04
        "03-hadoop",  # → 05
        "03-kafka-streaming",  # → 06
        "04-orchestration",  # → 07
        "04-procesamiento-batch",  # → 08
        "05-streaming",  # → 09
        "06-data-lake",  # → 10
        "07-orchestration",  # → 11
        "08-hive",  # → 12
        "09-presto",  # → 13
    ]
}

def renumber_folders():
    for section, folders in renumbering.items():
        section_path = base / section
        
        if not section_path.exists():
            print(f"⚠️ Section not found: {section}")
            continue
        
        print(f"\n📁 {section}")
        print("=" * 60)
        
        # Primero renombrar a temporales
        temp_mapping = {}
        for idx, old_name in enumerate(folders, start=1):
            old_path = section_path / old_name
            
            if not old_path.exists():
                print(f"  ⚠️ Not found: {old_name}")
                continue
            
            # Extraer nombre sin número
            name_without_num = re.sub(r'^\d+-', '', old_name)
            new_num = f"{idx:02d}"
            new_name = f"{new_num}-{name_without_num}"
            
            if old_name == new_name:
                print(f"  ✓ OK: {old_name}")
                continue
            
            # Renombrar a temporal primero
            temp_name = f"_TEMP_{idx:02d}_{name_without_num}"
            temp_path = section_path / temp_name
            
            print(f"  ➡️ {old_name} → {new_name}")
            old_path.rename(temp_path)
            temp_mapping[temp_name] = new_name
        
        # Luego renombrar de temporal a final
        for temp_name, final_name in temp_mapping.items():
            temp_path = section_path / temp_name
            final_path = section_path / final_name
            temp_path.rename(final_path)
        
        print(f"✅ {len(temp_mapping)} carpetas renumeradas")

if __name__ == "__main__":
    print("🔧 RENUMERANDO CARPETAS (SIN ELIMINAR NADA)")
    print("=" * 60)
    renumber_folders()
    print("\n" + "=" * 60)
    print("✅ ¡Renumeración completada!")
    print("\nRevisa las carpetas y luego haz:")
    print("  git add .")
    print("  git commit -m 'Fix: Renumber duplicate folder numbers'")
    print("  git push")
