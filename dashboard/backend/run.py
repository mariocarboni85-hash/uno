from flask import Flask
from flask_jwt_extended import JWTManager
from system_agent_api import bp as system_bp
from watchdog_agent import bp as watchdog_bp

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "super-secret-key"  # Sostituisci con una chiave sicura
jwt = JWTManager(app)
app.register_blueprint(system_bp)
app.register_blueprint(watchdog_bp)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
