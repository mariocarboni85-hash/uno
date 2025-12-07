from flask import Flask, request
import schedule
import requests
import threading

app = Flask(__name__)

@app.route("/optimize", methods=["POST"])
def optimize():
    data = request.json or {}
    # Logica di ottimizzazione simulata
    result = {"status": "ok", "input": data, "optimized": True}
    return result

def run_scheduler():
    def job():
        print("Ottimizzazione periodica eseguita.")
    schedule.every(10).minutes.do(job)
    while True:
        schedule.run_pending()

if __name__ == "__main__":
    threading.Thread(target=run_scheduler, daemon=True).start()
    app.run(host="0.0.0.0", port=8012)
