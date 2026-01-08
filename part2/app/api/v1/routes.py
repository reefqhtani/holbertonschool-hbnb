from flask_restx import Api
from .namespaces.health import ns as health_ns

def register_v1(api: Api) -> None:
    api.add_namespace(health_ns, path="/api/v1/health")
