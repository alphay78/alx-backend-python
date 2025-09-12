import sqlite3
import functools

# Decorator to handle database connection
def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect("users.db")  # Open connection
        try:
            result = func(conn, *args, **kwargs)  # Pass connection to the function
        finally:
            conn.close()  # Ensure connection is closed
        return result
    return wrapper

# Decorator to handle transactions
def transactional(func):
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        try:
            result = func(conn, *args, **kwargs)
            conn.commit()  # Commit if no exception
            return result
        except Exception as e:
            conn.rollback()  # Rollback on error
            raise e  # Propagate the exception
    return wrapper

# Example usage
@with_db_connection
@transactional
def update_user_email(conn, user_id, new_email):
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id))

# Update user's email with automatic transaction handling
try:
    update_user_email(user_id=1, new_email='Crawford_Cartwright@hotmail.com')
    print("Email updated successfully!")
except Exception as e:
    print("Failed to update email:", e)
