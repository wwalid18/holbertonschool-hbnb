from flask_restx import Namespace, Resource, fields
from app.services.facade import HBnBFacade

# Define the namespace
ns = Namespace('amenities', description='Amenity operations')

# Initialize the facade
facade = HBnBFacade()

# Define the Amenity model for request validation
amenity_model = ns.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity'),
    'place_id': fields.String(required=True, description='ID of the place'),
    'user_id': fields.String(required=True, description='ID of the user')
})

@ns.route('/')
class AmenityList(Resource):
    @ns.expect(amenity_model, validate=True)
    @ns.response(201, 'amenity successfully created')
    @ns.response(400, 'Invalid input data')
    def post(self):
        """Register a new amenity"""
        amenity_data = ns.payload
        try:
            new_amenity = facade.create_amenity(amenity_data)
            return new_amenity, 201
        except ValueError as e:
            return {'error': str(e)}, 400

    @ns.response(200, 'List of amenities retrieved successfully')
    def get(self):
        """Retrieve a list of all amenities"""
        amenities = facade.get_all_amenities()
        return [{
            'id': amenity.id,
            'name': amenity.name,
            'place_id': amenity.place_id
        } for amenity in amenities], 200

@ns.route('/<string:amenity_id>')
class AmenityResource(Resource):
    @ns.response(200, 'Amenity details retrieved successfully')
    @ns.response(404, 'Amenity not found')
    def get(self, amenity_id):
        """Get amenity details by ID"""
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {'error': 'Amenity not found'}, 404
        return {
            'id': amenity.id,
            'name': amenity.name,
            'place_id': amenity.place_id
        }, 200

    @ns.expect(amenity_model, validate=True)
    @ns.response(200, 'Amenity updated successfully')
    @ns.response(404, 'Amenity not found')
    @ns.response(400, 'Invalid input data')
    def put(self, amenity_id):
        """Update an amenity's information"""
        amenity_data = ns.payload

        updated_amenity = facade.update_amenity(amenity_id, amenity_data)
        if not updated_amenity:
            return {'error': 'Amenity not found'}, 404

        return {
            'message': 'Amenity updated successfully'
        }, 200
