from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS

db      = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object("app.config.Config")

    db.init_app(app)
    migrate.init_app(app, db)
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    from app.models import AlertSeverity, Alert

    from app.routes import alerts_bp, severities_bp
    app.register_blueprint(alerts_bp)
    app.register_blueprint(severities_bp)

    @app.route("/health")
    def health():
        return {"status": "ok", "service": "alerts_service", "port": 5015}, 200

    return app

