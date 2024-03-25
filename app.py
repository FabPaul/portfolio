#!/usr/bin/env python3
"""See-Say Cameroon route"""


from flask import Flask, request, render_template, redirect, url_for, flash, send_from_directory, jsonify
import mysql.connector
import os
from db_utils import db_config, connect_to_database, create_user
from auth import login_manager
import flask_login
from datetime import datetime, timedelta
import requests


# Placeholder for db credentialsloaded from .env

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')
login_manager.init_app(app)
API_KEY = os.getenv("API_KEY")

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
        current_user = flask_login.current_user
        user_id = current_user.id if current_user.is_authenticated else None
        incident_type = request.form["incident_type"]
        details = request.form["details"]
        location = request.form.get("location", "")
        status = request.form["status"]
    except KeyError as e:
        flash("Missing required fied: {e}", "error")
        return redirect(url_for("report_form"))

    # Connect to db
    connection = connect_to_database()

    if connection:
        cursor = connection.cursor()
        try:
            # SQL statement to insert report without user_id
            sql = """INSERT INTO incidents (user_id, incident_type, details,
            status, location) VALUES (%s, %s, %s, %s, %s)"""
            values = (user_id, incident_type, details, status, location)
            cursor.execute(sql, values)
            connection.commit()
            flash("Incident report submitted succesfully!", "success")
            return redirect(url_for("home"))
        except mysql.connector.Error as err:
            flash("Error submitting report", "error")
            return redirect(url_for("home"))
        finally:
            connection.close()
    else:
        flash("Database connection failed", "error")
        return redirect(url_for("home"))
    

@app.route("/")
@app.route("/home")
def home():
    """Home screen for display of all the 10 regions of cameroon"""
    connection = connect_to_database()
    cursor = connection.cursor(dictionary=True)

    query = "SELECT * FROM regions LIMIT 10"
    cursor.execute(query)
    regions = cursor.fetchall()
    cursor.close()
    connection.close()

    return render_template("index.html", regions=regions)


@app.route("/top_cities/<int:region_id>")
def region_details(region_id):
    """Display every detail about a region"""
    connection = connect_to_database()
    cursor = connection.cursor(dictionary=True)

    query = "SELECT * FROM regions WHERE id = %s"
    values = (region_id,)
    cursor.execute(query, values)

    region = cursor.fetchone()

    if not region:
        flash("Region not found!", "error")
        return redirect(url_for("home"))

    query = "SELECT * FROM top_cities WHERE region_id = %s"
    values = (region_id,)
    cursor.execute(query, values)
    top_cities = cursor.fetchall()

    places_query = "SELECT * FROM places WHERE region = %s"
    places_values = (region['name'],)
    cursor.execute(places_query, places_values)

    places = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template("region_details.html", region=region, top_cities=top_cities, places=places)


@app.route("/cities/<int:city_id>")
def city_details(city_id):
    """Display the weather of any top city clicked"""
    connection = connect_to_database()
    cursor = connection.cursor(dictionary=True)

    query = "SELECT * FROM top_cities WHERE id = %s"
    values = (city_id,)
    cursor.execute(query, values)

    city = cursor.fetchone()

    if not city:
        flash("City not found!", "error")
        return redirect(url_for("home"))


    base_url = "https://api.openweathermap.org/data/2.5/weather"

    params = {"q": city['city_name'], "appid": API_KEY}

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()

        weather_data = {
      "temperature": round(data["main"]["temp"] - 273.15, 1),
      "feels_like": round(data["main"]["feels_like"] - 273.15, 1),
      "description": data["weather"][0]["description"],
      "wind": {
        "speed": data["wind"]["speed"],
        "deg": data["wind"]["deg"]
      },
      "precipitation": None
    }

    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather data: {e}")
        weather_data = None

    cursor.close()
    connection.close()

    return render_template("city_details.html", city=city, weather_data=weather_data)


@app.route("/images/<filename>")
def get_image(filename):
    """Load images"""
    return send_from_directory("static/images", filename)


"""@app.route("/register", methods=["GET", "POST"])
def register():
    ""Handle registration requests""
    if request.method == "GET":
        return render_template("registration.html")
    elif request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        create_user(username, password)
        return redirect(url_for('login'))
    else:
        return "Method not allowed", 405"""


"""app.add_url_rule("/login", "login", login, methods=["POST"])
app.add_url_rule("/logout", "/logout", logout, methods=["GET"])"""


"""@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('profile'))

    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.get_user_by_username(username)

        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            # flash('Login successful!', 'success')
            return redirect(url_for('profile'))
        else:
            flash('Invalid username or password', 'error')
    return render_template('login.html', title='Login', form=form)


@app.route("/profile", methods=["GET"])
@login_required
def profile():
    return render_template('profiles.html')



@app.route('/logout')
def logout():
    flash('You have been logged out')
    return redirect(url_for('home'))
"""

@app.route("/report_form")
def report_form():
    """Report submission form"""
    return render_template("report.html")


@app.route("/location/<lat>/<lng>")
def get_location_name(lat, lng):
  """Get location by user's longitude and latitudes, using api"""
  url = f"https://nominatim.openstreetmap.org/reverse?format=json&lat={lat}&lon={lng}"
  response = requests.get(url)
  if response.status_code == 200:
    data = response.json()
    return jsonify({"address": data.get("display_name")})
  else:
    print(f"Error fetching location name: {response.status_code}")
    return jsonify({"error": "Failed to retrieve location name"})

@app.route("/recent_reports", methods=["GET"], strict_slashes=False)
def recent_reports():
    """Display recent reports"""
    connection = connect_to_database()
    cursor = connection.cursor(dictionary=True)

    sql = """SELECT * FROM incidents WHERE reported_at >=%s
    AND status IN (%s, %s) ORDER BY reported_at DESC"""
    threshold = datetime.now() - timedelta(days=7)
    values = (threshold, "pending", "investigating")

    cursor.execute(sql, values)
    recent_reports = cursor.fetchall()
    connection.close()

    return render_template("recent_reports.html", reports=recent_reports)


@app.route("/full_report/<int:report_id>", methods=["GET"],
           strict_slashes=False)
def full_report(report_id):
    """Display the full details of a report"""
    connection = connect_to_database()
    cursor = connection.cursor(dictionary=True)

    sql = "SELECT * FROM incidents WHERE id = %s"
    values = (report_id,)
    cursor.execute(sql, values)
    full_report = cursor.fetchone()
    connection.close()

    return render_template("full_report.html", report=full_report)


if __name__ == "__main__":
    app.run(debug=True)
