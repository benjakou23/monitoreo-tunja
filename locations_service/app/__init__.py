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

    from app.models import Location

    from app.routes import locations_bp
    app.register_blueprint(locations_bp)

    @app.route("/health")
    def health():
        return {"status": "ok", "service": "locations_service", "port": 5013}, 200

    return app

