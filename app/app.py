from flask import Flask, jsonify

app = Flask(__name__)

# Endpoint 1: Welcome message
@app.route("/")
def home():
    return jsonify({"message": "Welcome to the Flask App!"})

# Endpoint 2: Static user data
@app.route("/users", methods=["GET"])
def get_users():
    users = [
        {"id": 1, "name": "Alice", "email": "alice@example.com"},
        {"id": 2, "name": "Bob", "email": "bob@example.com"},
        {"id": 3, "name": "Charlie", "email": "charlie@example.com"}
    ]
    return jsonify({"users": users})

if __name__ == "__main__":
    app.run(debug=True)










