from flask import Blueprint
from bson.json_util import dumps
from mongo import mongo
from datetime import datetime
from app import create_app
from mongo import mongo
from flask import jsonify
from bson.json_util import dumps
from bson.objectid import ObjectId
import json
from flask import request

prove = Blueprint("provee", __name__)


@prove.route('/proveedores/get_all', methods=['GET'])
def listar_prove():
    data = mongo.db.proveedores.find({})
    r = dumps(data)
    return r


# ____________________________________________________________________________________________________
#http://192.168.1.67:4000/proveedores/porNombre/Proveedor C
@prove.route('/proveedores/porNombre/<string:nombre>', methods=['GET'])
def obtener_PorNombre(nombre):
    query = {'nombre': {'$eq': nombre}}
    sort = [('nombre', 1)]
    project = {
        '_id': 0,
        'nombre': 1,
        'direccion':1,
        'telefono': 1,
        'correoElectronico': 1  
    }

    try:
        resultado = list(mongo.db.proveedores.find(query, project).sort(sort))

        if resultado:
            # Si la consulta es exitosa, devuelve los datos en formato JSON
            return jsonify(resultado)
        else:
            # Si no se encuentra el documento, devuelve un mensaje adecuado
            return jsonify({"mensaje": "Documento no encontrado"}), 404
    except Exception as e:
        # Manejo de la excepción, puedes personalizar el mensaje de error según tus necesidades
        return jsonify({"error": str(e)}), 500

# ___________________________________________________________________________________________________________
#http://192.168.1.67:4000/proveedores/porID/65b11513d66a2764b2c2741e
@prove.route('/proveedores/porID/<string:id>', methods=['GET'])
def obtener_PorID(id):
    query = {'_id': ObjectId(id)}
    project = {"_id": 0, "nombre": 1, "telefono": 1, "correoElectronico": 1, "direccion": 1}  
    try:
        resultado = mongo.db.proveedores.find_one(query, project)
        if resultado:
            # Si la consulta es exitosa, devuelve los datos en formato JSON
            return jsonify(resultado)
        else:
            # Si no se encuentra el documento, devuelve un mensaje adecuado
            return jsonify({"mensaje": "Documento no encontrado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
