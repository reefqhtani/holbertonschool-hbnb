from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from config import config
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
jwt = JWTManager()
bcrypt = Bcrypt()

def create_app(config_class=config.DevelopmentConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)
    bcrypt.init_app(app)

    # Import and register namespaces (example)
    from app.api.v1.auth import api as auth_ns
    from app.api.v1.places import api as places_ns
    from app.api.v1.reviews import api as reviews_ns

    from flask_restx import Api
    api = Api(app)
    api.add_namespace(auth_ns, path='/api/v1/auth')
    api.add_namespace(places_ns, path='/api/v1/places')
    api.add_namespace(reviews_ns, path='/api/v1/reviews')

    return app
