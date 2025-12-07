"""
Asynchronous Web Scraper

Generated: 2025-11-26 09:00:17
"""

import asyncio
import aiohttp
from bs4 import BeautifulSoup
from typing import List, Dict
import json

async def fetch_page(session: aiohttp.ClientSession, url: str) -> str:
    """
    Fetch page content.
    
    Args:
        session (aiohttp.ClientSession): 
        url (str): 
    
    Returns:
        str
    """
    async with session.get(url) as response:
        return await response.text()

def parse_page(html: str, url: str) -> Dict:
    """
    Parse HTML and extract data.
    
    Args:
        html (str): 
        url (str): 
    
    Returns:
        Dict
    """
    soup = BeautifulSoup(html, 'html.parser')

    # Extract title
    title = soup.find('title')
    title_text = title.text if title else 'No title'

    # Extract links
    links = [a.get('href') for a in soup.find_all('a', href=True)]

    # Extract headings
    headings = [h.text for h in soup.find_all(['h1', 'h2', 'h3'])]

    return {
        'url': url,
        'title': title_text,
        'links_count': len(links),
        'links': links[:10],  # First 10 links
        'headings': headings
    }

async def scrape_urls(urls: List[str]) -> List[Dict]:
    """
    Scrape multiple URLs concurrently.
    
    Args:
        urls (List[str]): 
    
    Returns:
        List[Dict]
    """
    async with aiohttp.ClientSession() as session:
        tasks = []
        for url in urls:
            task = fetch_page(session, url)
            tasks.append(task)
        
        # Fetch all pages concurrently
        pages = await asyncio.gather(*tasks)
        
        # Parse all pages
        results = []
        for url, html in zip(urls, pages):
            data = parse_page(html, url)
            results.append(data)
        
        return results



if __name__ == '__main__':

    # URLs to scrape
    urls = [
        'https://example.com',
        'https://python.org',
        'https://github.com'
    ]

    # Run async scraper
    results = asyncio.run(scrape_urls(urls))

    # Save results
    with open('scraped_data.json', 'w') as f:
        json.dump(results, f, indent=2)

    print(f'Scraped {len(results)} pages')
    for result in results:
        print(f"- {result['title']}: {result['links_count']} links")