from flask_restx import Namespace, Resource, fields

api = Namespace('places', description='Place operations')

# Define models for related entities as per requirements
amenity_model = api.model('PlaceAmenity', {
    'id': fields.String(description='Amenity ID'),
    'name': fields.String(description='Name of the amenity')
})

user_model = api.model('PlaceUser', {
    'id': fields.String(description='User ID'),
    'first_name': fields.String(description='First name of the owner'),
    'last_name': fields.String(description='Last name of the owner'),
    'email': fields.String(description='Email of the owner')
})

# Define the place model for input validation and documentation
place_input_model = api.model('PlaceInput', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    'owner_id': fields.String(required=True, description='ID of the owner'),
    'amenities': fields.List(fields.String, required=False, description="List of amenities ID's")
})

# Response model that matches requirements
place_response_model = api.model('PlaceResponse', {
    'id': fields.String(readonly=True, description='Place ID'),
    'title': fields.String(description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(description='Price per night'),
    'latitude': fields.Float(description='Latitude of the place'),
    'longitude': fields.Float(description='Longitude of the place'),
    'owner': fields.Nested(user_model, description='Owner details'),
    'amenities': fields.List(fields.Nested(amenity_model), description='Amenities'),
    'created_at': fields.DateTime(description='Creation timestamp'),
    'updated_at': fields.DateTime(description='Last update timestamp')
})

# Simplified model for list view (just basic info)
place_list_model = api.model('PlaceList', {
    'id': fields.String(description='Place ID'),
    'title': fields.String(description='Title of the place'),
    'latitude': fields.Float(description='Latitude of the place'),
    'longitude': fields.Float(description='Longitude of the place')
})

@api.route('/')
class PlaceList(Resource):
    @api.marshal_list_with(place_list_model)
    def get(self):
        """Retrieve a list of all places"""
        from app.services import facade
        places = facade.get_all_places()
        return [{
            'id': place.id,
            'title': place.title,
            'latitude': place.latitude,
            'longitude': place.longitude
        } for place in places], 200
    
    @api.expect(place_input_model)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new place"""
        from app.services import facade
        data = api.payload
        
        try:
            # Handle amenities if provided
            amenities_ids = data.pop('amenities', [])
            place = facade.create_place(data)
            
            # Add amenities to place
            for amenity_id in amenities_ids:
                facade.add_amenity_to_place(place.id, amenity_id)
            
            # Get updated place with amenities
            place = facade.get_place(place.id)
            return place.to_dict(), 201
        except ValueError as e:
            api.abort(400, str(e))
        except Exception as e:
            api.abort(400, f"Failed to create place: {str(e)}")

@api.route('/<string:place_id>')
class PlaceResource(Resource):
    @api.marshal_with(place_response_model)
    @api.response(200, 'Place details retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get place details by ID"""
        from app.services import facade
        place = facade.get_place(place_id)
        if place:
            return place.to_dict(), 200
        api.abort(404, f"Place {place_id} not found")
    
    @api.expect(place_input_model)
    @api.response(200, 'Place updated successfully')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    def put(self, place_id):
        """Update a place's information"""
        from app.services import facade
        data = api.payload
        
        place = facade.update_place(place_id, data)
        if place:
            # Handle amenities update if provided
            if 'amenities' in data:
                # Remove all existing amenities
                current_amenities = place.get_amenities()
                for amenity in current_amenities:
                    facade.remove_amenity_from_place(place_id, amenity.id)
                # Add new amenities
                for amenity_id in data['amenities']:
                    facade.add_amenity_to_place(place_id, amenity_id)
                # Get updated place
                place = facade.get_place(place_id)
            
            return place.to_dict(), 200
        api.abort(404, f"Place {place_id} not found")
    
    # Note: DELETE endpoint removed as per instructions
