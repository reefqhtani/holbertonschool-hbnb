from flask_restx import Namespace, Resource, fields
from business.user import User
from persistence.repository import Repository

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
