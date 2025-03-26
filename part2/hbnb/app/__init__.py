# app/__init__.py
from flask import Flask, jsonify
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()

def create_app(config_class="config.DevelopmentConfig"):
    app = Flask(__name__)
    app.config.from_object(config_class)  # Load configuration from the provided config class

    # Initialize extensions
    db.init_app(app)
    migrate = Migrate(app, db)

    # Define the home route
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

    # Initialize the API
    api = Api(app, version='1.0', title='HBnB API', description='HBnB Application API', 
              doc='/api/v1/docs')

    # Import and register API namespaces
    from app.api.v1.users import ns as user_namespace
    from app.api.v1.places import ns as place_namespace
    from app.api.v1.amenities import ns as amenity_namespace
    from app.api.v1.reviews import ns as review_namespace
    from app.api.v1.auth import ns as auth_namespace  # Assuming you have an auth namespace

    api.add_namespace(user_namespace, path='/api/v1/users')
    api.add_namespace(place_namespace, path='/api/v1/places')
    api.add_namespace(amenity_namespace, path='/api/v1/amenities')
    api.add_namespace(review_namespace, path='/api/v1/reviews')
    api.add_namespace(auth_namespace, path='/api/v1/auth')

    return app
