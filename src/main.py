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
from models import db, User, Characters, Planets, Ships
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
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
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200

@app.route('/characters', methods=['GET'])
def my_characters():
    characters_query = Characters.query.all()
    all_characters = list(map(lambda character: character.serialize(), characters_query))
    return jsonify(all_characters), 200

@app.route('/characters/<int:characters_id>', methods=['GET'])
def my_character_id(characters_id):
    user1 = Characters.query.get(characters_id)

    return jsonify(user1.serialize()), 200

@app.route('/planets', methods=['GET'])
def my_planets():
    planets_query = Planets.query.all()
    all_planets = list(map(lambda planets: planets.serialize(), planets_query))
    return jsonify(all_planets), 200

@app.route('/planets/<int:planets_id>', methods=['GET'])
def my_planets_id(planets_id):
    user1 = Planets.query.get(planets_id)

    return jsonify(user1.serialize()), 200


@app.route('/ships', methods=['GET'])
def my_ships():
    ships_query = Ships.query.all()
    all_ships = list(map(lambda ships: ships.serialize(), ships_query))
    return jsonify(all_ships), 200

@app.route('/ships/<int:ships_id>', methods=['GET'])
def my_ships_id(ships_id):
    user1 = Ships.query.get(planets_id)

    return jsonify(user1.serialize()), 200

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
