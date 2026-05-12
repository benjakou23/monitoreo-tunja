import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import create_app, db
from app.config import Config

app = create_app()

def seed_severities():
    from app.models.alert_severity import AlertSeverity
    severities = [
        {"name": "info",     "level": 1, "color": "#3B8BD4", "description": "Información general del sistema"},
        {"name": "warning",  "level": 2, "color": "#EF9F27", "description": "Advertencia, requiere atención"},
        {"name": "critical", "level": 3, "color": "#E24B4A", "description": "Crítico, requiere acción inmediata"},
        {"name": "emergency","level": 4, "color": "#7F77DD", "description": "Emergencia, servicio caído"},
    ]
    for s in severities:
        if not AlertSeverity.query.filter_by(name=s["name"]).first():
            db.session.add(AlertSeverity(**s))
    db.session.commit()
    print("✅ Severidades de alertas creadas")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        seed_severities()
        print("🚨 Alerts Service corriendo en http://localhost:5015")
    app.run(host="0.0.0.0", port=Config.PORT, debug=True)

