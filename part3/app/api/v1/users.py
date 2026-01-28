from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services import facade

api = Namespace('users', description='User operations')

user_update_model = api.model('UserUpdate', {
    'first_name': fields.String(required=False),
    'last_name': fields.String(required=False)
})

@api.route('/<user_id>')
class UserResource(Resource):
    @jwt_required()
    @api.expect(user_update_model)
    def put(self, user_id):
        """Update user info (self only, no email/password)"""
        current_user = get_jwt_identity()
        if user_id != current_user:
            return {'error': 'Unauthorized action'}, 403

        data = api.payload
        if 'email' in data or 'password' in data:
            return {'error': 'You cannot modify email or password'}, 400

        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404

        user.update(data)
        facade.save_user(user)
        return user.to_dict(), 200
