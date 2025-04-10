from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import create_access_token
from app.services import facade
from flask import current_app

api = Namespace('auth', description='Authentication operations')

# Model for input validation
login_model = api.model('Login', {
    'email': fields.String(required=True, description='User email'),
    'password': fields.String(required=True, description='User password')
})

@api.route('/login')
class Login(Resource):
    @api.expect(login_model)
    def post(self):
        """Authenticate user and return a JWT token"""
        credentials = api.payload  # Get the email and password from the request payload
        current_app.logger.debug(f"Login attempt for email: {credentials['email']}")
        
        # Step 1: Retrieve the user based on the provided email
        user = facade.get_user_by_email(credentials['email'])
        current_app.logger.debug(f"User found: {user is not None}")
        
        # Step 2: Check if the user exists and the password is correct
        if not user:
            current_app.logger.debug("User not found")
            return {'error': 'Invalid credentials'}, 401
            
        if not user.verify_password(credentials['password']):
            current_app.logger.debug("Invalid password")
            return {'error': 'Invalid credentials'}, 401

        # Step 3: Create a JWT token with user's id and admin status
        access_token = create_access_token(
            identity=str(user.id),  # Use string ID as subject
            additional_claims={
                'is_admin': user.is_admin
            }
        )
        current_app.logger.debug("Token created successfully")
        
        # Step 4: Return the JWT token and user info to the client
        return {
            'access_token': access_token,
            'user': {
                'id': user.id,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'is_admin': user.is_admin
            }
        }, 200 