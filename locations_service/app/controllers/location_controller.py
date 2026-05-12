from flask import request
from app import db
from app.models.location import Location
from app.schemas.location_schema import LocationCreateSchema, LocationUpdateSchema
from shared.responses import (
    success_response, error_response, created_response,
    not_found_response, validation_error_response
)

location_create_schema = LocationCreateSchema()
location_update_schema = LocationUpdateSchema()


def get_all_locations():
    building_filter = request.args.get("building")
    floor_filter    = request.args.get("floor")
    active_filter   = request.args.get("is_active")

    query = Location.query

    if building_filter:
        query = query.filter(Location.building.ilike(f"%{building_filter}%"))
    if floor_filter:
        query = query.filter(Location.floor.ilike(f"%{floor_filter}%"))
    if active_filter is not None:
        is_active = active_filter.lower() == "true"
        query = query.filter_by(is_active=is_active)

    locations = query.order_by(Location.building, Location.floor, Location.name).all()
    return success_response(
        data={"locations": [l.to_dict() for l in locations], "total": len(locations)}
    )


def get_location_by_id(location_id: int):
    location = Location.query.get(location_id)
    if not location:
        return not_found_response("Ubicación no encontrada")
    return success_response(data=location.to_dict())


def create_location(data: dict):
    errors = location_create_schema.validate(data)
    if errors:
        return validation_error_response(errors)

    # Verificar duplicado por nombre + edificio + piso
    existing = Location.query.filter_by(
        name     = data["name"],
        building = data.get("building"),
        floor    = data.get("floor"),
    ).first()
    if existing:
        return error_response("Ya existe una ubicación con ese nombre en ese edificio y piso", status_code=409)

    location = Location(
        name        = data["name"],
        building    = data.get("building"),
        floor       = data.get("floor"),
        room        = data.get("room"),
        description = data.get("description"),
        is_active   = data.get("is_active", True),
    )
    db.session.add(location)
    db.session.commit()
    return created_response(data=location.to_dict(), message="Ubicación creada exitosamente")


def update_location(location_id: int, data: dict):
    errors = location_update_schema.validate(data)
    if errors:
        return validation_error_response(errors)

    location = Location.query.get(location_id)
    if not location:
        return not_found_response("Ubicación no encontrada")

    fields_to_update = ["name", "building", "floor", "room", "description", "is_active"]
    for field in fields_to_update:
        if data.get(field) is not None:
            setattr(location, field, data[field])

    db.session.commit()
    return success_response(data=location.to_dict(), message="Ubicación actualizada exitosamente")


def delete_location(location_id: int):
    location = Location.query.get(location_id)
    if not location:
        return not_found_response("Ubicación no encontrada")

    # Soft delete
    location.is_active = False
    db.session.commit()
    return success_response(message=f"Ubicación '{location.name}' desactivada exitosamente")


def get_buildings():
    """Retorna lista única de edificios registrados."""
    results = db.session.query(Location.building)\
        .filter(Location.building.isnot(None))\
        .distinct()\
        .order_by(Location.building)\
        .all()
    buildings = [r[0] for r in results]
    return success_response(data={"buildings": buildings, "total": len(buildings)})


def get_floors_by_building(building: str):
    """Retorna pisos de un edificio específico."""
    results = db.session.query(Location.floor)\
        .filter(Location.building == building)\
        .filter(Location.floor.isnot(None))\
        .distinct()\
        .order_by(Location.floor)\
        .all()
    floors = [r[0] for r in results]
    return success_response(data={"building": building, "floors": floors, "total": len(floors)})

