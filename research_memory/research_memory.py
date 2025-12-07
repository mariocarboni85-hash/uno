import schedule
import time
import wikipedia
import feedparser
import requests
import sqlite3
from flask import Flask, request

app = Flask(__name__)

BRAIN_URL = "http://brain:8000"

# --- Database memoria ---
MEMORY_DB = "/app/memory/memory.db"  # percorso nel container
conn = sqlite3.connect(MEMORY_DB, check_same_thread=False)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS knowledge (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source TEXT,
                content TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )''')
conn.commit()

def save_to_memory(source, content):
    c.execute("INSERT INTO knowledge (source, content) VALUES (?, ?)", (source, content))
    conn.commit()

def send_to_brain(data):
    try:
        requests.post(f"{BRAIN_URL}/research", json=data)
    except:
        pass

def search_cycle():
    results = {}

    # --- WIKIPEDIA ---
    try:
        page = wikipedia.summary("Artificial Intelligence", sentences=3)
        results["wikipedia"] = page
        save_to_memory("wikipedia", page)
    except:
        results["wikipedia"] = None

    # --- RSS FEED ---
    try:
        rss = feedparser.parse("https://news.google.com/rss?hl=it&gl=IT&ceid=IT:it")
        if rss.entries:
            results["rss"] = rss.entries[0].title
            save_to_memory("rss", rss.entries[0].title)
    except:
        results["rss"] = None

    # --- DATI OPEN-DATA ---
    try:
        r = requests.get("https://jsonplaceholder.typicode.com/posts/1")
        results["opendata"] = r.json()
        save_to_memory("opendata", str(r.json()))
    except:
        results["opendata"] = None

    # --- INVIO AL CERVELLO ---
    send_to_brain(results)

@app.route("/alive")
def alive():
    return {"status": "ok"}

@app.route("/memory", methods=["GET"])
def get_memory():
    c.execute("SELECT * FROM knowledge ORDER BY timestamp DESC LIMIT 50")
    rows = c.fetchall()
    return {"memory": rows}

def consulta_memoria(limit=10):
    try:
        c.execute("SELECT source, content, timestamp FROM knowledge ORDER BY timestamp DESC LIMIT ?", (limit,))
        rows = c.fetchall()
        mem_data = [{"source": r[0], "content": r[1], "timestamp": r[2]} for r in rows]
        return mem_data
    except:
        return []

def main():
    schedule.every(10).minutes.do(search_cycle)
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main()
