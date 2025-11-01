from flask import Flask, jsonify, request

app = Flask(__name__)

# Store products as proper dictionaries
products = [
    {"id": 201, "name": "Laptop", "price": 55000},
    {"id": 202, "name": "Mobile", "price": 20000}
]


@app.route("/reset", methods=["DELETE"])
def reset_data():
    global products
    products = []
    print("🧹 Products reset!")
    return jsonify({"status": "reset done"}), 200


@app.route('/products', methods=['GET'])
def get_products():
    """Return all products (valid JSON array)."""
    return jsonify(products), 200


@app.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    """Return single product by ID."""
    product = next((p for p in products if p["id"] == product_id), None)
    if product:
        return jsonify(product), 200
    return jsonify({"error": "Product not found"}), 404


@app.route('/add_product', methods=['POST'])
def add_product():
    """Add new product with name + price."""
    data = request.get_json()

    if not data or "name" not in data or "price" not in data:
        return jsonify({"error": "Invalid input"}), 400

    try:
        price = float(data["price"])
    except ValueError:
        return jsonify({"error": "Price must be a number"}), 400

    new_product = {
        "id": len(products) + 201,
        "name": data["name"],
        "price": price
    }
    products.append(new_product)
    print(f"✅ New product added: {new_product}")
    return jsonify(new_product), 201


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002)
