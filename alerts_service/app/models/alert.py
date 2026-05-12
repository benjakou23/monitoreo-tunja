from app import db
from datetime import datetime

class Alert(db.Model):
    __tablename__ = "alerts"

    id           = db.Column(db.Integer, primary_key=True)
    title        = db.Column(db.String(200), nullable=False)
    message      = db.Column(db.Text, nullable=False)
    device_id    = db.Column(db.Integer, nullable=True)    # FK lógica → devices_service
    metric_id    = db.Column(db.Integer, nullable=True)    # FK lógica → metrics_service
    severity_id  = db.Column(db.Integer, db.ForeignKey("alert_severities.id"), nullable=False)
    status       = db.Column(
                     db.Enum("activa", "reconocida", "resuelta", name="alert_status"),
                     default="activa", nullable=False
                   )
    acknowledged_by = db.Column(db.Integer, nullable=True)  # FK lógica → users_service
    acknowledged_at = db.Column(db.DateTime, nullable=True)
    resolved_by     = db.Column(db.Integer, nullable=True)
    resolved_at     = db.Column(db.DateTime, nullable=True)
    created_at      = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at      = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    severity = db.relationship("AlertSeverity", back_populates="alerts")

    def to_dict(self):
        return {
            "id":               self.id,
            "title":            self.title,
            "message":          self.message,
            "device_id":        self.device_id,
            "metric_id":        self.metric_id,
            "severity":         self.severity.to_dict() if self.severity else None,
            "status":           self.status,
            "acknowledged_by":  self.acknowledged_by,
            "acknowledged_at":  self.acknowledged_at.isoformat() if self.acknowledged_at else None,
            "resolved_by":      self.resolved_by,
            "resolved_at":      self.resolved_at.isoformat() if self.resolved_at else None,
            "created_at":       self.created_at.isoformat() if self.created_at else None,
            "updated_at":       self.updated_at.isoformat() if self.updated_at else None,
        }

    def __repr__(self):
        return f"<Alert {self.title} - {self.status}>"

