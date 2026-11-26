from flask import jsonify, request
from my_project.auth.service.city_service import CityService
from my_project.auth.domain.city import City

class CityController:
    def __init__(self):
        self.service = CityService()

    def get_all(self):
        cities = self.service.get_all()
        return jsonify([c.put_into_dto() for c in cities]), 200

    def get_by_id(self, city_id: int):
        city = self.service.get_by_id(city_id)
        if not city:
            return jsonify({"message": "Місто не знайдено"}), 404
        return jsonify(city.put_into_dto()), 200

    def create(self):
        data = request.get_json()
        city = City.create_from_dto(data)
        created = self.service.create(city)
        return jsonify(created.put_into_dto()), 201

    def update(self, city_id: int):
        data = request.get_json()
        city = City.create_from_dto(data)
        if not self.service.update(city_id, city):
            return jsonify({"message": "Місто не знайдено"}), 404
        return jsonify({"message": "Оновлено успішно"}), 200

    def delete(self, city_id: int):
        if not self.service.delete(city_id):
            return jsonify({"message": "Місто не знайдено"}), 404
        return jsonify({"message": "Видалено успішно"}), 200

    def get_cities_with_stations(self):
        return jsonify(self.service.get_cities_with_stations()), 200

    def get_trips_with_drivers(self):
        return jsonify(self.service.get_trips_with_drivers()), 200