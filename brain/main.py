from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route("/brain/ping")
def ping():
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
    res = requests.post(url, json=task)
    return res.json(), res.status_code

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8001)