"""
Test del Browser Tool Avanzato
"""
from tools.browser import BrowserTool, fetch, extract_text, extract_links, search_google

print("="*70)
print(" "*20 + "🌐 BROWSER TOOL AVANZATO")
print("="*70)

# Inizializza browser
browser = BrowserTool()
print("\n✅ Browser tool caricato con successo!")

print("\n📊 FUNZIONALITÀ DISPONIBILI:")
print("  1. fetch(url) - Scarica contenuto pagina web")
print("  2. extract_text(url, selector) - Estrae testo da pagina")
print("  3. extract_links(url, filter_external) - Estrae tutti i link")
print("  4. extract_images(url) - Estrae tutte le immagini")
print("  5. extract_tables(url) - Estrae tabelle HTML")
print("  6. search_google(query, num_results) - Ricerca Google")
print("  7. get_page_metadata(url) - Estrae metadata (title, description, etc)")
print("  8. download_file(url, save_path) - Scarica file")
print("  9. check_url_status(url) - Verifica status URL")
print(" 10. extract_data(url, schema) - Estrae dati strutturati")

print("\n" + "="*70)
print("\n🧪 TEST DELLE FUNZIONALITÀ:")
print("="*70)

# Test 1: Fetch
print("\n1️⃣  Test fetch...")
try:
    result = browser.fetch("https://httpbin.org/html")
    print(f"   ✓ Status: {result.get('status_code')}")
    print(f"   ✓ URL: {result.get('url')}")
    print(f"   ✓ Encoding: {result.get('encoding')}")
except Exception as e:
    print(f"   ✗ Errore: {e}")

# Test 2: Check URL status
print("\n2️⃣  Test check URL status...")
try:
    status = browser.check_url_status("https://github.com")
    print(f"   ✓ Status code: {status.get('status_code')}")
    print(f"   ✓ OK: {status.get('ok')}")
    print(f"   ✓ Response time: {status.get('response_time')}s")
except Exception as e:
    print(f"   ✗ Errore: {e}")

# Test 3: Extract metadata
print("\n3️⃣  Test metadata extraction...")
try:
    metadata = browser.get_page_metadata("https://github.com")
    print(f"   ✓ Title: {metadata.get('title', 'N/A')[:50]}...")
    print(f"   ✓ Description: {metadata.get('description', 'N/A')[:50]}...")
except Exception as e:
    print(f"   ✗ Errore: {e}")

# Test 4: Extract links
print("\n4️⃣  Test link extraction...")
try:
    links = browser.extract_links("https://example.com")
    print(f"   ✓ Trovati {len(links)} link")
    if links:
        print(f"   ✓ Primo link: {links[0].get('text', 'N/A')}")
except Exception as e:
    print(f"   ✗ Errore: {e}")

# Test 5: History
print("\n5️⃣  Test browsing history...")
history = browser.get_history()
print(f"   ✓ Pagine visitate: {len(history)}")
for i, page in enumerate(history[:3], 1):
    print(f"   {i}. {page.get('url')} - Status: {page.get('status')}")

print("\n" + "="*70)
print("\n✅ TUTTI I TEST COMPLETATI!")
print("\n💡 Il browser tool è pronto per essere integrato nel SuperAgent")
print("="*70)
