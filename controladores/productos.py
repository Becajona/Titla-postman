# productos.py
from flask import Blueprint, Flask, jsonify, request
from flask_pymongo import PyMongo
from bson import Decimal128, ObjectId
from datetime import datetime

from bson import Decimal128, ObjectId
from bson import ObjectId

from flask import Blueprint, jsonify
from flask_pymongo import PyMongo

productos = Blueprint('productos', __name__, url_prefix='/api/v1/productos')

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb+srv://ros:ros2021@cluster0.ymcp4od.mongodb.net/db_administrator?retryWrites=true&w=majority'
mongo = PyMongo(app)
@productos.route('/get_all', methods=['GET'])
def get_productos():
    try:
        productos_cursor = mongo.db.productos.find({})
        productos_list = [producto for producto in productos_cursor]
        
        # Convertir el ID del producto a una cadena
        for producto in productos_list:
            producto['_id'] = str(producto['_id'])

        # Agregar el ID del proveedor como una cadena si existe
        for producto in productos_list:
            if 'provId' in producto:
                producto['provId'] = str(producto['provId'])

        return jsonify(productos_list), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


#CREAR

@productos.route('/nuevoProd', methods=['POST'])
def agregar_nuevo_producto():
    try:
        data = request.get_json()

        required_fields = ['nombre', 'categoria', 'marcasId', 'version', 'idiomas', 'jugadores', 'descripcion', 'costo', 'precio', 'foto', 'cantidadExistente', 'estado', 'origen', 'provId']
        if not all(field in data for field in required_fields):
            return jsonify({"error": "Faltan campos requeridos"}), 400

        # Convierte provId a ObjectId para buscar el proveedor en la base de datos
        prov_id = ObjectId(data['provId'])
        proveedor = mongo.db.proveedores.find_one({"_id": prov_id})
        if not proveedor:
            return jsonify({"error": "El proveedor especificado no existe"}), 400

        # Crea el objeto de producto, convirtiendo provId a cadena
        producto = {
            "nombre": str(data['nombre']),
            "categoria": str(data['categoria']),
            "marcasId": str(data['marcasId']),
            "version": str(data.get('version', '')), 
            "idiomas": str(data['idiomas']),
            "jugadores": int(data.get('jugadores', 1)), 
            "descripcion": str(data.get('descripcion', '')), 
            "costo": int(data['costo']),
            "precio": int(data['precio']),
            "foto": str(data['foto']),
            "cantidadExistente": int(data['cantidadExistente']),
            "estado": str(data['estado']),
            "origen": str(data['origen']),
            "provId": str(prov_id),  # Convierte el ObjectId a cadena
        }

        # Insertamos el producto en la base de datos
        result = mongo.db.productos.insert_one(producto)

        if result.inserted_id:
            return jsonify({"mensaje": "Producto insertado", "id": str(result.inserted_id)}), 201
        else:
            return jsonify({"error": "Producto no insertado"}), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500



@productos.route('/porID/<string:id>', methods=['GET'])
def obtener_producto_por_id(id):
    try:
        object_id = ObjectId(id)

        query = {'_id': object_id}

        resultado = mongo.db.productos.find_one(query, {'_id': 0})  

        if resultado:
            # Convertir el ID del proveedor a una cadena si existe
            if 'provId' in resultado:
                resultado['provId'] = str(resultado['provId'])
            
            return jsonify(resultado)
        else:
            return jsonify({"error": "No se encontró ningún producto con el ID proporcionado"}), 404
    except Exception as e:
        return jsonify({"error": "Ha ocurrido un error"}), 500

    
    
@productos.route('/actualizar/<string:id>', methods=['PUT'])
def actualizar_producto(id):
    try:
        if request.content_type != 'application/json':
            return jsonify({"error": "Unsupported Media Type: Content-Type must be 'application/json'"}), 415

        data = request.get_json()

       
        if '_id' in data:
            del data['_id']

        
        required_fields = ['nombre', 'categoria', 'version','idiomas','jugadores','descripcion','costo', 'precio', 'foto', 'cantidadExistente', 'estado', 'origen', 'provId', 'marcasId']
        if not all(field in data for field in required_fields):
            return jsonify({"error": "Faltan campos requeridos"}), 400


        
        producto_actualizado = { 
            "nombre": str(data['nombre']),
            "categoria": str(data['categoria']),
            "marcasId": str(data['marcasId']),
            "version": str(data.get('version', '')), 
            "idiomas": str(data['idiomas']),
            "jugadores": int(data.get('jugadores', 1)), 
            "descripcion": str(data.get('descripcion', '')), 
            "costo": int(data['costo']), 
            "precio": int(data['precio']),  
            "foto": str(data['foto']),
            "cantidadExistente": int(data['cantidadExistente']),
            "estado": str(data['estado']),
            "origen": str(data['origen']),
            "provId": str(data['provId']), 
        }

        
        resultado = mongo.db.productos.update_one({'_id': ObjectId(id)}, {"$set": producto_actualizado})

        if resultado.modified_count:
            return jsonify({"mensaje": "Documento actualizado"})
        else:
            return jsonify({"mensaje": "Documento no encontrado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500




#Eliminar
@productos.route('/eliminar/<string:id>', methods=['DELETE'])
def eliminar_producto(id):
    try:
        
        str_id = str(id)

        
        object_id = ObjectId(str_id)

       
        resultado = mongo.db.productos.delete_one({'_id': object_id})
        
        if resultado.deleted_count:
           
            return jsonify({"mensaje": "Documento eliminado"})
        else:
            
            return jsonify({"mensaje": "Documento no encontrado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
