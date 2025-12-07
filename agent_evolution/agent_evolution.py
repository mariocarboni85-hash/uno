import requests
from flask import Flask, request
import schedule
import time
from datetime import datetime
import sqlite3

app = Flask(__name__)

EXTERNAL_AGENTS = [
    "http://external_agent_1:8000",
    "http://external_agent_2:8000"
]

BRAIN_URL = "http://brain:8000/brain/query"

conn = sqlite3.connect("agent_evolution_memory.db", check_same_thread=False)
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS knowledge (id INTEGER PRIMARY KEY, source TEXT, content TEXT)")
conn.commit()

def fetch_and_learn():
    print(f"[{datetime.now()}] 🔄 Apprendimento dai dati degli agenti esterni...")
    for agent_url in EXTERNAL_AGENTS:
        try:
            r = requests.get(f"{agent_url}/data")
            if r.status_code == 200:
                data = r.json()
                # Invia dati al cervello per apprendimento e aggiornamento prompt team
                requests.post(BRAIN_URL, json={"query": f"Apprendi e ottimizza dai dati esterni: {data}"})
                # Salva nella memoria
                c.execute("INSERT INTO knowledge (source, content) VALUES (?, ?)", ("external_agent_evolution", data))
                conn.commit()
        except Exception as e:
            print(f"[Agent Evolution] Errore con {agent_url}: {e}")

@app.route("/alive")
def alive():
    return {"status": "ok"}

@app.route("/learn_and_update", methods=["POST"])
def learn_and_update():
    data = request.json
    if data is None:
        content = ""
    else:
        content = str(data.get("query", ""))
    # Salva nella memoria
    c.execute("INSERT INTO knowledge (source, content) VALUES (?, ?)", ("external_agent_evolution", content))
    conn.commit()
    # Aggiorna prompt dei team in base a dati esterni
    for team in ["teamA", "teamB", "teamC"]:
        try:
            requests.post(f"http://{team}:8000/update_prompt", json={"new_prompt": content})
        except:
            pass
    return {"status": "ok"}

def main():
    schedule.every(5).minutes.do(fetch_and_learn)  # aggiornamento più frequente
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main()
