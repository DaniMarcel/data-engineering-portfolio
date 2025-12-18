# 🎨 Decoradores para Data Pipelines

## 🎯 Objetivos

- ✅ Crear decoradores reutilizables
- ✅ Logging automático
- ✅ Medición de tiempos
- ✅ Retry logic
- ✅ Validación de inputs
- ✅ Caché de resultados

## 🚀 Quick Start

```bash
cd src
python decoradores.py
```

## 📚 Decoradores Incluidos

### Básicos

- `@timing` - Mide tiempo de ejecución
- `@log_execution` - Registra ejecución
- `@retry(max_attempts, delay)` - Reintenta en caso de error
- `@validate_input(**validators)` - Valida parámetros
- `@cache_result` - Cachea resultados (memoization)

### Para Data Pipelines

- `@data_pipeline_step(name)` - Marca paso de pipeline
- `@count_records` - Cuenta registros entrada/salida

## 💡 Ejemplo de Uso

```python
@data_pipeline_step("Extract")
@count_records
def extract_data(source):
    return read_data(source)

@timing
@retry(max_attempts=3)
def api_call():
    return requests.get(url)
```

## 🎓 Conceptos Avanzados

- Closures y scope
- `functools.wraps`
- Decoradores con parámetros
- Decoradores apilados
- Memoization

---

Los decoradores hacen el código más limpio, reutilizable y fácil de mantener.
