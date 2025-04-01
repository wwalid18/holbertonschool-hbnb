# app/api/v1/amenities.py
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required
from app.services.facade import HBnBFacade
from app.utils.decorators import admin_required

ns = Namespace('amenities', description='Amenity operations (Admin only)')

amenity_model = ns.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity'),
    'place_id': fields.String(required=True, description='ID of the place')
})

@ns.route('/')
class AmenityList(Resource):

    @ns.expect(amenity_model, validate=True)
    @ns.response(201, 'Amenity successfully created')
    @ns.response(400, 'Invalid input data')
    def post(self):
        """(Admin only) Add a new amenity."""
        facade = HBnBFacade()
        amenity_data = ns.payload
        try:
            new_amenity = facade.create_amenity(amenity_data)
            # Return the amenity as a dict
            return {'amenity': new_amenity.to_dict(), 'message': 'Amenity successfully created'}, 201
        except ValueError as e:
            return {'error': str(e)}, 400

@ns.route('/<string:amenity_id>')
class AmenityResource(Resource):
    @jwt_required()
    @admin_required
    @ns.expect(amenity_model, validate=True)
    @ns.response(200, 'Amenity updated successfully')
    @ns.response(404, 'Amenity not found')
    def put(self, amenity_id):
        """(Admin only) Modify the details of an amenity."""
        facade = HBnBFacade()
        amenity_data = ns.payload
        try:
            updated_amenity = facade.update_amenity(amenity_id, amenity_data)
            if not updated_amenity:
                return {'error': 'Amenity not found'}, 404
            return {'amenity': updated_amenity.to_dict(), 'message': 'Amenity updated successfully'}, 200
        except ValueError as e:
            return {'error': str(e)}, 400

    @jwt_required()
    @admin_required
    @ns.response(200, 'Amenity deleted successfully')
    @ns.response(404, 'Amenity not found')
    def delete(self, amenity_id):
        """(Admin only) Delete an amenity."""
        facade = HBnBFacade()
        try:
            deleted = facade.delete_amenity(amenity_id)
            if not deleted:
                return {'error': 'Amenity not found'}, 404
            return {'message': 'Amenity deleted successfully'}, 200
        except ValueError as e:
            return {'error': str(e)}, 400
