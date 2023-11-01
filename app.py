from flask import Flask, request, jsonify 
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
#import os

app = Flask(__name__)
CORS(app)
#creamos una base de datos, pasamos en el directorio base al que queremos que vaya y le damos el nombre
#basedir = os.path.abspath(os.path.dirname(__file__))
#app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "app.sqlite")
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://dpvnsahhloytfq:ac81d880e6558b468b51ecf1ae447232ab9032fae3ac55709ffdc1376c1c74cc@ec2-54-171-193-12.eu-west-1.compute.amazonaws.com:5432/dc6r4h9f3o6sso"
db = SQLAlchemy(app)
ma = Marshmallow(app)

#crear el esquema para nuestra tabla
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    prod_name = db.Column(db.String(100), unique=True)
    prod_description = db.Column(db.String(250), unique=False)
    prod_price = db.Column(db.Float, unique=False)
    prod_image = db.Column(db.String, unique=True)
    thumbnail_image = db.Column(db.String, unique=True)

    def __init__(self, prod_name, prod_description, prod_price, prod_image, thumbnail_image):
        self.prod_name = prod_name
        self.prod_description = prod_description
        self.prod_price = prod_price
        self.prod_image = prod_image
        self.thumbnail_image = thumbnail_image

#crear la clase de esquema en si
class ProductSchema(ma.Schema):
    class Meta:
        fields = ("prod_name", "prod_description", "prod_price", "prod_image", "thumbnail_image")

#instanciar ProductSchema con dos variables, una cuando trabajemos con un solo producto y otra con multiples
product_schema = ProductSchema()
products_schema = ProductSchema(many=True)

#Endpoint to create a new product
@app.route("/product", methods=["POST"])
def add_product():
    prod_name = request.json["prod_name"]
    prod_description = request.json["prod_description"]
    prod_price = request.json["prod_price"]
    prod_image = request.json["prod_image"]
    thumbnail_image = request.json["thumbnail_image"]

    new_product = Product(prod_name, prod_description, prod_price, prod_image, thumbnail_image)

    db.session.add(new_product)
    db.session.commit()

    product = Product.query.get(new_product.id)

    return product_schema.jsonify(product)

#Endpoint to query all products
@app.route("/products", methods=["GET"])
def get_products():
    all_products = Product.query.all()
    result = products_schema.dump(all_products)
    return jsonify(result)

#Endpoint for queryng a single product
@app.route("/product/<id>", methods=["GET"])
def get_product(id):
    product = Product.query.get(id)
    return product_schema.jsonify(product)

#Endpoint for updating a product
@app.route("/product/<id>", methods=["PUT"])
def product_update(id):
    product = Product.query.get(id)
    prod_name = request.json["prod_name"]
    prod_description = request.json["prod_description"]
    prod_price = request.json["prod_price"]
    prod_image = request.json["prod_image"]
    thumbnail_image = request.json["thumbnail_image"]

    product.prod_name = prod_name
    product.prod_description = prod_description
    product.prod_price = prod_price
    product.prod_image = prod_image
    product.thumbnail_image = thumbnail_image

    db.session.commit()
    return product_schema.jsonify(product)

#Endpoint for deleting a product
@app.route("/product/<id>", methods=["DELETE"])
def product_delete(id):
    product = Product.query.get(id)
    db.session.delete(product)
    db.session.commit()

    return product_schema.jsonify(product)


if __name__ == "__main__":
    app.run(debug=True)

