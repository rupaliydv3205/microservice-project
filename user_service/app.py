from flask import Flask, jsonify, request

app = Flask(__name__)

# --- In-memory data store ---
users = [
    {"id": 1, "name": "Mitali"},
    {"id": 2, "name": "Dipali"}
]

# --- 🧹 Reset Route (for Reset Button) ---
@app.route("/reset", methods=["DELETE"])
def reset_data():
    global users
    users = []  # Clear all users
    print("🧹 All users have been reset!")
    return jsonify({"status": "reset done"}), 200


# --- 👥 Fetch All Users ---
@app.route('/users', methods=['GET'])
def get_users():
    return jsonify(users), 200


# --- ➕ Add New User ---
@app.route('/add_user', methods=['POST'])
def add_user():
    data = request.get_json()

    if not data or "name" not in data:
        return jsonify({"error": "Invalid input"}), 400

    new_user = {
        "id": len(users) + 1,
        "name": data["name"]
    }
    users.append(new_user)
    print(f"✅ Added new user: {new_user}")
    return jsonify(new_user), 201


# --- 🔌 Run Service ---
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
