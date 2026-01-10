from flask_restx import Namespace, Resource, fields

api_amenities = Namespace('amenities', description='Amenity operations')

# Model for Swagger documentation
amenity_model = api_amenities.model('Amenity', {
    'name': fields.String(required=True, description='Amenity name')
})

amenity_response_model = api_amenities.model('AmenityResponse', {
    'id': fields.String(readonly=True, description='Amenity ID'),
    'name': fields.String(description='Amenity name'),
    'created_at': fields.DateTime(description='Creation timestamp'),
    'updated_at': fields.DateTime(description='Last update timestamp')
})

@api_amenities.route('/')
class AmenityList(Resource):
    @api_amenities.marshal_list_with(amenity_response_model)
    def get(self):
        """List all amenities"""
        from app.services import facade
        amenities = facade.get_all_amenities()
        return [amenity.to_dict() for amenity in amenities], 200
    
    @api_amenities.expect(amenity_model)
    @api_amenities.marshal_with(amenity_response_model, code=201)
    @api_amenities.response(400, 'Invalid input data')
    def post(self):
        """Create a new amenity"""
        from app.services import facade
        data = api_amenities.payload
        
        try:
            amenity = facade.create_amenity(data)
            return amenity.to_dict(), 201
        except ValueError as e:
            api_amenities.abort(400, str(e))

@api_amenities.route('/<string:amenity_id>')
class Amenity(Resource):
    @api_amenities.marshal_with(amenity_response_model)
    @api_amenities.response(404, 'Amenity not found')
    def get(self, amenity_id):
        """Get amenity by ID"""
        from app.services import facade
        amenity = facade.get_amenity(amenity_id)
        if amenity:
            return amenity.to_dict(), 200
        api_amenities.abort(404, f"Amenity {amenity_id} not found")
    
    @api_amenities.expect(amenity_model)
    @api_amenities.marshal_with(amenity_response_model)
    @api_amenities.response(404, 'Amenity not found')
    @api_amenities.response(400, 'Invalid input data')
    def put(self, amenity_id):
        """Update amenity"""
        from app.services import facade
        data = api_amenities.payload
        
        amenity = facade.update_amenity(amenity_id, data)
        if amenity:
            return amenity.to_dict(), 200
        api_amenities.abort(404, f"Amenity {amenity_id} not found")
    
    @api_amenities.response(200, 'Amenity deleted')
    @api_amenities.response(404, 'Amenity not found')
    def delete(self, amenity_id):
        """Delete amenity"""
        from app.services import facade
        success = facade.delete_amenity(amenity_id)
        if success:
            return {'message': f'Amenity {amenity_id} deleted'}, 200
        api_amenities.abort(404, f"Amenity {amenity_id} not found")
