# 🔧 Pipeline ETL Básico con Python Puro

## 🎯 Objetivos de Aprendizaje

- ✅ Comprender el proceso **ETL** (Extract-Transform-Load)
- ✅ Implementar pipeline sin frameworks externos
- ✅ Validación y limpieza de datos
- ✅ Sistema de logging profesional
- ✅ Manejo robusto de errores

## 🎓 Nivel

**Intermedio** - Requiere conocimientos de Python y manejo de archivos

## 📋 Conceptos Clave

### ETL

- **Extract**: Lectura de datos de múltiples fuentes
- **Transform**: Limpieza, validación y enriquecimiento
- **Load**: Almacenamiento en formato optimizado

### Componentes

- **Logging**: Registro de todas las operaciones
- **Validación**: Reglas de negocio
- **Limpieza**: Normalización de datos
- **Enriquecimiento**: Campos calculados

## 🚀 Quick Start

```bash
cd src
python etl_pipeline.py
```

El pipeline:

1. Extrae datos del proyecto EDA (transacciones.csv)
2. Valida y transforma datos
3. Guarda en `data/processed/` (CSV y JSON)
4. Genera log en `logs/`

## 🔄 Proceso ETL

### 1. EXTRACT (Extracción)

```python
def extract_csv(self, file_path):
    try:
        with open(file_path, 'r') as f:
            reader = csv.DictReader(f)
            data = list(reader)
        return data
    except Exception as e:
        logger.error(f"Error: {e}")
        return []
```

**Fuentes soportadas**:

- CSV files
- JSON files
- Fácil extender para APIs, bases de datos, etc.

### 2. TRANSFORM (Transformación)

**Validación**:

```python
def validate_record(self, record):
    # Verificar campos requeridos
    # Verificar tipos de datos
    # Verificar rangos válidos
    return is_valid, errors
```

**Limpieza**:

```python
def clean_record(self, record):
    # Eliminar espacios en blanco
    # Normalizar formatos
    # Convertir tipos de datos
    return cleaned_record
```

**Enriquecimiento**:

```python
def enrich_record(self, record):
    # Añadir timestamps
    # Calcular campos derivados
    # Añadir metadatos
    return enriched_record
```

### 3. LOAD (Carga)

```python
def load_json(self, output_path, data):
    with open(output_path, 'w') as f:
        json.dump(data, f, indent=2)
```

**Formatos de salida**:

- JSON (human-readable)
- CSV (compatible con Excel)
- Parquet (columnar, optimizado) - fácil de añadir

## 📊 Configuración

El pipeline se configura mediante diccionario:

```python
config = {
    'sources': [
        {'path': 'data/input.csv', 'type': 'csv'},
        {'path': 'data/input.json', 'type': 'json'}
    ],
    'outputs': [
        {'path': 'data/output.json', 'type': 'json'},
        {'path': 'data/output.csv', 'type': 'csv'}
    ],
    'required_fields': ['id', 'fecha', 'total'],
    'numeric_fields': ['cantidad', 'precio', 'total']
}
```

## 📝 Logging

Cada ejecución genera un log completo:

```
2024-12-18 14:30:00 - INFO - 🚀 INICIANDO PIPELINE ETL
2024-12-18 14:30:00 - INFO - 📥 Extrayendo datos de CSV
2024-12-18 14:30:01 - INFO -    ✅ 50000 registros extraídos
2024-12-18 14:30:01 - INFO - 🔄 FASE 2: TRANSFORM
2024-12-18 14:30:05 - WARNING - ⚠️  Registro inválido: campo vacío
2024-12-18 14:30:10 - INFO - 💾 Guardando en JSON
2024-12-18 14:30:12 - INFO - ✨ PIPELINE COMPLETADO
2024-12-18 14:30:12 - INFO - ⏱️  Duración: 12.34 segundos
```

## 💡 Estadísticas

El pipeline rastrea:

- Registros extraídos
- Registros transformados
- Registros cargados
- Errores encontrados
- Tiempo de ejecución

## 🔧 Personalización

### Añadir nueva fuente de datos

```python
def extract_api(self, api_url):
    import requests
    response = requests.get(api_url)
    return response.json()
```

### Añadir nueva regla de validación

```python
def validate_record(self, record):
    # Tu regla personalizada
    if record.get('total', 0) < 0:
        return False, ['Total negativo']
    return True, []
```

### Añadir nueva transformación

```python
def enrich_record(self, record):
    # Calcular descuento
    if 'subtotal' in record and 'total' in record:
        record['descuento'] = record['subtotal'] - record['total']
    return record
```

## 📈 Salida Esperada

```
======================================================================
🚀 INICIANDO PIPELINE ETL
======================================================================

======================================================================
🔄 FASE 1: EXTRACT (Extracción)
======================================================================
📥 Extrayendo datos de CSV: transacciones.csv
   ✅ 50000 registros extraídos

📊 Total registros extraídos: 50000

======================================================================
🔄 FASE 2: TRANSFORM (Transformación)
======================================================================

📊 Registros válidos: 49000
❌ Registros inválidos: 1000

======================================================================
🔄 FASE 3: LOAD (Carga)
======================================================================
💾 Guardando en JSON: transacciones_procesadas.json
   ✅ 49000 registros guardados
💾 Guardando en CSV: transacciones_procesadas.csv
   ✅ 49000 registros guardados

======================================================================
✨ PIPELINE COMPLETADO
======================================================================
⏱️  Duración: 15.45 segundos
📊 Estadísticas:
   - Extraídos: 50000
   - Transformados: 49000
   - Cargados: 98000
   - Errores: 0
```

## 🐛 Troubleshooting

**No se encuentran los datos**

- Primero ejecuta el generador de datos del proyecto EDA
- O especifica tu propia fuente en config

**Registros inválidos**

- Revisa el log para ver qué campos faltan
- Ajusta `required_fields` en config
- Los datos intencionales tienen ~2% de problemas

**Error de permisos**

- Verifica que puedas escribir en `data/processed/`
- Verifica que puedas escribir en `logs/`

## 📚 Próximos Pasos

1. **Añadir más transformaciones**:

   - Deduplicación de registros
   - Detección de outliers
   - Normalización de texto

2. **Conectar a base de datos**:

   - SQLite para práctica local
   - PostgreSQL para producción
   - DuckDB para analytics

3. **Añadir scheduling**:

   - Cron jobs en Linux
   - Task Scheduler en Windows
   - Apache Airflow para orquestación

4. **Siguiente proyecto**:
   - ETL con SQLAlchemy
   - Pipeline con validación Pydantic
   - Streaming con Apache Kafka

## 💻 Mejoras Sugeridas

### Deduplicación

```python
def deduplicate(self, data):
    seen = set()
    unique = []
    for record in data:
        key = record['transaccion_id']
        if key not in seen:
            seen.add(key)
            unique.append(record)
    return unique
```

### Retry Logic

```python
def extract_with_retry(self, file_path, max_retries=3):
    for attempt in range(max_retries):
        try:
            return self.extract_csv(file_path)
        except Exception as e:
            if attempt == max_retries - 1:
                raise
            time.sleep(2 ** attempt)
```

### Parallelización

```python
from concurrent.futures import ThreadPoolExecutor

def transform_parallel(self, data):
    with ThreadPoolExecutor(max_workers=4) as executor:
        results = executor.map(self.transform_record, data)
    return list(results)
```

## 📊 Benchmarks

Con 50,000 registros en hardware promedio:

- Extract: ~2 segundos
- Transform: ~10 segundos
- Load: ~3 segundos
- **Total**: ~15 segundos

## 📝 Notas

- El pipeline usa solo la biblioteca estándar de Python
- Los datos se procesan en memoria (ajustar para datasets grandes)
- Los logs son rotados automáticamente
- Todos los errores se registran para análisis posterior

---

**🔧 Build robust data pipelines!**
