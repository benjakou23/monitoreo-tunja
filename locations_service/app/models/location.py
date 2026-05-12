from app import db
from datetime import datetime

class Location(db.Model):
    __tablename__ = "locations"

    id          = db.Column(db.Integer, primary_key=True)
    name        = db.Column(db.String(150), nullable=False)
    building    = db.Column(db.String(100), nullable=True)
    floor       = db.Column(db.String(50),  nullable=True)
    room        = db.Column(db.String(100), nullable=True)
    description = db.Column(db.Text, nullable=True)
    is_active   = db.Column(db.Boolean, default=True, nullable=False)
    created_at  = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at  = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            "id":          self.id,
            "name":        self.name,
            "building":    self.building,
            "floor":       self.floor,
            "room":        self.room,
            "description": self.description,
            "is_active":   self.is_active,
            "created_at":  self.created_at.isoformat() if self.created_at else None,
            "updated_at":  self.updated_at.isoformat() if self.updated_at else None,
        }

    def __repr__(self):
        return f"<Location {self.name} - {self.building}>"

