from flask import Blueprint, request
from app.controllers import (
    get_all_locations, get_location_by_id, create_location,
    update_location, delete_location, get_buildings, get_floors_by_building
)
from shared.auth_middleware import token_required, role_required

locations_bp = Blueprint("locations", __name__, url_prefix="/api/locations")


@locations_bp.route("/", methods=["GET"])
@token_required
def list_locations():
    return get_all_locations()


@locations_bp.route("/<int:location_id>", methods=["GET"])
@token_required
def get_location(location_id):
    return get_location_by_id(location_id)


@locations_bp.route("/", methods=["POST"])
@role_required("admin", "tecnico")
def new_location():
    return create_location(request.get_json() or {})


@locations_bp.route("/<int:location_id>", methods=["PUT"])
@role_required("admin", "tecnico")
def edit_location(location_id):
    return update_location(location_id, request.get_json() or {})


@locations_bp.route("/<int:location_id>", methods=["DELETE"])
@role_required("admin")
def remove_location(location_id):
    return delete_location(location_id)


@locations_bp.route("/buildings", methods=["GET"])
@token_required
def list_buildings():
    return get_buildings()


@locations_bp.route("/buildings/<string:building>/floors", methods=["GET"])
@token_required
def list_floors(building):
    return get_floors_by_building(building)

