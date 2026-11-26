import mysql.connector
from my_project.auth.domain.city import City


class CityDAO:
    def _get_connection(self):
        cfg = {}
        with open("config/app.yml", "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if ":" in line and not line.startswith("mysql"):
                    k, v = line.split(":", 1)
                    cfg[k.strip()] = v.strip()
        return mysql.connector.connect(**cfg)
    
    def find_all(self) -> list[City]:
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, country FROM cities")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return [City(id=r[0], name=r[1], country=r[2]) for r in rows]

    def find_by_id(self, city_id: int) -> City | None:
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, country FROM cities WHERE id = %s", (city_id,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        return City(id=row[0], name=row[1], country=row[2]) if row else None

    def create(self, city: City) -> City:
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO cities (name, country) VALUES (%s, %s)", (city.name, city.country))
        conn.commit()
        city.id = cursor.lastrowid
        cursor.close()
        conn.close()
        return city

    def update(self, city_id: int, city: City) -> bool:
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE cities SET name = %s, country = %s WHERE id = %s",
            (city.name, city.country, city_id)
        )
        conn.commit()
        updated = cursor.rowcount > 0
        cursor.close()
        conn.close()
        return updated

    def delete(self, city_id: int) -> bool:
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM cities WHERE id = %s", (city_id,))
        conn.commit()
        deleted = cursor.rowcount > 0
        cursor.close()
        conn.close()
        return deleted

    def get_cities_with_stations(self) -> list[dict]:
        conn = self._get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT c.id AS city_id, c.name AS city_name, c.country,
                   s.id AS station_id, s.station_name, s.address
            FROM cities c
            LEFT JOIN stations s ON c.id = s.city_id
            ORDER BY c.id
        """)
        rows = cursor.fetchall()
        cursor.close()
        conn.close()

        result = {}
        for r in rows:
            cid = r["city_id"]
            if cid not in result:
                result[cid] = {
                    "city_id": cid,
                    "city_name": r["city_name"],
                    "country": r["country"],
                    "stations": []
                }
            if r["station_id"] is not None:
                result[cid]["stations"].append({
                    "station_id": r["station_id"],
                    "station_name": r["station_name"],
                    "address": r["address"]
                })
        return list(result.values())

    def get_trips_with_drivers(self) -> list[dict]:
        conn = self._get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT t.id AS trip_id, r.route_code, t.departure_time, t.status,
                   d.id AS driver_id, d.first_name, d.last_name, td.role
            FROM trips t
            JOIN routes r ON t.route_id = r.id
            LEFT JOIN trip_drivers td ON t.id = td.trip_id
            LEFT JOIN drivers d ON td.driver_id = d.id
            ORDER BY t.id
        """)
        rows = cursor.fetchall()
        cursor.close()
        conn.close()

        result = {}
        for r in rows:
            tid = r["trip_id"]
            if tid not in result:
                result[tid] = {
                    "trip_id": tid,
                    "route_code": r["route_code"],
                    "departure_time": str(r["departure_time"]),
                    "status": r["status"],
                    "drivers": []
                }
            if r["driver_id"] is not None:
                result[tid]["drivers"].append({
                    "driver_id": r["driver_id"],
                    "full_name": f"{r['first_name']} {r['last_name']}",
                    "role": r["role"]
                })
        return list(result.values())