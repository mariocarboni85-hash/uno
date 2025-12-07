def perform_browser_action(params):
    """
    Esegue azioni browser: 'goto' (apre URL), 'screenshot' (mock).
    params: {'op': 'goto'|'screenshot', 'url': ...}
    """
    op = params.get('op')
    url = params.get('url')
    if op == 'goto' and url:
        # Qui si potrebbe integrare Selenium o simili
        return {'result': f'Navigato su {url}'}
    elif op == 'screenshot' and url:
        return {'result': f'Screenshot di {url} (mock)'}
    return {'error': 'Operazione non valida'}
"""Advanced Browser Tool for SuperAgent.

NOTE: This project uses only the lightweight HTTP fetch in the main flow.
BeautifulSoup and advanced scraping features are optional; if `bs4` is not
installed, only the basic `simple_fetch` will be used.
"""

import requests
try:  # bs4 is optional
    from bs4 import BeautifulSoup
except Exception:  # pragma: no cover - optional dep
    BeautifulSoup = None  # type: ignore

import json
import re
from urllib.parse import urljoin, urlparse
from typing import Dict, List, Optional, Union
import time


class BrowserTool:
    """Advanced browser automation and web scraping tool."""
    
    def __init__(self, headless: bool = True):
        self.headless = headless
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })
        self.history = []
        self.cookies = {}
    
    def fetch(self, url: str, timeout: int = 10, method: str = "GET", data: dict = None) -> dict:
        """
        Fetch URL content with advanced options.
        
        Args:
            url: URL to fetch
            timeout: Request timeout in seconds
            method: HTTP method (GET, POST, etc.)
            data: Data to send with POST requests
            
        Returns:
            dict with status_code, text, headers, cookies
        """
        try:
            if method.upper() == "GET":
                response = self.session.get(url, timeout=timeout)
            elif method.upper() == "POST":
                response = self.session.post(url, data=data, timeout=timeout)
            else:
                return {"error": f"Unsupported method: {method}"}
            
            self.history.append({
                'url': url,
                'status': response.status_code,
                'timestamp': time.time()
            })
            
            return {
                "status_code": response.status_code,
                "url": response.url,
                "text": response.text,
                "headers": dict(response.headers),
                "cookies": dict(response.cookies),
                "encoding": response.encoding
            }
        except Exception as e:
            return {"error": str(e)}
    
    def parse_html(self, html: str):
        """Parse HTML content with BeautifulSoup, if available."""
        if BeautifulSoup is None:
            raise RuntimeError("BeautifulSoup (bs4) non è installato.")
        return BeautifulSoup(html, 'lxml')
    
    def extract_links(self, url: str, filter_external: bool = False) -> List[Dict[str, str]]:
        """
        Extract all links from a webpage.
        
        Args:
            url: URL to scrape
            filter_external: If True, only return links from same domain
            
        Returns:
            List of dicts with 'text' and 'href'
        """
        if BeautifulSoup is None:
            return []
        try:
            response = self.fetch(url)
            if 'error' in response:
                return []
            
            soup = self.parse_html(response['text'])
            links = []
            base_domain = urlparse(url).netloc
            
            for link in soup.find_all('a', href=True):
                href = urljoin(url, link['href'])
                text = link.get_text(strip=True)
                
                if filter_external:
                    link_domain = urlparse(href).netloc
                    if link_domain != base_domain:
                        continue
                
                links.append({
                    'text': text,
                    'href': href
                })
            
            return links
        except Exception as e:
            return []
    
    def extract_text(self, url: str, selector: Optional[str] = None) -> str:
        """
        Extract text content from webpage.
        
        Args:
            url: URL to scrape
            selector: Optional CSS selector to extract specific element
            
        Returns:
            Extracted text content
        """
        if BeautifulSoup is None:
            return ""
        try:
            response = self.fetch(url)
            if 'error' in response:
                return ""
            
            soup = self.parse_html(response['text'])
            
            if selector:
                element = soup.select_one(selector)
                if element:
                    return element.get_text(strip=True)
                return ""
            
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()
            
            text = soup.get_text()
            # Clean up whitespace
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = '\n'.join(chunk for chunk in chunks if chunk)
            
            return text
        except Exception as e:
            return f"Error: {e}"
    
    def extract_data(self, url: str, schema: Dict) -> Dict:
        """
        Extract structured data from webpage based on schema.
        
        Args:
            url: URL to scrape
            schema: Dict mapping field names to CSS selectors
            
        Returns:
            Dict with extracted data
        """
        try:
            response = self.fetch(url)
            if 'error' in response:
                return {"error": response['error']}
            
            soup = self.parse_html(response['text'])
            data = {}
            
            for field, selector in schema.items():
                element = soup.select_one(selector)
                if element:
                    data[field] = element.get_text(strip=True)
                else:
                    data[field] = None
            
            return data
        except Exception as e:
            return {"error": str(e)}
    
    def extract_images(self, url: str) -> List[Dict[str, str]]:
        """
        Extract all images from webpage.
        
        Returns:
            List of dicts with 'src', 'alt', 'title'
        """
        try:
            response = self.fetch(url)
            if 'error' in response:
                return []
            
            soup = self.parse_html(response['text'])
            images = []
            
            for img in soup.find_all('img'):
                src = img.get('src', '')
                if src:
                    src = urljoin(url, src)
                
                images.append({
                    'src': src,
                    'alt': img.get('alt', ''),
                    'title': img.get('title', '')
                })
            
            return images
        except Exception as e:
            return []
    
    def search_google(self, query: str, num_results: int = 10) -> List[Dict[str, str]]:
        """
        Search Google and extract results.
        
        Args:
            query: Search query
            num_results: Number of results to return
            
        Returns:
            List of dicts with 'title', 'link', 'snippet'
        """
        try:
            search_url = f"https://www.google.com/search?q={requests.utils.quote(query)}&num={num_results}"
            
            response = self.fetch(search_url)
            if 'error' in response:
                return []
            
            soup = self.parse_html(response['text'])
            results = []
            
            for g in soup.find_all('div', class_='g'):
                title_elem = g.find('h3')
                link_elem = g.find('a')
                snippet_elem = g.find('div', class_=['VwiC3b', 'yXK7lf'])
                
                if title_elem and link_elem:
                    results.append({
                        'title': title_elem.get_text(strip=True),
                        'link': link_elem.get('href', ''),
                        'snippet': snippet_elem.get_text(strip=True) if snippet_elem else ''
                    })
            
            return results[:num_results]
        except Exception as e:
            return []
    
    def download_file(self, url: str, save_path: str) -> bool:
        """
        Download file from URL.
        
        Args:
            url: File URL
            save_path: Local path to save file
            
        Returns:
            True if successful, False otherwise
        """
        try:
            response = self.session.get(url, stream=True, timeout=30)
            response.raise_for_status()
            
            with open(save_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            return True
        except Exception as e:
            print(f"Download error: {e}")
            return False
    
    def get_page_metadata(self, url: str) -> Dict[str, str]:
        """
        Extract page metadata (title, description, keywords, etc.).
        
        Returns:
            Dict with metadata
        """
        try:
            response = self.fetch(url)
            if 'error' in response:
                return {"error": response['error']}
            
            soup = self.parse_html(response['text'])
            metadata = {}
            
            # Title
            title = soup.find('title')
            metadata['title'] = title.get_text(strip=True) if title else ''
            
            # Meta tags
            meta_tags = {
                'description': soup.find('meta', attrs={'name': 'description'}),
                'keywords': soup.find('meta', attrs={'name': 'keywords'}),
                'author': soup.find('meta', attrs={'name': 'author'}),
                'og:title': soup.find('meta', property='og:title'),
                'og:description': soup.find('meta', property='og:description'),
                'og:image': soup.find('meta', property='og:image'),
            }
            
            for key, tag in meta_tags.items():
                if tag:
                    content = tag.get('content', '')
                    metadata[key] = content
            
            return metadata
        except Exception as e:
            return {"error": str(e)}
    
    def check_url_status(self, url: str) -> Dict[str, Union[int, str, bool]]:
        """
        Check if URL is accessible.
        
        Returns:
            Dict with status_code, ok, response_time
        """
        try:
            start = time.time()
            response = self.session.head(url, timeout=10, allow_redirects=True)
            response_time = time.time() - start
            
            return {
                'url': url,
                'status_code': response.status_code,
                'ok': response.ok,
                'response_time': round(response_time, 3),
                'final_url': response.url
            }
        except Exception as e:
            return {
                'url': url,
                'error': str(e),
                'ok': False
            }
    
    def extract_tables(self, url: str) -> List[List[List[str]]]:
        """
        Extract all tables from webpage.
        
        Returns:
            List of tables, each table is a list of rows, each row is a list of cells
        """
        try:
            response = self.fetch(url)
            if 'error' in response:
                return []
            
            soup = self.parse_html(response['text'])
            tables = []
            
            for table in soup.find_all('table'):
                table_data = []
                rows = table.find_all('tr')
                
                for row in rows:
                    cells = row.find_all(['td', 'th'])
                    row_data = [cell.get_text(strip=True) for cell in cells]
                    table_data.append(row_data)
                
                if table_data:
                    tables.append(table_data)
            
            return tables
        except Exception as e:
            return []
    
    def get_history(self) -> List[Dict]:
        """Get browsing history."""
        return self.history
    
    def clear_history(self):
        """Clear browsing history."""
        self.history = []
    
    def set_cookie(self, name: str, value: str, domain: str = ''):
        """Set a cookie."""
        self.session.cookies.set(name, value, domain=domain)
    
    def get_cookies(self) -> Dict:
        """Get all cookies."""
        return dict(self.session.cookies)


# Convenience functions for quick access
_browser = BrowserTool()

def fetch(url: str, timeout: int = 10) -> dict:
    """Quick fetch URL."""
    return _browser.fetch(url, timeout)

def extract_text(url: str, selector: Optional[str] = None) -> str:
    """Quick text extraction."""
    return _browser.extract_text(url, selector)

def extract_links(url: str, filter_external: bool = False) -> List[Dict[str, str]]:
    """Quick link extraction."""
    return _browser.extract_links(url, filter_external)

def search_google(query: str, num_results: int = 10) -> List[Dict[str, str]]:
    """Quick Google search."""
    return _browser.search_google(query, num_results)

def get_page_metadata(url: str) -> Dict[str, str]:
    """Quick metadata extraction."""
    return _browser.get_page_metadata(url)

def download_file(url: str, save_path: str) -> bool:
    """Quick file download."""
    return _browser.download_file(url, save_path)
