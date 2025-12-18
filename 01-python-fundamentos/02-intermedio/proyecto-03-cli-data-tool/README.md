# 🔧 CLI Data Tool

## 🎯 Objetivos

- ✅ Herramienta de línea de comandos profesional
- ✅ Conversión entre formatos
- ✅ Filtrado y análisis rápido
- ✅ Validación de calidad
- ✅ Interfaz intuitiva con Click

## 🚀 Instalación

```bash
pip install -r requirements.txt
```

## 📋 Comandos

### convert - Convertir formatos

```bash
python data_tool.py convert input.csv output.json
python data_tool.py convert data.json data.parquet -f parquet
```

### head - Ver primeras filas

```bash
python data_tool.py head data.csv --rows 20
```

### info - Información del archivo

```bash
python data_tool.py info data.csv
```

### filter - Filtrar datos

```bash
python data_tool.py filter data.csv -c ciudad -v Madrid -o madrid.csv
```

### stats - Estadísticas

```bash
python data_tool.py stats data.csv
python data_tool.py stats data.csv -c categoria
```

### validate - Validar calidad

```bash
python data_tool.py validate data.csv
```

## 💡 Características

- Soporta CSV, JSON, Excel, Parquet
- Detección automática de formato
- Mensajes informativos con emojis
- Manejo de errores robusto
- Ayuda integrada (`--help`)

## 🎓 Conceptos

- Click para CLIs profesionales
- Decoradores de comandos
- Opciones y argumentos
- Validación de inputs
- Mensajes de error amigables

---

Perfecto para automatizar tareas de datos desde la terminal.
