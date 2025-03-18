from flask import Flask, jsonify
from flask_restx import Api

def create_app():
    """
    Create and configure the Flask application.

    Returns:
        Flask: The configured Flask application.
    """
    # Initialize the Flask app
    app = Flask(__name__)

    # ✅ Add root route BEFORE initializing the API
    @app.route('/')
    def home():
        return jsonify({
            "message": "Welcome to the HBnB API! 🎉",
            "documentation": "/api/v1/docs",
            "available_endpoints": [
                "/api/v1/users",
                "/api/v1/places",
                "/api/v1/amenities",
                "/api/v1/reviews"
            ]
        })

    # ✅ Add a root endpoint for /api/v1/
    @app.route('/api/v1/')
    def api_v1_root():
        return jsonify({
            "message": "Welcome to the HBnB API (v1)! 🎉",
            "documentation": "/api/v1/docs",
            "available_endpoints": [
                "/api/v1/users",
                "/api/v1/places",
                "/api/v1/amenities",
                "/api/v1/reviews"
            ]
        })

    # ✅ Initialize the API AFTER defining the root route
    api = Api(app, version='1.0', title='HBnB API', description='HBnB Application API', 
              doc='/api/v1/docs')

    # ✅ Import namespaces from individual files
    from app.api.v1.users import ns as user_namespace
    from app.api.v1.places import ns as place_namespace
    from app.api.v1.amenities import ns as amenity_namespace
    from app.api.v1.reviews import ns as review_namespace

    # ✅ Register namespaces correctly
    api.add_namespace(user_namespace, path='/api/v1/users')
    api.add_namespace(place_namespace, path='/api/v1/places')
    api.add_namespace(amenity_namespace, path='/api/v1/amenities')

    api.add_namespace(review_namespace, path='/api/v1/reviews')

    return app
