from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import create_access_token
from app.services import facade
from app.models.user import User
from flask import session, redirect, url_for
from flask import request

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

        # curl -X POST "http://127.0.0.1:5001/api/v1/users/" -H "Content-Type: application/json" -d '{ "first_name": "John", "last_name": "Doe", "email": "john.doe@example.com", "password": "cowabunga"}'
        # curl -X POST "http://127.0.0.1:5001/api/v1/auth/login" -H "Content-Type: application/json" -d '{ "email": "john.doe@example.com", "password": "cowabunga" }'
        email = request.form.get('email')
        password = request.form.get('password')
        # Get the email and password from the request payload

        # Step 1: Retrieve the user based on the provided email
        user = facade.get_user_by_email(email)

        # Step 2: Check if the user exists and the password is correct
        if not user or not user.verify_password(password):
            return {'error': 'Invalid credentials. Please try again.'}, 401

        # Step 3: Create a JWT token with the user's id and is_admin flag
        access_token = create_access_token(identity={'id': str(user.id), 'is_admin': user.is_admin})
        
        #Step 4: Store the JWT token in session or cookies for future requests
        session['jwt_token'] = access_token
        session['user_id'] = user.id

        # Step 4: Return the JWT token to the client
        print("Logging in...")
        return {'access_token': access_token}, 200