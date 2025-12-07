from flask import Flask

app = Flask(__name__)

@app.route("/analytics/ping")
def ping():
    return {"analytics": "alive"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9000)