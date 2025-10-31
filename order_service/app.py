from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

orders = []

# ✅ Replace with your Railway-deployed URLs
USER_SERVICE_URL = "https://user-service-production.up.railway.app"
PRODUCT_SERVICE_URL = "https://product-service-production.up.railway.app"

@app.route('/add_order', methods=['POST'])
def add_order():
    data = request.get_json()
    user_id = data.get("user_id")
    product_id = data.get("product_id")

    if not user_id or not product_id:
        return jsonify({"error": "Missing user_id or product_id"}), 400

    try:
        # Fetch full user & product details
        user = requests.get(f"{USER_SERVICE_URL}/users/{user_id}").json()
        product = requests.get(f"{PRODUCT_SERVICE_URL}/products/{product_id}").json()

        # 🧱 Validate that product is a dict with price
        if isinstance(product, dict) and "price" in product:
            order = {
                "order_id": len(orders) + 1,
                "user": user,
                "product": product
            }
            orders.append(order)
            print(f"✅ Order created: {order}")
            return jsonify(order), 201
        else:
            print("⚠️ Product fetch returned:", product)
            return jsonify({"error": "Invalid product data"}), 500

    except Exception as e:
        print(f"❌ Error adding order: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/orders', methods=['GET'])
def get_orders():
    return jsonify({"orders": orders}), 200

@app.route('/reset', methods=['DELETE'])
def reset_orders():
    orders.clear()
    print("🧹 Orders cleared")
    return jsonify({"message": "Orders reset successful"}), 200

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5004)
