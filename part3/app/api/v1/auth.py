from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import create_access_token
from app.services import facade  # Your HBnBFacade service

api = Namespace('auth', description='Authentication operations')

# Model for input validation
login_model = api.model('Login', {
    'email': fields.String(required=True, description='User email'),
    'password': fields.String(required=True, description='User password')
})

@api.route('/login')
class Login(Resource):
    @api.expect(login_model)
    def post(self):
        """Authenticate user and return a JWT token"""
        credentials = api.payload

        # Step 1: Retrieve the user by email
        user = facade.get_user_by_email(credentials['email'])

        # Step 2: Verify password
        if not user or not user.verify_password(credentials['password']):
            return {'error': 'Invalid credentials'}, 401

        # Step 3: Create JWT token with user ID and is_admin
        access_token = create_access_token(
            identity=str(user.id),
            additional_claims={"is_admin": user.is_admin}
        )

        # Step 4: Return JWT token
        return {'access_token': access_token}, 200
