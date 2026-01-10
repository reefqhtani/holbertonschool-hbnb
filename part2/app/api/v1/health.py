from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('health', description='Health check')

health_response_model = api.model('HealthResponse', {
    'status': fields.String(description='Overall status'),
    'timestamp': fields.DateTime(description='Current timestamp'),
    'services': fields.Raw(description='Service status'),
    'counts': fields.Raw(description='Entity counts')
})

@api.route('/')
class Health(Resource):
    @api.marshal_with(health_response_model)
    def get(self):
        """Get system health status"""
        from datetime import datetime
        
        # Get counts from facade
        user_count = len(facade.get_all_users())
        place_count = len(facade.get_all_places())
        review_count = len(facade.get_all_reviews())
        amenity_count = len(facade.get_all_amenities())
        
        return {
            'status': 'healthy',
            'timestamp': datetime.now(),
            'services': {
                'database': 'connected',
                'api': 'running'
            },
            'counts': {
                'users': user_count,
                'places': place_count,
                'reviews': review_count,
                'amenities': amenity_count
            }
        }, 200
