#!/usr/bin/env python3
"""User models definition"""

from werkzeug.security import generate_password_hash, check_password_hash


class User:
    """User class"""

    def __init__(self, username, password):
        """Init module"""
        self.username = username
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """Check if password matches user's hased password"""
        pswd = check_password_hash(self.password_hash, password)
        return pswd
