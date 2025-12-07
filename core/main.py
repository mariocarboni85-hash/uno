from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route("/core/ping")
def ping():
    return {"status": "core alive"}

@app.route("/core/run", methods=["POST"])
def run():
    task = request.json
    # Inoltra al brain
    res = requests.post("http://brain:8001/brain/route", json=task)
    return res.json(), res.status_code

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)