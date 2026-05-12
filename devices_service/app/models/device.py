from app import db
from datetime import datetime

class Device(db.Model):
    __tablename__ = "devices"

    id             = db.Column(db.Integer, primary_key=True)
    name           = db.Column(db.String(150), nullable=False)
    ip_address     = db.Column(db.String(45), unique=True, nullable=True)
    mac_address    = db.Column(db.String(17), unique=True, nullable=True)
    serial_number  = db.Column(db.String(100), unique=True, nullable=True)
    brand          = db.Column(db.String(100), nullable=True)
    model          = db.Column(db.String(100), nullable=True)
    status         = db.Column(
                        db.Enum("activo", "inactivo", "mantenimiento", "falla",
                                name="device_status"),
                        default="activo", nullable=False
                     )
    device_type_id = db.Column(db.Integer, db.ForeignKey("device_types.id"), nullable=True)
    location_id    = db.Column(db.Integer, nullable=True)   # FK lógica al locations_service
    description    = db.Column(db.Text, nullable=True)
    created_at     = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at     = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    device_type = db.relationship("DeviceType", back_populates="devices")

    def to_dict(self):
        return {
            "id":            self.id,
            "name":          self.name,
            "ip_address":    self.ip_address,
            "mac_address":   self.mac_address,
            "serial_number": self.serial_number,
            "brand":         self.brand,
            "model":         self.model,
            "status":        self.status,
            "device_type":   self.device_type.to_dict() if self.device_type else None,
            "location_id":   self.location_id,
            "description":   self.description,
            "created_at":    self.created_at.isoformat() if self.created_at else None,
            "updated_at":    self.updated_at.isoformat() if self.updated_at else None,
        }

    def __repr__(self):
        return f"<Device {self.name} - {self.ip_address}>"

