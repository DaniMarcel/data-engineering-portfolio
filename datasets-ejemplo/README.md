# 📁 Datasets de Ejemplo

Este directorio contiene datasets sintéticos pero realistas para usar en todos los proyectos del portafolio.

## 🎯 Propósito

- Proporcionar datos consistentes para practicar
- Evitar repetir generación de datos en cada proyecto
- Ofrecer diferentes formatos (CSV, JSON, Parquet, etc.)
- Incluir diferentes dominios (usuarios, ventas, logs, IoT)

## 📊 Datasets Disponibles

### 👥 Usuarios (10,000 registros)

**Formatos**: CSV, JSON, Parquet

Información de usuarios para proyectos de análisis:

- IDs únicos
- Información demográfica (nombre, edad, país)
- Estado de cuenta (activo, premium)
- Fecha de registro

**Uso**: Análisis de usuarios, joins, segmentación

---

### 🖥️ Server Logs (100,000 registros)

**Formatos**: CSV, JSONL

Logs de servidor web con:

- Timestamps
- IPs de origen
- Métodos HTTP (GET, POST, PUT, DELETE)
- Endpoints
- Status codes
- Tiempos de respuesta
- User agents

**Uso**: Análisis de logs, time series, detección de anomalías

---

### 🌡️ IoT Sensors (500,000 registros)

**Formatos**: CSV, Parquet

Lecturas de sensores IoT:

- 50 sensores diferentes
- Temperatura, humedad, presión
- Ubicaciones variadas
- Lecturas cada 5 minutos
- Incluye anomalías (~0.1%)

**Uso**: Time series analysis, detección de anomalías, agregaciones

---

### 🌐 API Responses (10,000 registros)

**Formatos**: JSON, JSONL

Respuestas simuladas de API REST:

- Posts/artículos
- Metadatos (likes, comments, tags)
- Timestamps
- Estados de publicación

**Uso**: Procesamiento de JSON, ETL, APIs

---

## 🚀 Generación de Datos

Para generar todos los datasets:

```bash
cd datasets-ejemplo
python generar_datasets.py
```

Esto creará todas las carpetas y archivos necesarios.

## 📂 Estructura

```
datasets-ejemplo/
├── generar_datasets.py    # Script generador
├── usuarios/
│   ├── usuarios.csv
│   ├── usuarios.json
│   └── usuarios.parquet
├── logs/
│   ├── server_logs.csv
│   └── server_logs.jsonl
├── time-series/
│   ├── iot_sensors.csv
│   └── iot_sensors.parquet
├── api-responses/
│   ├── api_data.json
│   └── api_data.jsonl
├── ventas/              # Creado por proyecto EDA
├── productos/           # Creado por proyecto EDA
└── transacciones/       # Creado por proyecto EDA
```

## 💡 Características

- ✅ **Realistas**: Distribuciones y patrones similares a datos reales
- ✅ **Escalables**: Fácil cambiar número de registros
- ✅ **Diversos**: Diferentes tipos de datos y formatos
- ✅ **Con problemas**: Incluyen anomalías y problemas de calidad intencionales
- ✅ **Documentados**: Cada dataset tiene descripción clara

## 🔄 Actualización

Los datasets se pueden regenerar en cualquier momento:

```bash
python generar_datasets.py
```

**Nota**: Los datos son aleatorios pero con seed fijada, así que la regeneración produce datos diferentes pero consistentes.

## 📖 Uso en Proyectos

Referencia estos datasets en tus proyectos:

```python
# Desde cualquier proyecto
import pandas as pd
from pathlib import Path

# Ruta relativa a datasets-ejemplo
base = Path(__file__).parents[3] / 'datasets-ejemplo'

df_usuarios = pd.read_csv(base / 'usuarios' / 'usuarios.csv')
df_logs = pd.read_csv(base / 'logs' / 'server_logs.csv')
```

## 📊 Estadísticas

| Dataset       | Registros | Tamaño (CSV) | Formatos           |
| ------------- | --------- | ------------ | ------------------ |
| Usuarios      | 10,000    | ~500 KB      | CSV, JSON, Parquet |
| Logs          | 100,000   | ~15 MB       | CSV, JSONL         |
| IoT Sensors   | 500,000   | ~30 MB       | CSV, Parquet       |
| API Responses | 10,000    | ~2 MB        | JSON, JSONL        |

---

**🎲 Todos los datos son ficticios y generados para propósitos educativos**
