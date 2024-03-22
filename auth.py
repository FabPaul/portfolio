#!/usr/bin/env python3
"""User Authentication"""

from flask import Flask, request, jsonify
from flask_login import LoginManager
from db_utils import connect_to_database
from user import User

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(username):
    """Load user object by ID"""
    user = User.get_user_by_username(username)
    if user:
        return User(user.id, user.username, user.password_hash)
    return None
