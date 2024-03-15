import mysql.connector

db_config = {
    "host": None,
    "user": None,
    "password": None,
    "database": None
}


def connect_to_database():
    """Connect to the database"""
    try:
        connection = mysql.connector.connect(**db_config)
        return connection
    except mysql.connector.Error as err:
        print("Error connecting to database:", err)
        return None