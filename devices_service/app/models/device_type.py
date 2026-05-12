from app import db
from datetime import datetime

class DeviceType(db.Model):
    __tablename__ = "device_types"

    id          = db.Column(db.Integer, primary_key=True)
    name        = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.String(255), nullable=True)
    created_at  = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at  = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    devices = db.relationship("Device", back_populates="device_type", lazy="dynamic")

    def to_dict(self):
        return {
            "id":          self.id,
            "name":        self.name,
            "description": self.description,
            "created_at":  self.created_at.isoformat() if self.created_at else None,
        }

    def __repr__(self):
        return f"<DeviceType {self.name}>"

