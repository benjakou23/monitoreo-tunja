from flask import request
from datetime import datetime, timedelta
from app import db
from app.models.metric import Metric
from app.models.metric_type import MetricType
from app.schemas.metric_schema import MetricTypeCreateSchema, MetricCreateSchema, MetricBulkCreateSchema
from shared.responses import (
    success_response, error_response, created_response,
    not_found_response, validation_error_response
)

metric_type_schema      = MetricTypeCreateSchema()
metric_create_schema    = MetricCreateSchema()
metric_bulk_schema      = MetricBulkCreateSchema()


# ── HELPERS ────────────────────────────────────────────────

def _auto_status(value: float, metric_type: MetricType) -> str:
    """Calcula el status automáticamente según los umbrales del tipo."""
    if metric_type.max_value is None:
        return "normal"
    threshold_warning  = metric_type.max_value * 0.75
    threshold_critical = metric_type.max_value * 0.90
    if value >= threshold_critical:
        return "critical"
    elif value >= threshold_warning:
        return "warning"
    return "normal"


# ── TIPOS DE MÉTRICA ───────────────────────────────────────

def get_all_metric_types():
    types = MetricType.query.order_by(MetricType.id).all()
    return success_response(
        data={"metric_types": [t.to_dict() for t in types], "total": len(types)}
    )

def get_metric_type_by_id(type_id: int):
    mt = MetricType.query.get(type_id)
    if not mt:
        return not_found_response("Tipo de métrica no encontrado")
    return success_response(data=mt.to_dict())

def create_metric_type(data: dict):
    errors = metric_type_schema.validate(data)
    if errors:
        return validation_error_response(errors)

    if MetricType.query.filter_by(name=data["name"]).first():
        return error_response("El tipo de métrica ya existe", status_code=409)

    mt = MetricType(
        name        = data["name"],
        unit        = data.get("unit"),
        description = data.get("description"),
        min_value   = data.get("min_value"),
        max_value   = data.get("max_value"),
    )
    db.session.add(mt)
    db.session.commit()
    return created_response(data=mt.to_dict(), message="Tipo de métrica creado exitosamente")

def update_metric_type(type_id: int, data: dict):
    mt = MetricType.query.get(type_id)
    if not mt:
        return not_found_response("Tipo de métrica no encontrado")

    for field in ["name", "unit", "description", "min_value", "max_value"]:
        if data.get(field) is not None:
            setattr(mt, field, data[field])

    db.session.commit()
    return success_response(data=mt.to_dict(), message="Tipo de métrica actualizado exitosamente")

def delete_metric_type(type_id: int):
    mt = MetricType.query.get(type_id)
    if not mt:
        return not_found_response("Tipo de métrica no encontrado")

    if mt.metrics.count() > 0:
        return error_response("No se puede eliminar un tipo con métricas registradas", status_code=409)

    db.session.delete(mt)
    db.session.commit()
    return success_response(message=f"Tipo '{mt.name}' eliminado exitosamente")


# ── MÉTRICAS ───────────────────────────────────────────────

def get_all_metrics():
    device_id   = request.args.get("device_id", type=int)
    type_id     = request.args.get("metric_type_id", type=int)
    status      = request.args.get("status")
    hours       = request.args.get("hours", type=int)
    limit       = request.args.get("limit", default=100, type=int)

    query = Metric.query

    if device_id:
        query = query.filter_by(device_id=device_id)
    if type_id:
        query = query.filter_by(metric_type_id=type_id)
    if status:
        query = query.filter_by(status=status)
    if hours:
        since = datetime.utcnow() - timedelta(hours=hours)
        query = query.filter(Metric.recorded_at >= since)

    metrics = query.order_by(Metric.recorded_at.desc()).limit(limit).all()
    return success_response(
        data={"metrics": [m.to_dict() for m in metrics], "total": len(metrics)}
    )

def get_metric_by_id(metric_id: int):
    metric = Metric.query.get(metric_id)
    if not metric:
        return not_found_response("Métrica no encontrada")
    return success_response(data=metric.to_dict())

def create_metric(data: dict):
    errors = metric_create_schema.validate(data)
    if errors:
        return validation_error_response(errors)

    mt = MetricType.query.get(data["metric_type_id"])
    if not mt:
        return not_found_response("Tipo de métrica no encontrado")

    # Status automático si no viene en el payload
    status = data.get("status") or _auto_status(data["value"], mt)

    metric = Metric(
        device_id      = data["device_id"],
        metric_type_id = data["metric_type_id"],
        value          = data["value"],
        unit           = data.get("unit") or mt.unit,
        status         = status,
        recorded_at    = data.get("recorded_at") or datetime.utcnow(),
    )
    db.session.add(metric)
    db.session.commit()
    return created_response(data=metric.to_dict(), message="Métrica registrada exitosamente")

def create_metrics_bulk(data: dict):
    """Inserción masiva de métricas (para agentes de monitoreo)."""
    errors = metric_bulk_schema.validate(data)
    if errors:
        return validation_error_response(errors)

    created = []
    for item in data["metrics"]:
        mt = MetricType.query.get(item["metric_type_id"])
        if not mt:
            continue
        status = item.get("status") or _auto_status(item["value"], mt)
        metric = Metric(
            device_id      = item["device_id"],
            metric_type_id = item["metric_type_id"],
            value          = item["value"],
            unit           = item.get("unit") or mt.unit,
            status         = status,
            recorded_at    = item.get("recorded_at") or datetime.utcnow(),
        )
        db.session.add(metric)
        created.append(metric)

    db.session.commit()
    return created_response(
        data={"created": len(created)},
        message=f"{len(created)} métricas registradas exitosamente"
    )

def delete_metric(metric_id: int):
    metric = Metric.query.get(metric_id)
    if not metric:
        return not_found_response("Métrica no encontrada")
    db.session.delete(metric)
    db.session.commit()
    return success_response(message="Métrica eliminada exitosamente")

def get_device_summary(device_id: int):
    """Última métrica de cada tipo para un dispositivo."""
    from sqlalchemy import func

    subquery = db.session.query(
        Metric.metric_type_id,
        func.max(Metric.recorded_at).label("last_recorded")
    ).filter_by(device_id=device_id)\
     .group_by(Metric.metric_type_id)\
     .subquery()

    metrics = Metric.query.join(
        subquery,
        (Metric.metric_type_id == subquery.c.metric_type_id) &
        (Metric.recorded_at    == subquery.c.last_recorded)
    ).filter(Metric.device_id == device_id).all()

    return success_response(
        data={
            "device_id": device_id,
            "latest_metrics": [m.to_dict() for m in metrics],
            "total": len(metrics)
        }
    )

def get_stats_by_device(device_id: int):
    """Estadísticas por tipo de métrica para un dispositivo."""
    from sqlalchemy import func

    hours = request.args.get("hours", default=24, type=int)
    since = datetime.utcnow() - timedelta(hours=hours)

    results = db.session.query(
        MetricType.name,
        MetricType.unit,
        func.avg(Metric.value).label("avg"),
        func.min(Metric.value).label("min"),
        func.max(Metric.value).label("max"),
        func.count(Metric.id).label("count"),
    ).join(Metric, Metric.metric_type_id == MetricType.id)\
     .filter(Metric.device_id == device_id)\
     .filter(Metric.recorded_at >= since)\
     .group_by(MetricType.name, MetricType.unit)\
     .all()

    stats = [
        {
            "metric_type": r.name,
            "unit":  r.unit,
            "avg":   round(r.avg,  2) if r.avg  else None,
            "min":   round(r.min,  2) if r.min  else None,
            "max":   round(r.max,  2) if r.max  else None,
            "count": r.count,
        }
        for r in results
    ]
    return success_response(
        data={"device_id": device_id, "hours": hours, "stats": stats}
    )

