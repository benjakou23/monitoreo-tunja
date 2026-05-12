from app import db
from datetime import datetime

class Metric(db.Model):
    __tablename__ = "metrics"

    id             = db.Column(db.Integer, primary_key=True)
    device_id      = db.Column(db.Integer, nullable=False)   # FK lógica → devices_service
    metric_type_id = db.Column(db.Integer, db.ForeignKey("metric_types.id"), nullable=False)
    value          = db.Column(db.Float,   nullable=False)
    unit           = db.Column(db.String(30), nullable=True)
    status         = db.Column(
                        db.Enum("normal", "warning", "critical", name="metric_status"),
                        default="normal", nullable=False
                     )
    recorded_at    = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    created_at     = db.Column(db.DateTime, default=datetime.utcnow)

    metric_type = db.relationship("MetricType", back_populates="metrics")

    def to_dict(self):
        return {
            "id":             self.id,
            "device_id":      self.device_id,
            "metric_type":    self.metric_type.to_dict() if self.metric_type else None,
            "value":          self.value,
            "unit":           self.unit,
            "status":         self.status,
            "recorded_at":    self.recorded_at.isoformat() if self.recorded_at else None,
            "created_at":     self.created_at.isoformat() if self.created_at else None,
        }

    def __repr__(self):
        return f"<Metric device={self.device_id} type={self.metric_type_id} val={self.value}>"

