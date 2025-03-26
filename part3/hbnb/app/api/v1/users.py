# app/api/v1/users.py
from flask_restx import Namespace, Resource, fields
from app.services.facade import HBnBFacade

ns = Namespace('users', description='User operations')

# Define the user registration model including password
user_registration_model = ns.model('UserRegistration', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email address of the user'),
    'password': fields.String(required=True, description='Password for the user')
})

# Define the user response model (without password)
user_response_model = ns.model('UserResponse', {
    'id': fields.String(description='User ID'),
    'message': fields.String(description='Success message')
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
            # The User model's __init__ automatically calls hash_password()
            new_user = facade.create_user(user_data)
            # Return only the user ID and a success message
            return {'id': new_user.id, 'message': 'User successfully registered'}, 200
        except ValueError as e:
            return {'error': str(e)}, 400

    @ns.response(200, 'List of users retrieved successfully')
    def get(self):
        """Retrieve a list of all users (without passwords)"""
        facade = HBnBFacade()
        users = facade.get_all_users()
        # Each user's to_dict() omits the password
        return [user.to_dict() for user in users], 200

@ns.route('/<string:user_id>')
class UserResource(Resource):
    @ns.response(200, 'User details retrieved successfully')
    @ns.response(404, 'User not found')
    def get(self, user_id):
        """Get user details by ID (without password)"""
        facade = HBnBFacade()
        user = facade.get_user_by_id(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        # to_dict() does not include the password field
        return user.to_dict(), 200
