#!/usr/bin/env python3
"""Forms"""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired
from db_utils import connect_to_database
from werkzeug.security import check_password_hash

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

    def validate_username(self, username):
        """Validate username"""
        connection = connect_to_database()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM users WHERE username = %s", (username.data,))
        user = cursor.fetchone()
        connection.close()

        if not user:
            raise ValidationError('Invalid username.')

    def validate_password(self, password):
        """Validate password"""
        connection = connect_to_database()
        cursor = connection.cursor()
        cursor.execute("SELECT password_hash FROM users WHERE username = %s", (self.username.data,))
        user_password_hash = cursor.fetchone()
        connection.close()

        if user_password_hash and not check_password_hash(user_password_hash[0], password.data):
            raise ValidationError('Invalid password.')

