"""
Generador de datos de ventas para el proyecto de lector de archivos CSV.
Este script genera datos sintéticos realistas de ventas de productos.
"""

import csv
import random
from datetime import datetime, timedelta
from pathlib import Path

# Configuración
NUM_REGISTROS = 1000
ARCHIVO_SALIDA = Path(__file__).parent.parent / "data" / "raw" / "ventas_2024.csv"

# Datos de ejemplo
PRODUCTOS = [
    ("Laptop Dell XPS 13", 1299.99, "Electrónica"),
    ("Mouse Logitech MX Master", 99.99, "Accesorios"),
    ("Teclado Mecánico Keychron", 89.99, "Accesorios"),
    ("Monitor LG 27 4K", 449.99, "Electrónica"),
    ("Webcam Logitech C920", 79.99, "Electrónica"),
    ("Auriculares Sony WH-1000XM4", 349.99, "Audio"),
    ("Micrófono Blue Yeti", 129.99, "Audio"),
    ("SSD Samsung 1TB", 109.99, "Almacenamiento"),
    ("RAM Corsair 16GB", 79.99, "Componentes"),
    ("GPU NVIDIA RTX 3060", 399.99, "Componentes"),
    ("Silla Gamer DXRacer", 299.99, "Muebles"),
    ("Escritorio Ajustable", 349.99, "Muebles"),
    ("Cable HDMI 2.1", 19.99, "Cables"),
    ("Hub USB-C", 49.99, "Accesorios"),
    ("Power Bank Anker 20000mAh", 59.99, "Accesorios"),
]

CIUDADES = ["Madrid", "Barcelona", "Valencia", "Sevilla", "Bilbao", "Málaga", "Zaragoza"]
METODOS_PAGO = ["Tarjeta Crédito", "Tarjeta Débito", "PayPal", "Transferencia", "Efectivo"]

def generar_fecha_aleatoria():
    """Genera una fecha aleatoria en 2024."""
    inicio = datetime(2024, 1, 1)
    fin = datetime(2024, 12, 18)
    dias_diferencia = (fin - inicio).days
    fecha_aleatoria = inicio + timedelta(days=random.randint(0, dias_diferencia))
    return fecha_aleatoria.strftime("%Y-%m-%d")

def generar_ventas(num_registros):
    """Genera registros de ventas sintéticos."""
    ventas = []
    
    for i in range(1, num_registros + 1):
        producto, precio, categoria = random.choice(PRODUCTOS)
        cantidad = random.randint(1, 5)
        descuento = random.choice([0, 0, 0, 0.05, 0.10, 0.15, 0.20])  # 60% sin descuento
        
        # Calcular totales
        subtotal = precio * cantidad
        monto_descuento = subtotal * descuento
        total = subtotal - monto_descuento
        
        # Ocasionalmente introducir valores problemáticos para practicar limpieza
        if random.random() < 0.02:  # 2% de registros con problemas
            if random.choice([True, False]):
                cantidad = ""  # Valor vacío
            else:
                total = "ERROR"  # Valor inválido
        
        venta = {
            "id_venta": i,
            "fecha": generar_fecha_aleatoria(),
            "producto": producto,
            "categoria": categoria,
            "cantidad": cantidad,
            "precio_unitario": round(precio, 2),
            "subtotal": round(subtotal, 2),
            "descuento_porcentaje": int(descuento * 100),
            "monto_descuento": round(monto_descuento, 2),
            "total": round(total, 2) if isinstance(total, float) else total,
            "ciudad": random.choice(CIUDADES),
            "metodo_pago": random.choice(METODOS_PAGO),
        }
        ventas.append(venta)
    
    return ventas

def guardar_csv(ventas, archivo):
    """Guarda las ventas en un archivo CSV."""
    archivo.parent.mkdir(parents=True, exist_ok=True)
    
    with open(archivo, 'w', newline='', encoding='utf-8') as f:
        campos = [
            "id_venta", "fecha", "producto", "categoria", "cantidad",
            "precio_unitario", "subtotal", "descuento_porcentaje",
            "monto_descuento", "total", "ciudad", "metodo_pago"
        ]
        writer = csv.DictWriter(f, fieldnames=campos)
        writer.writeheader()
        writer.writerows(ventas)
    
    print(f"✅ Archivo generado: {archivo}")
    print(f"📊 Total de registros: {len(ventas)}")

if __name__ == "__main__":
    print("🔄 Generando datos de ventas...")
    ventas = generar_ventas(NUM_REGISTROS)
    guardar_csv(ventas, ARCHIVO_SALIDA)
    print("✨ ¡Listo!")
