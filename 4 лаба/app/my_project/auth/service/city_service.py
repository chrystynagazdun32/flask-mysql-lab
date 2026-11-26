from my_project.auth.dao.city_dao import CityDAO
from my_project.auth.domain.city import City


class CityService:
    def __init__(self):
        self.dao = CityDAO()

    def get_all(self) -> list[City]:
        return self.dao.find_all()

    def get_by_id(self, city_id: int) -> City | None:
        return self.dao.find_by_id(city_id)

    def create(self, city: City) -> City:
        return self.dao.create(city)

    def update(self, city_id: int, city: City) -> bool:
        return self.dao.update(city_id, city)

    def delete(self, city_id: int) -> bool:
        return self.dao.delete(city_id)

    def get_cities_with_stations(self) -> list[dict]:
        return self.dao.get_cities_with_stations()

    def get_trips_with_drivers(self) -> list[dict]:
        return self.dao.get_trips_with_drivers()