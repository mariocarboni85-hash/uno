from flask import Flask, request, jsonify, g
from sqlalchemy import create_engine, Column, Integer, String, Text, MetaData, Table
from utils.jwt_utils import require_jwt
import os
app = Flask(__name__)
DB_PATH = os.environ.get('DB_PATH', 'memory.db')
engine = create_engine(f'sqlite:///{DB_PATH}', connect_args={"check_same_thread": False})
metadata = MetaData()
mem = Table('memory', metadata,
            Column('id', Integer, primary_key=True),
            Column('key', String, nullable=False),
            Column('value', Text, nullable=False))
metadata.create_all(engine)

@app.route('/save', methods=['POST'])
@require_jwt
def save():
    data = request.json or {}
    key = data.get('key')
    value = data.get('value')
    if not key or value is None:
        return jsonify({'error': 'key/value required'}), 400
    ins = mem.insert().values(key=key, value=value)
    conn = engine.connect()
    conn.execute(ins)
    return jsonify({'status': 'saved'})

@app.route('/get/<key>', methods=['GET'])
@require_jwt
def get_key(key):
    conn = engine.connect()
    sel = mem.select().where(mem.c.key == key)
    res = conn.execute(sel).fetchall()
    return jsonify([dict(r) for r in res])

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5003))
    app.run(host='0.0.0.0', port=port)
