import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
import importlib
import requests

modules = [
    "system_agent_api",
    "watchdog_agent"
]

print("--- TEST IMPORT MODULI BACKEND ---")
for mod in modules:
    try:
        importlib.import_module(mod)
        print(f"[IMPORT OK] {mod}")
    except Exception as e:
        print(f"[IMPORT ERROR] {mod}: {e}")
print("--- FINE TEST ---")
