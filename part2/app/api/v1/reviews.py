from flask_restx import Namespace, Resource, fields

api_reviews = Namespace('reviews', description='Review operations')

# Model for Swagger documentation
review_model = api_reviews.model('Review', {
    'user_id': fields.String(required=True),
    'place_id': fields.String(required=True),
    'text': fields.String(required=True)
})

@api_reviews.route('/')
class ReviewList(Resource):
    @api_reviews.marshal_list_with(review_model)
    def get(self):
        """List all reviews"""
        return {'message': 'Review endpoint will be implemented'}, 200
    
    @api_reviews.expect(review_model)
    @api_reviews.marshal_with(review_model, code=201)
    def post(self):
        """Create a new review"""
        return {'message': 'Create review endpoint will be implemented'}, 201

@api_reviews.route('/<review_id>')
class Review(Resource):
    @api_reviews.marshal_with(review_model)
    def get(self, review_id):
        """Get review by ID"""
        return {'message': f'Get review {review_id} endpoint will be implemented'}, 200
    
    @api_reviews.expect(review_model)
    @api_reviews.marshal_with(review_model)
    def put(self, review_id):
        """Update review"""
        return {'message': f'Update review {review_id} endpoint will be implemented'}, 200
    
    def delete(self, review_id):
        """Delete review"""
        return {'message': f'Delete review {review_id} endpoint will be implemented'}, 200
