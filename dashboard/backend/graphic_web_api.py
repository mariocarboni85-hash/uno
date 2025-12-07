from flask import Blueprint, request, jsonify
from core.brain import crea_progetto_grafico_web
from flask_jwt_extended import jwt_required

bp = Blueprint('graphic_web', __name__)

@bp.route('/api/graphic_web_project', methods=['POST'])
@jwt_required()
def create_graphic_web_project():
    data = request.get_json()
    nome = data.get('nome', 'Progetto Creativo')
    descrizione = data.get('descrizione', 'Progetto grafico e web completo')
    tipo = data.get('tipo', 'webapp')
    progetto = crea_progetto_grafico_web(nome, descrizione, tipo)
    return jsonify(progetto)
