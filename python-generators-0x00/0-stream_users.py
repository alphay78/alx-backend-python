#!/usr/bin/python3
import mysql.connector

def stream_users():
    """Generator that fetches rows from user_data one by one."""
    connection = None
    cursor = None
    try:
        # Connect to the ALX_prodev database
        connection = mysql.connector.connect(
            host="localhost",
            user="root",          # Replace with your MySQL username
            password="password",  # Replace with your MySQL password
            database="ALX_prodev"
        )
        # Use dictionary cursor to get results as dicts
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM user_data;")
        
        # Single loop to yield each row one by one
        for row in cursor:
            yield row

    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
