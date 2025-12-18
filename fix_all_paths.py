"""Script para arreglar paths en todo el portafolio"""
from pathlib import Path
import re

# Lista de archivos a arreglar
files_to_fix = [
    r"c:\Users\WARRIOR\Documents\data engineer\06-proyectos-integradores\proyecto-03-ml-pipeline-complete\src\ml_pipeline.py",
    r"c:\Users\WARRIOR\Documents\data engineer\05-big-data-avanzado\01-apache-spark\proyecto-02-spark-etl\src\spark_etl.py",
    r"c:\Users\WARRIOR\Documents\data engineer\05-big-data-avanzado\01-apache-spark\proyecto-01-intro-pyspark\src\intro_spark.py",
    r"c:\Users\WARRIOR\Documents\data engineer\03-ingenieria-datos\03-calidad-datos\proyecto-02-data-profiling\src\profiler.py",
    r"c:\Users\WARRIOR\Documents\data engineer\02-analisis-datos\13-clustering\proyecto-01-kmeans\src\clustering.py",
    r"c:\Users\WARRIOR\Documents\data engineer\02-analisis-datos\12-statistical-analysis\proyecto-01-hypothesis-testing\src\stats_tests.py",
    r"c:\Users\WARRIOR\Documents\data engineer\02-analisis-datos\11-optimizacion\proyecto-01-performance-pandas\src\optimization.py",
    r"c:\Users\WARRIOR\Documents\data engineer\02-analisis-datos\09-machine-learning\proyecto-01-regression-basics\src\regression.py",
    r"c:\Users\WARRIOR\Documents\data engineer\02-analisis-datos\08-series-temporales\proyecto-01-forecasting\src\forecast.py",
    r"c:\Users\WARRIOR\Documents\data engineer\02-analisis-datos\05-automatizacion\proyecto-03-pdf-reports\src\pdf_generator.py",
    r"c:\Users\WARRIOR\Documents\data engineer\02-analisis-datos\05-automatizacion\proyecto-02-email-reports\src\email_reporter.py",
    r"c:\Users\WARRIOR\Documents\data engineer\02-analisis-datos\05-automatizacion\proyecto-01-reportes-excel\src\generar_reporte.py",
    r"c:\Users\WARRIOR\Documents\data engineer\02-analisis-datos\03-matplotlib-seaborn\proyecto-01-visualizacion-avanzada\src\visualizaciones.py",
    r"c:\Users\WARRIOR\Documents\data engineer\03-ingenieria-datos\06-api-data\proyecto-01-rest-data-service\src\app.py",
    r"c:\Users\WARRIOR\Documents\data engineer\02-analisis-datos\02-visualizacion\proyecto-01-plotly-interactivo\src\visualizaciones.py",
    r"c:\Users\WARRIOR\Documents\data engineer\03-ingenieria-datos\02-bases-datos\03-duckdb\proyecto-01-analytics-local\src\analytics.py",
    r"c:\Users\WARRIOR\Documents\data engineer\03-ingenieria-datos\01-etl-python-puro\proyecto-02-incremental-etl\src\incremental_etl.py",
    r"c:\Users\WARRIOR\Documents\data engineer\03-ingenieria-datos\01-etl-python-puro\proyecto-01-pipeline-basico\src\etl_pipeline.py",
    r"c:\Users\WARRIOR\Documents\data engineer\01-python-fundamentos\02-intermedio\proyecto-04-fastapi-rest\api\main.py",
]

# Código de reemplazo robusto
replacement_code = """# Buscar carpeta base 'data engineer'
current_path = Path(__file__).resolve()
base_path = None
for parent in current_path.parents:
    if parent.name == 'data engineer':
        base_path = parent
        break
if base_path is None:
    raise FileNotFoundError("No se pudo encontrar la carpeta base 'data engineer'")
"""

fixed_count = 0

for filepath in files_to_fix:
    try:
        file_path = Path(filepath)
        if not file_path.exists():
            print(f"⚠️  Archivo no encontrado: {filepath}")
            continue
        
        # Leer contenido
        content = file_path.read_text(encoding='utf-8')
        
        # Reemplazar patterns problemáticos
        # Pattern: base = Path(__file__).parents[N]
        pattern1 = r'(\s*)base(?:_path)?\s*=\s*Path\(__file__\)\.parents\[\d+\]'
        replacement1 = r'\1# Buscar carpeta base \'data engineer\'\n\1current_path = Path(__file__).resolve()\n\1base_path = None\n\1for parent in current_path.parents:\n\1    if parent.name == \'data engineer\':\n\1        base_path = parent\n\1        break\n\1if base_path is None:\n\1    raise FileNotFoundError("No se pudo encontrar la carpeta base \'data engineer\'")'
        
        new_content = re.sub(pattern1, replacement1, content)
        
        # Reemplazar referencias a 'base' por 'base_path' si es necesario
        # pero solo si no está ya definido como base_path
        if 'base_path' not in content and 'base =' in content:
            new_content = new_content.replace('base /', 'base_path /')
        
        if new_content != content:
            file_path.write_text(new_content, encoding='utf-8')
            print(f"✅ Arreglado: {file_path.name}")
            fixed_count += 1
        else:
            print(f"ℹ️  Sin cambios: {file_path.name}")
    
    except Exception as e:
        print(f"❌ Error con {filepath}: {e}")

print(f"\n🎉 Arreglados {fixed_count} de {len(files_to_fix)} archivos!")
