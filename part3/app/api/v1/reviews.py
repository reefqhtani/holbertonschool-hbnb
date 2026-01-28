from flask import request
from flask_restx import Namespace, Resource
from flask_jwt_extended import jwt_required, get_jwt
from app.services import facade

api = Namespace('reviews', description='Review operations')

@api.route('/')
class ReviewList(Resource):
    @jwt_required()
    def post(self):
        """Create a review if user is authenticated and not the owner"""
        current_user = get_jwt()
        user_id = current_user.get('id')

        data = request.json
        place = facade.get_place(data.get('place_id'))
        if not place:
            return {'error': 'Place not found'}, 404

        if place.owner_id == user_id:
            return {'error': 'You cannot review your own place'}, 400

        existing_review = facade.get_user_review_for_place(user_id, place.id)
        if existing_review:
            return {'error': 'You have already reviewed this place'}, 400

        data['user_id'] = user_id
        review = facade.create_review(data)
        return review.to_dict(), 201

@api.route('/<review_id>')
class ReviewResource(Resource):
    @jwt_required()
    def put(self, review_id):
        """Update a review if owner or admin"""
        current_user = get_jwt()
        is_admin = current_user.get('is_admin', False)
        user_id = current_user.get('id')

        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404

        if not is_admin and review.user_id != user_id:
            return {'error': 'Unauthorized action'}, 403

        data = request.json
        updated_review = facade.update_review(review_id, data)
        return updated_review.to_dict(), 200

    @jwt_required()
    def delete(self, review_id):
        """Delete a review if owner or admin"""
        current_user = get_jwt()
        is_admin = current_user.get('is_admin', False)
        user_id = current_user.get('id')

        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404

        if not is_admin and review.user_id != user_id:
            return {'error': 'Unauthorized action'}, 403

        facade.delete_review(review_id)
        return {}, 204
