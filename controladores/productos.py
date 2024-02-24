from datetime import datetime
from flask import Blueprint
from app import create_app
from mongo import mongo
from flask import jsonify
from bson.json_util import dumps
from bson.objectid import ObjectId
import json
from flask import request
from bson import ObjectId
from flask import Flask
from flask_cors import CORS
from flask_pymongo import PyMongo

# ________________________________________________________________________________________
prod = Blueprint("products", __name__)
app = create_app()


@prod.route('/productos/get_all', methods=['GET'])
def listar_prod():
    data = mongo.db.productos.find({})
    r = dumps(data)
    return r

# _______________________________________________________________________________________from flask import Flask, jsonify



@app.route('/productos/porNombre/<string:nombre>', methods=['GET'])
def obtener_PorNombre(nombre):
    try:
        # Utiliza ObjectId solo si el parámetro es un ObjectId válido
        if ObjectId.is_valid(nombre):
            query = {'_id': ObjectId(nombre)}
        else:
            query = {'nombre': {'$eq': nombre}}

        sort = [('nombre', 1)]
        project = {
            '_id': 1,
            'nombre': 1,
            'categoria': 1,
            'version': 1,
            'precio': 1,
            'estado': 1
        }

        resultado = list(mongo.db.productos.find(query, project).sort(sort))

        if resultado:
            # Si la consulta es exitosa, devuelve los datos en formato JSON
            return jsonify(resultado)
        else:
            # Si no se encuentra el documento, devuelve un mensaje adecuado
            return jsonify({"mensaje": "Producto no encontrado"}), 404
    except Exception as e:
        # Manejo de la excepción, puedes personalizar el mensaje de error según tus necesidades
        return jsonify({"error": str(e)}), 500
# __________________________________________________________________________________________

#http://192.168.1.67:4000/productos/porID/65b11507d66a2764b2c2740f
#
@prod.route('/productos/porID/<string:id>', methods=['GET'])
def obtener_PorID(id):
    try:
        # Convertir el ID a ObjectId
        object_id = ObjectId(id)

        query = {'_id': object_id}
        project = {"_id": 0, "nombre": 1, "precio": 1, "categoria": 1}

        resultado = mongo.db.productos.find_one(query, project)

        if resultado:
            # Si la consulta es exitosa, devuelve los datos en formato JSON
            return jsonify(resultado)
        else:
            # Si no se encuentra el documento, devuelve un mensaje adecuado
            return jsonify({"mensaje": "Documento no encontrado"}), 404
    except Exception as e:
        # Manejo de la excepción, puedes personalizar el mensaje de error según tus necesidades
        return jsonify({"error": str(e)}), 500

# ________________________________________________________________________________________________

from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from bson import ObjectId
from datetime import datetime

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb+srv://ros:ros2021@cluster0.ymcp4od.mongodb.net/db_administrator?retryWrites=true&w=majority'
mongo = PyMongo(app)

@app.route('/productos/nuevoProd', methods=['POST'])
def add_producto():
    try:
        data = request.json

        # Validación de campos requeridos
        required_fields = ['nombre', 'categoria', 'costo', 'precio', 'foto', 'fechaAdquisicion', 'cantidadExistente', 'estado', 'origen', 'provId', 'marcasId']
        if not all(field in data for field in required_fields):
            return jsonify({"error": "Campos requeridos faltantes"}), 400

        # Convertir fecha de adquisición
        fecha_str_adq = {"$date": "2024-05-01T00:00:00Z"}
        fechaAdq = datetime.utcfromtimestamp(int(fecha_str_adq) / 1000.0)

        product = {
            "nombre": "Ejemplo de Producto",
            "categoria": {"categoria": "Adultos", "tipo": "EjemploTipo"},
            "costo": 50.0,
            "precio": 89.99,
            "foto": "ejemplo_producto.jpg",
            "fechaAdquisicion": fechaAdq,
            "cantidadExistente": 10.0,
            "estado": "Vigente",
            "origen": "Proveedor de Ejemplo",
            "provId": ObjectId("5f7f1c1b014b6a5711fdb16c"),  # Se debe reemplazar con el ObjectId correcto
            "marcasId": [ObjectId("5f7f1c1b014b6a5711fdb16d"), ObjectId("5f7f1c1b014b6a5711fdb16e")]  # Se deben reemplazar con los ObjectId correctos
            }

        # Verificar duplicados (por ejemplo, por nombre o clave) si es necesario

        # Insertar en la base de datos
        resultado = mongo.db.productos.insert_one(product)

        if resultado.inserted_id:
            # Devolver el ID del producto insertado
            return jsonify({"mensaje": "Documento insertado", "id": str(resultado.inserted_id)})
        else:
            return jsonify({"mensaje": "Documento no insertado"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

# __________________________________________________________________________________________________________

#http://192.168.1.67:4000/productos/eliminar/65b11507d66a2764b2c2740c
#
@prod.route('/productos/eliminar/<string:id>', methods=['DELETE'])
def eliminar(id):
    try:
        resultado = mongo.db.productos.delete_one({'_id': ObjectId(id)})
        
        if resultado.deleted_count:
            # Si la consulta es exitosa, devuelve los datos en formato JSON
            return jsonify({"mensaje": "Documento eliminado"})
        else:
            # Si no se encuentra el documento, devuelve un mensaje adecuado
            return jsonify({"mensaje": "Documento no encontrado"}), 404
    except Exception as e:
        
        return jsonify({"error": str(e)}), 500

# ____________________________________________________________________________________________________________
#falta
from flask import jsonify
#http://127.0.0.1:4000/productos/actualizar/65b11507d66a2764b2c27419
@prod.route('/productos/actualizar/<string:id>', methods=['PUT'])
def actualizar_costo(id):
    try:
        if request.content_type != 'application/json':
            return jsonify({"error": "Unsupported Media Type: Content-Type must be 'application/json'"}), 415

        nuevo_costo = request.json['costo']

        resultado = mongo.productos.update_one({'_id': ObjectId(id)}, {"$set": {'costo': nuevo_costo}})
        if resultado.modified_count:
            actualizar_precio(id, nuevo_costo)
            return jsonify({"mensaje": "Documento actualizado"})
        else:
            return jsonify({"mensaje": "Documento no encontrado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
def actualizar_precio(id, nuevo_costo):
    try:
        nuevo_precio = nuevo_costo + (nuevo_costo * 0.2)  # Assuming a 20% price increase
        resultado = mongo.db_administrator.productos.update_one({'_id': ObjectId(id)}, {'$set': {'precio': nuevo_precio}})
        if resultado.modified_count:
            return jsonify({"mensaje": "Precio actualizado"})
        else:
            return jsonify({"mensaje": "Documento no encontrado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ________________________________________________________________________________________________________________
#http://127.0.0.1:4000/productos/prod_prov
@prod.route('/productos/prod_prov', methods=['GET'])
def obtener_prod_prov():
    query = [
        {
            '$lookup': {
                'from': "proveedores",
                'localField': "provId",  # Assuming provId is the corresponding field in productos collection
                'foreignField': "provId",
                'as': "proveedor"
            }
        },
        {
            '$unwind': "$proveedor"
        },
        {
            '$project': {
                "_id": 0,
                "nombreprod": "$nombre",
                "precio": 1,
                "proveedor.correo": 1,
                "proveedor.nombre": 1
            }
        }
    ]

    try:
        resultado = list(mongo.db.productos.aggregate(query))
        if resultado:
            return jsonify(resultado)
        else:
            return jsonify({"mensaje": "Documento no encontrado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
