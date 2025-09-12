import time
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

# Decorator to retry function on failure
def retry_on_failure(retries=3, delay=2):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(1, retries + 1):
                try:
                    return func(*args, **kwargs)  # Try executing the function
                except Exception as e:
                    last_exception = e
                    print(f"[Retry {attempt}/{retries}] Function failed: {e}. Retrying in {delay} seconds...")
                    time.sleep(delay)
            # If all retries fail, raise the last exception
            raise last_exception
        return wrapper
    return decorator

# Example usage
@with_db_connection
@retry_on_failure(retries=3, delay=1)
def fetch_users_with_retry(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()

# Attempt to fetch users with automatic retry on failure
try:
    users = fetch_users_with_retry()
    print(users)
except Exception as e:
    print("Failed to fetch users after retries:", e)
