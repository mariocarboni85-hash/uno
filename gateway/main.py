from flask import Flask, request
import requests

app = Flask(__name__)

@app.route("/")
def home():
    return {"superagent": "gateway active"}

@app.route("/task", methods=["POST"])
def task():
    task = request.json
    res = requests.post("http://core:8000/core/run", json=task)
    return res.json()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)