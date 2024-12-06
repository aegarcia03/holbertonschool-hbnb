from flask_restx import Namespace, Resource, fields
# from app.services.facade import HBnBFacade
from app.services import facade

api = Namespace('places', description='Place operations')

# Define the models for related entities
amenity_model = api.model('Amenity', {
    'id': fields.String(description='Amenity ID'),
    'name': fields.String(description='Name of the amenity')
})

user_model = api.model('User', {
    'id': fields.String(description='User ID'),
    'first_name': fields.String(description='First name of the owner'),
    'last_name': fields.String(description='Last name of the owner'),
    'email': fields.String(description='Email of the owner')
})

# Adding the review model
review_model = api.model('Review', {
    'id': fields.String(description='Review ID'),
    'text': fields.String(description='Text of the review'),
    'rating': fields.Integer(description='Rating of the place (1-5)'),
    'user_id': fields.String(description='ID of the user')
})

place_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    'owner_id': fields.String(required=True, description='ID of the owner'),
    'owner': fields.Nested(user_model, description='Owner of the place'),
    'amenities': fields.List(fields.Nested(amenity_model), description='List of amenities'),
    'reviews': fields.List(fields.Nested(review_model), description='List of reviews')
})

# facade = HBnBFacade()

@api.route('/')
class PlaceList(Resource):
    @api.expect(place_model)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    @api.response(400, 'Setter validation failure')
    def post(self):
        # Need to add at least one user first so that we have someone in the system as an owner

        # curl -X POST "http://127.0.0.1:5000/api/v1/users/" -H "Content-Type: application/json" -d '{"first_name": "John","last_name": "Doe","email": "john.doe@example.com"}'

        # curl -X POST "http://127.0.0.1:5000/api/v1/places/" -H "Content-Type: application/json" -d '{"title": "Cozy Apartment","description": "A nice place to stay","price": 100.0,"latitude": 37.7749,"longitude": -122.4194,"owner_id": ""}'

        """Register a new place"""
        places_data = api.payload
        wanted_keys_list = ['title', 'description', 'price', 'latitude', 'longitude', 'owner_id']

        # Check whether the keys are present
        if not all(name in wanted_keys_list for name in places_data):
            return { 'error': "Invalid input data" }, 400

        # check that user exists
        user = facade.get_user(str(places_data.get('owner_id')))
        if not user:
            return { 'error': "Invalid input data - user does not exist" }, 400

        # the try catch is here in case setter validation fails
        new_place = None
        try:
        #     # NOTE: We're storing a user object in the owner slot and getting rid of owner_id
        # store owner id not object
            # places_data['owner'] = user
            # del places_data['owner_id']

            new_place = facade.create_place(places_data)
        except ValueError as error:
            return { 'error': "Setter validation failure: {}".format(error) }, 400

        output = {
            'id': str(new_place.id),
            "title": new_place.title,
            "description": new_place.description,
            "price": new_place.price,
            'latitude': new_place.latitude,
            'longitude': new_place.longitude,
            "owner_name": user.first_name,
            "owner_id": user.id,
            "created_at": str(new_place.created_at)
        }
        return output, 201

    @api.response(200, 'List of places retrieved successfully')
    def get(self):
        """Retrieve a list of all places"""
        all_places = facade.get_all_places()
        output = []

        for place in all_places:
            reviews = place.reviews_r
            if reviews:
                average = sum([review.rating for review in reviews]) / len(reviews)
            else:
                average = "No reviews available"

        for place in all_places:
            output.append({
                'id': str(place.id),
                'title': place.title,
                'price': place.price,
                'description': place.description,
                'latitude': place.latitude,
                'longitude': place.longitude,
                'average_rating': average
            })

        return output, 200

@api.route('/<place_id>')
class PlaceResource(Resource):#
    @api.response(200, 'Place details retrieved successfully')
    @api.response(404, 'Place not found')
    @api.response(404, 'Place owner not found')
    def get(self, place_id):
        """Get place details by ID"""
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404

        owner = place.owner_r
        if not owner:
            return {'error': 'Owner not found'}, 404

        amenities_list = []
        for amenity in place.amenities_r:
            amenities_list.append({
                'amenity_id': str(amenity.id),
                'name': amenity.name
            })
        reviews_list = []
        ratings = []
        for review in place.reviews_r:
            author = review.author_r
            reviews_list.append({
                'review': review.text,
                'rating': review.rating,
                'author': f"{author.first_name} {author.last_name}"
            })
            ratings.append(review.rating)

        if ratings:
            average_rating = sum(ratings) / len(ratings)
        else:
            average_rating = "Not rated yet"

        output = {
            'place_id': str(place.id),
            'title': place.title,
            'price': place.price,
            'description': place.description,
            'latitude': place.latitude,
            'longitude': place.longitude,
            'owner': {
                'owner_id': str(owner.id),
                'first_name': owner.first_name,
                'last_name': owner.last_name,
                'email': owner.email
            },
            'amenities': amenities_list,
            'reviews_list': reviews_list,
            'average_rating': average_rating

        }
        return output, 200

    @api.response(200, 'Place deleted successfully')
    @api.response(404, 'Place not found')
    def delete(self, place_id):
        """Delete a place"""
        try:
            facade.delete_place(place_id)
        except ValueError:
            return { 'error': "Place not found" }, 400

        return {'message': 'Place deleted successfully'}, 200

    @api.expect(place_model)
    @api.response(200, 'Place updated successfully')
    @api.response(400, 'Invalid input data')
    @api.response(400, 'Setter validation failure')
    @api.response(404, 'Place not found')
    def put(self, place_id):
        # curl -X PUT "http://127.0.0.1:5000/api/v1/places/<place_id>" -H "Content-Type: application/json" -H "Authorization: Bearer <token_goes_here>" -d '{"title": "Not So Cozy Apartment","description": "A terrible place to stay","price": 999.99}'

        """Update a place's information"""
        place_data = api.payload
        wanted_keys_list = ['title', 'description', 'price']

        if len(place_data) != len(wanted_keys_list) or not all(key in wanted_keys_list for key in place_data):
            return {'error': 'Invalid input data - required attributes missing'}, 400

        # Check that place exists first before updating them
        place = facade.get_place(place_id)
        if place:
            try:
                facade.update_place(place_id, place_data)
            except ValueError as error:
                return { 'error': "Setter validation failure: {}".format(error) }, 400

            return {'message': 'Place updated successfully'}, 200

        return {'error': 'Place not found'}, 404

@api.route('/<place_id>/<relationship>/')
class PlaceRelations(Resource):
    @api.response(404, 'Unable to retrieve Amenities linked to this property')
    @api.response(404, 'Unable to retrieve Reviews written about this place')
    @api.response(404, 'Unable to retrieve Owner details for this property')
    def get(self, place_id, relationship):
        """
        Use relation as a placeholder
        """
        output = []
        # AMENITIES
        # curl -X GET http://localhost:5000/api/v1/places/<place_id>/amenities/
        if relationship == "amenities":
            all_amenities = facade.get_place_amenities(place_id)
            if not all_amenities:
                return {'error': 'Unable to get Amenities linked to this property'}, 404

            place = facade.get_place(place_id)
            if not place:
                return {'error': 'Place not found'}, 404

            owner = facade.get_place_owner(place_id)
            if not owner:
                return {'error': f'Cannot find the owner'}, 404

            for amenity in all_amenities:
                output.append({
                    'id': str(amenity.id),
                    'amenity': amenity.name,
                    'property': {
                        'title': place.title,
                        'description': place.description,
                        'owner': owner.first_name
                    }
                })
        # REVIEWS
        # curl -X GET http://localhost:5000/api/v1/places/<place_id>/reviews/
        elif relationship == "reviews":
            all_reviews = facade.get_place_reviews(place_id)
            if not all_reviews:
                return {'error': 'Unable to get Reviews written about this place'}, 404

            place = facade.get_place(place_id)
            if not place:
                return {'error': 'Place not found'}, 404

            for review in all_reviews:
                user = facade.get_user(review.user_id)
                if not user:
                    return {'error': f'User not found for review {review.id}'}, 404

            for review in all_reviews:
                output.append({
                    'author': user.first_name,
                    'review_id': str(review.id),
                    'review': review.text,
                    'rating': review.rating,
                    'property': {
                        'property_name': place.title,
                        'description': place.description
                    }
                })
        # OWNER
        # curl -X GET http://localhost:5000/api/v1/places/<place_id>/owner/
        elif relationship == "owner":
            owner = facade.get_place_owner(place_id)
            if not owner:
                return {'error': 'Unable to get Owner details for this property'}, 404

            place = facade.get_place(place_id)
            if not owner:
                return {'error': 'Place not found'}, 404

            output = {
                'owner_id': str(owner.id),
                'first_name': owner.first_name,
                'last_name': owner.last_name,
                'email': owner.email,
                'place': {
                    'place_id': place.id,
                    'title': place.title,
                    'description': place.description
                }
            }
        return output, 200
