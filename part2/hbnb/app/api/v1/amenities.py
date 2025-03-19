from flask_restx import Namespace, Resource, fields
from app.services.facade import HBnBFacade

# Define the namespace
ns = Namespace('amenities', description='Amenity operations')

# Initialize the facade
facade = HBnBFacade()

# Define the Amenity model for request validation
amenity_model = ns.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity'),
    'user_id': fields.String(required=True, description='ID of the user creating the amenity'),
    'place_id': fields.String(required=True, description='ID of the place to link the amenity')
})

@ns.route('/')
class AmenityList(Resource):
    @ns.expect(amenity_model)  # Expect the review_model as input
    @ns.response(201, 'Review successfully created')
    @ns.response(400, 'Invalid input data')
    @ns.response(404, 'User or Place not found')
    def post(self):
        """
        Register a new review.
        
        Example payload:
        {
          "text": "Great place to stay!",
          "rating": 5,
          "user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
          "place_id": "1fa85f64-5717-4562-b3fc-2c963f66afa6"
        }
        """
        review_data = ns.payload  # Get the JSON payload from the request

        try:
            # Use the facade to create the review
            new_review = facade.create_amenity(review_data)
            return {
                "id": new_review.id,
                "name": new_review.text,
                "user_id": new_review.user.id,
                "place_id": new_review.place.id
            }, 201
        except ValueError as e:
            return {"error": str(e)}, 400
        except Exception as e:
            return {"error": "User or Place not found"}, 404

@ns.route('/<string:amenity_id>')
class AmenityResource(Resource):
    @ns.response(200, 'Amenity details retrieved successfully')
    @ns.response(404, 'Amenity not found')
    def get(self, amenity_id):
        """Get amenity details by ID"""
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {'error': 'Amenity not found'}, 404
        return amenity.to_dict(), 200

    @ns.expect(amenity_model, validate=True)
    @ns.response(200, 'Amenity updated successfully')
    @ns.response(404, 'Amenity not found')
    @ns.response(400, 'Invalid input data')
    def put(self, amenity_id):
        """Update an amenity's information"""
        amenity_data = ns.payload

        try:
            updated_amenity = facade.update_amenity(amenity_id, amenity_data)
            if not updated_amenity:
                return {'error': 'Amenity not found'}, 404
            return updated_amenity.to_dict(), 200
        except ValueError as e:
            return {'error': str(e)}, 400