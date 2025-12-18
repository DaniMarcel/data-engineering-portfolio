"""
Decoradores para Data Pipelines
================================

Decoradores personalizados para:
- Logging automático
- Medición de tiempos
- Retry logic
- Validación de datos
- Caché de resultados
"""

import time
import functools
from datetime import datetime
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


# ============= DECORADORES BÁSICOS =============

def timing(func):
    """Mide el tiempo de ejecución de una función."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        logger.info(f"⏱️  {func.__name__} tardó {end - start:.4f} segundos")
        return result
    return wrapper


def log_execution(func):
    """Registra la ejecución de una función."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logger.info(f"🔄 Ejecutando: {func.__name__}")
        logger.info(f"   Args: {args}")
        logger.info(f"   Kwargs: {kwargs}")
        
        try:
            result = func(*args, **kwargs)
            logger.info(f"✅ {func.__name__} completado exitosamente")
            return result
        except Exception as e:
            logger.error(f"❌ Error en {func.__name__}: {e}")
            raise
    
    return wrapper


def retry(max_attempts=3, delay=1):
    """Reintenta una función si falla."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts:
                        logger.error(f"❌ {func.__name__} falló después de {max_attempts} intentos")
                        raise
                    logger.warning(f"⚠️  Intento {attempt}/{max_attempts} falló: {e}")
                    time.sleep(delay * attempt)
        
        return wrapper
    return decorator


def validate_input(**validators):
    """Valida los inputs de una función."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Validar kwargs
            for param, validator in validators.items():
                if param in kwargs:
                    value = kwargs[param]
                    if not validator(value):
                        raise ValueError(f"Validación falló para {param}={value}")
            
            return func(*args, **kwargs)
        
        return wrapper
    return decorator


def cache_result(func):
    """Cachea el resultado de una función (memoization)."""
    cache = {}
    
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Crear key del cache
        key = str(args) + str(kwargs)
        
        if key in cache:
            logger.info(f"📦 Usando resultado cacheado para {func.__name__}")
            return cache[key]
        
        result = func(*args, **kwargs)
        cache[key] = result
        logger.info(f"💾 Resultado cacheado para {func.__name__}")
        
        return result
    
    return wrapper


# ============= DECORADORES PARA DATA PIPELINES =============

def data_pipeline_step(step_name):
    """Decorador para pasos de un data pipeline."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            logger.info(f"\n{'='*60}")
            logger.info(f"📊 PASO: {step_name}")
            logger.info(f"{'='*60}")
            
            start = time.time()
            
            try:
                result = func(*args, **kwargs)
                end = time.time()
                
                # Log resultado
                if hasattr(result, '__len__'):
                    logger.info(f"✅ Completado: {len(result)} registros")
                else:
                    logger.info(f"✅ Completado")
                
                logger.info(f"⏱️  Tiempo: {end - start:.2f}s")
                
                return result
            
            except Exception as e:
                logger.error(f"❌ Error en {step_name}: {e}")
                raise
        
        return wrapper
    return decorator


def count_records(func):
    """Cuenta registros de entrada y salida."""
    @functools.wraps(func)
    def wrapper(data, *args, **kwargs):
        input_count = len(data) if hasattr(data, '__len__') else 0
        logger.info(f"📥 Input: {input_count:,} registros")
        
        result = func(data, *args, **kwargs)
        
        output_count = len(result) if hasattr(result, '__len__') else 0
        logger.info(f"📤 Output: {output_count:,} registros")
        
        diff = output_count - input_count
        if diff > 0:
            logger.info(f"   ➕ +{diff:,} registros")
        elif diff < 0:
            logger.info(f"   ➖ {diff:,} registros")
        
        return result
    
    return wrapper


# ============= EJEMPLOS DE USO =============

@timing
@log_execution
def procesar_datos_basico(data):
    """Ejemplo básico con timing y logging."""
    time.sleep(0.5)  # Simular procesamiento
    return [x * 2 for x in data]


@retry(max_attempts=3, delay=1)
def api_call_simulada():
    """Simula llamada a API que puede fallar."""
    import random
    if random.random() < 0.7:  # 70% probabilidad de fallar
        raise ConnectionError("API no disponible")
    return {"status": "success", "data": [1, 2, 3]}


@validate_input(
    edad=lambda x: 0 <= x <= 120,
    nombre=lambda x: len(x) > 0
)
def crear_usuario(nombre, edad):
    """Crea usuario con validación de inputs."""
    return {"nombre": nombre, "edad": edad}


@cache_result
@timing
def operacion_costosa(n):
    """Operación costosa que se beneficia de caché."""
    time.sleep(1)  # Simular operación lenta
    return sum(range(n))


@data_pipeline_step("Extract - Leer Datos")
@count_records
def extract_data(source):
    """Paso 1: Extraer datos."""
    # Simular lectura
    return source


@data_pipeline_step("Transform - Limpiar Datos")
@count_records
def transform_data(data):
    """Paso 2: Transformar datos."""
    # Simular limpieza (remover valores inválidos)
    return [x for x in data if x > 0]


@data_pipeline_step("Load - Guardar Datos")
@count_records
def load_data(data):
    """Paso 3: Cargar datos."""
    # Simular guardado
    logger.info(f"💾 Datos guardados exitosamente")
    return data


def ejemplo_pipeline():
    """Ejemplo completo de pipeline con decoradores."""
    print("\n" + "="*60)
    print("🔧 EJEMPLO: DATA PIPELINE CON DECORADORES")
    print("="*60)
    
    # Datos de ejemplo
    datos = [10, -5, 20, 0, 30, -10, 40]
    
    # Pipeline
    extracted = extract_data(datos)
    transformed = transform_data(extracted)
    loaded = load_data(transformed)
    
    print(f"\n✨ Pipeline completado: {len(loaded)} registros finales")


def ejemplo_retry():
    """Ejemplo de retry."""
    print("\n" + "="*60)
    print("🔄 EJEMPLO: RETRY LOGIC")
    print("="*60)
    
    try:
        result = api_call_simulada()
        print(f"✅ API call exitosa: {result}")
    except Exception as e:
        print(f"❌ API call falló finalmente: {e}")


def ejemplo_validacion():
    """Ejemplo de validación."""
    print("\n" + "="*60)
    print("✅ EJEMPLO: VALIDACIÓN DE INPUTS")
    print("="*60)
    
    # Válido
    try:
        usuario1 = crear_usuario("Juan", 25)
        print(f"✅ Usuario creado: {usuario1}")
    except ValueError as e:
        print(f"❌ Error: {e}")
    
    # Inválido
    try:
        usuario2 = crear_usuario("", 150)
        print(f"✅ Usuario creado: {usuario2}")
    except ValueError as e:
        print(f"❌ Error: {e}")


def ejemplo_cache():
    """Ejemplo de caché."""
    print("\n" + "="*60)
    print("📦 EJEMPLO: CACHÉ DE RESULTADOS")
    print("="*60)
    
    # Primera llamada (lenta)
    resultado1 = operacion_costosa(1000)
    
    # Segunda llamada (rápida, usa caché)
    resultado2 = operacion_costosa(1000)
    
    print(f"Resultados iguales: {resultado1 == resultado2}")


def main():
    """Función principal."""
    print("="*60)
    print("🎨 DECORADORES PARA DATA PIPELINES")
    print("="*60)
    
    ejemplo_pipeline()
    ejemplo_retry()
    ejemplo_validacion()
    ejemplo_cache()
    
    print("\n" + "="*60)
    print("✨ EJEMPLOS COMPLETADOS")
    print("="*60)


if __name__ == "__main__":
    main()
