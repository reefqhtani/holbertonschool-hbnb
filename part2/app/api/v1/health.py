from flask_restx import Namespace, Resource

api_health = Namespace('health', description='Health check')

@api_health.route('/')
class Health(Resource):
    def get(self):
        return {'status': 'healthy'}, 200
