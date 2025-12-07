# Watchdog Agent - Monitoraggio spesa e notifiche
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
import datetime

bp = Blueprint('watchdog_agent', __name__)

# Stato del watchdog
watchdog_state = {
    'active': False,
    'limit': 1000,  # Soglia di spesa
    'blocked': False,
    'notifications': []
}

# Simulazione movimenti/spesa
movements = []

@bp.route('/api/watchdog/activate', methods=['POST'])
@jwt_required()
def activate_watchdog():
    watchdog_state['active'] = True
    return jsonify({'msg': 'Watchdog attivato'}), 200

@bp.route('/api/watchdog/deactivate', methods=['POST'])
@jwt_required()
def deactivate_watchdog():
    watchdog_state['active'] = False
    return jsonify({'msg': 'Watchdog disattivato'}), 200

@bp.route('/api/watchdog/set_limit', methods=['POST'])
@jwt_required()
def set_limit():
    data = request.get_json()
    limit = data.get('limit')
    if limit:
        watchdog_state['limit'] = limit
        return jsonify({'msg': f'Soglia impostata a {limit}'}), 200
    return jsonify({'msg': 'Limite non valido'}), 400

@bp.route('/api/watchdog/add_movement', methods=['POST'])
@jwt_required()
def add_movement():
    data = request.get_json()
    amount = data.get('amount')
    desc = data.get('desc', '')
    if amount:
        movements.append({'amount': amount, 'desc': desc, 'date': datetime.datetime.now().isoformat()})
        check_spending()
        return jsonify({'msg': 'Movimento aggiunto'}), 200
    return jsonify({'msg': 'Importo non valido'}), 400

@bp.route('/api/watchdog/notifications', methods=['GET'])
@jwt_required()
def get_notifications():
    return jsonify(watchdog_state['notifications'])

@bp.route('/api/watchdog/status', methods=['GET'])
@jwt_required()
def get_status():
    return jsonify(watchdog_state)

# Logica di controllo spesa

def check_spending():
    if not watchdog_state['active']:
        return
    total = sum(m['amount'] for m in movements)
    if total > watchdog_state['limit']:
        watchdog_state['blocked'] = True
        msg = f'Soglia superata! Spesa totale: {total}. Blocco attivato.'
        watchdog_state['notifications'].append({'type': 'alert', 'msg': msg, 'date': datetime.datetime.now().isoformat()})
    else:
        watchdog_state['blocked'] = False

# Funzione per invio notifica (mock)
def send_notification(message):
    watchdog_state['notifications'].append({'type': 'info', 'msg': message, 'date': datetime.datetime.now().isoformat()})
