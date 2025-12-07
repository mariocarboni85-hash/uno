import requests

BASE_URL = "http://localhost:5000/api"

# Testa la route /scan_apps (GET)
try:
    r = requests.get(f"{BASE_URL}/scan_apps")
    print("/scan_apps:", r.status_code, r.json())
except Exception as e:
    print("Errore /scan_apps:", e)

# Testa la route /list_processes (GET)
try:
    r = requests.get(f"{BASE_URL}/list_processes")
    print("/list_processes:", r.status_code, r.json())
except Exception as e:
    print("Errore /list_processes:", e)
