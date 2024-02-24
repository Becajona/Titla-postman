from mongo import mongo 
from flask import Blueprint
from bson.json_util import dumps
from app import create_app
from mongo import mongo 
from flask import Blueprint
from bson.json_util import dumps
from flask import jsonify
from bson import ObjectId
from flask import request
from datetime import datetime

usuario = Blueprint("usuario", __name__)

@usuario.route('/usuario/get_all', methods=['GET'])
def Lista_Client():
    data = mongo.db.usuarios.find({})
    r=dumps(data)
    return r

#http://192.168.1.67:4000/usuario/Jonathan/1234
@usuario.route('/usuario/<email>/<password>', methods=['GET'])
def Buscar_usuario(email, password):
    try:
        result = mongo.db.usuarios.find_one({"email": email, "password": password},{"_id":0,"email":1,"password":1, "rol":1})
        if result:
            return jsonify("mensaje", "True")
        else:
            return jsonify("mensaje", "false")
    except Exception as e:
        return jsonify({"error", str(e)}), 500
    
    
#http://192.168.1.67:4000/usuario/eliminar/65d697ee4206cb2d82c21a75  
#Delete postman
@usuario.route('/usuario/eliminar/<string:id>', methods=['DELETE'])
def eliminar(id):
    try:
        resultado = mongo.db.usuarios.delete_one({'_id': ObjectId(id)})
        if resultado:
            return jsonify ({"mensaje": "Documento Eliminado"})
        else:
            return jsonify({"mensaje": "Documento no encontrado"})
    except Exception as e:
        return jsonify({"error": str(e)}),500
    
    
#http://192.168.1.67:4000/proveedor/nuevoProd
#postman post
@usuario.route('/proveedor/nuevoProd', methods=['POST'])
def add_producto():
    try:
        n = request.json["nombre"]
        c = request.json["contacto"]
        po = request.json["direccion"]
        co = request.json["correo_electronico"]

        if request.method == 'POST':
            product = {
                "nombre": n,
                "contacto": c,
                "direccion": po,
                "correo_electronico": co
            }

            resultado = mongo.db.proveedores.insert_one(product)

            if resultado.inserted_id:
                # Si la consulta es exitosa, devuelve los datos en formato JSON
                return jsonify({"mensaje": "Documento insertado"})
            else:
                # Si no se pudo insertar el documento, devuelve un mensaje
                return jsonify({"mensaje": "Documento no insertado"}), 404

    except Exception as e:
        # Manejo de la excepción, puedes personalizar el mensaje de error según tus necesidades
        return jsonify({"error": str(e)}), 500
