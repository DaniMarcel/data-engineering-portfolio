"""
Generador de Datasets Compartidos
==================================

Este script genera datasets comunes que se usan en múltiples proyectos del portafolio.
Incluye datos realistas de diferentes dominios y formatos.
"""

import pandas as pd
import numpy as np
import json
from datetime import datetime, timedelta
from pathlib import Path
import random

np.random.seed(42)
random.seed(42)

BASE_PATH = Path(__file__).parent

def generar_logs_servidor(n=100000):
    """Genera logs de servidor web simulados."""
    print("\n🖥️  Generando logs de servidor...")
    
    METODOS = ['GET', 'GET', 'GET', 'POST', 'POST', 'PUT', 'DELETE']
    ENDPOINTS = [
        '/api/users', '/api/products', '/api/orders', '/api/auth/login',
        '/api/auth/register', '/api/products/search', '/api/cart',
        '/static/css/main.css', '/static/js/app.js', '/favicon.ico'
    ]
    STATUS_CODES = {
        200: 0.70,  # OK
        201: 0.05,  # Created
        204: 0.03,  # No Content
        301: 0.02,  # Redirect
        400: 0.05,  # Bad Request
        401: 0.03,  # Unauthorized
        404: 0.07,  # Not Found
        500: 0.03,  # Server Error
        503: 0.02   # Service Unavailable
    }
    
    USER_AGENTS = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/91.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) Safari/14.0',
        'Mozilla/5.0 (X11; Linux x86_64) Firefox/89.0',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) Safari/604.1'
    ]
    
    logs = []
    start_time = datetime(2024, 1, 1, 0, 0, 0)
    
    for i in range(n):
        timestamp = start_time + timedelta(
            seconds=random.randint(0, 31536000)  # Todo el año 2024
        )
        
        metodo = random.choice(METODOS)
        endpoint = random.choice(ENDPOINTS)
        status = np.random.choice(
            list(STATUS_CODES.keys()),
            p=list(STATUS_CODES.values())
        )
        
        # Tamaño de respuesta basado en status
        if status == 200:
            size = random.randint(500, 50000)
        elif status == 404:
            size = random.randint(200, 500)
        else:
            size = random.randint(100, 1000)
        
        response_time = random.lognormvariate(4, 1.5)  # Distribución log-normal
        
        ip = f"{random.randint(1, 255)}.{random.randint(1, 255)}." \
             f"{random.randint(1, 255)}.{random.randint(1, 255)}"
        
        log_entry = {
            'timestamp': timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            'ip': ip,
            'method': metodo,
            'endpoint': endpoint,
            'status_code': status,
            'response_size_bytes': size,
            'response_time_ms': round(response_time, 2),
            'user_agent': random.choice(USER_AGENTS)
        }
        logs.append(log_entry)
    
    df = pd.DataFrame(logs)
    df = df.sort_values('timestamp').reset_index(drop=True)
    
    # Guardar en múltiples formatos
    logs_path = BASE_PATH / 'logs'
    logs_path.mkdir(exist_ok=True)
    
    df.to_csv(logs_path / 'server_logs.csv', index=False)
    df.to_json(logs_path / 'server_logs.jsonl', orient='records', lines=True)
    
    print(f"   ✅ {len(df):,} logs generados")
    return df

def generar_time_series_iot(n=500000):
    """Genera datos de sensores IoT de temperatura, humedad, etc."""
    print("\n🌡️  Generando time series IoT...")
    
    SENSORES = [f'SENSOR_{i:03d}' for i in range(1, 51)]  # 50 sensores
    UBICACIONES = ['Almacén A', 'Almacén B', 'Oficina', 'Producción', 'Exteriores']
    
    readings = []
    start_time = datetime(2024, 1, 1, 0, 0, 0)
    
    # Cada sensor lee cada 5 minutos
    for i in range(n):
        timestamp = start_time + timedelta(minutes=i % 105120)  # Año completo
        sensor_id = random.choice(SENSORES)
        ubicacion = random.choice(UBICACIONES)
        
        # Temperatura base según ubicación
        base_temp = {
            'Almacén A': 18,
            'Almacén B': 20,
            'Oficina': 22,
            'Producción': 25,
            'Exteriores': 15
        }[ubicacion]
        
        # Variación diurna
        hora = timestamp.hour
        variacion_diurna = 3 * np.sin((hora - 6) * np.pi / 12)
        
        temperatura = base_temp + variacion_diurna + random.gauss(0, 1)
        humedad = 50 + random.gauss(0, 10)
        
        # Occasional anomalies
        if random.random() < 0.001:  # 0.1% anomalías
            temperatura += random.choice([-10, 10])
        
        readings.append({
            'timestamp': timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            'sensor_id': sensor_id,
            'ubicacion': ubicacion,
            'temperatura_celsius': round(temperatura, 2),
            'humedad_porcentaje': round(max(0, min(100, humedad)), 2),
            'presion_hpa': round(1013 + random.gauss(0, 5), 2),
        })
    
    df = pd.DataFrame(readings)
    df = df.sort_values('timestamp').reset_index(drop=True)
    
    # Guardar
    ts_path = BASE_PATH / 'time-series'
    ts_path.mkdir(exist_ok=True)
    
    df.to_csv(ts_path / 'iot_sensors.csv', index=False)
    df.to_parquet(ts_path / 'iot_sensors.parquet')
    
    print(f"   ✅ {len(df):,} lecturas generadas")
    return df

def generar_api_responses(n=10000):
    """Genera respuestas simuladas de API REST."""
    print("\n🌐 Generando API responses...")
    
    responses = []
    
    for i in range(1, n + 1):
        response = {
            'id': i,
            'user_id': random.randint(1, 5000),
            'title': f'Post {i}: ' + random.choice([
                'New Feature Released', 'Bug Fix Update', 'Performance Improvements',
                'Security Patch', 'UI Redesign', 'API Changes'
            ]),
            'body': 'Lorem ipsum dolor sit amet ' * random.randint(5, 20),
            'created_at': (datetime(2024, 1, 1) + timedelta(days=random.randint(0, 350))).isoformat(),
            'likes': random.randint(0, 1000),
            'comments': random.randint(0, 100),
            'tags': random.sample(['python', 'data', 'api', 'web', 'ml', 'etl'], k=random.randint(1, 3)),
            'published': random.choice([True, True, True, False]),  # 75% publicados
        }
        responses.append(response)
    
    # Guardar en JSON
    api_path = BASE_PATH / 'api-responses'
    api_path.mkdir(exist_ok=True)
    
    with open(api_path / 'api_data.json', 'w') as f:
        json.dump(responses, f, indent=2)
    
    # También JSONL
    with open(api_path / 'api_data.jsonl', 'w') as f:
        for resp in responses:
            f.write(json.dumps(resp) + '\n')
    
    print(f"   ✅ {len(responses):,} responses generadas")
    return responses

def generar_usuarios(n=10000):
    """Genera datos de usuarios para diversos proyectos."""
    print("\n👥 Generando usuarios...")
    
    NOMBRES = ['Ana', 'Carlos', 'María', 'Juan', 'Laura', 'David', 'Carmen', 'Miguel']
    APELLIDOS = ['García', 'Rodríguez', 'González', 'Fernández', 'López', 'Martínez']
    PAISES = ['España', 'México', 'Argentina', 'Colombia', 'Chile', 'Perú']
    
    usuarios = []
    for i in range(1, n + 1):
        nombre = random.choice(NOMBRES)
        apellido = random.choice(APELLIDOS)
        
        usuario = {
            'user_id': i,
            'username': f'{nombre.lower()}{apellido.lower()}{random.randint(1, 999)}',
            'email': f'{nombre.lower()}.{apellido.lower()}{i}@email.com',
            'nombre': nombre,
            'apellido': apellido,
            'edad': random.randint(18, 75),
            'pais': random.choice(PAISES),
            'fecha_registro': (datetime(2021, 1, 1) + timedelta(days=random.randint(0, 1460))).strftime('%Y-%m-%d'),
            'activo': random.choice([True, True, True, False]),  # 75% activos
            'premium': random.choice([True, False, False, False]),  # 25% premium
        }
        usuarios.append(usuario)
    
    df = pd.DataFrame(usuarios)
    
    # Guardar
    users_path = BASE_PATH / 'usuarios'
    users_path.mkdir(exist_ok=True)
    
    df.to_csv(users_path / 'usuarios.csv', index=False)
    df.to_json(users_path / 'usuarios.json', orient='records', indent=2)
    df.to_parquet(users_path / 'usuarios.parquet')
    
    print(f"   ✅ {len(df):,} usuarios generados")
    return df

def main():
    """Genera todos los datasets compartidos."""
    print("="*80)
    print("🔄 GENERANDO DATASETS COMPARTIDOS")
    print("="*80)
    
    generar_usuarios(10000)
    generar_logs_servidor(100000)
    generar_time_series_iot(500000)
    generar_api_responses(10000)
    
    print("\n" + "="*80)
    print("✨ TODOS LOS DATASETS GENERADOS")
    print("="*80)
    print(f"\n📁 Ubicación: {BASE_PATH.absolute()}")
    print("\n📊 Datasets disponibles:")
    print("   - usuarios/ (CSV, JSON, Parquet)")
    print("   - logs/ (CSV, JSONL)")
    print("   - time-series/ (CSV, Parquet)")
    print("   - api-responses/ (JSON, JSONL)")

if __name__ == "__main__":
    main()
