from flask_restx import Namespace, Resource, fields

from app.business.user import User
from app.business.place import Place
from app.business.review import Review
from app.business.amenity import Amenity
from app.persistence.repository import Repository

# =====================================================
# Shared Repository (IMPORTANT: only ONE instance)
# =====================================================
repo = Repository()

# =====================================================
# Namespaces
# =====================================================
api_health = Namespace('health', description='Health check')
api_users = Namespace('users', description='User operations')
api_amenities = Namespace('amenities', description='Amenity operations')
api_places = Namespace('places', description='Place operations')
api_reviews = Namespace('reviews', description='Review operations')

# =====================================================
# Models (Swagger)
# =====================================================
user_model = api_users.model('User', {
    'email': fields.String(required=True),
    'password': fields.String(required=True),
    'first_name': fields.String,
    'last_name': fields.String
})

amenity_model = api_amenities.model('Amenity', {
    'name': fields.String(required=True)
})

place_model = api_places.model('Place', {
    'name': fields.String(required=True),
    'description': fields.String,
    'owner_id': fields.String(required=True),
    'amenity_ids': fields.List(fields.String),
    'price_by_night': fields.Float(required=True),
    'latitude': fields.Float,
    'longitude': fields.Float
})

review_model = api_reviews.model('Review', {
    'user_id': fields.String(required=True),
    'place_id': fields.String(required=True),
    'text': fields.String(required=True)
})

# =====================================================
# Health
# =====================================================
@api_health.route('/')
class Health(Resource):
    def get(self):
        return {"status": "HBnB API running"}, 200

# =====================================================
# Users
# =====================================================
@api_users.route('/')
class UserList(Resource):
    @api_users.expect(user_model)
    def post(self):
        data = api_users.payload

        if not data.get('email'):
            return {"message": "Email is required"}, 400
        if not data.get('password'):
            return {"message": "Password is required"}, 400

        user = User(
            email=data['email'],
            password=data['password'],
            first_name=data.get('first_name'),
            last_name=data.get('last_name')
        )
        repo.add('User', user)

        result = user.to_dict()
        result.pop('password', None)
        return result, 201

    def get(self):
        users = repo.all('User')
        result = []
        for u in users:
            d = u.to_dict()
            d.pop('password', None)
            result.append(d)
        return result, 200


@api_users.route('/<string:user_id>')
class UserItem(Resource):
    def get(self, user_id):
        user = repo.get('User', user_id)
        if not user:
            return {"message": "User not found"}, 404
        d = user.to_dict()
        d.pop('password', None)
        return d, 200

    @api_users.expect(user_model)
    def put(self, user_id):
        user = repo.get('User', user_id)
        if not user:
            return {"message": "User not found"}, 404

        data = api_users.payload
        user.first_name = data.get('first_name', user.first_name)
        user.last_name = data.get('last_name', user.last_name)
        user.email = data.get('email', user.email)
        if 'password' in data:
            user.password = data['password']

        user.save()
        d = user.to_dict()
        d.pop('password', None)
        return d, 200

# =====================================================
# Amenities
# =====================================================
@api_amenities.route('/')
class AmenityList(Resource):
    @api_amenities.expect(amenity_model)
    def post(self):
        data = api_amenities.payload
        if not data.get('name'):
            return {"message": "Amenity name required"}, 400

        amenity = Amenity(name=data['name'])
        repo.add('Amenity', amenity)
        return amenity.to_dict(), 201

    def get(self):
        return [a.to_dict() for a in repo.all('Amenity')], 200


@api_amenities.route('/<string:amenity_id>')
class AmenityItem(Resource):
    def get(self, amenity_id):
        amenity = repo.get('Amenity', amenity_id)
        if not amenity:
            return {"message": "Amenity not found"}, 404
        return amenity.to_dict(), 200

    @api_amenities.expect(amenity_model)
    def put(self, amenity_id):
        amenity = repo.get('Amenity', amenity_id)
        if not amenity:
            return {"message": "Amenity not found"}, 404

        data = api_amenities.payload
        amenity.name = data.get('name', amenity.name)
        amenity.save()
        return amenity.to_dict(), 200

# =====================================================
# Places
# =====================================================
@api_places.route('/')
class PlaceList(Resource):
    @api_places.expect(place_model)
    def post(self):
        data = api_places.payload

        owner = repo.get('User', data.get('owner_id'))
        if not owner:
            return {"message": "Owner not found"}, 400

        try:
            price = float(data['price_by_night'])
        except Exception:
            return {"message": "price_by_night must be a number"}, 400

        amenities = []
        for aid in data.get('amenity_ids', []):
            amenity = repo.get('Amenity', aid)
            if not amenity:
                return {"message": f"Amenity {aid} not found"}, 400
            amenities.append(amenity)

        place = Place(
            name=data['name'],
            description=data.get('description'),
            owner_id=owner.id,
            amenities=amenities,
            price_by_night=price,
            latitude=data.get('latitude'),
            longitude=data.get('longitude')
        )
        repo.add('Place', place)

        result = place.to_dict()
        result['owner'] = {
            "first_name": owner.first_name,
            "last_name": owner.last_name
        }
        return result, 201

    def get(self):
        result = []
        for p in repo.all('Place'):
            owner = repo.get('User', p.owner_id)
            d = p.to_dict()
            if owner:
                d['owner'] = {
                    "first_name": owner.first_name,
                    "last_name": owner.last_name
                }
            result.append(d)
        return result, 200


@api_places.route('/<string:place_id>')
class PlaceItem(Resource):
    def get(self, place_id):
        place = repo.get('Place', place_id)
        if not place:
            return {"message": "Place not found"}, 404

        owner = repo.get('User', place.owner_id)
        d = place.to_dict()
        if owner:
            d['owner'] = {
                "first_name": owner.first_name,
                "last_name": owner.last_name
            }
        return d, 200

    @api_places.expect(place_model)
    def put(self, place_id):
        place = repo.get('Place', place_id)
        if not place:
            return {"message": "Place not found"}, 404

        data = api_places.payload
        place.name = data.get('name', place.name)
        place.description = data.get('description', place.description)
        place.price_by_night = data.get('price_by_night', place.price_by_night)
        place.latitude = data.get('latitude', place.latitude)
        place.longitude = data.get('longitude', place.longitude)
        place.save()
        return place.to_dict(), 200

# =====================================================
# Reviews (WITH DELETE)
# =====================================================
@api_reviews.route('/')
class ReviewList(Resource):
    @api_reviews.expect(review_model)
    def post(self):
        data = api_reviews.payload

        if not repo.get('User', data.get('user_id')):
            return {"message": "User not found"}, 400
        if not repo.get('Place', data.get('place_id')):
            return {"message": "Place not found"}, 400
        if not data.get('text'):
            return {"message": "Review text required"}, 400

        review = Review(
            user_id=data['user_id'],
            place_id=data['place_id'],
            text=data['text']
        )
        repo.add('Review', review)
        return review.to_dict(), 201

    def get(self):
        return [r.to_dict() for r in repo.all('Review')], 200


@api_reviews.route('/<string:review_id>')
class ReviewItem(Resource):
    def get(self, review_id):
        review = repo.get('Review', review_id)
        if not review:
            return {"message": "Review not found"}, 404
        return review.to_dict(), 200

    @api_reviews.expect(review_model)
    def put(self, review_id):
        review = repo.get('Review', review_id)
        if not review:
            return {"message": "Review not found"}, 404

        review.text = api_reviews.payload.get('text', review.text)
        review.save()
        return review.to_dict(), 200

    def delete(self, review_id):
        review = repo.get('Review', review_id)
        if not review:
            return {"message": "Review not found"}, 404
        repo.delete('Review', review_id)
        return {}, 204

