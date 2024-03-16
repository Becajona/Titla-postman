# marcas.py

from flask import Blueprint, jsonify
from flask_pymongo import PyMongo  # Importa PyMongo
from flask_pymongo import PyMongo
from bson import ObjectId
from flask import Flask
from flask_cors import CORS
# Crea un objeto Blueprint para las marcas
marcas_blueprint = Blueprint("marcas", __name__)


app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb+srv://ros:ros2021@cluster0.ymcp4od.mongodb.net/db_administrator?retryWrites=true&w=majority'
mongo = PyMongo(app)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

@app.route('/api/v1/marcas/get_all', methods=['GET'])
def listar_marcas():
    # Recuperar todas las marcas de la colección 'marcas'
    marcas_cursor = mongo.db.marcas.find({})

    # Convertir el cursor a una lista de diccionarios
    marcas = list(marcas_cursor)

    # Convertir ObjectId a str para cada marca
    for marca in marcas:
        marca['_id'] = str(marca['_id'])

    # Devolver las marcas como JSON
    return jsonify(marcas)
