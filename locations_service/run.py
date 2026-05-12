import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import create_app, db
from app.config import Config

app = create_app()

def seed_locations():
    from app.models.location import Location
    locations = [
        {"name": "Data Center Principal",   "building": "Edificio A", "floor": "Sótano 1", "room": "DC-01"},
        {"name": "Sala de Servidores",       "building": "Edificio A", "floor": "Sótano 1", "room": "DC-02"},
        {"name": "Urgencias - Enfermería",   "building": "Edificio B", "floor": "Piso 1",   "room": "101"},
        {"name": "UCI Adultos",              "building": "Edificio B", "floor": "Piso 2",   "room": "201"},
        {"name": "Quirófano Central",        "building": "Edificio C", "floor": "Piso 1",   "room": "QX-01"},
        {"name": "Radiología",               "building": "Edificio C", "floor": "Piso 1",   "room": "RAD-01"},
        {"name": "Laboratorio Clínico",      "building": "Edificio D", "floor": "Piso 1",   "room": "LAB-01"},
        {"name": "Admisiones",               "building": "Edificio A", "floor": "Piso 1",   "room": "ADM-01"},
        {"name": "Dirección TI",             "building": "Edificio A", "floor": "Piso 3",   "room": "TI-01"},
        {"name": "Consulta Externa",         "building": "Edificio E", "floor": "Piso 1",   "room": "CE-01"},
    ]
    for loc in locations:
        if not Location.query.filter_by(name=loc["name"]).first():
            db.session.add(Location(**loc))
    db.session.commit()
    print("✅ Ubicaciones del hospital creadas")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        seed_locations()
        print("📍 Locations Service corriendo en http://localhost:5013")
    app.run(host="0.0.0.0", port=Config.PORT, debug=True)

