"""
Generador de Dataset Completo de E-commerce
============================================

Genera un dataset realista de ventas de e-commerce con:
- Múltiples productos y categorías
- Transacciones con información de clientes
- Datos temporales (ventas a lo largo del año)
- Información geográfica
- Diferentes canales de venta

Este dataset es ideal para practicar EDA (Exploratory Data Analysis)
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Configuración
np.random.seed(42)
random.seed(42)

NUM_CLIENTES = 5000
NUM_PRODUCTOS = 100
NUM_TRANSACCIONES = 50000

# Datos base
CATEGORIAS = {
    'Electrónica': ['Laptop', 'Tablet', 'Smartphone', 'Auriculares', 'Smartwatch', 'Monitor', 'Teclado', 'Mouse'],
    'Hogar': ['Silla', 'Mesa', 'Lámpara', 'Estantería', 'Escritorio', 'Sofá', 'Cama', 'Armario'],
    'Deporte': ['Bicicleta', 'Pesas', 'Esterilla Yoga', 'Ropa Deportiva', 'Zapatillas Running', 'Mancuernas'],
    'Libros': ['Novela', 'Técnico', 'Autoayuda', 'Infantil', 'Cómic', 'Biografía', 'Cocina', 'Historia'],
    'Belleza': ['Crema Facial', 'Champú', 'Maquillaje', 'Perfume', 'Serum', 'Mascarilla'],
    'Alimentación': ['Café', 'Té', 'Snacks', 'Cereales', 'Pasta', 'Aceite', 'Especias', 'Chocolate'],
}

CIUDADES_ESPAÑA = {
    'Madrid': 0.20,
    'Barcelona': 0.18,
    'Valencia': 0.10,
    'Sevilla': 0.09,
    'Zaragoza': 0.08,
    'Málaga': 0.07,
    'Murcia': 0.06,
    'Palma': 0.05,
    'Bilbao': 0.08,
    'Alicante': 0.05,
    'Otras': 0.04,
}

CANALES = ['Web', 'Móvil', 'Tienda Física', 'Marketplace']
METODOS_PAGO = ['Tarjeta Crédito', 'Tarjeta Débito', 'PayPal', 'Transferencia', 'Contra Reembolso']
ESTADOS_PEDIDO = ['Completado', 'Completado', 'Completado', 'Completado', 'Cancelado', 'Devuelto']  # Mayoría completados

def generar_productos(n=NUM_PRODUCTOS):
    """Genera catálogo de productos."""
    productos = []
    pid = 1
    
    for categoria, tipos in CATEGORIAS.items():
        for tipo in tipos:
            # Generar variaciones de cada tipo
            num_variaciones = random.randint(1, 3)
            for v in range(num_variaciones):
                marca = random.choice(['ProBrand', 'TechMax', 'HomeStyle', 'SportPro', 'BeautyLux', 'Premium'])
                nombre = f"{marca} {tipo}" + (f" v{v+1}" if num_variaciones > 1 else "")
                
                # Precio basado en categoría
                if categoria == 'Electrónica':
                    precio = round(random.uniform(50, 2000), 2)
                elif categoria == 'Hogar':
                    precio = round(random.uniform(30, 800), 2)
                elif categoria == 'Deporte':
                    precio = round(random.uniform(15, 500), 2)
                elif categoria == 'Libros':
                    precio = round(random.uniform(10, 50), 2)
                elif categoria == 'Belleza':
                    precio = round(random.uniform(8, 150), 2)
                else:  # Alimentación
                    precio = round(random.uniform(3, 40), 2)
                
                productos.append({
                    'producto_id': pid,
                    'nombre_producto': nombre,
                    'categoria': categoria,
                    'subcategoria': tipo,
                    'precio_base': precio,
                    'costo': round(precio * random.uniform(0.4, 0.7), 2),  # Margen
                    'stock': random.randint(0, 500),
                    'peso_kg': round(random.uniform(0.1, 20), 2),
                })
                pid += 1
                
                if pid > n:
                    return pd.DataFrame(productos)
    
    return pd.DataFrame(productos)

def generar_clientes(n=NUM_CLIENTES):
    """Genera base de clientes."""
    nombres = ['Ana', 'Carlos', 'María', 'Juan', 'Laura', 'David', 'Carmen', 'Miguel', 'Elena', 'Javier']
    apellidos = ['García', 'Rodríguez', 'González', 'Fernández', 'López', 'Martínez', 'Sánchez', 'Pérez']
    
    clientes = []
    for i in range(1, n + 1):
        nombre = random.choice(nombres)
        apellido = random.choice(apellidos)
        email = f"{nombre.lower()}.{apellido.lower()}{random.randint(1, 999)}@email.com"
        
        # Fecha de registro (últimos 3 años)
        fecha_registro = datetime(2021, 1, 1) + timedelta(days=random.randint(0, 1095))
        
        # Ciudad según distribución
        ciudad = np.random.choice(list(CIUDADES_ESPAÑA.keys()), p=list(CIUDADES_ESPAÑA.values()))
        
        clientes.append({
            'cliente_id': i,
            'nombre': nombre,
            'apellido': apellido,
            'email': email,
            'ciudad': ciudad,
            'fecha_registro': fecha_registro.strftime('%Y-%m-%d'),
            'edad': random.randint(18, 75),
            'genero': random.choice(['M', 'F', 'Otro']),
            'segmento': random.choice(['Premium', 'Regular', 'Ocasional']),
        })
    
    return pd.DataFrame(clientes)

def generar_transacciones(productos_df, clientes_df, n=NUM_TRANSACCIONES):
    """Genera transacciones de ventas."""
    transacciones = []
    
    # Clientes que compran más (distribución Pareto: 20% generan 80% ventas)
    clientes_activos = clientes_df['cliente_id'].values
    pesos_clientes = np.array([1/(i+1)**0.8 for i in range(len(clientes_activos))])
    pesos_clientes = pesos_clientes / pesos_clientes.sum()
    
    for i in range(1, n + 1):
        # Fecha aleatoria en 2024
        fecha = datetime(2024, 1, 1) + timedelta(days=random.randint(0, 350))
        
        # Cliente (algunos compran más que otros)
        cliente_id = np.random.choice(clientes_activos, p=pesos_clientes)
        
        # Producto aleatorio
        producto = productos_df.sample(1).iloc[0]
        
        # Cantidad (mayoría compran 1-2 unidades)
        cantidad = np.random.choice([1, 1, 1, 2, 2, 3], p=[0.5, 0.2, 0.1, 0.1, 0.05, 0.05])
        
        # Descuento (mayoría sin descuento)
        descuento_prob = random.random()
        if descuento_prob < 0.7:
            descuento = 0
        elif descuento_prob < 0.9:
            descuento = random.choice([5, 10, 15])
        else:
            descuento = random.choice([20, 25, 30, 40])
        
        # Cálculos
        precio_unitario = producto['precio_base']
        subtotal = precio_unitario * cantidad
        monto_descuento = subtotal * (descuento / 100)
        
        # Envío gratis >50€, sino 5€
        gastos_envio = 0 if subtotal > 50 else 5.0
        
        total = subtotal - monto_descuento + gastos_envio
        
        # Datos adicionales
        hora = random.randint(8, 23)
        canal = random.choice(CANALES)
        metodo_pago = random.choice(METODOS_PAGO)
        estado = random.choice(ESTADOS_PEDIDO)
        
        # Información de envío (algunas ciudades tienen más demanda)
        cliente_info = clientes_df[clientes_df['cliente_id'] == cliente_id].iloc[0]
        ciudad_envio = cliente_info['ciudad']
        
        transacciones.append({
            'transaccion_id': f'T{i:06d}',
            'fecha': fecha.strftime('%Y-%m-%d'),
            'hora': f'{hora:02d}:{random.randint(0, 59):02d}',
            'año': fecha.year,
            'mes': fecha.month,
            'mes_nombre': fecha.strftime('%B'),
            'trimestre': f'Q{(fecha.month-1)//3 + 1}',
            'dia_semana': fecha.strftime('%A'),
            'cliente_id': int(cliente_id),
            'producto_id': int(producto['producto_id']),
            'producto_nombre': producto['nombre_producto'],
            'categoria': producto['categoria'],
            'subcategoria': producto['subcategoria'],
            'cantidad': cantidad,
            'precio_unitario': round(precio_unitario, 2),
            'subtotal': round(subtotal, 2),
            'descuento_porcentaje': descuento,
            'monto_descuento': round(monto_descuento, 2),
            'gastos_envio': gastos_envio,
            'total': round(total, 2),
            'canal': canal,
            'metodo_pago': metodo_pago,
            'estado_pedido': estado,
            'ciudad_envio': ciudad_envio,
            'peso_total_kg': round(producto['peso_kg'] * cantidad, 2),
        })
    
    return pd.DataFrame(transacciones)

def introducir_problemas_calidad(df, porcentaje=0.02):
    """Introduce problemas de calidad de datos intencionales."""
    n_problemas = int(len(df) * porcentaje)
    indices = np.random.choice(df.index, n_problemas, replace=False)
    
    df_copia = df.copy()
    
    for idx in indices:
        problema = random.choice(['missing', 'outlier', 'duplicate'])
        
        if problema == 'missing':
            # Hacer algunos valores NaN
            col = random.choice(['cantidad', 'descuento_porcentaje', 'ciudad_envio'])
            df_copia.at[idx, col] = np.nan
        
        elif problema == 'outlier':
            # Crear valores extremos
            df_copia.at[idx, 'cantidad'] = random.randint(100, 1000)
        
        # 'duplicate' se manejará después
    
    return df_copia

def main():
    """Genera todos los datasets."""
    print("🔄 Generando datasets de e-commerce...")
    print("="*60)
    
    # 1. Productos
    print("\n📦 Generando catálogo de productos...")
    productos = generar_productos()
    print(f"   ✅ {len(productos)} productos generados")
    
    # 2. Clientes
    print("\n👥 Generando base de clientes...")
    clientes = generar_clientes()
    print(f"   ✅ {len(clientes)} clientes generados")
    
    # 3. Transacciones
    print("\n💰 Generando transacciones...")
    transacciones = generar_transacciones(productos, clientes)
    transacciones = introducir_problemas_calidad(transacciones)
    print(f"   ✅ {len(transacciones)} transacciones generadas")
    
    # Guardar archivos
    print("\n💾 Guardando archivos...")
    
    base_path = '../data/raw/'
    
    productos.to_csv(f'{base_path}productos.csv', index=False, encoding='utf-8')
    print(f"   ✅ productos.csv")
    
    clientes.to_csv(f'{base_path}clientes.csv', index=False, encoding='utf-8')
    print(f"   ✅ clientes.csv")
    
    transacciones.to_csv(f'{base_path}transacciones.csv', index=False, encoding='utf-8')
    print(f"   ✅ transacciones.csv")
    
    # También guardar en otros formatos para práctica
    transacciones.to_json(f'{base_path}transacciones.json', orient='records', lines=True)
    print(f"   ✅ transacciones.json (JSONL)")
    
    transacciones.to_parquet(f'{base_path}transacciones.parquet')
    print(f"   ✅ transacciones.parquet")
    
    # Estadísticas
    print("\n" + "="*60)
    print("📊 RESUMEN DE DATOS GENERADOS")
    print("="*60)
    print(f"Productos: {len(productos):,}")
    print(f"Categorías: {productos['categoria'].nunique()}")
    print(f"Clientes: {len(clientes):,}")
    print(f"Transacciones: {len(transacciones):,}")
    print(f"Ingresos totales: €{transacciones['total'].sum():,.2f}")
    print(f"Ticket promedio: €{transacciones['total'].mean():.2f}")
    print(f"Rango de fechas: {transacciones['fecha'].min()} a {transacciones['fecha'].max()}")
    print("\n✨ ¡Datasets listos para análisis!")

if __name__ == "__main__":
    main()
