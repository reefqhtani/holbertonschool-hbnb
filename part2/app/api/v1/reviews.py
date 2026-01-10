from flask_restx import Namespace, Resource, fields

api = Namespace('reviews', description='Review operations')

# Model for Swagger documentation
review_model = api.model('Review', {
    'text': fields.String(required=True, description='Review text'),
    'rating': fields.Integer(required=True, min=1, max=5, description='Rating (1-5)'),
    'place_id': fields.String(required=True, description='Place ID'),
    'user_id': fields.String(required=True, description='User ID')
})

review_response_model = api.model('ReviewResponse', {
    'id': fields.String(readonly=True, description='Review ID'),
    'text': fields.String(description='Review text'),
    'rating': fields.Integer(description='Rating (1-5)'),
    'place_id': fields.String(description='Place ID'),
    'user_id': fields.String(description='User ID'),
    'created_at': fields.DateTime(description='Creation timestamp'),
    'updated_at': fields.DateTime(description='Last update timestamp')
})

@api.route('/')
class ReviewList(Resource):
    @api.marshal_list_with(review_response_model)
    def get(self):
        """List all reviews"""
        from app.services import facade
        reviews = facade.get_all_reviews()
        return [review.to_dict() for review in reviews], 200
    
    @api.expect(review_model)
    @api.marshal_with(review_response_model, code=201)
    @api.response(400, 'Invalid input data')
    def post(self):
        """Create a new review"""
        from app.services import facade
        data = api.payload
        
        try:
            review = facade.create_review(data)
            return review.to_dict(), 201
        except ValueError as e:
            api.abort(400, str(e))

@api.route('/<string:review_id>')
class Review(Resource):
    @api.marshal_with(review_response_model)
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """Get review by ID"""
        from app.services import facade
        review = facade.get_review(review_id)
        if review:
            return review.to_dict(), 200
        api.abort(404, f"Review {review_id} not found")
    
    @api.expect(review_model)
    @api.marshal_with(review_response_model)
    @api.response(404, 'Review not found')
    @api.response(400, 'Invalid input data')
    def put(self, review_id):
        """Update review"""
        from app.services import facade
        data = api.payload
        
        review = facade.update_review(review_id, data)
        if review:
            return review.to_dict(), 200
        api.abort(404, f"Review {review_id} not found")
    
    @api.response(200, 'Review deleted')
    @api.response(404, 'Review not found')
    def delete(self, review_id):
        """Delete review"""
        from app.services import facade
        success = facade.delete_review(review_id)
        if success:
            return {'message': f'Review {review_id} deleted'}, 200
        api.abort(404, f"Review {review_id} not found")
