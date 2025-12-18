from flask import Flask, jsonify, request, render_template_string


app = Flask(__name__)

HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>SuperAgent Dashboard</title>
    <style>
        body { font-family: Arial, sans-serif; background: #f5f5f5; }
        .container { max-width: 600px; margin: 40px auto; background: #fff; border-radius: 10px; box-shadow: 0 2px 10px #0001; padding: 30px; }
        h1 { color: #333; }
        label { font-weight: bold; }
        input, select, button { font-size: 16px; margin: 5px 0; padding: 8px; border-radius: 5px; border: 1px solid #ccc; }
        button { background: #4CAF50; color: #fff; border: none; cursor: pointer; }
        button:hover { background: #388e3c; }
        .result { background: #e3f2fd; margin-top: 20px; padding: 10px; border-radius: 5px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>SuperAgent Dashboard</h1>
        <form method="post">
            <label>Agente:</label>
            <select name="agent">
                <option value="system">System</option>
                <option value="notifier">Notifier</option>
            </select><br>
            <label>Task (JSON):</label><br>
            <input type="text" name="task" value='{"action": "check"}' style="width:100%"><br>
            <button type="submit">Invia Task</button>
        </form>
        {% if result %}
        <div class="result">
            <b>Risposta agente:</b><br>{{ result }}
        </div>
        {% endif %}
    </div>
</body>
</html>
'''




# --- REGISTRAZIONE ROUTE SEMPRE ATTIVA ---
from agent_manager import AgentManager
manager = AgentManager()

@app.route("/api/run", methods=["POST"])
def run_task():
    data = request.get_json(silent=True)
    if not data or "agent" not in data or "task" not in data:
        return jsonify({"error": "Dati POST mancanti o malformati. Richiesto: agent, task."}), 400
    result = manager.run_task(data["agent"], data["task"])
    return jsonify(result)

@app.route("/api/context", methods=["GET"])
def get_context():
    return jsonify(manager.get_context_memory())

@app.route("/api/plugins", methods=["POST"])
def add_plugin():
    data = request.get_json(silent=True)
    if not data or "plugin" not in data:
        return jsonify({"error": "Dati POST mancanti o malformati. Richiesto: plugin."}), 400
    manager.add_plugin(data["plugin"])
    return jsonify({"status": "plugin aggiunto"})

@app.route("/", methods=["GET", "POST"])
def home():
    result = None
    if request.method == "POST":
        agent = request.form.get("agent", "system")
        import json
        try:
            task = json.loads(request.form.get("task", "{}"))
        except Exception as e:
            task = {}
        result = manager.run_task(agent, task)
    return render_template_string(HTML, result=result)




# Funzione per avviare il dashboard da altri moduli
def run_dashboard(host="0.0.0.0", port=5000, debug=True):
    app.run(host=host, port=port, debug=debug)

# Permetti esecuzione standalone
if __name__ == "__main__":
    run_dashboard()

