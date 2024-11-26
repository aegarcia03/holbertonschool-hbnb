
from flask import Flask, render_template
from flask_restx import Api
from app.api.v1.users import api as users_ns
from app.api.v1.amenities import api as amenities_ns
from app.api.v1.places import api as places_ns
from app.api.v1.reviews import api as reviews_ns
from flask_cors import CORS
import requests

app = Flask(__name__)

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

@app.route('/login')
def login():
    return render_template('login.html')

CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
api = Api(app, version='1.0', title='HBnB API', description='HBnB Application API', doc='/swagger')

api.add_namespace(users_ns, path='/api/v1/users')
api.add_namespace(amenities_ns, path='/api/v1/amenities')
api.add_namespace(places_ns, path='/api/v1/places')
api.add_namespace(reviews_ns, path='/api/v1/reviews')


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5001)