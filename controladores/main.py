# main.py

from flask import Flask
from flask_cors import CORS
from flask_pymongo import PyMongo  
from productos import app as productos
from proveedores import listar_proveedores
from carrito import carrito
from Usuario import usuario
from cliente import client
from marcas import marcas_blueprint  # Importa el blueprint de marcas

app = Flask(__name__)
CORS(app)

# Configura la URI de MongoDB
app.config['MONGO_URI'] = 'mongodb+srv://ros:ros2021@cluster0.ymcp4od.mongodb.net/db_administrator?retryWrites=true&w=majority'

# Inicializa PyMongo con la instancia de la aplicación Flask
mongo = PyMongo(app)

# Registrar los blueprints
app.register_blueprint(productos)
app.register_blueprint(proveedores)
app.register_blueprint(carrito, url_prefix='/carrito')
app.register_blueprint(usuario, url_prefix='/usuario')
app.register_blueprint(client, url_prefix='/cliente')
app.register_blueprint(marcas_blueprint, url_prefix='/marcas')  # Utiliza el objeto blueprint importado correctamente

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=4000, debug=True)
