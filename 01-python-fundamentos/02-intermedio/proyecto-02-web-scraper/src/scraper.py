"""
Web Scraper - Extracción de Datos de Páginas Web
=================================================

Este proyecto demuestra web scraping con BeautifulSoup y requests.
Incluye ejemplos de:
- Scraping de páginas estáticas
- Navegación por múltiples páginas
- Extracción de tablas
- Manejo de errores
- Rate limiting y headers
"""

import requests
from bs4 import BeautifulSoup
import json
import time
from pathlib import Path
from datetime import datetime
import csv

class WebScraper:
    """Clase base para web scraping."""
    
    def __init__(self, base_url):
        """
        Inicializa el scraper.
        
        Args:
            base_url (str): URL base del sitio a scrapear
        """
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        self.output_dir = Path(__file__).parent.parent / 'output'
        self.output_dir.mkdir(exist_ok=True)
    
    def get_page(self, url, retries=3):
        """
        Obtiene el contenido de una página.
        
        Args:
            url (str): URL a scrapear
            retries (int): Número de reintentos
            
        Returns:
            BeautifulSoup: Objeto parseado o None si falla
        """
        for attempt in range(retries):
            try:
                print(f"📡 Scrapeando: {url}")
                response = self.session.get(url, timeout=10)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.content, 'html.parser')
                time.sleep(1)  # Rate limiting
                
                return soup
            
            except requests.exceptions.RequestException as e:
                print(f"⚠️  Intento {attempt + 1}/{retries} falló: {e}")
                if attempt < retries - 1:
                    time.sleep(2 ** attempt)
                else:
                    print(f"❌ Error obteniendo {url}")
                    return None
    
    def extract_links(self, soup, selector='a'):
        """
        Extrae todos los links de una página.
        
        Args:
            soup (BeautifulSoup): Página parseada
            selector (str): Selector CSS
            
        Returns:
            list: Lista de URLs
        """
        links = []
        for link in soup.select(selector):
            href = link.get('href')
            if href:
                # Convertir a URL absoluta si es relativa
                if href.startswith('/'):
                    href = self.base_url + href
                elif not href.startswith('http'):
                    href = self.base_url + '/' + href
                links.append(href)
        return links
    
    def extract_table(self, soup, table_selector='table'):
        """
        Extrae datos de una tabla HTML.
        
        Args:
            soup (BeautifulSoup): Página parseada
            table_selector (str): Selector de la tabla
            
        Returns:
            list: Lista de diccionarios con los datos
        """
        table = soup.select_one(table_selector)
        if not table:
            return []
        
        # Extraer headers
        headers = []
        for th in table.select('thead th, th'):
            headers.append(th.get_text(strip=True))
        
        # Extraer filas
        rows = []
        for tr in table.select('tbody tr, tr'):
            cells = tr.select('td')
            if cells:
                row = {}
                for i, cell in enumerate(cells):
                    header = headers[i] if i < len(headers) else f'col_{i}'
                    row[header] = cell.get_text(strip=True)
                rows.append(row)
        
        return rows


class QuotesScraper(WebScraper):
    """
    Scraper de ejemplo para http://quotes.toscrape.com
    Sitio web de práctica para web scraping.
    """
    
    def __init__(self):
        super().__init__('http://quotes.toscrape.com')
    
    def scrape_quotes(self, max_pages=5):
        """
        Scrapea quotes del sitio.
        
        Args:
            max_pages (int): Máximo de páginas a scrapear
            
        Returns:
            list: Lista de quotes
        """
        all_quotes = []
        page = 1
        
        print(f"\n{'='*70}")
        print("🕷️  SCRAPING QUOTES")
        print(f"{'='*70}\n")
        
        while page <= max_pages:
            url = f"{self.base_url}/page/{page}/"
            soup = self.get_page(url)
            
            if not soup:
                break
            
            # Extraer quotes de esta página
            quotes = soup.select('.quote')
            
            if not quotes:
                print(f"✅ No más quotes encontrados")
                break
            
            for quote in quotes:
                text = quote.select_one('.text').get_text(strip=True)
                author = quote.select_one('.author').get_text(strip=True)
                tags = [tag.get_text(strip=True) for tag in quote.select('.tag')]
                
                all_quotes.append({
                    'text': text,
                    'author': author,
                    'tags': tags,
                    'page': page
                })
            
            print(f"   📄 Página {page}: {len(quotes)} quotes encontrados")
            page += 1
        
        print(f"\n✅ Total quotes scrapeados: {len(all_quotes)}")
        return all_quotes
    
    def scrape_authors(self):
        """Scrapea información de autores."""
        print(f"\n{'='*70}")
        print("👤 SCRAPING AUTHORS")
        print(f"{'='*70}\n")
        
        # Primero obtener lista de autores
        soup = self.get_page(self.base_url)
        author_links = set()
        
        for link in soup.select('a[href^="/author/"]'):
            author_links.add(self.base_url + link['href'])
        
        authors = []
        for i, author_url in enumerate(author_links, 1):
            soup = self.get_page(author_url)
            if not soup:
                continue
            
            name = soup.select_one('.author-title').get_text(strip=True)
            born_date = soup.select_one('.author-born-date').get_text(strip=True)
            born_location = soup.select_one('.author-born-location').get_text(strip=True)
            description = soup.select_one('.author-description').get_text(strip=True)
            
            authors.append({
                'name': name,
                'born_date': born_date,
                'born_location': born_location,
                'description': description[:200] + '...'  # Truncar
            })
            
            print(f"   👤 {i}. {name}")
        
        print(f"\n✅ Total autores scrapeados: {len(authors)}")
        return authors


class WikiTableScraper(WebScraper):
    """
    Ejemplo de scraping de tablas de Wikipedia.
    """
    
    def __init__(self):
        super().__init__('https://en.wikipedia.org')
    
    def scrape_country_table(self):
        """
        Scrapea tabla de países de Wikipedia.
        Ejemplo: https://en.wikipedia.org/wiki/List_of_countries_by_population_(United_Nations)
        """
        url = self.base_url + '/wiki/List_of_countries_by_population_(United_Nations)'
        
        print(f"\n{'='*70}")
        print("🌍 SCRAPING COUNTRY POPULATION TABLE")
        print(f"{'='*70}\n")
        
        soup = self.get_page(url)
        if not soup:
            return []
        
        # Encontrar la tabla principal
        table = soup.select_one('table.wikitable')
        data = self.extract_table(soup, 'table.wikitable')
        
        print(f"✅ {len(data)} países extraídos")
        
        return data[:50]  # Primeros 50


def main():
    """Función principal."""
    print("="*70)
    print("🕷️  WEB SCRAPER - EXTRACCIÓN DE DATOS WEB")
    print("="*70)
    
    output_dir = Path(__file__).parent.parent / 'output'
    
    # 1. Scrapear quotes
    quotes_scraper = QuotesScraper()
    quotes = quotes_scraper.scrape_quotes(max_pages=3)
    
    # Guardar quotes
    with open(output_dir / 'quotes.json', 'w', encoding='utf-8') as f:
        json.dump(quotes, f, indent=2, ensure_ascii=False)
    print(f"\n💾 Quotes guardados en: quotes.json")
    
    # 2. Scrapear autores
    authors = quotes_scraper.scrape_authors()
    
    with open(output_dir / 'authors.json', 'w', encoding='utf-8') as f:
        json.dump(authors, f, indent=2, ensure_ascii=False)
    print(f"💾 Autores guardados en: authors.json")
    
    # 3. Ejemplo de tabla de Wikipedia
    print("\n" + "="*70)
    print("💡 EJEMPLO: TABLA DE WIKIPEDIA")
    print("="*70)
    print("Para scrapear Wikipedia, descomenta el siguiente código:")
    print("# wiki_scraper = WikiTableScraper()")
    print("# countries = wiki_scraper.scrape_country_table()")
    
    # Resumen final
    print("\n" + "="*70)
    print("✨ SCRAPING COMPLETADO")
    print("="*70)
    print(f"\n📊 Estadísticas:")
    print(f"   - Quotes: {len(quotes)}")
    print(f"   - Autores: {len(authors)}")
    print(f"\n📁 Archivos generados en: {output_dir}")
    
    # Análisis rápido
    print(f"\n📈 Análisis rápido:")
    
    # Autores más citados
    from collections import Counter
    author_counts = Counter(q['author'] for q in quotes)
    print(f"\n   Top 5 autores más citados:")
    for author, count in author_counts.most_common(5):
        print(f"      {author}: {count} quotes")
    
    # Tags más comunes
    all_tags = []
    for q in quotes:
        all_tags.extend(q['tags'])
    tag_counts = Counter(all_tags)
    print(f"\n   Top 5 tags más comunes:")
    for tag, count in tag_counts.most_common(5):
        print(f"      #{tag}: {count} veces")


if __name__ == "__main__":
    main()
