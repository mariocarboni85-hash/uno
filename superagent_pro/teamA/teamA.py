from flask import Flask, request
import openai

app = Flask(__name__)
openai.api_key = "INSERISCI_API"

@app.route("/generate-code", methods=["POST"])
def generate_code():
    prompt = request.json["prompt"]
    return {"code": f"# Codice generato per: {prompt}"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8100)
