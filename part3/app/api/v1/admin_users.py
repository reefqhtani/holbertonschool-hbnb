from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt
from flask import request
from app.services import facade

api = Namespace('admin_users', description='Administrator User Operations')

user_model = api.model('User', {
    'email': fields.String(required=True),
    'password': fields.String(required=True),
    'first_name': fields.String(required=False),
    'last_name': fields.String(required=False),
    'is_admin': fields.Boolean(default=False)
})

@api.route('/users/')
class AdminUserCreate(Resource):
    @jwt_required()
    @api.expect(user_model)
    def post(self):
        """Create a new user (admin only)"""
        current_user = get_jwt()
        if not current_user.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403

        data = request.json
        email = data.get('email')
        if facade.get_user_by_email(email):
            return {'error': 'Email already registered'}, 400

        user = facade.create_user(data)
        return user.to_dict(), 201

@api.route('/users/<user_id>')
class AdminUserModify(Resource):
    @jwt_required()
    @api.expect(user_model)
    def put(self, user_id):
        """Modify any user's details (admin only)"""
        current_user = get_jwt()
        if not current_user.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403

        data = request.json
        email = data.get('email')
        if email:
            existing_user = facade.get_user_by_email(email)
            if existing_user and existing_user.id != user_id:
                return {'error': 'Email is already in use'}, 400

        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404

        user.update(data)
        facade.save_user(user)
        return user.to_dict(), 200
