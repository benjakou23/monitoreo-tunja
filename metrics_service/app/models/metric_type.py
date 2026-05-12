from app import db
from datetime import datetime

class MetricType(db.Model):
    __tablename__ = "metric_types"

    id          = db.Column(db.Integer, primary_key=True)
    name        = db.Column(db.String(100), unique=True, nullable=False)
    unit        = db.Column(db.String(30),  nullable=True)   # %, MB, GB, ms, etc.
    description = db.Column(db.String(255), nullable=True)
    min_value   = db.Column(db.Float, nullable=True)
    max_value   = db.Column(db.Float, nullable=True)
    created_at  = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at  = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    metrics = db.relationship("Metric", back_populates="metric_type", lazy="dynamic")

    def to_dict(self):
        return {
            "id":          self.id,
            "name":        self.name,
            "unit":        self.unit,
            "description": self.description,
            "min_value":   self.min_value,
            "max_value":   self.max_value,
            "created_at":  self.created_at.isoformat() if self.created_at else None,
        }

    def __repr__(self):
        return f"<MetricType {self.name}>"

