# 🌐 API Consumer - Consumidor de APIs REST

## 🎯 Objetivos de Aprendizaje

- ✅ Consumir APIs REST con **requests**
- ✅ Manejar autenticación (API keys, tokens)
- ✅ Procesar respuestas JSON
- ✅ Implementar paginación
- ✅ Manejo robusto de errores
- ✅ Rate limiting y buenas prácticas

## 🎓 Nivel

**Intermedio** - Requiere conocimientos básicos de Python y HTTP

## 📋 Conceptos Clave

### APIs REST

- Peticiones HTTP (GET, POST, PUT, DELETE)
- Status codes (200, 404, 500, etc.)
- Headers y autenticación
- Query parameters
- Request/Response body (JSON)

### Biblioteca Requests

- `requests.Session()` para conexiones persistentes
- Manejo de timeouts
- Manejo de excepciones
- Headers personalizados

### Buenas Prácticas

- Rate limiting (esperar entre peticiones)
- Manejo de errores HTTP
- Logging de peticiones
- Guardar respuestas para análisis

## 🚀 Quick Start

### 1. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 2. Ejecutar ejemplos

```bash
cd src
python main.py
```

El script consumirá varias APIs públicas y guardará los datos en `output/`.

## 🌍 APIs Utilizadas

### 1. JSONPlaceholder

**URL**: https://jsonplaceholder.typicode.com  
**Autenticación**: No requerida  
**Uso**: API de prueba con datos fake

**Endpoints usados**:

- `GET /users` - Lista de usuarios
- `GET /posts` - Lista de posts
- `POST /posts` - Crear post (simulado)

### 2. GitHub API

**URL**: https://api.github.com  
**Autenticación**: Opcional (sin auth: 60 req/hora)  
**Uso**: Información de repositorios

**Endpoints usados**:

- `GET /repos/:owner/:repo` - Info de repositorio

## 📊 Datos Generados

El script genera:

| Archivo                | Descripción                 | Registros |
| ---------------------- | --------------------------- | --------- |
| usuarios.json          | Usuarios de JSONPlaceholder | 10        |
| posts.json             | Posts (paginados)           | 100       |
| github_repo.json       | Info repositorio Python     | 1         |
| resumen_ejecucion.json | Resumen de la ejecución     | -         |

## 💡 Explicación del Código

### Clase `APIConsumer`

Encapsula toda la lógica de consumo de APIs:

```python
class APIConsumer:
    def __init__(self, base_url, api_key=None):
        self.session = requests.Session()
        # Headers y autenticación

    def get(self, endpoint, params=None):
        # Petición GET con manejo de errores

    def post(self, endpoint, data):
        # Petición POST

    def fetch_paginated(self, endpoint, limit=100):
        # Obtener datos paginados automáticamente
```

### Manejo de Errores

```python
try:
    response = self.session.get(url, timeout=10)
    response.raise_for_status()  # Raise si 4xx o 5xx
    return response.json()

except requests.exceptions.HTTPError as e:
    # Manejar errores HTTP
except requests.exceptions.Timeout:
    # Manejar timeouts
except requests.exceptions.RequestException as e:
    # Otros errores de requests
```

### Paginación Automática

```python
def fetch_paginated(self, endpoint, limit=100, max_pages=None):
    all_items = []
    page = 1

    while True:
        params = {'_page': page, '_limit': limit}
        data = self.get(endpoint, params=params)

        if not data or len(data) == 0:
            break

        all_items.extend(data)
        page += 1
        time.sleep(0.5)  # Rate limiting

    return all_items
```

## 🔧 Personalización

### Añadir nueva API

```python
def ejemplo_mi_api():
    api = APIConsumer('https://api.ejemplo.com', api_key='tu_key')

    datos = api.get('/endpoint')

    if datos:
        # Procesar datos
        print(datos)
```

### Usar API con autenticación

```python
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv('MI_API_KEY')
api = APIConsumer('https://api.ejemplo.com', api_key=api_key)
```

### Cambiar rate limiting

```python
# En fetch_paginated()
time.sleep(1.0)  # Cambiar de 0.5s a 1s entre peticiones
```

## 📈 Salida Esperada

```
====================================================================
🚀 API CONSUMER - CONSUMIDOR DE APIs REST
====================================================================

====================================================================
🌐 EJEMPLO: JSONPlaceholder API
====================================================================

📋 1. Obteniendo usuarios...
📡 GET https://jsonplaceholder.typicode.com/users
   ✅ 10 usuarios obtenidos

   Ejemplo - Usuario 1:
   - Nombre: Leanne Graham
   - Email: Sincere@april.biz
   - Ciudad: Gwenborough

   💾 Guardado en: usuarios.json


📝 2. Obteniendo posts (paginado)...
📡 GET https://jsonplaceholder.typicode.com/posts
   📄 Página 1: 20 items (Total: 20)
   📄 Página 2: 20 items (Total: 40)
   ...
```

## 🐛 Troubleshooting

**Error: requests module not found**

```bash
pip install requests
```

**Timeout errors**

- Aumenta el timeout: `api.get(endpoint, timeout=30)`
- Verifica tu conexión a internet

**Rate limit exceeded**

- Aumenta el tiempo entre peticiones en `fetch_paginated()`
- Usa autenticación si la API lo permite

**JSON decode error**

- La API puede estar devolviendo HTML en lugar de JSON
- Verifica que el endpoint sea correcto

## 📚 Próximos Pasos

1. **Añadir más APIs**:

   - OpenWeather API (clima)
   - News API (noticias)
   - CoinGecko API (criptomonedas)

2. **Mejorar el código**:

   - Implementar retry logic
   - Añadir caching de respuestas
   - Logging más detallado

3. **Integrar con análisis**:

   - Usar pandas para analizar los datos
   - Crear visualizaciones
   - Guardar en base de datos

4. **Siguiente proyecto**:
   - `proyecto-02-web-scraper` - Extraer datos de páginas web
   - Proyecto ETL completo con APIs

## 💻 APIs Recomendadas para Practicar

### Sin Autenticación

- **JSONPlaceholder** - https://jsonplaceholder.typicode.com - Datos fake
- **RESTCountries** - https://restcountries.com - Info de países
- **Cat Facts** - https://catfact.ninja - Datos curiosos de gatos

### Con Autenticación (Gratis)

- **GitHub** - https://api.github.com - Repositorios
- **OpenWeather** - https://openweathermap.org/api - Clima
- **News API** - https://newsapi.org - Noticias
- **CoinGecko** - https://www.coingecko.com/en/api - Crypto

### España

- **Datos Abiertos** - https://datos.gob.es
- **AEMET** - https://opendata.aemet.es - Meteorología

## 📝 Notas

- Respeta los límites de rate limiting de cada API
- No compartas tus API keys en repositorios públicos
- Usa `.env` para guardar credenciales
- Siempre lee la documentación oficial de la API

---

**🌐 El mundo de datos está a una petición HTTP de distancia!**
