from flask import Flask
from flask_restx import Api
from app.api.v1.routes import api as api_v1
from app.api.v1.routes import api_users

api.add_namespace(api_users, path="/api/v1/users")


def create_app():
    app = Flask(__name__)
    api = Api(app, title="HBnB API", version="1.0")

    api.add_namespace(api_v1, path="/api/v1")
    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host="0.0.0.0", port=5000i)
