#!/usr/bin/env python3
"""User models definition"""

from werkzeug.security import generate_password_hash, check_password_hash
from db_utils import connect_to_database
from flask_login import UserMixin


class User(UserMixin):
    """User class"""

    def __init__(self, id, username, password_hash):
        """Init module"""
        self.id = id
        self.username = username
        self.password_hash = password_hash

    def authenticate(self, password):
        """Check if password matches user's hased password"""
        return check_password_hash(self.password_hash, password)
    
    def verify_password(password_hash, password):
        return check_password_hash(password_hash, password)

    @staticmethod
    def get_user_by_username(username):
        """Gets user information by username"""
        connection = connect_to_database()
        cursor = connection.cursor()
        sql = "SELECT * FROM users WHERE username = %s"
        values = (username,)
        cursor.execute(sql, values)
        user_data = cursor.fetchone()
        connection.close()
        if user_data:
            return User(user_data[0], user_data[1], user_data[2])
        else:
            return None
