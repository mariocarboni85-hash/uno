"""
Demo pratico del Browser Tool Avanzato
Test con siti reali
"""
from tools.browser import BrowserTool
import json

print("="*70)
print(" "*20 + "🧪 DEMO BROWSER TOOL")
print("="*70)

browser = BrowserTool()

# Test 1: Ricerca Google
print("\n1️⃣  RICERCA GOOGLE: 'Python web scraping'")
print("-"*70)
results = browser.search_google("Python web scraping", num_results=5)
for i, result in enumerate(results[:3], 1):
    print(f"\n{i}. {result['title']}")
    print(f"   URL: {result['link']}")
    print(f"   Snippet: {result['snippet'][:100]}...")

# Test 2: Estrazione testo da Wikipedia
print("\n\n2️⃣  ESTRAZIONE TESTO: Wikipedia")
print("-"*70)
text = browser.extract_text("https://en.wikipedia.org/wiki/Python_(programming_language)")
print(f"Estratto primi 500 caratteri:\n{text[:500]}...")

# Test 3: Metadata di un sito
print("\n\n3️⃣  METADATA: Python.org")
print("-"*70)
metadata = browser.get_page_metadata("https://www.python.org")
print(f"Title: {metadata.get('title')}")
print(f"Description: {metadata.get('description', 'N/A')}")

# Test 4: Estrazione link
print("\n\n4️⃣  ESTRAZIONE LINK: Example.com")
print("-"*70)
links = browser.extract_links("https://example.com")
print(f"Totale link trovati: {len(links)}")
for link in links[:5]:
    print(f"  - {link['text']}: {link['href']}")

# Test 5: Check multipli URL
print("\n\n5️⃣  VERIFICA STATUS MULTIPLI URL")
print("-"*70)
urls = [
    "https://github.com",
    "https://stackoverflow.com",
    "https://www.python.org",
    "https://nonexistent-site-12345.com"
]

for url in urls:
    status = browser.check_url_status(url)
    if status.get('ok'):
        print(f"✅ {url} - {status['status_code']} ({status['response_time']}s)")
    else:
        print(f"❌ {url} - {status.get('error', 'Errore')}")

# Test 6: Estrazione immagini
print("\n\n6️⃣  ESTRAZIONE IMMAGINI: Example.com")
print("-"*70)
images = browser.extract_images("https://example.com")
print(f"Totale immagini trovate: {len(images)}")
for img in images[:3]:
    print(f"  - {img['alt'] or 'No alt'}: {img['src'][:60]}...")

# Test 7: History
print("\n\n7️⃣  CRONOLOGIA NAVIGAZIONE")
print("-"*70)
history = browser.get_history()
print(f"Pagine visitate in questa sessione: {len(history)}")
for i, page in enumerate(history[-5:], 1):
    print(f"  {i}. [{page['status']}] {page['url']}")

print("\n" + "="*70)
print("✅ DEMO COMPLETATA!")
print("="*70)
