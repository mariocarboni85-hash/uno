from flask import Flask, request

app = Flask(__name__)

@app.route("/sandbox/run", methods=["POST"])
def run():
    code = request.json.get("code","")
    output = {}
    try:
        exec(code, {}, output)
    except Exception as e:
        return {"error": str(e)}
    return {"result": output}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8007)