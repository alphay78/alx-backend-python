#!/usr/bin/python3
import mysql.connector

def stream_users_in_batches(batch_size):
    """
    Generator that fetches users from the database in batches of batch_size.
    """
    connection = None
    cursor = None
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",          # replace with your MySQL username
            password="password",  # replace with your MySQL password
            database="ALX_prodev"
        )
        cursor = connection.cursor(dictionary=True)
        offset = 0

        while True:
            cursor.execute(
                "SELECT * FROM user_data LIMIT %s OFFSET %s;",
                (batch_size, offset)
            )
            batch = cursor.fetchall()
            if not batch:
                break
            yield batch  # yield the entire batch
            offset += batch_size

    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


def batch_processing(batch_size):
    """
    Process each batch to filter users over the age of 25 and print them.
    """
    for batch in stream_users_in_batches(batch_size):  # loop 1: batch fetching
        for user in batch:  # loop 2: iterate through users in batch
            if user['age'] > 25:  # filter condition
                print(user)
