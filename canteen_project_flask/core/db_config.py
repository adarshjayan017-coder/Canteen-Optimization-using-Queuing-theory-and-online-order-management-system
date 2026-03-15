import mysql.connector
from mysql.connector import Error

def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Pvkpvk@123", # Your Password
            database="canteen_mgmt_system"
        )
        return connection
    except Error as e:
        print(f"❌ Connection Error: {e}")
        return None