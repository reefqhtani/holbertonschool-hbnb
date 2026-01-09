from business.place import Place
from business.user import User
from business.amenity import Amenity
from persistence.repository import Repository
from flask_restx import Namespace, Resource, fields
from flask_restx import Namespace, Resource, fields
from business.amenity import Amenity
from persistence.repository import Repository
from flask_restx import Namespace, Resource, fields
from business.user import User
from persistence.repository import Repository

# Namespace for places
api_places = Namespace('places', description='Place operations')

# Reuse in-memory repository
repo = Repository()

place_model = api_places.model('Place', {
    'name': fields.String(required=True, description="Place name"),
    'description': fields.String(required=False, description="Place description"),
    'owner_id': fields.String(required=True, description="ID of the owner user"),
    'amenity_ids': fields.List(fields.String, description="List of Amenity IDs"),
    'price_by_night': fields.Float(required=True, description="Price per night"),
    'latitude': fields.Float(required=False, description="Latitude"),
    'longitude': fields.Float(required=False, description="Longitude")
})

@api_places.route('/')
class PlaceList(Resource):
    @api_places.expect(place_model)
    def post(self):
        """Create a new place"""
        data = api_places.payload

        # Validate owner exists
        owner_list = repo.all('User')
        if not any(u.id == data['owner_id'] for u in owner_list):
            return {"message": "Owner not found"}, 400

        # Validate amenities exist
        amenities_list = repo.all('Amenity')
        amenity_objs = []
        for amenity_id in data.get('amenity_ids', []):
            amenity = next((a for a in amenities_list if a.id == amenity_id), None)
            if amenity:
                amenity_objs.append(amenity)
            else:
                return {"message": f"Amenity {amenity_id} not found"}, 400

        new_place = Place(
            name=data['name'],
            description=data.get('description', ''),
            owner_id=data['owner_id'],
            amenities=amenity_objs,
            price_by_night=data['price_by_night'],
            latitude=data.get('latitude'),
            longitude=data.get('longitude')
        )
        repo.add('Place', new_place)

        # Return with owner details
        owner = next(u for u in owner_list if u.id == new_place.owner_id)
        place_dict = new_place.to_dict()
        place_dict['owner'] = {
            'first_name': owner.first_name,
            'last_name': owner.last_name
        }
        return place_dict, 201

    def get(self):
        """Get all places"""
        places = repo.all('Place')
        users = repo.all('User')
        result = []
        for p in places:
            owner = next((u for u in users if u.id == p.owner_id), None)
            place_dict = p.to_dict()
            if owner:
                place_dict['owner'] = {
                    'first_name': owner.first_name,
                    'last_name': owner.last_name
                }
            result.append(place_dict)
        return result, 200
@api_places.route('/<string:place_id>')
class PlaceItem(Resource):
    def get(self, place_id):
        """Get a place by ID"""
        places = repo.all('Place')
        users = repo.all('User')
        place = next((p for p in places if p.id == place_id), None)
        if not place:
            return {"message": "Place not found"}, 404

        owner = next((u for u in users if u.id == place.owner_id), None)
        place_dict = place.to_dict()
        if owner:
            place_dict['owner'] = {
                'first_name': owner.first_name,
                'last_name': owner.last_name
            }
        return place_dict, 200

    @api_places.expect(place_model)
    def put(self, place_id):
        """Update a place"""
        places = repo.all('Place')
        place = next((p for p in places if p.id == place_id), None)
        if not place:
            return {"message": "Place not found"}, 404

        data = api_places.payload
        if 'name' in data:
            place.name = data['name']
        if 'description' in data:
            place.description = data['description']
        if 'price_by_night' in data:
            place.price_by_night = data['price_by_night']
        if 'latitude' in data:
            place.latitude = data['latitude']
        if 'longitude' in data:
            place.longitude = data['longitude']

        # Update amenities if provided
        if 'amenity_ids' in data:
            amenities_list = repo.all('Amenity')
            amenity_objs = []
            for aid in data['amenity_ids']:
                amenity = next((a for a in amenities_list if a.id == aid), None)
                if amenity:
                    amenity_objs.append(amenity)
            place.amenities = amenity_objs

        place.save()

        # Return updated place with owner details
        users = repo.all('User')
        owner = next((u for u in users if u.id == place.owner_id), None)
        place_dict = place.to_dict()
        if owner:
            place_dict['owner'] = {
                'first_name': owner.first_name,
                'last_name': owner.last_name
            }
        return place_dict, 200

# Namespace for amenities
api_amenities = Namespace('amenities', description='Amenity operations')

# In-memory repository (shared with other entities)
repo = Repository()

amenity_model = api_amenities.model('Amenity', {
    'name': fields.String(required=True, description="Amenity name"),
    'description': fields.String(required=False, description="Amenity description")
})

@api_amenities.route('/')
class AmenityList(Resource):
    @api_amenities.expect(amenity_model)
    def post(self):
        """Create a new amenity"""
        data = api_amenities.payload
        new_amenity = Amenity(name=data['name'], description=data.get('description', ''))
        repo.add('Amenity', new_amenity)
        return new_amenity.to_dict(), 201

    def get(self):
        """Get list of all amenities"""
        amenities = repo.all('Amenity')
        return [a.to_dict() for a in amenities], 200

@api_amenities.route('/<string:amenity_id>')
class AmenityItem(Resource):
    def get(self, amenity_id):
        """Get an amenity by ID"""
        amenities = repo.all('Amenity')
        for a in amenities:
            if a.id == amenity_id:
                return a.to_dict(), 200
        return {"message": "Amenity not found"}, 404

    @api_amenities.expect(amenity_model)
    def put(self, amenity_id):
        """Update amenity"""
        amenities = repo.all('Amenity')
        for a in amenities:
            if a.id == amenity_id:
                data = api_amenities.payload
                a.name = data.get('name', a.name)
                a.description = data.get('description', a.description)
                a.save()
                return a.to_dict(), 200
        return {"message": "Amenity not found"}, 404

# Namespace for users
api_users = Namespace('users', description='User operations')

# In-memory repository
repo = Repository()

# User model for API documentation
user_model = api_users.model('User', {
    'first_name': fields.String(required=True, description="User's first name"),
    'last_name': fields.String(required=True, description="User's last name"),
    'email': fields.String(required=True, description="User's email"),
    'password': fields.String(required=True, description="User's password")
})

@api_users.route('/')
class UserList(Resource):
    @api_users.expect(user_model)
    def post(self):
        """Create a new user"""
        data = api_users.payload
        new_user = User(
            first_name=data['first_name'],
            last_name=data['last_name'],
            email=data['email'],
            password=data['password']
        )
        repo.add('User', new_user)
        user_dict = new_user.to_dict()
        user_dict.pop('password', None)  # do not return password
        return user_dict, 201

    def get(self):
        """Get list of all users"""
        users = repo.all('User')
        result = []
        for u in users:
            u_dict = u.to_dict()
            u_dict.pop('password', None)  # hide password
            result.append(u_dict)
        return result, 200

@api_users.route('/<string:user_id>')
class UserItem(Resource):
    def get(self, user_id):
        """Get a user by ID"""
        users = repo.all('User')
        for u in users:
            if u.id == user_id:
                u_dict = u.to_dict()
                u_dict.pop('password', None)
                return u_dict, 200
        return {"message": "User not found"}, 404

    @api_users.expect(user_model)
    def put(self, user_id):
        """Update user information"""
        users = repo.all('User')
        for u in users:
            if u.id == user_id:
                data = api_users.payload
                u.first_name = data.get('first_name', u.first_name)
                u.last_name = data.get('last_name', u.last_name)
                u.email = data.get('email', u.email)
                if 'password' in data:
                    u.password = data['password']
                u.save()
                u_dict = u.to_dict()
                u_dict.pop('password', None)
                return u_dict, 200
        return {"message": "User not found"}, 404

api = Namespace("health", description="Health check")


@api.route("/")
class Health(Resource):
    def get(self):
        return {"status": "HBnB API running"}
