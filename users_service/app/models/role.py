from app import db
from datetime import datetime

class Role(db.Model):
    __tablename__ = "roles"

    id          = db.Column(db.Integer, primary_key=True)
    name        = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.String(200), nullable=True)
    created_at  = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at  = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    users = db.relationship("User", back_populates="role", lazy="dynamic")

    def to_dict(self):
        return {
            "id":          self.id,
            "name":        self.name,
            "description": self.description,
            "created_at":  self.created_at.isoformat() if self.created_at else None,
        }

    def __repr__(self):
        return f"<Role {self.name}>"