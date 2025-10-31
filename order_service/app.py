from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

USER_API = "http://user_service:5001/users"
PRODUCT_API = "http://product_service:5002/products"
orders = []
@app.route("/reset", methods=["DELETE"])
def reset_data():
    global orders
    orders = []
    print("🧹 All orders have been reset!")
    return jsonify({"status": "reset done"}), 200
@app.route('/orders', methods=['GET'])
def get_orders():
    return jsonify({"orders": orders}), 200

@app.route('/add_order', methods=['POST'])
def add_order():
    data = request.get_json(silent=True) or {}
    user_id = data.get("user_id")
    product_id = data.get("product_id")

    if not user_id or not product_id:
        return jsonify({"error": "user_id and product_id required"}), 400

    # Fetch data from other services
    users = requests.get(USER_API).json()
    products = requests.get(PRODUCT_API).json()

    user = next((u for u in users if str(u["id"]) == str(user_id)), None)
    product = next((p for p in products if str(p["id"]) == str(product_id)), None)

    if not user or not product:
        return jsonify({"error": "Invalid user or product"}), 400

    new_order = {
        "order_id": len(orders) + 101,
        "user": user,
        "product": product
    }
    orders.append(new_order)
    return jsonify(new_order), 201


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5004)
