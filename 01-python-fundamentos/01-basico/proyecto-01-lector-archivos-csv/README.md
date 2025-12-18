# 📂 Proyecto 01: Lector y Analizador de Archivos CSV

## 🎯 Objetivos de Aprendizaje

Este proyecto te enseñará:

- ✅ Lectura y escritura de archivos CSV usando la biblioteca estándar de Python
- ✅ Manejo de excepciones y validación de datos
- ✅ Uso de estructuras de datos (diccionarios, listas, defaultdict, Counter)
- ✅ Programación orientada a objetos básica
- ✅ Formateo de salida para reportes legibles
- ✅ Buenas prácticas de organización de código

## 🎓 Nivel

**Básico** - Ideal para principiantes que están aprendiendo Python

## 📋 Conceptos Clave

### Python Estándar

- Módulo `csv` para leer archivos CSV
- `pathlib.Path` para manejo de rutas multiplataforma
- `collections.defaultdict` y `collections.Counter` para agregaciones
- Manejo de excepciones con `try/except`
- Context managers (`with` statement)

### Validación de Datos

- Conversión de tipos de datos
- Validación de campos obligatorios
- Manejo de datos faltantes o incorrectos
- Registro de errores para análisis posterior

## 🚀 Quick Start

### 1. Generar datos de ejemplo

```bash
cd src
python generar_datos.py
```

Esto creará el archivo `data/raw/ventas_2024.csv` con 1,000 registros de ventas sintéticos.

### 2. Ejecutar el analizador

```bash
python main.py
```

## 📊 Datos de Entrada

El archivo `ventas_2024.csv` contiene:

| Campo                | Tipo   | Descripción                    |
| -------------------- | ------ | ------------------------------ |
| id_venta             | int    | ID único de la transacción     |
| fecha                | string | Fecha en formato YYYY-MM-DD    |
| producto             | string | Nombre del producto            |
| categoria            | string | Categoría del producto         |
| cantidad             | int    | Unidades vendidas              |
| precio_unitario      | float  | Precio por unidad              |
| subtotal             | float  | Cantidad × Precio              |
| descuento_porcentaje | int    | Porcentaje de descuento (0-20) |
| monto_descuento      | float  | Dinero descontado              |
| total                | float  | Subtotal - Descuento           |
| ciudad               | string | Ciudad de la venta             |
| metodo_pago          | string | Método de pago utilizado       |

**Nota**: Los datos incluyen ~2% de registros con problemas intencionales para practicar validación y limpieza.

## 💡 Explicación del Código

### Estructura del Proyecto

```
proyecto-01-lector-archivos-csv/
├── data/
│   ├── raw/              # Datos originales
│   │   └── ventas_2024.csv
│   └── processed/        # Datos procesados (futuro)
├── src/
│   ├── generar_datos.py  # Generador de datos sintéticos
│   └── main.py          # Analizador principal
├── output/              # Reportes y resultados
│   └── errores_validacion.txt
└── README.md
```

### Clase `AnalizadorVentas`

La clase principal encapsula toda la lógica:

```python
class AnalizadorVentas:
    def __init__(self, archivo_csv):
        # Inicialización

    def leer_csv(self):
        # Lee y valida el CSV

    def _validar_fila(self, row, num_linea):
        # Valida cada fila individualmente

    def resumen_general(self):
        # Estadísticas generales

    def ventas_por_categoria(self):
        # Agregación por categoría

    # ... más métodos de análisis
```

### Flujo de Ejecución

1. **Lectura del CSV**: Se lee línea por línea usando `csv.DictReader`
2. **Validación**: Cada fila se valida y convierte a los tipos correctos
3. **Manejo de Errores**: Los registros problemáticos se registran pero no detienen el proceso
4. **Análisis**: Se calculan estadísticas usando agregaciones eficientes
5. **Reporte**: Se muestra un reporte formateado en consola

### Técnicas Destacadas

**1. defaultdict para Agregaciones**

```python
ventas_cat = defaultdict(lambda: {'total': 0, 'cantidad': 0})
for venta in self.ventas:
    ventas_cat[venta['categoria']]['total'] += venta['total']
```

**2. Counter para Conteos**

```python
metodos = Counter(v['metodo_pago'] for v in self.ventas)
```

**3. Ordenamiento con Lambda**

```python
categorias_ordenadas = sorted(
    ventas_cat.items(),
    key=lambda x: x[1]['total'],
    reverse=True
)
```

## 📈 Salida Esperada

El programa generará un reporte como este:

```
============================================================
📊 RESUMEN GENERAL DE VENTAS
============================================================
Total de transacciones: 980
Total de productos vendidos: 2,456
Ingresos totales: €412,589.45
Promedio por venta: €421.01
Venta mínima: €19.99
Venta máxima: €6,499.95

============================================================
📦 VENTAS POR CATEGORÍA
============================================================

Electrónica:
  💰 Ingresos: €145,234.76
  📦 Unidades vendidas: 789

...
```

## 🔧 Personalización

### Cambiar el número de registros

En `generar_datos.py`:

```python
NUM_REGISTROS = 5000  # Cambiar de 1000 a 5000
```

### Añadir nuevas categorías de productos

En `generar_datos.py`:

```python
PRODUCTOS = [
    ("Tu Producto", 99.99, "Tu Categoría"),
    # ... más productos
]
```

### Agregar nuevos análisis

Añade métodos a la clase `AnalizadorVentas`:

```python
def ventas_por_mes(self):
    """Analiza ventas mensuales."""
    # Tu implementación aquí
```

## 🐛 Troubleshooting

**Error: Archivo no encontrado**

- Asegúrate de ejecutar primero `generar_datos.py`
- Verifica que estés en el directorio correcto

**Error de encoding**

- Los archivos usan UTF-8, asegúrate de que tu sistema lo soporte

**Registros con errores**

- Es normal, ~2% de registros tienen problemas intencionales
- Revisa `output/errores_validacion.txt` para detalles

## 📚 Próximos Pasos

Después de este proyecto, puedes:

1. **Mejorar el código**:

   - Añadir exportación a JSON o Excel
   - Crear visualizaciones con matplotlib
   - Implementar filtros por fecha/categoría

2. **Siguiente proyecto**:

   - `proyecto-02-cli-tool` - Crear herramientas de línea de comandos
   - `02-analisis-datos/01-eda-exploratorio` - Usar pandas para análisis

3. **Aprender más**:
   - Pruebas unitarias con `pytest`
   - Type hints para mejor documentación
   - Logging en lugar de prints

## 💻 Código Limpio

Este proyecto demuestra:

- ✅ Nombres descriptivos de variables y funciones
- ✅ Docstrings en funciones y clases
- ✅ Separación de responsabilidades
- ✅ Manejo apropiado de errores
- ✅ Comentarios donde añaden valor

## 📝 Notas

- Este proyecto **NO usa pandas** intencionalmente para aprender los fundamentos
- Los datos son 100% sintéticos y generados con propósitos educativos
- Los errores en los datos son intencionales para practicar validación

---

**¡Feliz aprendizaje! 🚀**
