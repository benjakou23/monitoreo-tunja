from flask import Blueprint, request
from app.controllers import (
    get_all_severities, get_severity_by_id, create_severity,
    update_severity, delete_severity,
    get_all_alerts, get_alert_by_id, create_alert,
    update_alert, delete_alert,
    acknowledge_alert, resolve_alert, get_alerts_summary
)
from shared.auth_middleware import token_required, role_required

alerts_bp     = Blueprint("alerts",     __name__, url_prefix="/api/alerts")
severities_bp = Blueprint("severities", __name__, url_prefix="/api/severities")


# ── SEVERIDADES ────────────────────────────────────────────

@severities_bp.route("/", methods=["GET"])
@token_required
def list_severities():
    return get_all_severities()

@severities_bp.route("/<int:severity_id>", methods=["GET"])
@token_required
def get_severity(severity_id):
    return get_severity_by_id(severity_id)

@severities_bp.route("/", methods=["POST"])
@role_required("admin")
def new_severity():
    return create_severity(request.get_json() or {})

@severities_bp.route("/<int:severity_id>", methods=["PUT"])
@role_required("admin")
def edit_severity(severity_id):
    return update_severity(severity_id, request.get_json() or {})

@severities_bp.route("/<int:severity_id>", methods=["DELETE"])
@role_required("admin")
def remove_severity(severity_id):
    return delete_severity(severity_id)


# ── ALERTAS ────────────────────────────────────────────────

@alerts_bp.route("/", methods=["GET"])
@token_required
def list_alerts():
    return get_all_alerts()

@alerts_bp.route("/summary", methods=["GET"])
@token_required
def alerts_summary():
    return get_alerts_summary()

@alerts_bp.route("/<int:alert_id>", methods=["GET"])
@token_required
def get_alert(alert_id):
    return get_alert_by_id(alert_id)

@alerts_bp.route("/", methods=["POST"])
@role_required("admin", "tecnico", "operador")
def new_alert():
    return create_alert(request.get_json() or {})

@alerts_bp.route("/<int:alert_id>", methods=["PUT"])
@role_required("admin", "tecnico")
def edit_alert(alert_id):
    return update_alert(alert_id, request.get_json() or {})

@alerts_bp.route("/<int:alert_id>", methods=["DELETE"])
@role_required("admin")
def remove_alert(alert_id):
    return delete_alert(alert_id)

@alerts_bp.route("/<int:alert_id>/acknowledge", methods=["PATCH"])
@role_required("admin", "tecnico", "operador")
def ack_alert(alert_id):
    return acknowledge_alert(alert_id, request.get_json() or {})

@alerts_bp.route("/<int:alert_id>/resolve", methods=["PATCH"])
@role_required("admin", "tecnico")
def res_alert(alert_id):
    return resolve_alert(alert_id, request.get_json() or {})

