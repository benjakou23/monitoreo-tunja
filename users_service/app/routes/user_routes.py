from flask import Blueprint, request
from app.controllers import (
    get_all_users, get_user_by_id, create_user,
    update_user, delete_user, toggle_user_status,
    get_all_roles, get_role_by_id, create_role,
    update_role, delete_role
)
from shared.auth_middleware import token_required, role_required

users_bp = Blueprint("users", __name__, url_prefix="/api/users")
roles_bp = Blueprint("roles", __name__, url_prefix="/api/roles")


# ── USUARIOS ──────────────────────────────────────────────

@users_bp.route("/", methods=["GET"])
@token_required
def list_users():
    return get_all_users()


@users_bp.route("/<int:user_id>", methods=["GET"])
@token_required
def get_user(user_id):
    return get_user_by_id(user_id)


@users_bp.route("/", methods=["POST"])
@role_required("admin")
def new_user():
    return create_user(request.get_json() or {})


@users_bp.route("/<int:user_id>", methods=["PUT"])
@role_required("admin")
def edit_user(user_id):
    return update_user(user_id, request.get_json() or {})


@users_bp.route("/<int:user_id>", methods=["DELETE"])
@role_required("admin")
def remove_user(user_id):
    return delete_user(user_id)


@users_bp.route("/<int:user_id>/toggle", methods=["PATCH"])
@role_required("admin")
def toggle_user(user_id):
    return toggle_user_status(user_id)


# ── ROLES ──────────────────────────────────────────────────

@roles_bp.route("/", methods=["GET"])
@token_required
def list_roles():
    return get_all_roles()


@roles_bp.route("/<int:role_id>", methods=["GET"])
@token_required
def get_role(role_id):
    return get_role_by_id(role_id)


@roles_bp.route("/", methods=["POST"])
@role_required("admin")
def new_role():
    return create_role(request.get_json() or {})


@roles_bp.route("/<int:role_id>", methods=["PUT"])
@role_required("admin")
def edit_role(role_id):
    return update_role(role_id, request.get_json() or {})


@roles_bp.route("/<int:role_id>", methods=["DELETE"])
@role_required("admin")
def remove_role(role_id):
    return delete_role(role_id)

