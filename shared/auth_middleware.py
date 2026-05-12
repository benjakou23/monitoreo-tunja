

from functools import wraps
from flask import request, current_app
import jwt
from shared.responses import unauthorized_response, forbidden_response

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if "Authorization" in request.headers:
            auth_header = request.headers["Authorization"]
            parts = auth_header.split(" ")
            if len(parts) == 2 and parts[0] == "Bearer":
                token = parts[1]

        if not token:
            return unauthorized_response("Token de acceso requerido")

        try:
            payload = jwt.decode(
                token,
                current_app.config["JWT_SECRET_KEY"],
                algorithms=["HS256"]
            )
            request.current_user = payload
        except jwt.ExpiredSignatureError:
            return unauthorized_response("Token expirado, inicia sesión nuevamente")
        except jwt.InvalidTokenError:
            return unauthorized_response("Token inválido")

        return f(*args, **kwargs)
    return decorated


def role_required(*roles):
    def decorator(f):
        @wraps(f)
        @token_required
        def decorated(*args, **kwargs):
            user_role = request.current_user.get("role", "")
            if user_role not in roles:
                return forbidden_response(f"Se requiere rol: {', '.join(roles)}")
            return f(*args, **kwargs)
        return decorated
    return decorator