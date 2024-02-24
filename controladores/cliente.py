from mongo import mongo 
from flask import Blueprint
from bson.json_util import dumps

client = Blueprint("cliente", __name__) 


@client.route('/cliente/get_all', methods=['GET'])
def Lista_Client():
    data = mongo.db.cliente.find({})
    r=dumps(data)
    return r