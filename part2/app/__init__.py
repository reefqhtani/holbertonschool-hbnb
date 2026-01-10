from flask import Flask
from flask_restx import Api

def create_app():
    app = Flask(__name__)
    
    # Configure the API
    api = Api(app, 
              version='1.0', 
              title='HBnB API', 
              description='HBnB Application API',
              doc='/api/v1/')
    
    # Import and register namespaces
    from app.api.v1.health import api_health
    from app.api.v1.users import api_users
    from app.api.v1.places import api_places
    from app.api.v1.reviews import api_reviews
    from app.api.v1.amenities import api_amenities
    
    api.add_namespace(api_health, path='/api/v1/health')
    api.add_namespace(api_users, path='/api/v1/users')
    api.add_namespace(api_places, path='/api/v1/places')
    api.add_namespace(api_reviews, path='/api/v1/reviews')
    api.add_namespace(api_amenities, path='/api/v1/amenities')
    
    return app
