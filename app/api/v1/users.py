from flask_restx import Namespace, Resource, fields
# from app.services.facade import HBnBFacade
from app.services import facade

api = Namespace('users', description='User operations')

# Define the user model for input validation and documentation
user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user')
})

# facade = HBnBFacade()

@api.route('/')
class UserList(Resource):
    @api.expect(user_model)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered')
    @api.response(400, 'Invalid input data')
    @api.response(400, 'Setter validation failure')
    def post(self):
        # curl -X POST "http://127.0.0.1:5000/api/v1/users/" -H "Content-Type: application/json" -d '{"first_name": "John","last_name": "Doe","email": "john.doe@example.com"}'

        """Register a new user"""
        user_data = api.payload

        # Simulate email uniqueness check (to be replaced by real validation with persistence)
        existing_user = facade.get_user_by_email(user_data['email'])
        if existing_user:
            return {'error': 'Email already registered'}, 400

        # Validate input data
        if not all([user_data.get('first_name'), user_data.get('last_name'), user_data.get('email'), user_data.get('password')]):
            return {'error': 'Invalid input data'}, 400

        # the try catch is here in case setter validation fails
        new_user = None
        try:
            new_user = facade.create_user(user_data)
        except ValueError as error:
            return { 'error': "Setter validation failure: {}".format(error) }, 400

        return {'id': str(new_user.id), 'message': 'User created successfully'}, 201

    @api.response(200, 'Users list successfully retrieved')
    def get(self):
        """ Get list of all users """
        all_users = facade.get_all_users()
        output = []
        for user in all_users:
            # print(user)
            output.append({
                'id': str(user.id),
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email
            })

        return output, 200

@api.route('/<user_id>')
class UserResource(Resource):
    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """Get user details by ID"""
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404

        return {'id': str(user.id), 'first_name': user.first_name, 'last_name': user.last_name, 'email': user.email}, 200

    @api.expect(user_model)
    @api.response(200, 'User details updated successfully')
    @api.response(400, 'Invalid input data')
    @api.response(400, 'Setter validation failure')
    @api.response(404, 'User not found')
    def put(self, user_id):
        """ Update user specified by id """
        user_data = api.payload
        wanted_keys_list = ['first_name', 'last_name', 'email']

        # Ensure that user_data contains only what we want (e.g. first_name, last_name, email)
        # https://stackoverflow.com/questions/10995172/check-if-list-of-keys-exist-in-dictionary
        if len(user_data) != len(wanted_keys_list) or not all(key in wanted_keys_list for key in user_data):
            return {'error': 'Invalid input data - required attributes missing'}, 400

        # Check that user exists first before updating them
        user = facade.get_user(user_id)
        if user:
            try:
                facade.update_user(user_id, user_data)
            except ValueError as error:
                return { 'error': "Setter validation failure: {}".format(error) }, 400

            return {'message': 'User updated successfully'}, 200

        return {'error': 'User not found'}, 404

    @api.response(200, 'user deleted successfully')
    @api.response(404, 'user not found')
    def delete(self, user_id):
        """Delete a user"""
        try:
            facade.delete_user(user_id)
        except ValueError:
            return { 'error': "user not found" }, 400

        return {'message': 'user deleted successfully'}, 200

@api.route('/<user_id>/<relationship>/')
class UserRelations(Resource):
    @api.response(404, 'Unable to retrieve Places linked to this user')
    # @api.response(404, 'Unable to retrieve Reviews written about this place')
    def get(self, user_id, relationship):
        """
        Use relation as a placeholder
        """
        output = []
        # PLACES
        # curl -X GET http://localhost:5000/api/v1/users/<user_id>/places/
        if relationship == "places":
            all_places = facade.get_user_places(user_id)
            if not all_places:
                return {'error': 'Unable to get Places linked to this user'}, 404
            owner = facade.get_user(user_id)
            if not owner:
                return {'error': 'Unable to get Owner'}, 404

            for place in all_places:
                output.append({
                    'owner': owner.first_name,
                    'place_id': str(place.id),
                    'property_name': place.title,
                    'description': place.description,
                    'latitude': place.latitude,
                    'longitude': place.longitude
                })
        # REVIEWS
        # curl -X GET http://localhost:5000/api/v1/users/<user_id>/reviews/
        elif relationship == "reviews":
            all_reviews = facade.get_user_reviews(user_id)
            if not all_reviews:
                return {'error': 'Unable to get Reviews linked to this user'}, 404
            author = facade.get_user(user_id)
            if not author:
                return {'error': 'Unable to get Owner'}, 404

            for review in all_reviews:
                place = review.place_r
                if not place:
                    return {'error': 'Review is not linked to any user'}, 404
                place_owner = place.owner_r
                if not place_owner:
                    return {'error': 'Cannot find the owner of the property'}, 404
                output.append({
                    'author': author.first_name,
                    'review_id': str(review.id),
                    'review': review.text,
                    'rating': review.rating,
                    'property_name': place.title,
                    'owner_property': place_owner.first_name
                })
        return output, 200