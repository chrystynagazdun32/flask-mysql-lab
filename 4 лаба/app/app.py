from flask import Flask
from my_project.auth.route.city_route import city_bp

app = Flask(__name__)
app.json.ensure_ascii = False
app.register_blueprint(city_bp)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
    