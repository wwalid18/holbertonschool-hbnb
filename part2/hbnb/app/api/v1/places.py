from flask_restx import Namespace, Resource, fields
from app.services import facade

# Define the namespace
ns = Namespace('places', description='Place operations')

# ✅ Define the Review Model for Places
review_model = ns.model('PlaceReview', {
    'id': fields.String(description='Review ID'),
    'text': fields.String(description='Text of the review'),
    'rating': fields.Integer(description='Rating of the place (1-5)'),
    'user_id': fields.String(description='ID of the user who wrote the review')
})

# ✅ Define the Amenity Model for Places
amenity_model = ns.model('PlaceAmenity', {
    'id': fields.String(description='Amenity ID'),
    'name': fields.String(description='Name of the amenity')
})

# ✅ Define the User Model for Place Owners
user_model = ns.model('PlaceUser', {
    'id': fields.String(description='User ID'),
    'first_name': fields.String(description='First name of the owner'),
    'last_name': fields.String(description='Last name of the owner'),
    'email': fields.String(description='Email of the owner')
})

# ✅ Define the Place Model (Includes Owner, Amenities, and Reviews)
place_model = ns.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    'owner_id': fields.String(required=True, description='ID of the owner'),
    'owner': fields.Nested(user_model, description='Owner of the place'),
    'amenities': fields.List(fields.Nested(amenity_model), description='List of amenities'),
    'reviews': fields.List(fields.Nested(review_model), description='List of reviews')
})


@ns.route('/')  # ✅ Corrected: This correctly maps to /api/v1/places
class PlaceList(Resource):
    @ns.expect(place_model, validate=True)
    @ns.response(201, 'Place successfully created')
    @ns.response(400, 'Invalid input data')
    def post(self):
        """Register a new place"""
        place_data = ns.payload
        try:
            new_place = facade.create_place(place_data)
            return new_place, 201
        except ValueError as e:
            return {'error': str(e)}, 400

    @ns.response(200, 'List of places retrieved successfully')
    def get(self):
        """Retrieve a list of all places"""
        places = facade.get_all_places()
        return places, 200


@ns.route('/<string:place_id>')  # ✅ Corrected for valid route mapping
class PlaceResource(Resource):
    @ns.response(200, 'Place details retrieved successfully')
    @ns.response(404, 'Place not found')
    def get(self, place_id):
        """Get place details by ID"""
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404
        return place, 200

    @ns.expect(place_model, validate=True)
    @ns.response(200, 'Place updated successfully')
    @ns.response(404, 'Place not found')
    @ns.response(400, 'Invalid input data')
    def put(self, place_id):
        """Update a place's information"""
        update_data = ns.payload
        try:
            updated_place = facade.update_place(place_id, update_data)
            if not updated_place:
                return {'error': 'Place not found'}, 404
            return updated_place, 200
        except ValueError as e:
            return {'error': str(e)}, 400
