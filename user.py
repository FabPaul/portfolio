#!/usr/bin/env python3
"""User models definition"""

from werkzeug.security import generate_password_hash, check_password_hash
from db_utils import connect_to_database


class User:
    """User class"""

    def __init__(self, username, password):
        """Init module"""
        self.username = username
        self.password_hash = generate_password_hash(password)

    @classmethod
    def authenticate(cls, username, password):
        """Check if password matches user's hased password"""
        user = cls.get_user_by_username(username)
        if user and check_password_hash(user.password_hash, password):
            return user
        return None
    
    def get_user_by_username(username):
        """Gets user information by username"""
        connection = connect_to_database()
        cursor = connection.cursor()
        sql = "SELECT * FROM users WHERE username = %s"
        values = (username,)
        cursor.execute(sql, values)
        user = cursor.fetchone()
        connection.close()
        return user