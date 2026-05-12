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

    from app.models import MetricType, Metric

    from app.routes import metrics_bp, metric_types_bp
    app.register_blueprint(metrics_bp)
    app.register_blueprint(metric_types_bp)

    @app.route("/health")
    def health():
        return {"status": "ok", "service": "metrics_service", "port": 5014}, 200

    return app

