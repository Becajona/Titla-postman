from flask import Blueprint, Flask, jsonify
from flask_pymongo import PyMongo
from bson import ObjectId
from flask import request, jsonify

empleados = Blueprint("empleados", __name__, url_prefix='/api/v1/empleados')

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb+srv://ros:ros2021@cluster0.ymcp4od.mongodb.net/db_administrator?retryWrites=true&w=majority'
mongo = PyMongo(app)

@empleados.route('/get_all', methods=['GET'])
def listar_empleados():
    empleados_cursor = mongo.db.empleados.find({})
    empleados_list = [empleado for empleado in empleados_cursor]
    
    for empleado in empleados_list:
        empleado['_id'] = str(empleado['_id'])
    
    return jsonify(empleados_list)

@empleados.route('/nuevoempleado', methods=['POST'])
def agregar_nuevo_empleado():
    try:
        data = request.get_json()

        required_fields = ['Nombre', 'Edad', 'Genero', 'Salario', 'Telefono']
        if not all(field in data for field in required_fields):
            return jsonify({"error": "Faltan campos requeridos"}), 400

        empleado = {
            "Nombre": str(data['Nombre']),
            "Edad": int(data['Edad']),
            "Genero": str(data['Genero']),
            "Salario": int(data['Salario']),
            "Telefono": int(data['Telefono']),
        }

        result = mongo.db.empleados.insert_one(empleado)

        if result.inserted_id:
            return jsonify({"mensaje": "Empleado insertado", "id": str(result.inserted_id)}), 201
        else:
            return jsonify({"error": "Empleado no insertado"}), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    
    
@empleados.route('/porID/<string:id>', methods=['GET'])
def obtener_empleado_por_id(id):
    try:
        object_id = ObjectId(id)
        
        query = {'_id': object_id}

        resultado = mongo.db.empleados.find_one(query, {'_id': 0})  

        if resultado:
            return jsonify(resultado)
        else:
            return jsonify({"error": "No se encontró ningún empleado con el ID proporcionado"}), 404
    except Exception as e:
        return jsonify({"error": "Ha ocurrido un error"}), 500
    
    
@empleados.route('/actualizar/<string:id>', methods=['PUT'])
def actualizar_empleado_por_id(id):
    try:
        if request.content_type != 'application/json':
            return jsonify({"error": "Unsupported Media Type: Content-Type must be 'application/json'"}), 415

        data = request.get_json()

        if '_id' in data:
            del data['_id']

        # Validar campos requeridos
        required_fields = ['Nombre', 'Edad', 'Salario', 'Genero', 'Telefono']
        if not all(field in data for field in required_fields):
            return jsonify({"error": "Faltan campos requeridos"}), 400

        empleado_actualizado = {
            "Nombre": str(data['Nombre']),
            "Edad": int(data['Edad']),
            "Salario": int(data['Salario']),
            "Genero": str(data['Genero']),
            "Telefono": int(data['Telefono'])
        }

        resultado = mongo.db.empleados.update_one({'_id': ObjectId(id)}, {"$set": empleado_actualizado})

        if resultado.modified_count:
            return jsonify({"mensaje": "Empleado actualizado"})
        else:
            return jsonify({"mensaje": "Empleado no encontrado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    
@empleados.route('/eliminar/<string:id>', methods=['DELETE'])
def eliminar_empleado_por_id(id):
    try:
        str_id = str(id)

        object_id = ObjectId(str_id)

        resultado = mongo.db.empleados.delete_one({'_id': object_id})
        
        if resultado.deleted_count:
            return jsonify({"mensaje": "Empleado eliminado"})
        else:
            return jsonify({"mensaje": "Empleado no encontrado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500