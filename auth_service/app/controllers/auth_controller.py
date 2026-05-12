from flask import current_app
from datetime import datetime, timedelta
import jwt

from app import db
from app.models.user import User
from app.models.role import Role
from app.schemas.auth_schema import LoginSchema, RegisterSchema, ChangePasswordSchema
from shared.responses import (
    success_response, error_response, created_response,
    unauthorized_response, not_found_response, validation_error_response
)

login_schema    = LoginSchema()
register_schema = RegisterSchema()
change_pw_schema= ChangePasswordSchema()


def _generate_token(user: User) -> str:
    expiration = datetime.utcnow() + timedelta(
        hours=current_app.config["JWT_EXPIRATION_HOURS"]
    )
    payload = {
        "sub":      user.id,
        "username": user.username,
        "email":    user.email,
        "role":     user.role.name if user.role else "user",
        "exp":      expiration,
        "iat":      datetime.utcnow(),
    }
    return jwt.encode(
        payload,
        current_app.config["JWT_SECRET_KEY"],
        algorithm="HS256"
    )


def login(data: dict):
    errors = login_schema.validate(data)
    if errors:
        return validation_error_response(errors)

    user = User.query.filter_by(username=data["username"]).first()

    if not user or not user.check_password(data["password"]):
        return unauthorized_response("Credenciales inválidas")

    if not user.is_active:
        return unauthorized_response("Cuenta desactivada, contacte al administrador")

    token = _generate_token(user)

    return success_response(
        data={
            "token":      token,
            "token_type": "Bearer",
            "expires_in": current_app.config["JWT_EXPIRATION_HOURS"] * 3600,
            "user":       user.to_dict(),
        },
        message="Inicio de sesión exitoso"
    )


def register(data: dict):
    errors = register_schema.validate(data)
    if errors:
        return validation_error_response(errors)

    if User.query.filter_by(username=data["username"]).first():
        return error_response("El nombre de usuario ya existe", status_code=409)

    if User.query.filter_by(email=data["email"]).first():
        return error_response("El email ya está registrado", status_code=409)

    role = None
    if data.get("role_id"):
        role = Role.query.get(data["role_id"])
        if not role:
            return not_found_response("Rol no encontrado")

    user = User(
        username  = data["username"],
        email     = data["email"],
        full_name = data.get("full_name"),
        role_id   = role.id if role else None,
    )
    user.set_password(data["password"])

    db.session.add(user)
    db.session.commit()

    return created_response(data=user.to_dict(), message="Usuario registrado exitosamente")


def get_profile(user_id: int):
    user = User.query.get(user_id)
    if not user:
        return not_found_response("Usuario no encontrado")
    return success_response(data=user.to_dict())


def change_password(user_id: int, data: dict):
    errors = change_pw_schema.validate(data)
    if errors:
        return validation_error_response(errors)

    user = User.query.get(user_id)
    if not user:
        return not_found_response("Usuario no encontrado")

    if not user.check_password(data["current_password"]):
        return unauthorized_response("Contraseña actual incorrecta")

    user.set_password(data["new_password"])
    db.session.commit()

    return success_response(message="Contraseña actualizada exitosamente")


def refresh_token(user_id: int):
    user = User.query.get(user_id)
    if not user or not user.is_active:
        return unauthorized_response("Usuario no válido")

    token = _generate_token(user)
    return success_response(
        data={"token": token, "token_type": "Bearer"},
        message="Token renovado exitosamente"
    )