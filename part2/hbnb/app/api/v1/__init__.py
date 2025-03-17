from flask_restx import Api
from flask import Blueprint

# Create a Blueprint for the v1 API
v1_bp = Blueprint('v1', __name__, url_prefix='/api/v1')

# Initialize the Api object
api = Api(v1_bp, version='1.0', title='HBNB API', description='API for HBNB')

# Import and register namespaces (routes)
from .users import ns as users_ns  # ✅ Corrected: Import `ns` as `users_ns`
from .amenities import ns as amenities_ns
from .places import ns as places_ns
from .reviews import ns as reviews_ns

api.add_namespace(users_ns)
api.add_namespace(amenities_ns)
api.add_namespace(places_ns)
api.add_namespace(reviews_ns)
