from flask import Flask, jsonify
from flask_pymongo import PyMongo
from bson import ObjectId
from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb+srv://ros:ros2021@cluster0.ymcp4od.mongodb.net/db_administrator?retryWrites=true&w=majority'
mongo = PyMongo(app)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

@app.route('/api/v1/proveedores/get_all', methods=['GET'])
def listar_proveedores():
    # Recuperar todos los proveedores de la colección 'proveedores'
    proveedores_cursor = mongo.db.proveedores.find({})

    # Convertir el cursor a una lista de diccionarios
    proveedores = list(proveedores_cursor)

    # Convertir ObjectId a str para cada proveedor
    for proveedor in proveedores:
        proveedor['_id'] = str(proveedor['_id'])

    # Devolver los proveedores como JSON
    return jsonify(proveedores)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=4000, debug=True)
