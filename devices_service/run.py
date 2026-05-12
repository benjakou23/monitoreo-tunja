import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import create_app, db
from app.config import Config

app = create_app()

def seed_device_types():
    from app.models.device_type import DeviceType
    types = [
        {"name": "Servidor",          "description": "Servidores físicos y virtuales"},
        {"name": "Switch",            "description": "Switches de red"},
        {"name": "Router",            "description": "Routers y gateways"},
        {"name": "Access Point",      "description": "Puntos de acceso WiFi"},
        {"name": "Equipo Médico",     "description": "Equipos médicos conectados a red"},
        {"name": "Workstation",       "description": "Equipos de escritorio"},
        {"name": "Impresora",         "description": "Impresoras de red"},
        {"name": "UPS",               "description": "Sistemas de alimentación ininterrumpida"},
        {"name": "Firewall",          "description": "Dispositivos de seguridad perimetral"},
        {"name": "Cámara IP",         "description": "Cámaras de vigilancia IP"},
    ]
    for t in types:
        if not DeviceType.query.filter_by(name=t["name"]).first():
            db.session.add(DeviceType(**t))
    db.session.commit()
    print("✅ Tipos de dispositivo creados")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        seed_device_types()
        print("🖥️  Devices Service corriendo en http://localhost:5012")
    app.run(host="0.0.0.0", port=Config.PORT, debug=True)

