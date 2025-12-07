"""
Test avanzato delle capacità di lettura e scrittura file
"""
from tools.files import FileManager, read_file, write_file, write_json, read_json
import json

print("="*70)
print(" "*15 + "📁 TEST FILE MANAGER AVANZATO")
print("="*70)

fm = FileManager()

# Test directory
test_dir = "C:\\Users\\user\\Desktop\\m\\super_agent\\test_files"

print("\n1️⃣  CREAZIONE DIRECTORY")
print("-"*70)
result = fm.create_directory(test_dir)
print(f"✓ {result}")

# Test 1: Scrittura file di testo
print("\n2️⃣  SCRITTURA FILE TESTO")
print("-"*70)
text_content = """Questo è un file di test.
Contiene multiple righe.
Con vari contenuti."""

result = fm.write_file(f"{test_dir}/test.txt", text_content)
print(f"✓ File creato: {result}")

# Test 2: Lettura file
print("\n3️⃣  LETTURA FILE")
print("-"*70)
content = fm.read_file(f"{test_dir}/test.txt")
print(f"Contenuto letto:\n{content[:100]}...")

# Test 3: Append
print("\n4️⃣  APPEND AL FILE")
print("-"*70)
result = fm.append_file(f"{test_dir}/test.txt", "\nRiga aggiunta con append!")
print(f"✓ {result}")

# Test 4: JSON
print("\n5️⃣  SCRITTURA E LETTURA JSON")
print("-"*70)
data = {
    "nome": "SuperAgent",
    "versione": "1.0",
    "features": ["browser", "files", "shell", "arduino"],
    "config": {
        "timeout": 30,
        "debug": True
    }
}

result = fm.write_json(f"{test_dir}/config.json", data)
print(f"✓ JSON scritto: {result}")

loaded_data = fm.read_json(f"{test_dir}/config.json")
print(f"✓ JSON letto: {json.dumps(loaded_data, indent=2)[:150]}...")

# Test 5: CSV
print("\n6️⃣  SCRITTURA E LETTURA CSV")
print("-"*70)
csv_data = [
    {"nome": "AAPL", "prezzo": 150.25, "variazione": 2.5},
    {"nome": "MSFT", "prezzo": 380.50, "variazione": -1.2},
    {"nome": "GOOGL", "prezzo": 140.75, "variazione": 3.8}
]

result = fm.write_csv(f"{test_dir}/stocks.csv", csv_data)
print(f"✓ CSV scritto: {result}")

loaded_csv = fm.read_csv(f"{test_dir}/stocks.csv")
print(f"✓ CSV letto: {len(loaded_csv)} righe")
for row in loaded_csv:
    print(f"  {row}")

# Test 6: File info
print("\n7️⃣  INFORMAZIONI FILE")
print("-"*70)
info = fm.file_info(f"{test_dir}/config.json")
print(f"Nome: {info.get('name')}")
print(f"Dimensione: {info.get('size')} bytes ({info.get('size_mb')} MB)")
print(f"Tipo MIME: {info.get('mime_type')}")
print(f"Modificato: {info.get('modified')}")

# Test 7: List directory
print("\n8️⃣  ELENCO FILE NELLA DIRECTORY")
print("-"*70)
files = fm.list_dir(test_dir)
print(f"Trovati {len(files)} file:")
for f in files:
    print(f"  [{f['type']}] {f['name']} - {f['size']} bytes")

# Test 8: Search files
print("\n9️⃣  RICERCA FILE")
print("-"*70)
matches = fm.search_files(test_dir, "*.json")
print(f"File JSON trovati: {len(matches)}")
for match in matches:
    print(f"  - {match}")

# Test 9: Read lines
print("\n🔟 LETTURA RIGHE SPECIFICHE")
print("-"*70)
lines = fm.read_lines(f"{test_dir}/test.txt", 0, 2)
print(f"Prime 2 righe:")
for i, line in enumerate(lines, 1):
    print(f"  {i}. {line.strip()}")

# Test 10: Copy file
print("\n1️⃣1️⃣  COPIA FILE")
print("-"*70)
result = fm.copy_file(f"{test_dir}/test.txt", f"{test_dir}/test_copy.txt")
print(f"✓ {result}")

# Test 11: File size
print("\n1️⃣2️⃣  DIMENSIONE FILE")
print("-"*70)
size_bytes = fm.get_file_size(f"{test_dir}/config.json", 'bytes')
size_kb = fm.get_file_size(f"{test_dir}/config.json", 'kb')
print(f"config.json: {size_bytes} bytes = {size_kb} KB")

print("\n" + "="*70)
print("✅ TUTTI I TEST COMPLETATI!")
print("\n📋 FUNZIONALITÀ DISPONIBILI:")
print("  • read_file() / write_file() - Testo e binario")
print("  • read_json() / write_json() - File JSON")
print("  • read_csv() / write_csv() - File CSV")
print("  • append_file() - Aggiungi a file esistente")
print("  • read_lines() / write_lines() - Righe specifiche")
print("  • list_dir() - Elenca directory con dettagli")
print("  • file_info() - Info complete su file")
print("  • copy_file() / move_file() - Copia/sposta file")
print("  • delete_file() - Elimina file")
print("  • create_directory() - Crea cartelle")
print("  • search_files() - Ricerca file per nome/contenuto")
print("  • file_exists() - Verifica esistenza")
print("  • get_file_size() - Dimensione file")
print("="*70)
