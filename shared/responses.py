

from flask import jsonify

def success_response(data=None, message="Operación exitosa", status_code=200):
    response = {
        "success": True,
        "message": message,
        "data": data
    }
    return jsonify(response), status_code

def error_response(message="Error interno del servidor", status_code=500, errors=None):
    response = {
        "success": False,
        "message": message,
        "errors": errors
    }
    return jsonify(response), status_code

def created_response(data=None, message="Recurso creado exitosamente"):
    return success_response(data=data, message=message, status_code=201)

def not_found_response(message="Recurso no encontrado"):
    return error_response(message=message, status_code=404)

def unauthorized_response(message="No autorizado"):
    return error_response(message=message, status_code=401)

def forbidden_response(message="Acceso denegado"):
    return error_response(message=message, status_code=403)

def validation_error_response(errors, message="Error de validación"):
    return error_response(message=message, status_code=422, errors=errors)