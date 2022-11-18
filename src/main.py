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
from models import db, User
from models import db, Fav
from models import db, Planet
from models import db, Char
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


@app.route('/users', methods=['POST'])
def crear_user():
    body = request.get_json()
    if body == None: # se podría usar en vez de "==", "is", para validar, pero tiene otros usos
        return "Error, envie la información correctamente"
  
    email = body["email"]
    password = body["password"]

    user = User(
        email= email,
        password = password,
        is_active = True
    )

    db.session.add(user)#el db, viene de sql alchemy, como se ve en el archivo models.py
    db.session.commit()#mandar la información a la base de datos

    return jsonify(user.serialize())

@app.route('/users/listar', methods=['GET'])
def listar_users():
    users = User.query.all()
    #resultado = [user.serialize()for user in users]
    result=[]
    for user in users:
        result.append(user.serialize())
    return jsonify(result)
    #return jsonify(USERS)

@app.route('/users/listar/<int:id>', methods=['GET'])
def user(id):
    user = User.query.get(id)# el .query, viene de user, que viene del archivo __init__.py, ya que user hereda de db.model
    if user is None:
        return "no existe el usuario con id"+str(id)
    return jsonify(user.serialize())

@app.route('/addplanet', methods=['POST'])
def crear_planet():
    body = request.get_json()
    #validar!!!
    
    name = body["name"]
    # name = body.get("name")

    planet = Planet(
        name = name
    )

    db.session.add(planet)
    db.session.commit()
    return "crear_planet"

@app.route('/planet/listar', methods=['GET'])
def listar_planetas():
    planets = Planet.query.all()
    #resultado = [user.serialize()for user in users]
    result=[]
    for planet in planets:
        result.append(planet.serialize())
    return jsonify(result)

@app.route('/planet/listar/<id>', methods=['GET'])
def listar_planeta(id):
    #resultado = [user.serialize()for user in users]
    planet = Planet.query.get(id)# el .query, viene de user, que viene del archivo __init__.py, ya que user hereda de db.model
    if planet is None:
        return "no existe el planeta con id"+str(id)
    return jsonify(planet.serialize())

@app.route('/planet/listar/<id>', methods=['PUT'])
def modificar_planeta(id):
    #resultado = [user.serialize()for user in users]
    planet = Planet.query.get(id)
    body = request.get_json()
    name = body["name"]
    planet.name = name
    if planet is None:
        return "no existe el planeta con id"+str(id)

    db.session.add(planet)
    db.session.commit()
    return jsonify(planet.serialize())

@app.route('/planet/listar/<id>', methods=['DELETE'])
def borrar_planet(id):

    planetdown = Planet.query.get(id)
    db.session.delete(planetdown)
    db.session.commit()
    planets = Planet.query.all()

    result=[]
    for planet in planets:
        result.append(planet.serialize())
    return jsonify(result)


@app.route('/addchar', methods=['POST'])
def crear_char():
    body = request.get_json()
    #validar!!!

    name = body["name"]

    char = Char(
        name= name
    )

    db.session.add(char)
    db.session.commit()
    return "crear_char"

@app.route('/char/listar', methods=['GET'])
def listar_chars():
    chars = Char.query.all()
    #resultado = [user.serialize()for user in users]
    result=[]
    for char in chars:
        result.append(char.serialize())
    return jsonify(result)

@app.route('/char/listar/<id>', methods=['GET'])
def listar_char(id):
    #resultado = [user.serialize()for user in users]
    char = Char.query.get(id)
    if char is None:
        return "no existe el char con id"+str(id)
    return jsonify(char.serialize())

@app.route('/char/listar/<id>', methods=['PUT'])
def modificar_char(id):
    #resultado = [user.serialize()for user in users]
    char = Char.query.get(id)
    body = request.get_json()
    name = body["name"]
    char.name = name
    if char is None:
        return "no existe el personaje con id"+str(id)

    db.session.add(char)
    db.session.commit()
    return jsonify(char.serialize())

@app.route('/char/listar/<id>', methods=['DELETE'])
def borrar_char(id):

    chardown = Char.query.get(id)
    db.session.delete(chardown)
    db.session.commit()
    chars = Char.query.all()

    result=[]
    for char in chars:
        result.append(char.serialize())
    return jsonify(result)



@app.route('/addfav', methods=['POST'])
def crear_fav():
    body = request.get_json()
    #validar!!!

    #user_id = body.get("user_id")
    #planet_id = body.get("planet_id")
    #char_id = body.get("char_id")

    fav = Fav(
        user_id = body.get("user_id"),
        planet_id = body.get("planet_id"),
        char_id = body.get("char_id")
    )

    db.session.add(fav)
    db.session.commit()
    return "crear_fav"

@app.route('/fav/listar', methods=['GET'])
def listar_favs():
    favs = Fav.query.all()
    #resultado = [user.serialize()for user in users]
    result=[]
    for fav in favs:
        result.append(fav.serialize())
    return jsonify(result)

@app.route('/fav/listar/<int:id>', methods=['GET'])
def listar_unicofavs(id):
    favs = Fav.query.all()
    #resultado = [user.serialize()for user in users]
    result=[]
    for fav in favs:
        if fav.user_id==id:
            result.append(fav.serialize())
    return jsonify(result)

@app.route('/fav/listar/<id>', methods=['DELETE'])
def borrar_favs(id):

    favdown = Fav.query.get(id)
    db.session.delete(favdown)
    db.session.commit()
    favs = Fav.query.all()# el .query, viene de user, que viene del archivo __init__.py, ya que user hereda de db.model

    result=[]
    for favo in favs:
        result.append(favo.serialize())
    return jsonify(result)

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

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)


