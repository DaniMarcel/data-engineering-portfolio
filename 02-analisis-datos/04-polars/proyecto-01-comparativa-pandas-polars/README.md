# 🐻‍❄️ Pandas vs Polars - Comparativa de Rendimiento

## 🎯 Objetivos

- ✅ Comparar velocidad pandas vs polars
- ✅ 8 operaciones comunes benchmarked
- ✅ Comparativa de sintaxis
- ✅ Resultados automáticos guardados

## 🚀 Quick Start

```bash
pip install -r requirements.txt
cd src
python benchmark.py
```

## 📊 Operaciones Comparadas

1. Lectura de CSV
2. Filtrado de datos
3. GroupBy y agregaciones
4. Joins entre DataFrames
5. Columnas calculadas
6. Ordenamiento
7. Selección de columnas
8. Valores únicos

## 💡 Resultados Típicos

Polars suele ser **2-10x más rápido** que pandas para:

- Lectura de archivos grandes
- GroupBy complejos
- Joins
- Operaciones en múltiples columnas

## 📝 Salidas

- `benchmark_results.csv` - Tiempos detallados
- `resumen_benchmark.txt` - Resumen con speedups

---

Polars es ideal cuando necesitas máximo rendimiento en análisis de datos.
