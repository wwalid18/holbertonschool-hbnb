from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.facade import HBnBFacade

ns = Namespace('users', description='User operations')

# Model for user registration including password
user_registration_model = ns.model('UserRegistration', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email address of the user'),
    'password': fields.String(required=True, description='Password for the user')
})

# Model for registration response (excluding password)
user_response_model = ns.model('UserResponse', {
    'id': fields.String(description='User ID'),
    'message': fields.String(description='Success message')
})

# Model for updating user information (only first_name and last_name allowed)
user_update_model = ns.model('UserUpdate', {
    'first_name': fields.String(required=False, description='Updated first name of the user'),
    'last_name': fields.String(required=False, description='Updated last name of the user')
})

@ns.route('/')
class UserList(Resource):
    @ns.expect(user_registration_model, validate=True)
    @ns.response(200, 'User successfully registered', user_response_model)
    @ns.response(400, 'Invalid input data or email already registered')
    def post(self):
        """Register a new user with password hashing"""
        facade = HBnBFacade()
        user_data = ns.payload
        try:
            new_user = facade.create_user(user_data)
            return {'id': new_user.id, 'message': 'User successfully registered'}, 200
        except ValueError as e:
            return {'error': str(e)}, 400

    @jwt_required()
    @ns.response(200, 'List of users retrieved successfully')
    def get(self):
        """Retrieve a list of all users (protected, without passwords)"""
        facade = HBnBFacade()
        users = facade.get_all_users()
        return [user.to_dict() for user in users], 200

@ns.route('/<string:user_id>')
class UserResource(Resource):
    @jwt_required()
    @ns.response(200, 'User details retrieved successfully')
    @ns.response(404, 'User not found')
    def get(self, user_id):
        """Get user details by ID (protected, without password)"""
        facade = HBnBFacade()
        user = facade.get_user_by_id(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        return user.to_dict(), 200

    @jwt_required()
    @ns.expect(user_update_model, validate=True)
    @ns.response(200, 'User updated successfully')
    @ns.response(400, 'You cannot modify email or password.')
    @ns.response(403, 'Unauthorized action')
    @ns.response(404, 'User not found')
    def put(self, user_id):
        """
        Update user details (protected).
        Only the authenticated user can modify their own details.
        Allowed updates: first_name and last_name.
        If the payload includes email or password, return a 400 error.
        """
        current_user = get_jwt_identity()
        # Ensure the user is modifying their own details
        if current_user['id'] != user_id:
            return {'error': 'Unauthorized action'}, 403
        
        # Check payload for disallowed fields
        update_data = ns.payload
        if 'email' in update_data or 'password' in update_data:
            return {'error': 'You cannot modify email or password.'}, 400

        facade = HBnBFacade()
        user = facade.get_user_by_id(user_id)
        if not user:
            return {'error': 'User not found'}, 404

        # Only update allowed fields (first_name and/or last_name)
        if 'first_name' in update_data:
            user.first_name = update_data['first_name'].strip()
        if 'last_name' in update_data:
            user.last_name = update_data['last_name'].strip()
        
        try:
            updated_user = facade.update_user(user_id, update_data)
        except Exception as e:
            return {'error': str(e)}, 400
        
        return {'message': 'User updated successfully', 'user': updated_user.to_dict()}, 200
