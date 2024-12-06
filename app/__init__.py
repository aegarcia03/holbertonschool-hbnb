from flask import Flask
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy
from app.api.v1.users import api as users_ns
from app.api.v1.amenities import api as amenities_ns
from app.api.v1.places import api as places_ns
from app.api.v1.reviews import api as reviews_ns
from flask_cors import CORS
# from app import db
# from config import config

db = SQLAlchemy()

def create_app():
    """ method used to create an app instance """
    app = Flask(__name__)
    CORS(app)
    api = Api(app, version='1.0', title='HBnB API', description='HBnB Application API')
    # Register the namespaces
    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(amenities_ns, path='/api/v1/amenities')
    api.add_namespace(places_ns, path='/api/v1/places')
    api.add_namespace(reviews_ns, path='/api/v1/reviews')

    app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'  # Use a strong and unique key in production
    jwt = JWTManager(app)

    return app