import requests
import schedule
import time
from datetime import datetime

CONTAINERS = {
    "brain": "http://brain:8000/brain/query",
    "teamA": "http://teamA:8100/generate-code",
    "teamB": "http://teamB:8003/analyze",
    "teamC": "http://teamC:8004/report"
}

def evaluate_performance():
    print(f"[{datetime.now()}] 🚀 Valutazione performance team in corso...")

    report = {}
    for name, url in CONTAINERS.items():
        try:
            if name == "brain":
                r = requests.post(url, json={"query":"test auto ottimizzazione"}).json()
                report[name] = "ok" if r else "error"
            else:
                r = requests.post(url, json={"prompt":"test"}).json()
                report[name] = "ok" if r else "error"
        except:
            report[name] = "offline"

    print("[Optimizer] Stato team:", report)

    # Logica semplice di auto-ottimizzazione
    for team, status in report.items():
        if status != "ok":
            print(f"[Optimizer] ⚠️ Team {team} non performante, invio alert al cervello...")
            requests.post("http://brain:8000/brain/query", json={"query":f"Team {team} non performante"})


def main():
    schedule.every(10).minutes.do(evaluate_performance)
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main()
