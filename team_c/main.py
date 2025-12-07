from flask import Flask, request, jsonify
app = Flask(__name__)

@app.route("/team_c/ping")
def ping():
    return {"status": "team_c alive"}

@app.route("/report", methods=["POST"])
def report():
    return {"message": "Report generato"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8004)