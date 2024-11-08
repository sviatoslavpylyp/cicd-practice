# app.py

from flask import Flask
from controller import create_user, get_all_users

app = Flask(__name__)

# POST endpoint for adding a user
@app.route('/user', methods=['POST'])
def add_user():
    return create_user()

# GET endpoint for fetching all users
@app.route('/users', methods=['GET'])
def list_users():
    return get_all_users()

if __name__ == '__main__':
    app.run(debug=True)
