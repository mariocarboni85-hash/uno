from flask import Flask, request
import requests

app = Flask(__name__)

@app.route("/mobile/ping")
def ping():
    return {"mobile_api": "alive"}

@app.route("/mobile/task", methods=["POST"])
def forward():
    task = request.json
    r = requests.post("http://gateway:8000/task", json=task)
    return r.json()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8500)