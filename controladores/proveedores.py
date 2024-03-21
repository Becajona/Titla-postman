from flask import Blueprint, Flask, jsonify
from flask_pymongo import PyMongo
from bson import ObjectId
from flask import Flask
from flask_cors import CORS
from flask import request, jsonify
from bson import ObjectId

from flask import Blueprint, jsonify
from flask_pymongo import PyMongo


proveedor = Blueprint("proveedores", __name__, url_prefix='/api/v1/proveedores')

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb+srv://ros:ros2021@cluster0.ymcp4od.mongodb.net/db_administrator?retryWrites=true&w=majority'
mongo = PyMongo(app)

@proveedor.route('/get_all', methods=['GET'])
def listar_proveedores():
    proveedores_cursor = mongo.db.proveedores.find({})
    proveedores_list = [proveedor for proveedor in proveedores_cursor]
    
    for proveedor in proveedores_list:
        proveedor['_id'] = str(proveedor['_id'])
    
    return jsonify(proveedores_list)



@proveedor.route('/nuevoprove', methods=['POST'])
def agregar_nuevo_proveedor():
    try:
        data = request.get_json()

       
        required_fields = ['provId', 'nombre', 'direccion', 'correoElectronico', 'telefono']
        if not all(field in data for field in required_fields):
            return jsonify({"error": "Faltan campos requeridos"}), 400

        
        proveedor = {
            "provId": str(data['provId']),
            "nombre": str(data['nombre']),
            "direccion": str(data['direccion']),
            "correoElectronico": str(data['correoElectronico']),
            "telefono": int(data['telefono'])  
        }

        
        result = mongo.db.proveedores.insert_one(proveedor)

        if result.inserted_id:
            
            return jsonify({"mensaje": "Proveedor insertado", "id": str(result.inserted_id)}), 201
        else:
            return jsonify({"error": "Proveedor no insertado"}), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@proveedor.route('/porID/<string:id>', methods=['GET'])
def obtener_proveedor_por_id(id):
    try:
        object_id = ObjectId(id)

        query = {'_id': object_id}

        resultado = mongo.db.proveedores.find_one(query, {'_id': 0}) 

        if resultado:
            return jsonify(resultado)
        else:
            return jsonify({"error": "No se encontró ningún proveedor con el ID proporcionado"}), 404
    except Exception as e:
        return jsonify({"error": "Ha ocurrido un error"}), 500




@proveedor.route('/actualizar/<string:id>', methods=['PUT'])
def actualizar_proveedor(id):
    try:
        if request.content_type != 'application/json':
            return jsonify({"error": "Unsupported Media Type: Content-Type must be 'application/json'"}), 415

        data = request.get_json()

        if '_id' in data:
            del data['_id']

        required_fields = ['correoElectronico', 'direccion', 'nombre', 'provId', 'telefono']
        if not all(field in data for field in required_fields):
            return jsonify({"error": "Faltan campos requeridos"}), 400

        proveedor_actualizado = {
            "correoElectronico": str(data['correoElectronico']),
            "direccion": str(data['direccion']),
            "nombre": str(data['nombre']),
            "provId": str(data['provId']),
            "telefono": int(data['telefono']),  
        }

        resultado = mongo.db.proveedores.update_one({'_id': ObjectId(id)}, {"$set": proveedor_actualizado})

        if resultado.modified_count:
            return jsonify({"mensaje": "Documento actualizado"})
        else:
            return jsonify({"mensaje": "Documento no encontrado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@proveedor.route('/eliminar/<string:id>', methods=['DELETE'])
def eliminar_proveedor(id):
    try:
        str_id = str(id)

        object_id = ObjectId(str_id)

        resultado = mongo.db.proveedores.delete_one({'_id': object_id})
        
        if resultado.deleted_count:
            return jsonify({"mensaje": "Proveedor eliminado"})
        else:
            return jsonify({"mensaje": "Proveedor no encontrado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500




