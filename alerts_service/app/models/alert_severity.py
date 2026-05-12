from app import db
from datetime import datetime

class AlertSeverity(db.Model):
    __tablename__ = "alert_severities"

    id          = db.Column(db.Integer, primary_key=True)
    name        = db.Column(db.String(50), unique=True, nullable=False)
    level       = db.Column(db.Integer, nullable=False)   # 1=info, 2=warning, 3=critical
    color       = db.Column(db.String(20), nullable=True) # para el frontend
    description = db.Column(db.String(255), nullable=True)
    created_at  = db.Column(db.DateTime, default=datetime.utcnow)

    alerts = db.relationship("Alert", back_populates="severity", lazy="dynamic")

    def to_dict(self):
        return {
            "id":          self.id,
            "name":        self.name,
            "level":       self.level,
            "color":       self.color,
            "description": self.description,
        }

    def __repr__(self):
        return f"<AlertSeverity {self.name}>"

