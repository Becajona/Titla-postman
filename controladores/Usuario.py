from flask import Blueprint, jsonify, request
from bson.json_util import dumps
from mongo import mongo
from flask import Blueprint, Flask, jsonify, request
from flask_pymongo import PyMongo
from bson import Decimal128, ObjectId
from datetime import datetime

from bson import Decimal128, ObjectId
from bson import ObjectId

from flask import Blueprint, jsonify
from flask_pymongo import PyMongo

usuario = Blueprint("usuarios", __name__, url_prefix='/api/v1/usuarios')

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb+srv://ros:ros2021@cluster0.ymcp4od.mongodb.net/db_administrator?retryWrites=true&w=majority'
mongo = PyMongo(app)

@usuario.route('/get_all', methods=['GET'])
def listar_usuarios():
    usuarios_cursor = mongo.db.usuarios.find({})
    usuarios_list = [usuario for usuario in usuarios_cursor]
        
    for usuario in usuarios_list:
            usuario['_id'] = str(usuario['_id'])
    return jsonify(usuarios_list), 200
       
    
    
    
@usuario.route('/nuevousuario', methods=['POST'])
def agregar_nuevo_usuario():
    try:
        data = request.get_json()

        required_fields = ['email', 'password', 'rol']
        if not all(field in data for field in required_fields):
            return jsonify({"error": "Faltan campos requeridos"}), 400

        usuario = {
            "email": str(data['email']),
            "password": str(data['password']),
            "rol": str(data['rol'])
        }

        result = mongo.db.usuarios.insert_one(usuario)

        if result.inserted_id:
            return jsonify({"mensaje": "Usuario insertado", "id": str(result.inserted_id)}), 201
        else:
            return jsonify({"error": "Usuario no insertado"}), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@usuario.route('/porID/<string:id>', methods=['GET'])
def obtener_usuario_por_id(id):
    try:
        object_id = ObjectId(id)
        
        query = {'_id': object_id}

        resultado = mongo.db.usuarios.find_one(query, {'_id': 0})  

        if resultado:
            return jsonify(resultado)
        else:
            return jsonify({"error": "No se encontró ningún usuario con el ID proporcionado"}), 404
    except Exception as e:
        return jsonify({"error": "Ha ocurrido un error"}), 500


@usuario.route('/actualizar/<string:id>', methods=['PUT'])
def actualizar_usuario(id):
    try:
        if request.content_type != 'application/json':
            return jsonify({"error": "Unsupported Media Type: Content-Type must be 'application/json'"}), 415

        data = request.get_json()

        if '_id' in data:
            del data['_id']

        # Validar campos requeridos
        required_fields = ['email', 'password', 'rol']
        if not all(field in data for field in required_fields):
            return jsonify({"error": "Faltan campos requeridos"}), 400

        usuario_actualizado = {
            "email": str(data['email']),
            "password": str(data['password']),
            "rol": str(data['rol'])
        }

        resultado = mongo.db.usuarios.update_one({'_id': ObjectId(id)}, {"$set": usuario_actualizado})

        if resultado.modified_count:
            return jsonify({"mensaje": "Usuario actualizado"})
        else:
            return jsonify({"mensaje": "Usuario no encontrado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@usuario.route('/eliminar/<string:id>', methods=['DELETE'])
def eliminar_usuario_por_id(id):
    try:
        str_id = str(id)
        object_id = ObjectId(str_id)
        resultado = mongo.db.usuarios.delete_one({'_id': object_id})
        
        if resultado.deleted_count:
            return jsonify({"mensaje": "Usuario eliminado"})
        else:
            return jsonify({"mensaje": "Usuario no encontrado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
