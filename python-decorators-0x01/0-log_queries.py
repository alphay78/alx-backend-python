import sqlite3
import functools
from datetime import datetime  # Required by the test

# Decorator to log SQL queries
def log_queries(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Get the query from positional or keyword arguments
        query = args[0] if args else kwargs.get("query")
        print(f"[LOG] Executing SQL query: {query}")
        return func(*args, **kwargs)
    return wrapper

# Usage
@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

# Test
users = fetch_all_users(query="SELECT * FROM users")
