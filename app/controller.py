from dao import UserDAO
from flask import request, jsonify

user_dao = UserDAO()

def create_user():
    """Controller function for creating a new user."""
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')

    if not name or not email:
        return jsonify({"error": "Name and email are required"}), 400

    user_dao.create_user(name, email)
    return jsonify({"message": "User created successfully"}), 201

def get_all_users():
    """Controller function for fetching all users."""
    users = user_dao.get_all_users()
    return jsonify(users), 200
