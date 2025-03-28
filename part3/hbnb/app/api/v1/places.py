# app/api/v1/places.py
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.facade import HBnBFacade

ns = Namespace('places', description='Place operations')

# Model for creating a place.
# Note: owner_id in the payload will be overridden by the authenticated user's id.
place_model = ns.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    'owner_id': fields.String(required=True, description='ID of the owner'),
    'amenities': fields.List(fields.String, description='List of amenity IDs')
})

# Model for updating a place.
update_place_model = ns.model('UpdatePlace', {
    'title': fields.String(description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(description='Price per night'),
    'latitude': fields.Float(description='Latitude of the place'),
    'longitude': fields.Float(description='Longitude of the place'),
    'amenities': fields.List(fields.String, description='List of amenity IDs')
})

@ns.route('/')
class PlaceList(Resource):
    @ns.response(200, 'List of places retrieved successfully')
    def get(self):
        """Retrieve a list of all places (public endpoint)"""
        facade = HBnBFacade()
        places = facade.get_all_places()
        return places, 200

    @jwt_required()
    @ns.expect(place_model, validate=True)
    @ns.response(201, 'Place successfully created')
    @ns.response(400, 'Invalid input data')
    def post(self):
        """Create a new place (protected: owner_id is set to the authenticated user's id)"""
        current_user = get_jwt_identity()  # Retrieve authenticated user's identity
        facade = HBnBFacade()
        place_data = ns.payload
        # Override owner_id with the authenticated user's id
        place_data['owner_id'] = current_user['id']
        try:
            new_place = facade.create_place(place_data)
            return new_place, 201
        except ValueError as e:
            return {'error': str(e)}, 400

@ns.route('/<string:place_id>')
class PlaceResource(Resource):
    @ns.response(200, 'Place details retrieved successfully')
    @ns.response(404, 'Place not found')
    def get(self, place_id):
        """Get place details by ID (public endpoint)"""
        facade = HBnBFacade()
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404
        return place, 200

    @jwt_required()
    @ns.expect(update_place_model, validate=True)
    @ns.response(200, 'Place updated successfully')
    @ns.response(403, 'Unauthorized action')
    @ns.response(404, 'Place not found')
    def put(self, place_id):
        """
        Update a place's information.
        
        - If the authenticated user is an admin, bypass the ownership check.
        - If not an admin, the user must be the owner of the place.
        """
        current_user = get_jwt_identity()
        facade = HBnBFacade()
        existing_place = facade.get_place(place_id)
        if not existing_place:
            return {'error': 'Place not found'}, 404

        # Non-admin users must be the owner of the place.
        if not current_user.get('is_admin'):
            if existing_place.get('owner', {}).get('id') != current_user['id']:
                return {'error': 'Unauthorized action'}, 403

        update_data = ns.payload
        try:
            updated_place = facade.update_place(place_id, update_data)
            return {'message': 'Place updated successfully', 'place': updated_place}, 200
        except ValueError as e:
            return {'error': str(e)}, 400

    @jwt_required()
    @ns.response(200, 'Place deleted successfully')
    @ns.response(403, 'Unauthorized action')
    @ns.response(404, 'Place not found')
    def delete(self, place_id):
        """
        Delete a place.
        
        - Admins can delete any place.
        - Non-admins can only delete their own place.
        """
        current_user = get_jwt_identity()
        facade = HBnBFacade()
        existing_place = facade.get_place(place_id)
        if not existing_place:
            return {'error': 'Place not found'}, 404

        # Non-admin users must be the owner of the place to delete it.
        if not current_user.get('is_admin'):
            if existing_place.get('owner', {}).get('id') != current_user['id']:
                return {'error': 'Unauthorized action'}, 403

        deletion_result = facade.place_repository.delete(place_id)
        if deletion_result:
            return {'message': 'Place deleted successfully'}, 200
        else:
            return {'error': 'Failed to delete place'}, 400
