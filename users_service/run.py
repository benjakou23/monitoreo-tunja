import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import create_app, db
from app.config import Config

app = create_app()

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        print("✅ Tablas users/roles listas")
        print("👤 Users Service corriendo en http://localhost:5011")
    app.run(host="0.0.0.0", port=Config.PORT, debug=True)

