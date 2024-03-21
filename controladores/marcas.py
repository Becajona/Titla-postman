from flask import Blueprint, Flask, jsonify
from flask_pymongo import PyMongo
from bson import ObjectId
from flask import Flask
from flask_cors import CORS
from flask import request, jsonify
from bson import ObjectId


from flask import Blueprint, Flask, jsonify
from flask_pymongo import PyMongo

marcas = Blueprint("marcas", __name__, url_prefix='/api/v1/marcas')

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb+srv://ros:ros2021@cluster0.ymcp4od.mongodb.net/db_administrator?retryWrites=true&w=majority'
mongo = PyMongo(app)

@marcas.route('/get_all', methods=['GET'])
def listar_marcas():
    marcas_cursor = mongo.db.marcas.find({})
    marcas_list = [marca for marca in marcas_cursor]
    
    for marca in marcas_list:
        marca['_id'] = str(marca['_id'])
    
    return jsonify(marcas_list)




@marcas.route('/nuevamarca', methods=['POST'])
def agregar_nueva_marca():
    try:
        data = request.get_json()

        required_fields = ['marcaId', 'nombre', 'segmentoMercado', 'slogan', 'productosDestacados']
        if not all(field in data for field in required_fields):
            return jsonify({"error": "Faltan campos requeridos"}), 400

        marca = {
            "marcaId": int(data['marcaId']),
            "nombre": str(data['nombre']),
            "segmentoMercado": str(data['segmentoMercado']),
            "slogan": str(data['slogan']),
            "productosDestacados": str (data['productosDestacados']),
        }

        result = mongo.db.marcas.insert_one(marca)

        if result.inserted_id:
            return jsonify({"mensaje": "Marca insertada", "id": str(result.inserted_id)}), 201
        else:
            return jsonify({"error": "Marca no insertada"}), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    
from bson import ObjectId

@marcas.route('/porID/<string:id>', methods=['GET'])
def obtener_marca_por_id(id):
    try:
        object_id = ObjectId(id)
        
        query = {'_id': object_id}

        resultado = mongo.db.marcas.find_one(query, {'_id': 0})  

        if resultado:
            return jsonify(resultado)
        else:
            return jsonify({"error": "No se encontró ninguna marca con el ID proporcionado"}), 404
    except Exception as e:
        return jsonify({"error": "Ha ocurrido un error"}), 500
    
    
    
#FALTA CORREGIR
from bson import ObjectId

@marcas.route('/actualizar/<string:id>', methods=['PUT'])
def actualizar_marca(id):
    try:
        if request.content_type != 'application/json':
            return jsonify({"error": "Unsupported Media Type: Content-Type must be 'application/json'"}), 415

        data = request.get_json()

        if '_id' in data:
            del data['_id']

        # Validar campos requeridos
        required_fields = ['marcaId', 'nombre', 'segmentoMercado', 'slogan', 'productosDestacados']
        if not all(field in data for field in required_fields):
            return jsonify({"error": "Faltan campos requeridos"}), 400

        marca_actualizada = {
            "marcaId": int(data['marcaId']),
            "nombre": str(data['nombre']),
            "segmentoMercado": str(data['segmentoMercado']),
            "slogan": str(data['slogan']),
            "productosDestacados": str(data['productosDestacados']),
        }

        resultado = mongo.db.marcas.update_one({'_id': ObjectId(id)}, {"$set": marca_actualizada})

        if resultado.modified_count:
            return jsonify({"mensaje": "Documento actualizado"})
        else:
            return jsonify({"mensaje": "Documento no encontrado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    
    from bson import ObjectId

@marcas.route('/eliminar/<string:id>', methods=['DELETE'])
def eliminar_marca(id):
    try:
        str_id = str(id)

        object_id = ObjectId(str_id)

        resultado = mongo.db.marcas.delete_one({'_id': object_id})
        
        if resultado.deleted_count:
      
            return jsonify({"mensaje": "Marca eliminada"})
        else:
            return jsonify({"mensaje": "Marca no encontrada"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


