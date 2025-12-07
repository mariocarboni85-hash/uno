import requests
from flask import Flask, request
import schedule
import time
from datetime import datetime
import sqlite3

app = Flask(__name__)

# Lista agenti esterni (es. IP o hostname)
EXTERNAL_AGENTS = [
    "http://external_agent_1:8000",
    "http://external_agent_2:8000"
]

BRAIN_URL = "http://brain:8000/brain/query"

conn = sqlite3.connect("agent_hub_memory.db", check_same_thread=False)
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS knowledge (id INTEGER PRIMARY KEY, source TEXT, content TEXT)")
conn.commit()

def fetch_external_data():
    print(f"[{datetime.now()}] 🔄 Fetching data from external agents...")
    for agent_url in EXTERNAL_AGENTS:
        try:
            r = requests.get(f"{agent_url}/data")
            if r.status_code == 200:
                data = r.json()
                # Invia i dati al cervello per apprendimento
                requests.post(BRAIN_URL, json={"query": f"Apprendi dai dati esterni: {data}"})
                # Salva nella memoria
                c.execute("INSERT INTO knowledge (source, content) VALUES (?, ?)", ("external_agent", str(data)))
                conn.commit()
        except Exception as e:
            print(f"[Agent Hub] Errore con {agent_url}: {e}")

@app.route("/alive")
def alive():
    return {"status": "ok"}

@app.route("/external_data", methods=["POST"])
def external_data():
    data = request.json
    # Salva nella memoria
    c.execute("INSERT INTO knowledge (source, content) VALUES (?, ?)", ("external_agent", str(data)))
    conn.commit()
    return {"status": "ok"}

def main():
    # Ogni 10 minuti raccoglie dati dagli agenti esterni
    schedule.every(10).minutes.do(fetch_external_data)
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main()
