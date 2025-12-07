import requests
import time

API_URL = "http://127.0.0.1:8000"

def print_dashboard():
    try:
        r = requests.get(f"{API_URL}/agents")
        agents = r.json().get("agents", [])
        print("\n--- DASHBOARD AGENTI ---")
        for a in agents:
            print(f"[{a['id']}] {a['name']} | Stato: {a['status']} | Ultimo task: {a['last_task']} | Risultato: {a['last_result']} | Creato: {a['created_at']}")
        print("------------------------\n")
    except Exception as e:
        print(f"Errore dashboard: {e}")

if __name__ == "__main__":
    while True:
        print_dashboard()
        time.sleep(5)
