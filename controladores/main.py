from app import create_app
from productos import prod
from proveedores import prove
from carrito import carrito
from Usuario import usuario
from cliente import client
from marcas import marcas



app = create_app()
app.register_blueprint(prod)
app.register_blueprint(prove)
app.register_blueprint(carrito)
app.register_blueprint(usuario)
app.register_blueprint(client)
app.register_blueprint(marcas)



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=4000, debug=True)