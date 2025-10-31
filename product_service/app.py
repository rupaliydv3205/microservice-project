from flask import Flask, jsonify, request

app = Flask(__name__)

# In-memory products
products = [
    {"id": 201, "name": "Laptop", "price": 55000},
    {"id": 202, "name": "Mobile", "price": 20000}
]
@app.route("/reset", methods=["DELETE"])
def reset_data():
    global products
    products = []
    print("🧹 All products have been reset!")
    return jsonify({"status": "reset done"}), 200


@app.route('/products', methods=['GET'])
def get_products():
    return jsonify(products), 200

@app.route('/add_product', methods=['POST'])
def add_product_via_gateway():
    data = request.get_json(silent=True) or {}
    name = (data.get("name") or "").strip()
    price = data.get("price")

    if not name or price is None:
        return jsonify({"error": "name and price required"}), 400

    try:
        price = float(price)
    except ValueError:
        return jsonify({"error": "price must be a number"}), 400

    new_product = {
        "id": (products[-1]["id"] + 1) if products else 201,
        "name": name,
        "price": price
    }
    products.append(new_product)
    return jsonify(new_product), 201

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002)
