from flask import Flask, render_template, request, redirect, url_for, jsonify
import requests

app = Flask(__name__)
@app.route("/reset", methods=["DELETE"])
def reset_dashboard():
    try:
        requests.delete("http://user_service:5001/reset")
        requests.delete("http://product_service:5002/reset")
        requests.delete("http://order_service:5004/reset")
        return jsonify({"message": "All services reset successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

USER_SERVICE_URL = "https://user-service-production.up.railway.app"
PRODUCT_SERVICE_URL = "https://product-service-production.up.railway.app"
ORDER_SERVICE_URL = "https://order-service-production.up.railway.app"


@app.route('/')
def dashboard():
    users = requests.get(f"{USER_SERVICE_URL}/users").json()
    products = requests.get(f"{PRODUCT_SERVICE_URL}/products").json()
    orders = requests.get(f"{ORDER_SERVICE_URL}/orders").json().get("orders", [])
    return render_template("dashboard.html", users=users, products=products, orders=orders)

@app.route('/add_user', methods=['POST'])
def add_user():
    name = request.form['name']
    requests.post(f"{USER_SERVICE_URL}/add_user", json={"name": name})
    return redirect(url_for('dashboard'))

@app.route('/add_product', methods=['POST'])
def add_product():
    name = request.form['name']
    price = request.form['price']
    requests.post(f"{PRODUCT_SERVICE_URL}/add_product", json={"name": name, "price": price})
    return redirect(url_for('dashboard'))

@app.route('/add_order', methods=['POST'])
def add_order():
    user_id = request.form['user_id']
    product_id = request.form['product_id']
    requests.post(f"{ORDER_SERVICE_URL}/add_order", json={
        "user_id": user_id,
        "product_id": product_id
    })
    return redirect(url_for('dashboard'))



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
