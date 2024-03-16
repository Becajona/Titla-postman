# productos.py
from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from bson import Decimal128, ObjectId
from datetime import datetime
from flask import Flask, jsonify
from flask_pymongo import PyMongo
from bson import Decimal128, ObjectId

from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb+srv://ros:ros2021@cluster0.ymcp4od.mongodb.net/db_administrator?retryWrites=true&w=majority'
mongo = PyMongo(app)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

@app.route('/api/v1/productos/get_all', methods=['GET'])
def listar_prod():
    # Recuperar todos los productos de la colección 'productos'
    productos_cursor = mongo.db.productos.find({})

    # Convertir el cursor a una lista de diccionarios
    productos = list(productos_cursor)

    # Convertir los valores de Decimal128 a float
    for producto in productos:
        for key, value in producto.items():
            if isinstance(value, Decimal128):
                producto[key] = float(str(value))
            elif isinstance(value, ObjectId):
                producto[key] = str(value)

    # Devolver los productos como JSON
    return jsonify(productos)


@app.route('/api/v1/productos/porID/<string:id>', methods=['GET'])
def obtener_PorID(id):
    try:
        # Intenta convertir el ID a ObjectId
        object_id = ObjectId(id)

        # Construir la consulta para buscar el producto por su ID
        query = {'_id': object_id}

        # Realizar la búsqueda en la colección 'productos'
        resultado = mongo.db.productos.find_one(query)

        if resultado:
            # Convertir el ObjectId a una cadena
            resultado['_id'] = str(resultado['_id'])
            # Si la consulta es exitosa, devuelve los datos en formato JSON
            return jsonify(resultado)
        else:
            # Si no se encuentra el documento, devuelve un mensaje adecuado
            return jsonify({"error": "No se encontró ningún producto con el ID proporcionado"}), 404
    except Exception as e:
        # Manejo de la excepción, indica que el ID proporcionado no es válido
        return jsonify({"error": "El ID proporcionado no es válido"}), 400




@app.route('/api/v1/productos/nuevoProd', methods=['POST'])
def add_producto():
    try:
        data = request.get_json()

        # Validar campos requeridos
        required_fields = ['nombre', 'categoria', 'costo', 'precio', 'foto', 'fechaAdquisicion', 'cantidadExistente', 'estado', 'origen', 'provId', 'marcasId']
        if not all(field in data for field in required_fields):
            return jsonify({"error": "Faltan campos requeridos"}), 400

        # Convertir la fecha (suponiendo que 'fechaAdquisicion' está en formato ISO)
        fechaAdq = datetime.fromisoformat(data['fechaAdquisicion'])

        # Verificar duplicado (por ejemplo, por nombre)
        if mongo.db.productos.find_one({"nombre": data['nombre']}):
            return jsonify({"error": "Producto duplicado"}), 400

        # Verificar que provId sea un ObjectId válido
        try:
            prov_id = str(data['provId'])
        except Exception as e:
            return jsonify({"error": "El provId no es un string válido"}), 400

        # Preparar los datos del producto
        product = {
            "_id": str(ObjectId()),
            "clave": data.get('clave', ''), # Asegurarse de manejar el caso en que 'clave' no esté presente en los datos
            "nombre": data['nombre'],
            "categoria": data['categoria'],
            "marcasId": data['marcasId'],
            "version": data.get('version', ''), # Asegurarse de manejar el caso en que 'version' no esté presente en los datos
            "idiomas": data.get('idiomas', []), # Asegurarse de manejar el caso en que 'idiomas' no esté presente en los datos
            "jugadores": data.get('jugadores', 1), # Asegurarse de manejar el caso en que 'jugadores' no esté presente en los datos
            "descripcion": data.get('descripcion', ''), # Asegurarse de manejar el caso en que 'descripcion' no esté presente en los datos
            "costo": data['costo'],
            "precio": data['precio'],
            "foto": data['foto'],
            "fechaAdquisicion": fechaAdq,
            "fecharegistro": str(datetime.now()),
            "cantidadExistente": data['cantidadExistente'],
            "estado": data['estado'],
            "origen": data['origen'],
            "provId": prov_id,
        }

        # Insertar en la base de datos
        result = mongo.db.productos.insert_one(product)

        if result.inserted_id:
            # Devolver mensaje de éxito e ID del producto insertado
            return jsonify({"mensaje": "Producto insertado", "id": str(result.inserted_id)}), 201
        else:
            return jsonify({"error": "Producto no insertado"}), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=4000, debug=True)

    
    