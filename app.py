#!/usr/bin/env python3
"""Flask"""


from flask import Flask, request, jsonify
import mysql.connector
import os
from user import User
from db_utils import db_config, connect_to_database
from auth import login, logout, login_manager


# Placeholder for db credentialsloaded from .env

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')
login_manager.init_app(app)

def load_config():
    """Load config from environment variables"""
    global db_config
    db_config["host"] = os.environ.get("DB_HOST")
    db_config["user"] = os.environ.get("DB_USER")
    db_config["password"] = os.environ.get("DB_PASSWORD")
    db_config["database"] = os.environ.get("DB_NAME")

    if any(value is None for value in db_config.values()):
        raise ValueError("Missing database ENV Variables!")


# Load config at startup of application
load_config()


def connect_to_database():
    try:
        connection = mysql.connector.connect(**db_config)
        return connection
    except mysql.connector.Error as err:
        print("Error connecting to database", err)
        return None


@app.route("/report", methods=["POST"], strict_slashes=False)
def submit_report():
    """Submit a new incident report"""
    try:
        user_id = request.form.get("user_id")
        incident_type = request.form["incident_type"]
        details = request.form["details"]
        location = request.form.get("location", "")
    except KeyError as e:
        return jsonify({"error": f"Missing required field: {e}"}), 400

    # Connect to db
    connection = connect_to_database()

    if connection:
        cursor = connection.cursor()
        try:
            # SQL statement to insert report without user_id
            sql = "INSERT INTO incidents (incident_type, details, status, location) VALUES (%s, %s, %s, %s)"
            values = (incident_type, details, "pending", location)
            cursor.execute(sql, values)
            connection.commit()
            return jsonify({"message": "Incident report submitted succesfully!"}), 201
        except mysql.connector.Error as err:
            print("Error submitting report, please try again", err)
            return jsonify({"error": "Error submitting report"}), 500
        finally:
            connection.close()
    else:
        return jsonify({"error": "Database connection failed"}), 500


@app.route("/")
def home():
    """Home route"""
    return "See-Say Cameroon Backened (under development)"


@app.route("/login", methods=["POST"])
def login_route():
    """Login route (imported from auth.py)"""
    return login()


@app.route("/logout", methods=["GET"])
def logout_route():
    """Logout route (imported from auth.py)"""
    return logout()


if __name__ == "__main__":
    app.run(debug=True)
