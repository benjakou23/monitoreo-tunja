from app import db
from datetime import datetime
import bcrypt

class User(db.Model):
    __tablename__ = "users"

    id         = db.Column(db.Integer, primary_key=True)
    username   = db.Column(db.String(80), unique=True, nullable=False)
    email      = db.Column(db.String(120), unique=True, nullable=False)
    password   = db.Column(db.String(255), nullable=False)
    full_name  = db.Column(db.String(150), nullable=True)
    is_active  = db.Column(db.Boolean, default=True, nullable=False)
    role_id    = db.Column(db.Integer, db.ForeignKey("roles.id"), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    role = db.relationship("Role", back_populates="users")

    def set_password(self, plain_password: str):
        hashed = bcrypt.hashpw(plain_password.encode("utf-8"), bcrypt.gensalt())
        self.password = hashed.decode("utf-8")

    def check_password(self, plain_password: str) -> bool:
        return bcrypt.checkpw(
            plain_password.encode("utf-8"),
            self.password.encode("utf-8")
        )

    def to_dict(self):
        return {
            "id":        self.id,
            "username":  self.username,
            "email":     self.email,
            "full_name": self.full_name,
            "is_active": self.is_active,
            "role":      self.role.to_dict() if self.role else None,
            "created_at":self.created_at.isoformat() if self.created_at else None,
        }

    def __repr__(self):
        return f"<User {self.username}>"