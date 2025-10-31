from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

orders = []

USER_SERVICE_URL = "https://user-service-production.up.railway.app"
PRODUCT_SERVICE_URL = "https://product-service-production.up.railway.app"

@app.route('/add_order', methods=['POST'])
def add_order():
    data = request.get_json()
    user_id = data.get("user_id")
    product_id = data.get("product_id")

    # fetch real user and product details from their services
    user = requests.get(f"{USER_SERVICE_URL}/users/{user_id}").json()
    product = requests.get(f"{PRODUCT_SERVICE_URL}/products/{product_id}").json()

    # add order with full info
    order = {
        "order_id": len(orders) + 1,
        "user": user,
        "product": product
    }
    orders.append(order)
    return jsonify(order), 201

@app.route('/orders', methods=['GET'])
def get_orders():
    return jsonify({"orders": orders}), 200


@app.route('/reset', methods=['DELETE'])
def reset_orders():
    orders.clear()
    return jsonify({"message": "Orders reset"}), 200


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5004, debug=True)
