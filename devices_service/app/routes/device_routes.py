from flask import Blueprint, request
from app.controllers import (
    get_all_device_types, get_device_type_by_id, create_device_type,
    update_device_type, delete_device_type,
    get_all_devices, get_device_by_id, create_device,
    update_device, delete_device, change_device_status
)
from shared.auth_middleware import token_required, role_required

devices_bp      = Blueprint("devices",      __name__, url_prefix="/api/devices")
device_types_bp = Blueprint("device_types", __name__, url_prefix="/api/device-types")


# ── TIPOS DE DISPOSITIVO ───────────────────────────────────

@device_types_bp.route("/", methods=["GET"])
@token_required
def list_device_types():
    return get_all_device_types()

@device_types_bp.route("/<int:type_id>", methods=["GET"])
@token_required
def get_device_type(type_id):
    return get_device_type_by_id(type_id)

@device_types_bp.route("/", methods=["POST"])
@role_required("admin", "tecnico")
def new_device_type():
    return create_device_type(request.get_json() or {})

@device_types_bp.route("/<int:type_id>", methods=["PUT"])
@role_required("admin", "tecnico")
def edit_device_type(type_id):
    return update_device_type(type_id, request.get_json() or {})

@device_types_bp.route("/<int:type_id>", methods=["DELETE"])
@role_required("admin")
def remove_device_type(type_id):
    return delete_device_type(type_id)


# ── DISPOSITIVOS ───────────────────────────────────────────

@devices_bp.route("/", methods=["GET"])
@token_required
def list_devices():
    return get_all_devices()

@devices_bp.route("/<int:device_id>", methods=["GET"])
@token_required
def get_device(device_id):
    return get_device_by_id(device_id)

@devices_bp.route("/", methods=["POST"])
@role_required("admin", "tecnico")
def new_device():
    return create_device(request.get_json() or {})

@devices_bp.route("/<int:device_id>", methods=["PUT"])
@role_required("admin", "tecnico")
def edit_device(device_id):
    return update_device(device_id, request.get_json() or {})

@devices_bp.route("/<int:device_id>", methods=["DELETE"])
@role_required("admin")
def remove_device(device_id):
    return delete_device(device_id)

@devices_bp.route("/<int:device_id>/status", methods=["PATCH"])
@role_required("admin", "tecnico", "operador")
def update_status(device_id):
    return change_device_status(device_id, request.get_json() or {})

