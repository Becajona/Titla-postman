from mongo import mongo 
from flask import Blueprint
from bson.json_util import dumps
from app import create_app
from flask import Blueprint
from bson.json_util import dumps
from flask import jsonify
from bson import ObjectId
from flask import request
from datetime import datetime
from flask import Flask, jsonify
from bson.json_util import dumps



carrito = Blueprint("carrito", __name__)

#http://127.0.0.1:4000/carrito/get_all
@carrito.route('/carrito/get_all', methods=['GET'])
def Lista_Client():
    data = mongo.db.carrito.find({})
    r=dumps(data)
    return r
#
from flask import jsonify
from bson.json_util import dumps

@carrito.route('/carrito/porNombre/<string:nombre>', methods=['GET'])
def obtener_PorNombre(nombre):  
    query = {'nombre': nombre}  # Simplificamos la consulta
    project = {"_id": 0, "nombre": 1, 'correo': 1, 'contrasena': 1, 'tipo_usuario': 1}
    
    try:
        resultado = mongo.db.carrito.find_one(query, project)
        
        if resultado is not None:
            # Agregamos líneas para imprimir información de depuración
            print("Resultado encontrado:")
            print(resultado)
            return dumps(resultado)
        else:
            # Agregamos líneas para imprimir información de depuración
            print("Carrito no encontrado para el nombre:", nombre)
            return dumps({"mensaje": "Carrito no encontrado"}), 404
    except Exception as e:
        # Agregamos líneas para imprimir información de depuración
        print("Error durante la búsqueda:", str(e))
        return jsonify({"error": str(e)}), 500

#

@carrito.route('/carrito/porID/<string:id>', methods=['GET'])
def obtener_PorID(id):
    try:
        # Convertir el ID a ObjectId
        carrito_id = ObjectId(id)

        # Agregar líneas de impresión para depuración
        print(f'ID a buscar: {carrito_id}')
        
        # Realizar la operación de agregación
        resultado = mongo.db.carrito.aggregate([
            {
                '$match': {
                    '_id': carrito_id
                }
            },
            {
                '$lookup': {
                    'from': 'clientes',
                    'localField': 'cliente_id',
                    'foreignField': '_id',
                    'as': 'cliente_info'
                }
            },
            {
                '$unwind': '$cliente_info'
            },
            {
                '$project': {
                    '_id': 1,
                    'FechaCreacion': 1,
                    'ListaProductos': 1,
                    'cliente_info.nombre': 1,
                    'cliente_info.correo': 1,
                    'cliente_info.contrasena': 1,
                    'cliente_info.tipo_usuario': 1
                }
            }
        ])

        resultado = list(resultado)  # Convertir el resultado del agregado a una lista
        
        # Agregar líneas de impresión para depuración
        print(f'Resultado de la agregación: {resultado}')

        if resultado:
            # Acceder a los valores del campo 'FechaCreacion' de manera específica
            timestamp_obj = resultado[0]["FechaCreacion"]["$timestamp"]
            timestamp = timestamp_obj["t"]
            resultado[0]["FechaCreacion"] = datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

            return jsonify(resultado[0])
        else:
            return jsonify({"mensaje": "Documento no encontrado"}), 404

    except Exception as e:
        # Agregar líneas de impresión para depuración
        print(f'Error durante la ejecución: {str(e)}')
        return jsonify({"error": str(e)}), 500




    
#http://127.0.0.1:4000/carrito/eliminar/65da3a1e7439ecd396150110
#Delete
@carrito.route('/carrito/eliminar/<string:id>', methods=['DELETE'])
def eliminar(id):
    try:
        resultado = mongo.db.carrito.delete_one({'_id': ObjectId(id)})
        if resultado:
            return jsonify ({"mensaje": "Documento Eliminado"})
        else:
            return jsonify({"mensaje": "Documento no encontrado"})
    except Exception as e:
        return jsonify({"error": str(e)}),500
