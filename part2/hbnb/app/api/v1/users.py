from flask_restx import Namespace, Resource, fields
from app.services import facade

# Define the namespace
ns = Namespace('users', description='User operations')

# Define the user model for input validation and documentation
user_model = ns.model('User', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user'),
    'is_admin': fields.Boolean(required=False, description='is the user admin')
})

@ns.route('/')
class UserList(Resource):
    @ns.expect(user_model, validate=True)
    @ns.response(200, 'User successfully created')
    @ns.response(400, 'Email already registered')
    @ns.response(400, 'Invalid input data')
    def post(self):
        """Register a new user"""
        user_data = ns.payload

        # Simulate email uniqueness check (to be replaced by real validation with persistence)
        existing_user = facade.get_user_by_email(user_data['email'])
        if existing_user:
            return {'error': 'Email already registered'}, 400
        if not user_data['first_name'] or not user_data['last_name']:
            return {'error': 'Invalid input data'}, 400
        if '@' not in user_data['email']:
            return {'error': 'Invalid email format'}, 400 

        new_user = facade.create_user(user_data)
        return {'id': new_user.id, 'first_name': new_user.first_name, 'last_name': new_user.last_name, 'email': new_user.email, 'is_admin': new_user.is_admin}, 200

    @ns.response(200, 'List of users retrieved successfully')
    def get(self):
        """Retrieve a list of all users"""
        users = facade.get_all_users()
        return [{'id': user.id, 'first_name': user.first_name, 'last_name': user.last_name, 'email': user.email, 'is_admin': user.is_admin} for user in users], 200
        

@ns.route('/<user_id>')
class UserResource(Resource):
    @ns.response(200, 'User details retrieved successfully')
    @ns.response(404, 'User not found')
    def get(self, user_id):
        """Get user details by ID"""
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        return {'id': user.id, 'first_name': user.first_name, 'last_name': user.last_name, 'email': user.email}, 200

    @ns.response(200, 'user updated successfully')
    @ns.response(404, 'Review not found')
    @ns.response(400, 'Invalid input data')
    def put(self, user_id):
        """Update a review's information"""
        update_data = ns.payload
        try:
            updated_review = facade.update_ruser(user_id, update_data)
            if not updated_review:
                return {"error": "Review not found"}, 404

            return {"message": "Review updated successfully"}, 200
        except ValueError as e:
            return {"error": str(e)}, 400

    @ns.response(200, 'Review deleted successfully')
    @ns.response(404, 'Review not found')
    def delete(self, review_id):
        """Delete a review"""
        review = facade.get_review(review_id)
        if not review:
            return {"error": "Review not found"}, 404

        
