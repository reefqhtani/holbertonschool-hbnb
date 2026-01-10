from flask_restx import Namespace, Resource, fields

api_amenities = Namespace('amenities', description='Amenity operations')

# Model for Swagger documentation
amenity_model = api_amenities.model('Amenity', {
    'name': fields.String(required=True)
})

@api_amenities.route('/')
class AmenityList(Resource):
    @api_amenities.marshal_list_with(amenity_model)
    def get(self):
        """List all amenities"""
        return {'message': 'Amenity endpoint will be implemented'}, 200
    
    @api_amenities.expect(amenity_model)
    @api_amenities.marshal_with(amenity_model, code=201)
    def post(self):
        """Create a new amenity"""
        return {'message': 'Create amenity endpoint will be implemented'}, 201

@api_amenities.route('/<amenity_id>')
class Amenity(Resource):
    @api_amenities.marshal_with(amenity_model)
    def get(self, amenity_id):
        """Get amenity by ID"""
        return {'message': f'Get amenity {amenity_id} endpoint will be implemented'}, 200
    
    @api_amenities.expect(amenity_model)
    @api_amenities.marshal_with(amenity_model)
    def put(self, amenity_id):
        """Update amenity"""
        return {'message': f'Update amenity {amenity_id} endpoint will be implemented'}, 200
    
    def delete(self, amenity_id):
        """Delete amenity"""
        return {'message': f'Delete amenity {amenity_id} endpoint will be implemented'}, 200
