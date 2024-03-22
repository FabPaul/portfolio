#!/usr/bin/env python3

import mysql.connector
from werkzeug.security import generate_password_hash
from dotenv import load_dotenv
import os

load_dotenv()

db_config = {
    "host": os.getenv("DB_HOST"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME")
}


def connect_to_database():
    """Connect to the database"""
    try:
        connection = mysql.connector.connect(**db_config)
        return connection
    except mysql.connector.Error as err:
        return None


def create_user(username, password):
    """Creates a new user in the database"""
    connection = connect_to_database()
    cursor = connection.cursor()
    hashed_password = generate_password_hash(password)
    sql = "INSERT INTO users (username, password_hash) VALUES (%s, %s)"
    values = (username, hashed_password)
    try:
        cursor.execute(sql, values)
        connection.commit()
        print(f"User '{username}' created successfully!")
    except mysql.connector.Error as err:
        print(f"Error creating user: {err}")
    finally:
        connection.close()
