from flask_restx import Namespace, Resource, fields

api_users = Namespace('users', description='User operations')

# Model for Swagger documentation
user_model = api_users.model('User', {
    'email': fields.String(required=True),
    'password': fields.String(required=True),
    'first_name': fields.String,
    'last_name': fields.String
})

@api_users.route('/')
class UserList(Resource):
    @api_users.marshal_list_with(user_model)
    def get(self):
        """List all users"""
        return {'message': 'User endpoint will be implemented'}, 200
    
    @api_users.expect(user_model)
    @api_users.marshal_with(user_model, code=201)
    def post(self):
        """Create a new user"""
        return {'message': 'Create user endpoint will be implemented'}, 201

@api_users.route('/<user_id>')
class User(Resource):
    @api_users.marshal_with(user_model)
    def get(self, user_id):
        """Get user by ID"""
        return {'message': f'Get user {user_id} endpoint will be implemented'}, 200
    
    @api_users.expect(user_model)
    @api_users.marshal_with(user_model)
    def put(self, user_id):
        """Update user"""
        return {'message': f'Update user {user_id} endpoint will be implemented'}, 200
    
    def delete(self, user_id):
        """Delete user"""
        return {'message': f'Delete user {user_id} endpoint will be implemented'}, 200
