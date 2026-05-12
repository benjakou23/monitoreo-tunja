import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import create_app, db
from app.config import Config

app = create_app()

def seed_metric_types():
    from app.models.metric_type import MetricType
    types = [
        {"name": "CPU Usage",       "unit": "%",   "description": "Uso del procesador",          "min_value": 0,  "max_value": 100},
        {"name": "RAM Usage",       "unit": "%",   "description": "Uso de memoria RAM",           "min_value": 0,  "max_value": 100},
        {"name": "Disk Usage",      "unit": "%",   "description": "Uso del disco",                "min_value": 0,  "max_value": 100},
        {"name": "Network In",      "unit": "Mbps","description": "Tráfico de red entrante",      "min_value": 0,  "max_value": 1000},
        {"name": "Network Out",     "unit": "Mbps","description": "Tráfico de red saliente",      "min_value": 0,  "max_value": 1000},
        {"name": "Response Time",   "unit": "ms",  "description": "Tiempo de respuesta",          "min_value": 0,  "max_value": 5000},
        {"name": "Temperature",     "unit": "°C",  "description": "Temperatura del dispositivo",  "min_value": 0,  "max_value": 90},
        {"name": "Packet Loss",     "unit": "%",   "description": "Pérdida de paquetes de red",   "min_value": 0,  "max_value": 100},
        {"name": "Uptime",          "unit": "hrs", "description": "Tiempo en línea",              "min_value": 0,  "max_value": None},
        {"name": "Disk Read Speed", "unit": "MB/s","description": "Velocidad de lectura en disco","min_value": 0,  "max_value": 500},
    ]
    for t in types:
        if not MetricType.query.filter_by(name=t["name"]).first():
            db.session.add(MetricType(**t))
    db.session.commit()
    print("✅ Tipos de métricas creados")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        seed_metric_types()
        print("📊 Metrics Service corriendo en http://localhost:5014")
    app.run(host="0.0.0.0", port=Config.PORT, debug=True)

