from flask import Flask, request

app = Flask(__name__)

API_KEY = "SUPER_KEY_123"

@app.route("/auth", methods=["POST"])
def auth():
    req = request.json
    return {"authorized": req.get("api_key") == API_KEY}

@app.route('/')
def home():
    return 'Security attivo!'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8008)