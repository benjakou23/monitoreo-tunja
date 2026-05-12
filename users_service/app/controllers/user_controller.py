from app import db
from app.models.user import User
from app.models.role import Role
from app.schemas.user_schema import UserCreateSchema, UserUpdateSchema, RoleCreateSchema
from shared.responses import (
    success_response, error_response, created_response,
    not_found_response, validation_error_response
)

user_create_schema = UserCreateSchema()
user_update_schema = UserUpdateSchema()
role_create_schema = RoleCreateSchema()


# ── USUARIOS ──────────────────────────────────────────────

def get_all_users():
    users = User.query.order_by(User.id).all()
    return success_response(
        data={"users": [u.to_dict() for u in users], "total": len(users)}
    )


def get_user_by_id(user_id: int):
    user = User.query.get(user_id)
    if not user:
        return not_found_response("Usuario no encontrado")
    return success_response(data=user.to_dict())


def create_user(data: dict):
    errors = user_create_schema.validate(data)
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
        is_active = data.get("is_active", True),
        role_id   = role.id if role else None,
    )
    user.set_password(data["password"])

    db.session.add(user)
    db.session.commit()

    return created_response(data=user.to_dict(), message="Usuario creado exitosamente")


def update_user(user_id: int, data: dict):
    errors = user_update_schema.validate(data)
    if errors:
        return validation_error_response(errors)

    user = User.query.get(user_id)
    if not user:
        return not_found_response("Usuario no encontrado")

    if data.get("email") and data["email"] != user.email:
        if User.query.filter_by(email=data["email"]).first():
            return error_response("El email ya está en uso", status_code=409)
        user.email = data["email"]

    if data.get("full_name") is not None:
        user.full_name = data["full_name"]

    if data.get("is_active") is not None:
        user.is_active = data["is_active"]

    if data.get("role_id") is not None:
        role = Role.query.get(data["role_id"])
        if not role:
            return not_found_response("Rol no encontrado")
        user.role_id = role.id

    db.session.commit()
    return success_response(data=user.to_dict(), message="Usuario actualizado exitosamente")


def delete_user(user_id: int):
    user = User.query.get(user_id)
    if not user:
        return not_found_response("Usuario no encontrado")

    # Soft delete — solo desactiva
    user.is_active = False
    db.session.commit()
    return success_response(message=f"Usuario '{user.username}' desactivado exitosamente")


def toggle_user_status(user_id: int):
    user = User.query.get(user_id)
    if not user:
        return not_found_response("Usuario no encontrado")

    user.is_active = not user.is_active
    db.session.commit()
    status = "activado" if user.is_active else "desactivado"
    return success_response(data=user.to_dict(), message=f"Usuario {status} exitosamente")


# ── ROLES ──────────────────────────────────────────────────

def get_all_roles():
    roles = Role.query.order_by(Role.id).all()
    return success_response(
        data={"roles": [r.to_dict() for r in roles], "total": len(roles)}
    )


def get_role_by_id(role_id: int):
    role = Role.query.get(role_id)
    if not role:
        return not_found_response("Rol no encontrado")
    return success_response(data=role.to_dict())


def create_role(data: dict):
    errors = role_create_schema.validate(data)
    if errors:
        return validation_error_response(errors)

    if Role.query.filter_by(name=data["name"]).first():
        return error_response("El rol ya existe", status_code=409)

    role = Role(
        name        = data["name"],
        description = data.get("description"),
    )
    db.session.add(role)
    db.session.commit()
    return created_response(data=role.to_dict(), message="Rol creado exitosamente")


def update_role(role_id: int, data: dict):
    role = Role.query.get(role_id)
    if not role:
        return not_found_response("Rol no encontrado")

    if data.get("name") and data["name"] != role.name:
        if Role.query.filter_by(name=data["name"]).first():
            return error_response("Ese nombre de rol ya existe", status_code=409)
        role.name = data["name"]

    if data.get("description") is not None:
        role.description = data["description"]

    db.session.commit()
    return success_response(data=role.to_dict(), message="Rol actualizado exitosamente")


def delete_role(role_id: int):
    role = Role.query.get(role_id)
    if not role:
        return not_found_response("Rol no encontrado")

    if role.users.count() > 0:
        return error_response(
            "No se puede eliminar un rol con usuarios asignados",
            status_code=409
        )

    db.session.delete(role)
    db.session.commit()
    return success_response(message=f"Rol '{role.name}' eliminado exitosamente")

