from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS

db      = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object("app.config.Config")

    # Extensiones
    db.init_app(app)
    migrate.init_app(app, db)
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # Registrar modelos (para migraciones)
    from app.models import User, Role

    # Registrar blueprints
    from app.routes import auth_bp
    app.register_blueprint(auth_bp)

    # Health check
    @app.route("/health")
    def health():
        return {"status": "ok", "service": "auth_service", "port": 5001}, 200

    return app