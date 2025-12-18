# 🔍 Data Profiling - Análisis de Calidad

## 🎯 Objetivos

- ✅ Perfiles automáticos de datasets
- ✅ Estadísticas descriptivas completas
- ✅ Análisis de calidad de datos
- ✅ Detección de outliers
- ✅ Correlaciones
- ✅ Reportes JSON

## 🚀 Quick Start

```bash
pip install -r requirements.txt
cd src
python profiler.py
```

## 📊 Análisis Incluido

### Por Columna

- Tipo de dato
- Valores nulos y porcentaje
- Valores únicos
- Estadísticas (min, max, mean, std, percentiles)
- Outliers (método IQR)
- Top 10 valores más frecuentes
- Longitud de strings

### Calidad General

- Completitud por columna
- Unicidad (IDs duplicados)
- Filas duplicadas
- Uso de memoria

### Correlaciones

- Matriz de correlación
- Correlaciones fuertes (|r| > 0.7)

## 💡 Uso

```python
from profiler import DataProfiler

profiler = DataProfiler(df, "Mi Dataset")
profiler.generar_perfil_completo(output_dir)
```

---

Perfecto para análisis exploratorio rápido y validación de calidad.
