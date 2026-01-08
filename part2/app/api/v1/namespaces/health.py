from flask_restx import Namespace, Resource

ns = Namespace("health", description="Health checks")

@ns.route("/")
class HealthResource(Resource):
    def get(self):
        return {"status": "ok"}, 200
