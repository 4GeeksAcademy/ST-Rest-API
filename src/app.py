"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User,People,Planets
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def handle_users():
    users = User.query.all()
    all_users = list(map(lambda x: x.serialize(),users))   
    print(all_users)
    return jsonify(all_users), 200

@app.route('/user', methods=['GET'])
def get_user_by_id(user_id):
    Pick_user = User.query.filter_by(id=user_id).first()
    if Pick_user is None:
        raise APIException('Usuario no existe', status_code=404)
    print(Pick_user)
    return jsonify(Pick_user.serialize()), 200

@app.route('/user', methods=['POST'])
def post_users():
    request_body_users = request.get_json()   
    new_body = User(
        username = request_body_users['username'],
        email = request_body_users['email'],
        password = request_body_users['password'],
        is_active = request_body_users['is_active'])  
    db.session.add(new_body)
    db.session.commit()
    return jsonify(request_body_users), 200

@app.route('/people', methods=['GET'])
def handle_people():
    people = People.query.all()
    all_people = list(map(lambda x: x.serialize(), people))
    print(all_people)
    return jsonify(all_people), 200

@app.route('/people/<int:people_id>', methods=['GET'])
def handle_specific_people(people_id):
    person = People.query.get(people_id)
    if person is None:
        return jsonify({"error": "Person not found"}), 404
    return jsonify({'hola'}), 200

@app.route('/planets', methods=['GET'])
def handle_planets():
    planets = Planets.query.all()
    all_planets = list(map(lambda x: x.serialize(), planets))
    print(all_planets)
    return jsonify(all_planets), 200

@app.route('/planets/<int:planets_id>', methods=['GET'])
def handle_specific_planet(planet_id):
    planet = Planet.query.get(planet_id)
    if planet is None:
        return jsonify({"error": "Planet not found"}), 404
    return jsonify(planet.serialize()), 200




# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
