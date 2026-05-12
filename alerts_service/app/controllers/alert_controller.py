from flask import request
from datetime import datetime
from app import db
from app.models.alert import Alert
from app.models.alert_severity import AlertSeverity
from app.schemas.alert_schema import (
    AlertSeveritySchema, AlertCreateSchema,
    AlertUpdateSchema, AlertAcknowledgeSchema, AlertResolveSchema
)
from shared.responses import (
    success_response, error_response, created_response,
    not_found_response, validation_error_response
)

severity_schema    = AlertSeveritySchema()
alert_create_schema= AlertCreateSchema()
alert_update_schema= AlertUpdateSchema()
acknowledge_schema = AlertAcknowledgeSchema()
resolve_schema     = AlertResolveSchema()


# ── SEVERIDADES ────────────────────────────────────────────

def get_all_severities():
    severities = AlertSeverity.query.order_by(AlertSeverity.level).all()
    return success_response(
        data={"severities": [s.to_dict() for s in severities], "total": len(severities)}
    )

def get_severity_by_id(severity_id: int):
    s = AlertSeverity.query.get(severity_id)
    if not s:
        return not_found_response("Severidad no encontrada")
    return success_response(data=s.to_dict())

def create_severity(data: dict):
    errors = severity_schema.validate(data)
    if errors:
        return validation_error_response(errors)

    if AlertSeverity.query.filter_by(name=data["name"]).first():
        return error_response("La severidad ya existe", status_code=409)

    s = AlertSeverity(
        name        = data["name"],
        level       = data["level"],
        color       = data.get("color"),
        description = data.get("description"),
    )
    db.session.add(s)
    db.session.commit()
    return created_response(data=s.to_dict(), message="Severidad creada exitosamente")

def update_severity(severity_id: int, data: dict):
    s = AlertSeverity.query.get(severity_id)
    if not s:
        return not_found_response("Severidad no encontrada")

    for field in ["name", "level", "color", "description"]:
        if data.get(field) is not None:
            setattr(s, field, data[field])

    db.session.commit()
    return success_response(data=s.to_dict(), message="Severidad actualizada exitosamente")

def delete_severity(severity_id: int):
    s = AlertSeverity.query.get(severity_id)
    if not s:
        return not_found_response("Severidad no encontrada")

    if s.alerts.count() > 0:
        return error_response("No se puede eliminar una severidad con alertas asociadas", status_code=409)

    db.session.delete(s)
    db.session.commit()
    return success_response(message=f"Severidad '{s.name}' eliminada exitosamente")


# ── ALERTAS ────────────────────────────────────────────────

def get_all_alerts():
    status_filter   = request.args.get("status")
    severity_filter = request.args.get("severity_id", type=int)
    device_filter   = request.args.get("device_id", type=int)
    limit           = request.args.get("limit", default=100, type=int)

    query = Alert.query

    if status_filter:
        query = query.filter_by(status=status_filter)
    if severity_filter:
        query = query.filter_by(severity_id=severity_filter)
    if device_filter:
        query = query.filter_by(device_id=device_filter)

    alerts = query.order_by(Alert.created_at.desc()).limit(limit).all()
    return success_response(
        data={"alerts": [a.to_dict() for a in alerts], "total": len(alerts)}
    )

def get_alert_by_id(alert_id: int):
    alert = Alert.query.get(alert_id)
    if not alert:
        return not_found_response("Alerta no encontrada")
    return success_response(data=alert.to_dict())

def create_alert(data: dict):
    errors = alert_create_schema.validate(data)
    if errors:
        return validation_error_response(errors)

    if not AlertSeverity.query.get(data["severity_id"]):
        return not_found_response("Severidad no encontrada")

    alert = Alert(
        title       = data["title"],
        message     = data["message"],
        device_id   = data.get("device_id"),
        metric_id   = data.get("metric_id"),
        severity_id = data["severity_id"],
        status      = data.get("status", "activa"),
    )
    db.session.add(alert)
    db.session.commit()
    return created_response(data=alert.to_dict(), message="Alerta creada exitosamente")

def update_alert(alert_id: int, data: dict):
    errors = alert_update_schema.validate(data)
    if errors:
        return validation_error_response(errors)

    alert = Alert.query.get(alert_id)
    if not alert:
        return not_found_response("Alerta no encontrada")

    for field in ["title", "message", "status"]:
        if data.get(field) is not None:
            setattr(alert, field, data[field])

    if data.get("severity_id"):
        if not AlertSeverity.query.get(data["severity_id"]):
            return not_found_response("Severidad no encontrada")
        alert.severity_id = data["severity_id"]

    db.session.commit()
    return success_response(data=alert.to_dict(), message="Alerta actualizada exitosamente")

def delete_alert(alert_id: int):
    alert = Alert.query.get(alert_id)
    if not alert:
        return not_found_response("Alerta no encontrada")
    db.session.delete(alert)
    db.session.commit()
    return success_response(message="Alerta eliminada exitosamente")

def acknowledge_alert(alert_id: int, data: dict):
    errors = acknowledge_schema.validate(data)
    if errors:
        return validation_error_response(errors)

    alert = Alert.query.get(alert_id)
    if not alert:
        return not_found_response("Alerta no encontrada")

    if alert.status != "activa":
        return error_response(f"La alerta ya está en estado '{alert.status}'", status_code=409)

    alert.status         = "reconocida"
    alert.acknowledged_by = data["user_id"]
    alert.acknowledged_at = datetime.utcnow()
    db.session.commit()
    return success_response(data=alert.to_dict(), message="Alerta reconocida exitosamente")

def resolve_alert(alert_id: int, data: dict):
    errors = resolve_schema.validate(data)
    if errors:
        return validation_error_response(errors)

    alert = Alert.query.get(alert_id)
    if not alert:
        return not_found_response("Alerta no encontrada")

    if alert.status == "resuelta":
        return error_response("La alerta ya está resuelta", status_code=409)

    alert.status      = "resuelta"
    alert.resolved_by  = data["user_id"]
    alert.resolved_at  = datetime.utcnow()

    if data.get("message"):
        alert.message = alert.message + f"\n[Resolución]: {data['message']}"

    db.session.commit()
    return success_response(data=alert.to_dict(), message="Alerta resuelta exitosamente")

def get_alerts_summary():
    """Resumen de alertas por estado y severidad."""
    from sqlalchemy import func

    by_status = db.session.query(
        Alert.status, func.count(Alert.id).label("count")
    ).group_by(Alert.status).all()

    by_severity = db.session.query(
        AlertSeverity.name, AlertSeverity.color,
        func.count(Alert.id).label("count")
    ).join(Alert, Alert.severity_id == AlertSeverity.id)\
     .filter(Alert.status == "activa")\
     .group_by(AlertSeverity.name, AlertSeverity.color)\
     .all()

    return success_response(data={
        "by_status":   [{"status": r.status,   "count": r.count} for r in by_status],
        "active_by_severity": [
            {"severity": r.name, "color": r.color, "count": r.count}
            for r in by_severity
        ],
        "total_active": Alert.query.filter_by(status="activa").count(),
    })

