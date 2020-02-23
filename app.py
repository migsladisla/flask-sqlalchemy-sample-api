from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy 
from flask_marshmallow import Marshmallow 
import os

# Init app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False

# Init DB
db = SQLAlchemy(app)
#Init ma
ma = Marshmallow(app)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    description = db.Column(db.String(250))
    price = db.Column(db.Float)
    qty = db.Column(db.Integer)

    def __init__(self, name, description, price, qty):
        self.name = name
        self.description = description
        self.price = price
        self.qty = qty

# Product schema
class ProductSchema(ma.Schema):
    class Meta():
        fields = ('id', 'name', 'description', 'price', 'qty')

# Init schema
product_schema = ProductSchema()
products_schema = ProductSchema(many=True)

# Get products
@app.route('/product', methods=['GET'])
def get_products():
    all_products = Product.query.all()
    result = products_schema.dump(all_products)
    return jsonify(result)

# Get single product
@app.route('/product/<id>', methods=['GET'])
def get_product(id):
    try:
        product = Product.query.get(id)

        if product:
            return product_schema.jsonify(product), 200
        else:
            return {"message": "Product with the id of {} cannot be found.".format(id)}, 404
    except Exception as err:
        return {"message": str(err)}, 422

# Create product
@app.route('/product', methods=['POST'])
def add_product():
    try:
        name = request.json['name']
        description = request.json['description']
        price = request.json['price']
        qty = request.json['qty']

        new_product = Product(name, description, price, qty)

        db.session.add(new_product)
        db.session.commit()

        return {"message": "Product added successfully."}, 200
    except Exception as err:
        return {"message": str(err)}, 422

# Update product
@app.route('/product/<id>', methods=['PUT'])
def update_product(id):
    try:
        product = Product.query.get(id)

        name = request.json['name']
        description = request.json['description']
        price = request.json['price']
        qty = request.json['qty']

        product.name = name
        product.description = description
        product.price = price
        product.qty = qty

        db.session.commit()

        return {"message": "{} updated successfully.".format(name)}, 200
    except Exception as err:
        return {"message": str(err)}, 422

# Delete product
@app.route('/product/<id>', methods=['DELETE'])
def delete_product(id):
    try:
        product = Product.query.get(id)
        db.session.delete(product)
        db.session.commit()

        return {"message": "{} has been deleted.".format(product.name)}
    except Exception as err:
        return {"message": str(err)}, 422

# Run server
if __name__ == '__main__':
    app.run(debug=True)