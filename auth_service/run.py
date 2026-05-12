import sys
import os

# Para que Python encuentre el módulo shared desde cualquier servicio
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import create_app, db
from app.config import Config

app = create_app()

def seed_roles():
    """Crea los roles base si no existen."""
    from app.models.role import Role
    roles = [
        {"name": "admin",     "description": "Administrador del sistema"},
        {"name": "tecnico",   "description": "Técnico de infraestructura TI"},
        {"name": "operador",  "description": "Operador de monitoreo"},
        {"name": "viewer",    "description": "Solo lectura"},
    ]
    for r in roles:
        if not Role.query.filter_by(name=r["name"]).first():
            db.session.add(Role(**r))
    db.session.commit()
    print("✅ Roles base creados")

def seed_admin():
    """Crea el usuario admin si no existe."""
    from app.models.user import User
    from app.models.role import Role
    if not User.query.filter_by(username="admin").first():
        admin_role = Role.query.filter_by(name="admin").first()
        admin = User(
            username  = "admin",
            email     = "admin@hospital.gov.co",
            full_name = "Administrador del Sistema",
            role_id   = admin_role.id if admin_role else None,
            is_active = True,
        )
        admin.set_password("Admin123!")
        db.session.add(admin)
        db.session.commit()
        print("✅ Usuario admin creado  →  admin / Admin123!")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        seed_roles()
        seed_admin()
        print("🏥 Auth Service corriendo en http://localhost:5010")
    app.run(host="0.0.0.0", port=Config.PORT, debug=True)

