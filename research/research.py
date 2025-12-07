import schedule
import time
import wikipedia
import feedparser
import requests
from flask import Flask

app = Flask(__name__)

BRAIN_URL = "http://brain:8000"

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
    except:
        results["wikipedia"] = None

    # --- RSS FEED ---
    try:
        rss = feedparser.parse("https://news.google.com/rss?hl=it&gl=IT&ceid=IT:it")
        if rss.entries:
            results["rss"] = rss.entries[0].title
    except:
        results["rss"] = None

    # --- DATI OPEN-DATA ---
    try:
        r = requests.get("https://jsonplaceholder.typicode.com/posts/1")
        results["opendata"] = r.json()
    except:
        results["opendata"] = None

    # --- INVIO AL CERVELLO ---
    send_to_brain(results)

@app.route("/alive")
def alive():
    return {"status": "ok"}

def main():
    schedule.every(10).minutes.do(search_cycle)
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main()
