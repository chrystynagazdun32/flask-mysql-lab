from flask import Blueprint
from my_project.auth.controller.city_controller import CityController

city_bp = Blueprint("cities", __name__)
controller = CityController()


@city_bp.route("/cities", methods=["GET"])
def get_cities():
    return controller.get_all()


@city_bp.route("/cities/<int:city_id>", methods=["GET"])
def get_city(city_id):
    return controller.get_by_id(city_id)


@city_bp.route("/cities", methods=["POST"])
def create_city():
    return controller.create()


@city_bp.route("/cities/<int:city_id>", methods=["PUT"])
def update_city(city_id):
    return controller.update(city_id)


@city_bp.route("/cities/<int:city_id>", methods=["DELETE"])
def delete_city(city_id):
    return controller.delete(city_id)


@city_bp.route("/cities-stations", methods=["GET"])
def get_cities_with_stations():
    return controller.get_cities_with_stations()


@city_bp.route("/trips-drivers", methods=["GET"])
def get_trips_with_drivers():
    return controller.get_trips_with_drivers()