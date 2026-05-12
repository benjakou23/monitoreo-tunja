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

    from app.models import User, Role

    from app.routes import users_bp, roles_bp
    app.register_blueprint(users_bp)
    app.register_blueprint(roles_bp)

    @app.route("/health")
    def health():
        return {"status": "ok", "service": "users_service", "port": 5011}, 200

    return app

