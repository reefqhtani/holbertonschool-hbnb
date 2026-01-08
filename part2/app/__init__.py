from flask import Flask
from .config import Config
from .extensions import restx_api
from .api.v1.routes import register_v1

def create_app(config_object=Config) -> Flask:
    app = Flask(__name__)
    app.config.from_object(config_object)

    restx_api.init_app(app)
    register_v1(restx_api)

    return app
