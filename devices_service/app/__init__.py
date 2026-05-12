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

    from app.models import DeviceType, Device

    from app.routes import devices_bp, device_types_bp
    app.register_blueprint(devices_bp)
    app.register_blueprint(device_types_bp)

    @app.route("/health")
    def health():
        return {"status": "ok", "service": "devices_service", "port": 5012}, 200

    return app

