from flask_restx import Namespace, Resource, fields
from business.amenity import Amenity
from persistence.repository import Repository
from flask_restx import Namespace, Resource, fields
from business.user import User
from persistence.repository import Repository

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
