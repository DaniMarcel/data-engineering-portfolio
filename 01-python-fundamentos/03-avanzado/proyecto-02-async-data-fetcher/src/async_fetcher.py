"""
Async Data Fetcher - Descarga de Datos Asíncrona
================================================

Demuestra programación asíncrona con asyncio y aiohttp para:
- Descargar múltiples URLs en paralelo
- Procesar datos de forma asíncrona
- Manejo de concurrencia
- Rate limiting asíncrono
"""

import asyncio
import aiohttp
import time
from typing import List, Dict
import json

async def fetch_url(session: aiohttp.ClientSession, url: str, semaphore: asyncio.Semaphore) -> Dict:
    """
    Descarga una URL de forma asíncrona.
    
    Args:
        session: Sesión aiohttp
        url: URL a descargar
        semaphore: Semáforo para limitar concurrencia
    """
    async with semaphore:
        try:
            print(f"📡 Descargando: {url}")
            async with session.get(url) as response:
                data = await response.json()
                print(f"   ✅ Completado: {url}")
                return {'url': url, 'status': response.status, 'data': data}
        except Exception as e:
            print(f"   ❌ Error en {url}: {e}")
            return {'url': url, 'status': 'error', 'error': str(e)}


async def fetch_multiple_urls(urls: List[str], max_concurrent: int = 5) -> List[Dict]:
    """
    Descarga múltiples URLs en paralelo con límite de concurrencia.
    
    Args:
        urls: Lista de URLs
        max_concurrent: Máximo de descargas simultáneas
    """
    semaphore = asyncio.Semaphore(max_concurrent)
    
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_url(session, url, semaphore) for url in urls]
        results = await asyncio.gather(*tasks)
    
    return results


async def process_data_async(data_list: List[Dict]) -> List[Dict]:
    """Procesa datos de forma asíncrona."""
    async def process_item(item: Dict) -> Dict:
        # Simular procesamiento
        await asyncio.sleep(0.1)
        if 'data' in item:
            item['processed'] = True
        return item
    
    tasks = [process_item(item) for item in data_list]
    return await asyncio.gather(*tasks)


async def ejemplo_basico():
    """Ejemplo básico de async/await."""
    print("\n" + "="*70)
    print("🚀 EJEMPLO: ASYNC/AWAIT BÁSICO")
    print("="*70)
    
    # API pública de ejemplo
    urls = [
        'https://jsonplaceholder.typicode.com/posts/1',
        'https://jsonplaceholder.typicode.com/posts/2',
        'https://jsonplaceholder.typicode.com/posts/3',
        'https://jsonplaceholder.typicode.com/posts/4',
        'https://jsonplaceholder.typicode.com/posts/5',
    ]
    
    # Sync vs Async comparison
    print("\n⏱️  Comparando velocidad...")
    
    # Async
    start = time.time()
    results = await fetch_multiple_urls(urls, max_concurrent=5)
    async_time = time.time() - start
    
    print(f"\n📊 Resultados:")
    print(f"   URLs procesadas: {len(results)}")
    print(f"   Exitosas: {sum(1 for r in results if r.get('status') == 200)}")
    print(f"   Tiempo async: {async_time:.2f}s")
    print(f"   🚀 Las peticiones se hicieron en paralelo!")


async def ejemplo_rate_limiting():
    """Ejemplo con rate limiting."""
    print("\n" + "="*70)
    print("⏱️  EJEMPLO: RATE LIMITING")
    print("="*70)
    
    urls = [f'https://jsonplaceholder.typicode.com/posts/{i}' for i in range(1, 11)]
    
    print(f"\nDescargando {len(urls)} URLs con max 3 concurrent...")
    start = time.time()
    results = await fetch_multiple_urls(urls, max_concurrent=3)
    duration = time.time() - start
    
    print(f"\n✅ Completado en {duration:.2f}s")
    print(f"   Promedio: {duration/len(urls):.2f}s por URL")


async def ejemplo_procesamiento_pipeline():
    """Ejemplo de pipeline de procesamiento asíncrono."""
    print("\n" + "="*70)
    print("🔄 EJEMPLO: PIPELINE ASÍNCRONO")
    print("="*70)
    
    # 1. Fetch
    urls = [f'https://jsonplaceholder.typicode.com/users/{i}' for i in range(1, 6)]
    print("\n1️⃣ Fetching data...")
    data = await fetch_multiple_urls(urls, max_concurrent=5)
    
    # 2. Process
    print("\n2️⃣ Processing data...")
    processed = await process_data_async(data)
    
    # 3. Results
    print(f"\n✅ Pipeline completado:")
    print(f"   Items procesados: {len(processed)}")
    successful = [p for p in processed if p.get('processed')]
    print(f"   Exitosos: {len(successful)}")


def main():
    """Función principal."""
    print("="*70)
    print("⚡ ASYNC DATA FETCHER")
    print("="*70)
    
    # Ejecutar ejemplos
    asyncio.run(ejemplo_basico())
    asyncio.run(ejemplo_rate_limiting())
    asyncio.run(ejemplo_procesamiento_pipeline())
    
    print("\n" + "="*70)
    print("✨ EJEMPLOS COMPLETADOS")
    print("="*70)
    print("\n💡 Programación asíncrona permite:")
    print("   - Descargas paralelas eficientes")
    print("   - Mejor uso de recursos")
    print("   - Rate limiting controlado")
    print("   - Pipelines de datos escalables")


if __name__ == "__main__":
    main()
