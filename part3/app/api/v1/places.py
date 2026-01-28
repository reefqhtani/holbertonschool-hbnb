from flask import request
from flask_restx import Namespace, Resource
from flask_jwt_extended import jwt_required, get_jwt
from app.services import facade

api = Namespace('places', description='Place operations')

@api.route('/')
class PlaceList(Resource):
    @jwt_required()
    def post(self):
        """Create a new place for the logged-in user"""
        current_user = get_jwt()
        user_id = current_user.get('id')

        data = request.json
        data['owner_id'] = user_id  # assign owner

        place = facade.create_place(data)
        return place.to_dict(), 201

@api.route('/<place_id>')
class PlaceResource(Resource):
    @jwt_required()
    def put(self, place_id):
        """Update a place, only owner or admin"""
        current_user = get_jwt()
        is_admin = current_user.get('is_admin', False)
        user_id = current_user.get('id')

        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404

        # Admin bypasses ownership restriction
        if not is_admin and place.owner_id != user_id:
            return {'error': 'Unauthorized action'}, 403

        data = request.json
        updated_place = facade.update_place(place_id, data)
        return updated_place.to_dict(), 200

    @jwt_required()
    def delete(self, place_id):
        """Delete a place, only owner or admin"""
        current_user = get_jwt()
        is_admin = current_user.get('is_admin', False)
        user_id = current_user.get('id')

        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404

        if not is_admin and place.owner_id != user_id:
            return {'error': 'Unauthorized action'}, 403

        facade.delete_place(place_id)
        return {}, 204
