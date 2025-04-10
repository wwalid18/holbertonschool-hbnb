# part3/hbnb/app/__init__.py

import os
import sys
from flask import Flask, jsonify
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_cors import CORS  # Add CORS import

# Add the project root to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWTManager()  # Instantiate JWTManager

def create_app(config_class="config.DevelopmentConfig"):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize extensions
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)  # Register JWT middleware with the app
    
    # Configure CORS to allow requests from the front-end
    CORS(app, resources={
        r"/api/v1/*": {
            "origins": "http://127.0.0.1:5500"
        }
    }, supports_credentials=True)
    
    @app.route('/')
    def home():
        return jsonify({
            "message": "Welcome to the HBnB API! 🎉",
            "documentation": "/api/v1/docs",
            "available_endpoints": [
                "/api/v1/users",
                "/api/v1/places",
                "/api/v1/amenities",
                "/api/v1/reviews",
                "/api/v1/auth/login"
            ]
        })
    
    api = Api(app, version='1.0', title='HBnB API', description='HBnB Application API', doc='/api/v1/docs')
    
    # Import and register API namespaces
    from app.api.v1.users import ns as user_namespace
    from app.api.v1.places import ns as place_namespace
    from app.api.v1.amenities import ns as amenity_namespace
    from app.api.v1.reviews import ns as review_namespace
    from app.api.v1.auth import ns as auth_namespace  # New auth namespace
    
    api.add_namespace(user_namespace, path='/api/v1/users')
    api.add_namespace(place_namespace, path='/api/v1/places')
    api.add_namespace(amenity_namespace, path='/api/v1/amenities')
    api.add_namespace(review_namespace, path='/api/v1/reviews')
    api.add_namespace(auth_namespace, path='/api/v1/auth')
    

    
    return app