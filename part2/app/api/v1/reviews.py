from flask_restx import Namespace, Resource, fields

api_reviews = Namespace('reviews', description='Review operations')

# Model for Swagger documentation
review_model = api_reviews.model('Review', {
    'text': fields.String(required=True, description='Review text'),
    'rating': fields.Integer(required=True, min=1, max=5, description='Rating (1-5)'),
    'place_id': fields.String(required=True, description='Place ID'),
    'user_id': fields.String(required=True, description='User ID')
})

review_response_model = api_reviews.model('ReviewResponse', {
    'id': fields.String(readonly=True, description='Review ID'),
    'text': fields.String(description='Review text'),
    'rating': fields.Integer(description='Rating (1-5)'),
    'place_id': fields.String(description='Place ID'),
    'user_id': fields.String(description='User ID'),
    'created_at': fields.DateTime(description='Creation timestamp'),
    'updated_at': fields.DateTime(description='Last update timestamp')
})

@api_reviews.route('/')
class ReviewList(Resource):
    @api_reviews.marshal_list_with(review_response_model)
    def get(self):
        """List all reviews"""
        from app.services import facade
        reviews = facade.get_all_reviews()
        return [review.to_dict() for review in reviews], 200
    
    @api_reviews.expect(review_model)
    @api_reviews.marshal_with(review_response_model, code=201)
    @api_reviews.response(400, 'Invalid input data')
    def post(self):
        """Create a new review"""
        from app.services import facade
        data = api_reviews.payload
        
        try:
            review = facade.create_review(data)
            return review.to_dict(), 201
        except ValueError as e:
            api_reviews.abort(400, str(e))

@api_reviews.route('/<string:review_id>')
class Review(Resource):
    @api_reviews.marshal_with(review_response_model)
    @api_reviews.response(404, 'Review not found')
    def get(self, review_id):
        """Get review by ID"""
        from app.services import facade
        review = facade.get_review(review_id)
        if review:
            return review.to_dict(), 200
        api_reviews.abort(404, f"Review {review_id} not found")
    
    @api_reviews.expect(review_model)
    @api_reviews.marshal_with(review_response_model)
    @api_reviews.response(404, 'Review not found')
    @api_reviews.response(400, 'Invalid input data')
    def put(self, review_id):
        """Update review"""
        from app.services import facade
        data = api_reviews.payload
        
        review = facade.update_review(review_id, data)
        if review:
            return review.to_dict(), 200
        api_reviews.abort(404, f"Review {review_id} not found")
    
    @api_reviews.response(200, 'Review deleted')
    @api_reviews.response(404, 'Review not found')
    def delete(self, review_id):
        """Delete review"""
        from app.services import facade
        success = facade.delete_review(review_id)
        if success:
            return {'message': f'Review {review_id} deleted'}, 200
        api_reviews.abort(404, f"Review {review_id} not found")
