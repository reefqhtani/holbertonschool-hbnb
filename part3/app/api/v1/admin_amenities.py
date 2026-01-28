from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt
from flask import request
from app.services import facade

api = Namespace('admin_amenities', description='Administrator Amenity Operations')

amenity_model = api.model('Amenity', {
    'name': fields.String(required=True)
})

@api.route('/amenities/')
class AdminAmenityCreate(Resource):
    @jwt_required()
    @api.expect(amenity_model)
    def post(self):
        """Create a new amenity (admin only)"""
        current_user = get_jwt()
        if not current_user.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403

        data = request.json
        amenity = facade.create_amenity(data)
        return amenity.to_dict(), 201

@api.route('/amenities/<amenity_id>')
class AdminAmenityModify(Resource):
    @jwt_required()
    @api.expect(amenity_model)
    def put(self, amenity_id):
        """Update an amenity (admin only)"""
        current_user = get_jwt()
        if not current_user.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403

        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {'error': 'Amenity not found'}, 404

        data = request.json
        amenity.update(data)
        facade.save_amenity(amenity)
        return amenity.to_dict(), 200
