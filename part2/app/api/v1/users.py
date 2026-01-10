from flask_restx import Namespace, Resource, fields

api_users = Namespace('users', description='User operations')

# Model for Swagger documentation
user_model = api_users.model('User', {
    'first_name': fields.String(required=True, description='First name'),
    'last_name': fields.String(required=True, description='Last name'),
    'email': fields.String(required=True, description='Email address'),
    'password': fields.String(required=True, description='Password'),
    'is_admin': fields.Boolean(default=False, description='Is admin')
})

user_response_model = api_users.model('UserResponse', {
    'id': fields.String(readonly=True, description='User ID'),
    'first_name': fields.String(description='First name'),
    'last_name': fields.String(description='Last name'),
    'email': fields.String(description='Email address'),
    'is_admin': fields.Boolean(description='Is admin'),
    'created_at': fields.DateTime(description='Creation timestamp'),
    'updated_at': fields.DateTime(description='Last update timestamp')
})

@api_users.route('/')
class UserList(Resource):
    @api_users.marshal_list_with(user_response_model)
    def get(self):
        """List all users"""
        from app.services import facade
        users = facade.get_all_users()
        return [user.to_dict() for user in users], 200
    
    @api_users.expect(user_model)
    @api_users.marshal_with(user_response_model, code=201)
    @api_users.response(400, 'Invalid input data')
    def post(self):
        """Create a new user"""
        from app.services import facade
        data = api_users.payload
        
        # Check if email already exists
        existing_user = facade.get_user_by_email(data.get('email'))
        if existing_user:
            api_users.abort(400, f"User with email {data.get('email')} already exists")
        
        try:
            user = facade.create_user(data)
            return user.to_dict(), 201
        except ValueError as e:
            api_users.abort(400, str(e))

@api_users.route('/<string:user_id>')
class User(Resource):
    @api_users.marshal_with(user_response_model)
    @api_users.response(404, 'User not found')
    def get(self, user_id):
        """Get user by ID"""
        from app.services import facade
        user = facade.get_user(user_id)
        if user:
            return user.to_dict(), 200
        api_users.abort(404, f"User {user_id} not found")
    
    @api_users.expect(user_model)
    @api_users.marshal_with(user_response_model)
    @api_users.response(404, 'User not found')
    @api_users.response(400, 'Invalid input data')
    def put(self, user_id):
        """Update user"""
        from app.services import facade
        data = api_users.payload
        
        # Don't allow updating email via PUT for now
        if 'email' in data:
            del data['email']
        
        user = facade.update_user(user_id, data)
        if user:
            return user.to_dict(), 200
        api_users.abort(404, f"User {user_id} not found")
    
    @api_users.response(200, 'User deleted')
    @api_users.response(404, 'User not found')
    def delete(self, user_id):
        """Delete user"""
        from app.services import facade
        success = facade.delete_user(user_id)
        if success:
            return {'message': f'User {user_id} deleted'}, 200
        api_users.abort(404, f"User {user_id} not found")
