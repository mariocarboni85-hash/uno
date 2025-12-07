from flask import Flask, request, jsonify
import json
import requests
from core.super_agent_advanced import schedule_task, get_task_status
from utils.notifications import notify_desktop, notify_email, notify_webhook

app = Flask(__name__)
API_KEY = "MASTER_SLAVE_KEY"

@app.route('/task/add', methods=['POST'])
def add_task():
    token = request.headers.get('Authorization')
    if token != f"Bearer {API_KEY}":
        return jsonify({"error": "Unauthorized"}), 401
    task = request.json
    schedule_task(task)
    return jsonify({"status": "Task aggiunto"}), 200

@app.route('/task/status', methods=['GET'])
def task_status():
    token = request.headers.get('Authorization')
    if token != f"Bearer {API_KEY}":
        return jsonify({"error": "Unauthorized"}), 401
    return jsonify(get_task_status()), 200

@app.route('/agent/update', methods=['POST'])
def agent_update():
    token = request.headers.get('Authorization')
    if token != f"Bearer {API_KEY}":
        return jsonify({"error": "Unauthorized"}), 401
    # Logica per aggiornare agenti o modelli da remoto
    return jsonify({"status": "Agenti aggiornati"}), 200

@app.route('/notification/send', methods=['POST'])
def remote_notification():
    token = request.headers.get('Authorization')
    if token != f"Bearer {API_KEY}":
        return jsonify({"error": "Unauthorized"}), 401
    data = request.json
    notify_desktop(data.get('title', 'Notifica remota'), data.get('message', ''))
    notify_email(data.get('title', 'Notifica remota'), data.get('message', ''), data.get('email', 'utente@example.com'))
    notify_webhook(data.get('webhook_url', ''), data.get('message', ''))
    return jsonify({"status": "Notifica inviata"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5500)
