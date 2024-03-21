from flask import Flask
from flask_cors import CORS
from productos import productos
from carrito import carrito
from Usuario import usuario
from cliente import client
from marcas import marcas
from proveedores import proveedor
from empleados import empleados

app = Flask(__name__)
CORS(app)

app.config['MONGO_URI'] = 'mongodb+srv://ros:ros2021@cluster0.ymcp4od.mongodb.net/db_administrator?retryWrites=true&w=majority'

app.register_blueprint(productos)
app.register_blueprint(proveedor)
app.register_blueprint(carrito)
app.register_blueprint(usuario)
app.register_blueprint(client)
app.register_blueprint(marcas)
app.register_blueprint(empleados)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=4000, debug=True)
