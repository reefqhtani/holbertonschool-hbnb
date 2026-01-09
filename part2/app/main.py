from flask import Flask
from flask_restx import Api

from app.api.v1.routes import (
    api_health,
    api_users,
    api_amenities,
    api_places,
    api_reviews
)


def create_app():
    app = Flask(__name__)

    api = Api(
        app,
        title="HBnB API",
        version="1.0",
        description="HBnB Application API"
    )

    # Register namespaces
    api.add_namespace(api_health, path="/api/v1/health")
    api.add_namespace(api_users, path="/api/v1/users")
    api.add_namespace(api_amenities, path="/api/v1/amenities")
    api.add_namespace(api_places, path="/api/v1/places")
    api.add_namespace(api_reviews, path="/api/v1/reviews")

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host="0.0.0.0", port=5000)    
