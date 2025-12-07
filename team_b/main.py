from flask import Flask, request, jsonify
app = Flask(__name__)

@app.route("/team_b/ping")
def ping():
    return {"status": "team_b alive"}

@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.json
    return {"status": "ok", "analysis": "Analisi completata"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8003)