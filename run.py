from app import create_app
from flask import Flask, render_template
from flask_restx import Api
from flask_jwt_extended import JWTManager, create_access_token
from app.api.v1.users import api as users_ns
from app.api.v1.amenities import api as amenities_ns
from app.api.v1.places import api as places_ns
from app.api.v1.reviews import api as reviews_ns
from app.api.v1.auth import api as auth_ns
from app.api.v1.protected import api as protected_ns
from flask_cors import CORS
from flask import Flask, request, jsonify
from app.services.facade import HBnBFacade
import requests
from flask import session, redirect, url_for
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY', 'default_secret_key')
facade = HBnBFacade()
app.config['JWT_SECRET_KEY'] = 'HolbertonAustralia123'
jwt = JWTManager(app)

@app.route('/')
def index():
    try:
        response = requests.get('http://0.0.0.0:5001/api/v1/places/')
        if response.status_code == 200:
            places = response.json()
            print("Fetched data:", places)
        else:
            places = []
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        places = []

    return render_template('index.html', places=places)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        session['login'] = True
    return render_template('login.html')

@app.route('/place/<place_id>')
def place_page(place_id):
    try:
        place_url = f'http://0.0.0.0:5001/api/v1/places/{place_id}'
        place_response = requests.get(place_url)
        if place_response.status_code == 200:
            place = place_response.json()
            print("Fetched place data:", place)
        else:
            place = {}
        
        reviews_response = requests.get(f'http://0.0.0.0:5001/api/v1/reviews/{place_id}')
        if reviews_response.status_code == 200:
            reviews = reviews_response.json()
        else:
            reviews = []
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        place = {}
        reviews = []

    if not place:
        return render_template('404.html'), 400

    return render_template('place.html', place=place, reviews=reviews)

@app.route('/add_review/<place_id>')
def add_review(place_id):
    try:
        response = requests.get(f'http://0.0.0.0:5001/api/v1/places/{place_id}')
        if response.status_code == 200:
            place = response.json()
            print("Fetched data:", place)
        else:
            place = {}
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        place = {}

    return render_template('add_review.html', place=place)

CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
api = Api(app, version='1.0', title='HBnB API', description='HBnB Application API', doc='/swagger')

api.add_namespace(users_ns, path='/api/v1/users')
api.add_namespace(amenities_ns, path='/api/v1/amenities')
api.add_namespace(places_ns, path='/api/v1/places')
api.add_namespace(reviews_ns, path='/api/v1/reviews')
api.add_namespace(auth_ns, path='/api/v1/auth')
api.add_namespace(protected_ns, path='/api/v1/protected')


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5001)