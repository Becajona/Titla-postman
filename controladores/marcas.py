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
marcas = Blueprint("marcas", __name__)

@marcas.route('/marcas/get_all', methods=['GET'])
def listar_marcas():
    data = mongo.db.marcas.find({})
    r = dumps(data)
    return r
