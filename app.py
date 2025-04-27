# STAGE1

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///inventory.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ✅ Product Model
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    sku = db.Column(db.String(50), unique=True, nullable=False)
    category = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)

# ✅ Stock Movement Model
class StockMovement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    movement_type = db.Column(db.String(50), nullable=False)  # "stock-in", "sale", "manual-removal"
    quantity = db.Column(db.Integer, nullable=False)

# ✅ Initialize Database
with app.app_context():
    db.create_all()

# ✅ API to Add a Product (With SKU Uniqueness Check)
@app.route('/products', methods=['POST'])
def add_product():
    data = request.json

    # Check if SKU already exists
    existing_product = Product.query.filter_by(sku=data['sku']).first()
    if existing_product:
        return jsonify({"error": "SKU already exists"}), 400

    new_product = Product(
        name=data['name'],
        sku=data['sku'],
        category=data['category'],
        price=data['price']
    )

    try:
        db.session.add(new_product)
        db.session.commit()
        return jsonify({"message": "Product added successfully"}), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Integrity error occurred. SKU must be unique."}), 400

# ✅ API to Get All Products
@app.route('/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    return jsonify([{'id': p.id, 'name': p.name, 'sku': p.sku, 'category': p.category, 'price': p.price} for p in products])

# ✅ API to Add Stock Movement
@app.route('/stock-movement', methods=['POST'])
def add_stock_movement():
    data = request.json

    # Check if product exists before adding stock movement
    product = Product.query.get(data['product_id'])
    if not product:
        return jsonify({"error": "Product ID not found"}), 404

    stock_movement = StockMovement(
        product_id=data['product_id'],
        movement_type=data['movement_type'],
        quantity=data['quantity']
    )

    db.session.add(stock_movement)
    db.session.commit()
    return jsonify({'message': 'Stock movement recorded successfully'}), 201

# ✅ API to Get All Stock Movements
@app.route('/stock-movement', methods=['GET'])
def get_stock_movements():
    movements = StockMovement.query.all()
    return jsonify([{'id': m.id, 'product_id': m.product_id, 'movement_type': m.movement_type, 'quantity': m.quantity} for m in movements])

if __name__ == '__main__':
    app.run(debug=True)

