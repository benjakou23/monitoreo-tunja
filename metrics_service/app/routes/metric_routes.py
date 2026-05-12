from flask import Blueprint, request
from app.controllers import (
    get_all_metric_types, get_metric_type_by_id,
    create_metric_type, update_metric_type, delete_metric_type,
    get_all_metrics, get_metric_by_id, create_metric,
    create_metrics_bulk, delete_metric,
    get_device_summary, get_stats_by_device
)
from shared.auth_middleware import token_required, role_required

metrics_bp      = Blueprint("metrics",      __name__, url_prefix="/api/metrics")
metric_types_bp = Blueprint("metric_types", __name__, url_prefix="/api/metric-types")


# ── TIPOS DE MÉTRICA ───────────────────────────────────────

@metric_types_bp.route("/", methods=["GET"])
@token_required
def list_metric_types():
    return get_all_metric_types()

@metric_types_bp.route("/<int:type_id>", methods=["GET"])
@token_required
def get_metric_type(type_id):
    return get_metric_type_by_id(type_id)

@metric_types_bp.route("/", methods=["POST"])
@role_required("admin", "tecnico")
def new_metric_type():
    return create_metric_type(request.get_json() or {})

@metric_types_bp.route("/<int:type_id>", methods=["PUT"])
@role_required("admin", "tecnico")
def edit_metric_type(type_id):
    return update_metric_type(type_id, request.get_json() or {})

@metric_types_bp.route("/<int:type_id>", methods=["DELETE"])
@role_required("admin")
def remove_metric_type(type_id):
    return delete_metric_type(type_id)


# ── MÉTRICAS ───────────────────────────────────────────────

@metrics_bp.route("/", methods=["GET"])
@token_required
def list_metrics():
    return get_all_metrics()

@metrics_bp.route("/<int:metric_id>", methods=["GET"])
@token_required
def get_metric(metric_id):
    return get_metric_by_id(metric_id)

@metrics_bp.route("/", methods=["POST"])
@role_required("admin", "tecnico", "operador")
def new_metric():
    return create_metric(request.get_json() or {})

@metrics_bp.route("/bulk", methods=["POST"])
@role_required("admin", "tecnico", "operador")
def bulk_metrics():
    return create_metrics_bulk(request.get_json() or {})

@metrics_bp.route("/<int:metric_id>", methods=["DELETE"])
@role_required("admin")
def remove_metric(metric_id):
    return delete_metric(metric_id)

@metrics_bp.route("/device/<int:device_id>/summary", methods=["GET"])
@token_required
def device_summary(device_id):
    return get_device_summary(device_id)

@metrics_bp.route("/device/<int:device_id>/stats", methods=["GET"])
@token_required
def device_stats(device_id):
    return get_stats_by_device(device_id)

