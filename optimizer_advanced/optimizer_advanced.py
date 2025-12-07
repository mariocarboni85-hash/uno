import requests
import schedule
import time
from datetime import datetime
import random

# Container principali
CONTAINERS = {
    "brain": "http://brain:8000/brain/query",
    "teamA": "http://teamA:8100/generate-code",
    "teamB": "http://teamB:8003/analyze",
    "teamC": "http://teamC:8004/report"
}

# Storico performance
performance_history = {team: [] for team in CONTAINERS.keys()}

def measure_task_performance(team, url):
    try:
        start = time.time()
        if team == "brain":
            r = requests.post(url, json={"query":"test auto ottimizzazione"}).json()
        else:
            r = requests.post(url, json={"prompt":"test"}).json()
        end = time.time()
        duration = end - start
        success = r is not None
    except:
        duration = None
        success = False
    return duration, success

def evaluate_and_optimize():
    print(f"[{datetime.now()}] 🚀 Inizio valutazione avanzata team...")
    report = {}

    # --- Misura performance ---
    for team, url in CONTAINERS.items():
        duration, success = measure_task_performance(team, url)
        performance_history[team].append({"duration": duration, "success": success})
        report[team] = {"duration": duration, "success": success}

    print("[Optimizer Avanzato] Stato team:", report)

    # --- Analisi e riassegnazione ---
    for team, data in report.items():
        if not data["success"] or (data["duration"] and data["duration"] > 10):
            print(f"[Optimizer] ⚠️ Team {team} lento o fallito, riassegno task...")
            # Riassegna task al team più veloce
            faster_team = min(performance_history, key=lambda t: (performance_history[t][-1]["duration"] or float('inf')))
            print(f"[Optimizer] Task originario {team} riassegnato a {faster_team}")
            # Invio alert al cervello
            requests.post("http://brain:8000/brain/query", json={"query":f"Riassegna task da {team} a {faster_team}"})

    # --- Aggiornamento memoria cervello ---
    try:
        requests.post("http://brain:8000/brain/query", json={"query":"Aggiorna memoria sulle performance dei team"})
    except:
        pass

def main():
    schedule.every(10).minutes.do(evaluate_and_optimize)
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main()
