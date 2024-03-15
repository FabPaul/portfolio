#!/usr/bin/env python3
"""User Authentication"""

from flask import Flask, request, jsonify
from flask_login import login_user, logout_user, LoginManager
from db_utils import connect_to_database
from user import User

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    """Load user object by ID"""
    connection = connect_to_database()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
    user_data = cursor.fetchone()
    if user_data:
        return User(user_data[1], user_data[2])
    else:
        return None


@app.route("/login", methods=["POST"])
def login():
    """Login Attempt"""
    username = request.form.get("username")
    password = request.form.get("password")

    # Load user by username
    user = load_user(username)

    if user and user.verify_password(password):
        login_user(user)
        return jsonify({"message": "Login successful!"})
    else:
        return jsonify({"error": "Invalid username or password"}), 401


@app.route("/logout", methods=["GET"])
def logout():
    """Logout attempt"""
    logout_user()
    return jsonify({"message": "Logged out successfully!"})
