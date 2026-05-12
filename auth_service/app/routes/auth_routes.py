from flask import Blueprint, request
from app.controllers import login, register, get_profile, change_password, refresh_token
from shared.auth_middleware import token_required

auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")


@auth_bp.route("/login", methods=["POST"])
def login_route():
    return login(request.get_json() or {})


@auth_bp.route("/register", methods=["POST"])
def register_route():
    return register(request.get_json() or {})


@auth_bp.route("/profile", methods=["GET"])
@token_required
def profile_route():
    return get_profile(request.current_user["sub"])


@auth_bp.route("/change-password", methods=["PUT"])
@token_required
def change_password_route():
    return change_password(request.current_user["sub"], request.get_json() or {})


@auth_bp.route("/refresh", methods=["POST"])
@token_required
def refresh_route():
    return refresh_token(request.current_user["sub"])


@auth_bp.route("/verify", methods=["GET"])
@token_required
def verify_route():
    from shared.responses import success_response
    return success_response(
        data=request.current_user,
        message="Token válido"
    )

