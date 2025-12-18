"""
API Consumer - Consumidor de APIs REST
======================================

Este proyecto demuestra cómo trabajar con APIs REST públicas:
- Hacer peticiones HTTP GET/POST
- Manejar autenticación (API keys)
- Procesar respuestas JSON
- Manejo de errores y rate limiting
- Guardar datos en diferentes formatos
"""

import requests
import json
import time
from pathlib import Path
from datetime import datetime
import os

class APIConsumer:
    """Cliente para consumir APIs REST públicas."""
    
    def __init__(self, base_url, api_key=None):
        """
        Inicializa el cliente de API.
        
        Args:
            base_url (str): URL base de la API
            api_key (str): API key para autenticación (opcional)
        """
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.session = requests.Session()
        
        # Headers comunes
        self.session.headers.update({
            'User-Agent': 'Python API Consumer/1.0',
            'Accept': 'application/json'
        })
        
        if api_key:
            self.session.headers.update({'Authorization': f'Bearer {api_key}'})
    
    def get(self, endpoint, params=None, timeout=10):
        """
        Realiza petición GET a la API.
        
        Args:
            endpoint (str): Endpoint de la API (ej: '/users')
            params (dict): Parámetros query string
            timeout (int): Timeout en segundos
            
        Returns:
            dict: Respuesta JSON parseada
        """
        url = f"{self.base_url}{endpoint}"
        
        try:
            print(f"📡 GET {url}")
            response = self.session.get(url, params=params, timeout=timeout)
            response.raise_for_status()  # Raise exception para códigos 4xx/5xx
            
            return response.json()
        
        except requests.exceptions.HTTPError as e:
            print(f"❌ HTTP Error: {e}")
            print(f"   Status: {response.status_code}")
            print(f"   Response: {response.text[:200]}")
            return None
        
        except requests.exceptions.Timeout:
            print(f"❌ Timeout: La petición tardó más de {timeout}s")
            return None
        
        except requests.exceptions.RequestException as e:
            print(f"❌ Request Error: {e}")
            return None
        
        except json.JSONDecodeError:
            print(f"❌ Error parseando JSON")
            print(f"   Response: {response.text[:200]}")
            return None
    
    def post(self, endpoint, data, timeout=10):
        """
        Realiza petición POST a la API.
        
        Args:
            endpoint (str): Endpoint de la API
            data (dict): Datos a enviar en el body
            timeout (int): Timeout en segundos
            
        Returns:
            dict: Respuesta JSON parseada
        """
        url = f"{self.base_url}{endpoint}"
        
        try:
            print(f"📤 POST {url}")
            response = self.session.post(url, json=data, timeout=timeout)
            response.raise_for_status()
            
            return response.json()
        
        except requests.exceptions.RequestException as e:
            print(f"❌ Error: {e}")
            return None
    
    def fetch_paginated(self, endpoint, limit=100, max_pages=None):
        """
        Obtiene datos paginados de una API.
        
        Args:
            endpoint (str): Endpoint de la API
            limit (int): Elementos por página
            max_pages (int): Máximo de páginas a obtener (None = todas)
            
        Returns:
            list: Lista con todos los elementos obtenidos
        """
        all_items = []
        page = 1
        
        while True:
            if max_pages and page > max_pages:
                break
            
            params = {'_page': page, '_limit': limit}
            data = self.get(endpoint, params=params)
            
            if not data or len(data) == 0:
                break
            
            all_items.extend(data)
            print(f"   📄 Página {page}: {len(data)} items (Total: {len(all_items)})")
            
            page += 1
            time.sleep(0.5)  # Rate limiting - esperar entre peticiones
        
        return all_items


def ejemplo_jsonplaceholder():
    """
    Ejemplo usando JSONPlaceholder - API de prueba pública.
    https://jsonplaceholder.typicode.com/
    """
    print("="*70)
    print("🌐 EJEMPLO: JSONPlaceholder API")
    print("="*70 + "\n")
    
    api = APIConsumer('https://jsonplaceholder.typicode.com')
    output_dir = Path(__file__).parent.parent / 'output'
    output_dir.mkdir(exist_ok=True)
    
    # 1. Obtener usuarios
    print("\n📋 1. Obteniendo usuarios...")
    users = api.get('/users')
    
    if users:
        print(f"   ✅ {len(users)} usuarios obtenidos")
        print(f"\n   Ejemplo - Usuario 1:")
        print(f"   - Nombre: {users[0]['name']}")
        print(f"   - Email: {users[0]['email']}")
        print(f"   - Ciudad: {users[0]['address']['city']}")
        
        # Guardar usuarios
        with open(output_dir / 'usuarios.json', 'w', encoding='utf-8') as f:
            json.dump(users, f, indent=2, ensure_ascii=False)
        print(f"   💾 Guardado en: usuarios.json")
    
    # 2. Obtener posts con paginación
    print("\n\n📝 2. Obteniendo posts (paginado)...")
    posts = api.fetch_paginated('/posts', limit=20, max_pages=5)
    
    if posts:
        print(f"\n   ✅ Total posts obtenidos: {len(posts)}")
        
        # Análisis básico
        users_post_count = {}
        for post in posts:
            user_id = post['userId']
            users_post_count[user_id] = users_post_count.get(user_id, 0) + 1
        
        print(f"\n   📊 Posts por usuario:")
        for user_id, count in sorted(users_post_count.items())[:5]:
            print(f"      Usuario {user_id}: {count} posts")
        
        # Guardar
        with open(output_dir / 'posts.json', 'w', encoding='utf-8') as f:
            json.dump(posts, f, indent=2, ensure_ascii=False)
        print(f"\n   💾 Guardado en: posts.json")
    
    # 3. Obtener un post específico
    print("\n\n🔍 3. Obteniendo post específico (ID: 1)...")
    post = api.get('/posts/1')
    
    if post:
        print(f"   ✅ Post obtenido:")
        print(f"   - Título: {post['title']}")
        print(f"   - User ID: {post['userId']}")
    
    # 4. Crear un post (POST request)
    print("\n\n📤 4. Creando nuevo post...")
    new_post = {
        'title': 'Aprendiendo APIs con Python',
        'body': 'Este es un post de ejemplo creado con requests',
        'userId': 1
    }
    
    created = api.post('/posts', new_post)
    
    if created:
        print(f"   ✅ Post creado:")
        print(f"   - ID: {created['id']}")
        print(f"   - Título: {created['title']}")


def ejemplo_github_api():
    """
    Ejemplo usando GitHub API (sin autenticación - límite de 60 req/hora).
    https://docs.github.com/en/rest
    """
    print("\n\n" + "="*70)
    print("🐙 EJEMPLO: GitHub API")
    print("="*70 + "\n")
    
    api = APIConsumer('https://api.github.com')
    output_dir = Path(__file__).parent.parent / 'output'
    
    # Obtener información de un repositorio popular
    print("📦 Obteniendo info del repositorio 'python/cpython'...")
    repo = api.get('/repos/python/cpython')
    
    if repo:
        print(f"\n   ✅ Repositorio: {repo['full_name']}")
        print(f"   - Descripción: {repo['description']}")
        print(f"   - ⭐ Stars: {repo['stargazers_count']:,}")
        print(f"   - 🍴 Forks: {repo['forks_count']:,}")
        print(f"   - 👁️ Watchers: {repo['watchers_count']:,}")
        print(f"   - Lenguaje: {repo['language']}")
        print(f"   - Última actualización: {repo['updated_at']}")
        
        # Guardar info
        with open(output_dir / 'github_repo.json', 'w', encoding='utf-8') as f:
            json.dump(repo, f, indent=2, ensure_ascii=False)
        print(f"\n   💾 Guardado en: github_repo.json")


def ejemplo_api_publica_espanola():
    """
    Ejemplo usando una API pública española de datos abiertos.
    """
    print("\n\n" + "="*70)
    print("🇪🇸 EJEMPLO: API Pública Española")
    print("="*70 + "\n")
    
    # API de datos abiertos (ejemplo genérico)
    print("💡 Nota: Este es un ejemplo de estructura.")
    print("   Para APIs reales, consulta: datos.gob.es")


def guardar_resumen():
    """Guarda un resumen de todos los datos obtenidos."""
    output_dir = Path(__file__).parent.parent / 'output'
    
    resumen = {
        'fecha_ejecucion': datetime.now().isoformat(),
        'apis_consultadas': [
            {
                'nombre': 'JSONPlaceholder',
                'url': 'https://jsonplaceholder.typicode.com',
                'endpoints': ['/users', '/posts'],
                'total_registros': 'variable'
            },
            {
                'nombre': 'GitHub',
                'url': 'https://api.github.com',
                'endpoints': ['/repos/:owner/:repo'],
                'total_registros': 1
            }
        ],
        'archivos_generados': [
            'usuarios.json',
            'posts.json',
            'github_repo.json'
        ]
    }
    
    with open(output_dir / 'resumen_ejecucion.json', 'w', encoding='utf-8') as f:
        json.dump(resumen, f, indent=2, ensure_ascii=False)
    
    print("\n\n" + "="*70)
    print("📊 RESUMEN GUARDADO")
    print("="*70)
    print(f"📁 Directorio de salida: {output_dir.absolute()}")
    print(f"📄 Archivos generados: {len(resumen['archivos_generados'])}")


def main():
    """Función principal del programa."""
    print("="*70)
    print("🚀 API CONSUMER - CONSUMIDOR DE APIs REST")
    print("="*70 + "\n")
    
    print("Este programa demuestra cómo trabajar con APIs REST públicas.\n")
    
    # Ejecutar ejemplos
    ejemplo_jsonplaceholder()
    ejemplo_github_api()
    ejemplo_api_publica_espanola()
    guardar_resumen()
    
    print("\n\n✨ ¡Ejemplos completados!")


if __name__ == "__main__":
    main()
