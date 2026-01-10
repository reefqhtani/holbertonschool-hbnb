from flask_restx import Namespace, Resource, fields

api_places = Namespace('places', description='Place operations')

# Model for Swagger documentation
place_model = api_places.model('Place', {
    'title': fields.String(required=True, description='Place title'),
    'description': fields.String(description='Place description'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude'),
    'longitude': fields.Float(required=True, description='Longitude'),
    'owner_id': fields.String(required=True, description='Owner user ID')
})

place_response_model = api_places.model('PlaceResponse', {
    'id': fields.String(readonly=True, description='Place ID'),
    'title': fields.String(description='Place title'),
    'description': fields.String(description='Place description'),
    'price': fields.Float(description='Price per night'),
    'latitude': fields.Float(description='Latitude'),
    'longitude': fields.Float(description='Longitude'),
    'owner_id': fields.String(description='Owner user ID'),
    'created_at': fields.DateTime(description='Creation timestamp'),
    'updated_at': fields.DateTime(description='Last update timestamp'),
    'review_ids': fields.List(fields.String, description='Review IDs'),
    'amenity_ids': fields.List(fields.String, description='Amenity IDs')
})

@api_places.route('/')
class PlaceList(Resource):
    @api_places.marshal_list_with(place_response_model)
    def get(self):
        """List all places"""
        from app.services import facade
        places = facade.get_all_places()
        return [place.to_dict() for place in places], 200
    
    @api_places.expect(place_model)
    @api_places.marshal_with(place_response_model, code=201)
    @api_places.response(400, 'Invalid input data')
    def post(self):
        """Create a new place"""
        from app.services import facade
        data = api_places.payload
        
        try:
            place = facade.create_place(data)
            return place.to_dict(), 201
        except ValueError as e:
            api_places.abort(400, str(e))

@api_places.route('/<string:place_id>')
class Place(Resource):
    @api_places.marshal_with(place_response_model)
    @api_places.response(404, 'Place not found')
    def get(self, place_id):
        """Get place by ID"""
        from app.services import facade
        place = facade.get_place(place_id)
        if place:
            return place.to_dict(), 200
        api_places.abort(404, f"Place {place_id} not found")
    
    @api_places.expect(place_model)
    @api_places.marshal_with(place_response_model)
    @api_places.response(404, 'Place not found')
    @api_places.response(400, 'Invalid input data')
    def put(self, place_id):
        """Update place"""
        from app.services import facade
        data = api_places.payload
        
        place = facade.update_place(place_id, data)
        if place:
            return place.to_dict(), 200
        api_places.abort(404, f"Place {place_id} not found")
    
    @api_places.response(200, 'Place deleted')
    @api_places.response(404, 'Place not found')
    def delete(self, place_id):
        """Delete place"""
        from app.services import facade
        success = facade.delete_place(place_id)
        if success:
            return {'message': f'Place {place_id} deleted'}, 200
        api_places.abort(404, f"Place {place_id} not found")
