import sys
import importlib
import requests

# Moduli da testare
modules = [
    "flask",
    "flask_jwt_extended",
    "psutil",
    "requests",
    "system_agent_api",
    "watchdog_agent"
]

print("--- TEST ALLINEAMENTO ECOSISTEMA SUPER AGENT ---")

# Test import moduli
for mod in modules:
    try:
        importlib.import_module(mod)
        print(f"[IMPORT OK] {mod}")
    except Exception as e:
        print(f"[IMPORT ERROR] {mod}: {e}")

# Test API server
try:
    r = requests.get("http://localhost:5000/api/scan_apps")
    print(f"/api/scan_apps: {r.status_code} {r.text}")
except Exception as e:
    print(f"[API ERROR] /api/scan_apps: {e}")

try:
    r = requests.get("http://localhost:5000/api/list_processes")
    print(f"/api/list_processes: {r.status_code} {r.text}")
except Exception as e:
    print(f"[API ERROR] /api/list_processes: {e}")

print("--- FINE TEST ---")
