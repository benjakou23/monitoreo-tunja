from app import db
from app.models.device import Device
from app.models.device_type import DeviceType
from app.schemas.device_schema import DeviceTypeSchema, DeviceCreateSchema, DeviceUpdateSchema
from shared.responses import (
    success_response, error_response, created_response,
    not_found_response, validation_error_response
)

device_type_schema   = DeviceTypeSchema()
device_create_schema = DeviceCreateSchema()
device_update_schema = DeviceUpdateSchema()


# ── TIPOS DE DISPOSITIVO ───────────────────────────────────

def get_all_device_types():
    types = DeviceType.query.order_by(DeviceType.id).all()
    return success_response(
        data={"device_types": [t.to_dict() for t in types], "total": len(types)}
    )

def get_device_type_by_id(type_id: int):
    dt = DeviceType.query.get(type_id)
    if not dt:
        return not_found_response("Tipo de dispositivo no encontrado")
    return success_response(data=dt.to_dict())

def create_device_type(data: dict):
    errors = device_type_schema.validate(data)
    if errors:
        return validation_error_response(errors)

    if DeviceType.query.filter_by(name=data["name"]).first():
        return error_response("El tipo de dispositivo ya existe", status_code=409)

    dt = DeviceType(name=data["name"], description=data.get("description"))
    db.session.add(dt)
    db.session.commit()
    return created_response(data=dt.to_dict(), message="Tipo de dispositivo creado exitosamente")

def update_device_type(type_id: int, data: dict):
    dt = DeviceType.query.get(type_id)
    if not dt:
        return not_found_response("Tipo de dispositivo no encontrado")

    if data.get("name") and data["name"] != dt.name:
        if DeviceType.query.filter_by(name=data["name"]).first():
            return error_response("Ese nombre ya existe", status_code=409)
        dt.name = data["name"]

    if data.get("description") is not None:
        dt.description = data["description"]

    db.session.commit()
    return success_response(data=dt.to_dict(), message="Tipo actualizado exitosamente")

def delete_device_type(type_id: int):
    dt = DeviceType.query.get(type_id)
    if not dt:
        return not_found_response("Tipo de dispositivo no encontrado")

    if dt.devices.count() > 0:
        return error_response(
            "No se puede eliminar un tipo con dispositivos asignados",
            status_code=409
        )

    db.session.delete(dt)
    db.session.commit()
    return success_response(message=f"Tipo '{dt.name}' eliminado exitosamente")


# ── DISPOSITIVOS ───────────────────────────────────────────

def get_all_devices():
    status_filter = None
    from flask import request
    status_filter = request.args.get("status")
    type_filter   = request.args.get("device_type_id")

    query = Device.query

    if status_filter:
        query = query.filter_by(status=status_filter)
    if type_filter:
        query = query.filter_by(device_type_id=int(type_filter))

    devices = query.order_by(Device.id).all()
    return success_response(
        data={"devices": [d.to_dict() for d in devices], "total": len(devices)}
    )

def get_device_by_id(device_id: int):
    device = Device.query.get(device_id)
    if not device:
        return not_found_response("Dispositivo no encontrado")
    return success_response(data=device.to_dict())

def create_device(data: dict):
    errors = device_create_schema.validate(data)
    if errors:
        return validation_error_response(errors)

    # Validar unicidad de IP, MAC y serial
    if data.get("ip_address"):
        if Device.query.filter_by(ip_address=data["ip_address"]).first():
            return error_response("La dirección IP ya está registrada", status_code=409)

    if data.get("mac_address"):
        if Device.query.filter_by(mac_address=data["mac_address"]).first():
            return error_response("La dirección MAC ya está registrada", status_code=409)

    if data.get("serial_number"):
        if Device.query.filter_by(serial_number=data["serial_number"]).first():
            return error_response("El número de serie ya está registrado", status_code=409)

    if data.get("device_type_id"):
        if not DeviceType.query.get(data["device_type_id"]):
            return not_found_response("Tipo de dispositivo no encontrado")

    device = Device(
        name           = data["name"],
        ip_address     = data.get("ip_address"),
        mac_address    = data.get("mac_address"),
        serial_number  = data.get("serial_number"),
        brand          = data.get("brand"),
        model          = data.get("model"),
        status         = data.get("status", "activo"),
        device_type_id = data.get("device_type_id"),
        location_id    = data.get("location_id"),
        description    = data.get("description"),
    )
    db.session.add(device)
    db.session.commit()
    return created_response(data=device.to_dict(), message="Dispositivo creado exitosamente")

def update_device(device_id: int, data: dict):
    errors = device_update_schema.validate(data)
    if errors:
        return validation_error_response(errors)

    device = Device.query.get(device_id)
    if not device:
        return not_found_response("Dispositivo no encontrado")

    fields_to_update = ["name", "ip_address", "mac_address", "serial_number",
                        "brand", "model", "status", "location_id", "description"]

    for field in fields_to_update:
        if data.get(field) is not None:
            setattr(device, field, data[field])

    if data.get("device_type_id") is not None:
        if not DeviceType.query.get(data["device_type_id"]):
            return not_found_response("Tipo de dispositivo no encontrado")
        device.device_type_id = data["device_type_id"]

    db.session.commit()
    return success_response(data=device.to_dict(), message="Dispositivo actualizado exitosamente")

def delete_device(device_id: int):
    device = Device.query.get(device_id)
    if not device:
        return not_found_response("Dispositivo no encontrado")

    db.session.delete(device)
    db.session.commit()
    return success_response(message=f"Dispositivo '{device.name}' eliminado exitosamente")

def change_device_status(device_id: int, data: dict):
    valid = ["activo", "inactivo", "mantenimiento", "falla"]
    new_status = data.get("status")

    if not new_status or new_status not in valid:
        return error_response(f"Estado inválido. Valores permitidos: {', '.join(valid)}", status_code=422)

    device = Device.query.get(device_id)
    if not device:
        return not_found_response("Dispositivo no encontrado")

    device.status = new_status
    db.session.commit()
    return success_response(data=device.to_dict(), message=f"Estado actualizado a '{new_status}'")

