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

if __name__ == '__main__':
    app.run(debug=True)

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


@app.route('/productos/nuevoProd', methods=['POST'])
def add_producto():
    try:
        # Obtener datos del JSON enviado en la solicitud
        n = request.json["nombre"]
        cat = request.json["categoria"]["categoria"]
        desc = request.json["categoria"]["tipo"]
        cos = request.json["costo"]
        pre = request.json["precio"]
        f = request.json['foto']
        fecha_str_adq = request.json["fechaAdquisicion"]["$date"]
        fechaAdq = datetime.utcfromtimestamp(int(fecha_str_adq) / 1000.0)
        ce = request.json["cantidadExistente"]
        e = request.json["estado"]
        orig = request.json["origen"]
        provId = ObjectId(request.json["provId"])  # Convert provId to ObjectId
        marcasId = [ObjectId(m) for m in request.json["marcasId"]]  # Convert marcasId list to ObjectId

        if request.method == 'POST':
            product = {
                "nombre": n,
                "categoria": {"categoria": cat, "tipo": desc},
                "costo": cos,
                "precio": pre,
                "foto": f,
                "fechaAdquisicion": fechaAdq,
                "cantidadExistente": ce,
                "estado": e,
                "origen": orig,
                "provId": provId,
                "marcasId": marcasId
            }

            resultado = mongo.db.productos.insert_one(product)

            if resultado.inserted_id:
                # Si la consulta es exitosa, devuelve los datos en formato JSON
                return jsonify({"mensaje": "Documento insertado"})
            else:
                # Si no se pudo insertar el documento, devuelve un mensaje
                return jsonify({"mensaje": "Documento no insertado"}), 404

    except Exception as e:
        # Manejo de la excepción, puedes personalizar el mensaje de error según tus necesidades
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
@prod.route('/productos/actualizar/<string:id>', methods=['PUT'])
def actualizar_costo(id):
    nuevo_costo = request.json['costo']
    try:
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
        nuevo_precio = nuevo_costo + (nuevo_costo * 0.2)  # Asumiendo un 20% de incremento en el precio
        resultado = mongo.db_administrator.productos.update_one({'_id': ObjectId(id)}, {'$set': {'precio': nuevo_precio}})
        if resultado.modified_count:
            return jsonify({"mensaje": "Precio actualizado"})
        else:
            return jsonify({"mensaje": "Documento no encontrado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ________________________________________________________________________________________________________________
#http://192.168.1.67:4000/productos/prod_prov
@prod.route('/productos/prod_prov', methods=['GET'])
def obtener_prod_prov():
    query = [
        {
            '$lookup': {
                'from': "proveedores",
                'localField': "_id",
                'foreignField': "idProveedor",
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
