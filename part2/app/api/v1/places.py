from flask_restx import Namespace, Resource, fields

api_places = Namespace('places', description='Place operations')

# Model for Swagger documentation
place_model = api_places.model('Place', {
    'name': fields.String(required=True),
    'description': fields.String,
    'owner_id': fields.String(required=True),
    'amenity_ids': fields.List(fields.String),
    'price_by_night': fields.Float(required=True),
    'latitude': fields.Float,
    'longitude': fields.Float
})

@api_places.route('/')
class PlaceList(Resource):
    @api_places.marshal_list_with(place_model)
    def get(self):
        """List all places"""
        return {'message': 'Place endpoint will be implemented'}, 200
    
    @api_places.expect(place_model)
    @api_places.marshal_with(place_model, code=201)
    def post(self):
        """Create a new place"""
        return {'message': 'Create place endpoint will be implemented'}, 201

@api_places.route('/<place_id>')
class Place(Resource):
    @api_places.marshal_with(place_model)
    def get(self, place_id):
        """Get place by ID"""
        return {'message': f'Get place {place_id} endpoint will be implemented'}, 200
    
    @api_places.expect(place_model)
    @api_places.marshal_with(place_model)
    def put(self, place_id):
        """Update place"""
        return {'message': f'Update place {place_id} endpoint will be implemented'}, 200
    
    def delete(self, place_id):
        """Delete place"""
        return {'message': f'Delete place {place_id} endpoint will be implemented'}, 200
