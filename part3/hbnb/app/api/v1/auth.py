from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import create_access_token
from app.services.facade import HBnBFacade

# Create the auth namespace
ns = Namespace('auth', description='Authentication operations')

# Model for login input validation
login_model = ns.model('Login', {
    'email': fields.String(required=True, description='User email'),
    'password': fields.String(required=True, description='User password')
})

@ns.route('/login')
class Login(Resource):
    @ns.expect(login_model, validate=True)
    def post(self):
        """Authenticate user and return a JWT token"""
        credentials = ns.payload  # Retrieve credentials from the request payload
        
        facade = HBnBFacade()
        user = facade.get_user_by_email(credentials['email'])
        
        if not user or not user.verify_password(credentials['password']):
            ns.abort(401, "Invalid credentials")
        
        # Generate a JWT token embedding user's id and is_admin claim
        access_token = create_access_token(identity={'id': str(user.id), 'is_admin': user.is_admin})
        return {'access_token': access_token}, 200
