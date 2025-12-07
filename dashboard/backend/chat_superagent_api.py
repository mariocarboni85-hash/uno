from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from core.brain import chat_superagent

bp = Blueprint('chat_superagent', __name__)

@bp.route('/api/chat_superagent', methods=['POST'])
@jwt_required()
def chat():
    data = request.get_json()
    message = data.get('message', '')
    response = chat_superagent("User", message)
    return jsonify({'response': response})
