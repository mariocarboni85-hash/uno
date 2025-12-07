from flask import Flask, request, jsonify
app = Flask(__name__)

@app.route("/team_a/ping")
def ping():
    return {"status": "team_a alive"}

@app.route("/build", methods=["POST"])
def build():
    task = request.json
    return {
        "result": "Software generato correttamente",
        "task": task
    }

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8002)