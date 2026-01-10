from flask_restx import Namespace, Resource, fields

api = Namespace('users', description='User operations')

# Model for Swagger documentation
user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name'),
    'last_name': fields.String(required=True, description='Last name'),
    'email': fields.String(required=True, description='Email address'),
    'password': fields.String(description='Password'),
    'is_admin': fields.Boolean(default=False, description='Is admin')
})

user_response_model = api.model('UserResponse', {
    'id': fields.String(readonly=True, description='User ID'),
    'first_name': fields.String(description='First name'),
    'last_name': fields.String(description='Last name'),
    'email': fields.String(description='Email address'),
    'is_admin': fields.Boolean(description='Is admin'),
    'created_at': fields.DateTime(description='Creation timestamp'),
    'updated_at': fields.DateTime(description='Last update timestamp')
})

@api.route('/')
class UserList(Resource):
    @api.marshal_list_with(user_response_model)
    @api.response(200, 'List of users retrieved successfully')
    def get(self):
        """List all users"""
        from app.services import facade
        users = facade.get_all_users()
        return [user.to_dict() for user in users], 200
    
    @api.expect(user_model, validate=True)
    @api.marshal_with(user_response_model, code=201)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Create a new user"""
        from app.services import facade
        data = api.payload
        
        # Check if email already exists
        existing_user = facade.get_user_by_email(data.get('email'))
        if existing_user:
            api.abort(400, f"Email {data.get('email')} already registered")
        
        try:
            user = facade.create_user(data)
            return user.to_dict(), 201
        except ValueError as e:
            api.abort(400, str(e))

@api.route('/<string:user_id>')
class UserResource(Resource):
    @api.marshal_with(user_response_model)
    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """Get user details by ID"""
        from app.services import facade
        user = facade.get_user(user_id)
        if not user:
            api.abort(404, f"User {user_id} not found")
        return user.to_dict(), 200
    
    @api.expect(user_model, validate=True)
    @api.marshal_with(user_response_model)
    @api.response(200, 'User successfully updated')
    @api.response(404, 'User not found')
    @api.response(400, 'Invalid input data')
    def put(self, user_id):
        """Update user information"""
        from app.services import facade
        data = api.payload
        
        # Check if user exists
        user = facade.get_user(user_id)
        if not user:
            api.abort(404, f"User {user_id} not found")
        
        # Check if email is being changed and if new email already exists
        if 'email' in data and data['email'] != user.email:
            existing_user = facade.get_user_by_email(data['email'])
            if existing_user:
                api.abort(400, f"Email {data['email']} already registered")
        
        try:
            updated_user = facade.update_user(user_id, data)
            if updated_user:
                return updated_user.to_dict(), 200
            api.abort(404, f"User {user_id} not found")
        except ValueError as e:
            api.abort(400, str(e))
