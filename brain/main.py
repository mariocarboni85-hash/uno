
from flask import Flask, request, jsonify
import requests
import logging

# Configura logging dettagliato
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

# Definizione dell'app Flask
app = Flask(__name__)

@app.route("/brain/ping")
def ping():
    logging.info("Ping ricevuto su /brain/ping")
    return {"status": "brain alive"}

@app.route("/brain/route", methods=["POST"])
def route():
    task = request.json
    target = task.get("target","team_a")

    mapping = {
        "software": "http://team_a:8002/build",
        "analysis": "http://team_b:8003/analyze",
        "report":   "http://team_c:8004/report"
    }

    url = mapping.get(target, mapping["software"])
    logging.info(f"Ricevuta richiesta su /brain/route: target={target}, url={url}, payload={task}")
    try:
        res = requests.post(url, json=task, timeout=5)
        logging.info(f"Risposta da {url}: status={res.status_code}, body={res.text}")
        return res.json(), res.status_code
    except requests.exceptions.Timeout:
        logging.error(f"Timeout nella richiesta verso {url}")
        return jsonify({"error": "Timeout nella richiesta verso il servizio esterno."}), 504
    except requests.exceptions.RequestException as e:
        logging.error(f"Errore nella richiesta verso {url}: {e}")
        return jsonify({"error": str(e)}), 502

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8001)