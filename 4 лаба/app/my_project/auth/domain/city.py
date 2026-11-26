class City:
    def __init__(self, id: int = None, name: str = "", country: str = ""):
        self.id = id
        self.name = name
        self.country = country

    def put_into_dto(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "country": self.country
        }

    @staticmethod
    def create_from_dto(dto_dict: dict) -> "City":
        return City(
            id=dto_dict.get("id"),
            name=dto_dict.get("name"),
            country=dto_dict.get("country")
        )