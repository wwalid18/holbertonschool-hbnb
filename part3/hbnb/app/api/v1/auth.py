from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import (
    create_access_token, jwt_required, get_jwt_identity, get_jwt
)
from flask import request, jsonify
from app.services.facade import HBnBFacade


ns = Namespace('auth', description='Authentication operations')

# Model for login input validation
login_model = ns.model('Login', {
    'email': fields.String(required=True, description='User email'),
    'password': fields.String(required=True, description='User password')
})

@ns.route('/login')
class Login(Resource):
    @ns.expect(login_model, validate=True)
    @ns.response(200, 'Login successful')
    @ns.response(401, 'Invalid credentials')
    def post(self):
        """Authenticate user and return a JWT token."""
        credentials = ns.payload
        facade = HBnBFacade()
        user = facade.get_user_by_email(credentials['email'])
        if not user or not user.verify_password(credentials['password']):
            ns.abort(401, "Invalid credentials")
        # Generate JWT token including the user's id and is_admin flag
        access_token = create_access_token(
            identity=str(user.id),  # ✅ sub is now a string
            additional_claims={'is_admin': user.is_admin}  # ✅ admin flag goes here
        )
        return {'access_token': access_token}, 200

# Model for password reset input validation
reset_password_model = ns.model('ResetPassword', {
    'email': fields.String(required=True, description='User email'),
    'new_password': fields.String(required=True, description='New password for the user')
})

@ns.route('/reset_password')
class ResetPassword(Resource):
    @jwt_required()
    @ns.expect(reset_password_model, validate=True)
    @ns.response(200, 'Password reset successful')
    @ns.response(400, 'Invalid input or error in resetting password')
    def post(self):
        """
        Reset a user's password.
        
        Requires a valid JWT token.
        Expects a JSON payload with 'email' and 'new_password'.
        """
        data = request.get_json()
        email = data.get('email')
        new_password = data.get('new_password')
        if not email or not new_password:
            return {'error': 'Email and new_password are required.'}, 400
        facade = HBnBFacade()
        try:
            user = facade.reset_user_password(email, new_password)
            return {'message': 'Password reset successful', 'user_id': user.id}, 200
        except ValueError as e:
            return {'error': str(e)}, 400
