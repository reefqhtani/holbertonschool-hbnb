from app.business.models import User, Place, Amenity, Review
from app.business.exceptions import ValidationError

# User
u = User(email="test@example.com", first_name="A", last_name="B", password="secret12")
assert u.to_dict()["email"] == "test@example.com"

# Amenity
a = Amenity(name="WiFi")

# Place with amenity relationship via IDs
p = Place(
    title="My place",
    description="Nice",
    price_per_night=100,
    latitude=24.7136,
    longitude=46.6753,
    owner_id=u.id,
)
p.add_amenity(a.id)
assert a.id in p.amenity_ids

# Review relationship via foreign keys (user_id/place_id)
r = Review(text="Great", rating=5, user_id=u.id, place_id=p.id)

# Validation check
try:
    Review(text="", rating=7, user_id="x", place_id="y")
    raise RuntimeError("Expected ValidationError not raised")
except ValidationError:
    pass

print("OK: models created and validated")
