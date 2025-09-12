import sqlite3
import functools

# Decorator to log SQL queries
def log_queries():
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Assuming the first argument is the SQL query
            query = args[0] if args else kwargs.get("query")
            print(f"[LOG] Executing SQL query: {query}")
            return func(*args, **kwargs)
        return wrapper
    return decorator

# Usage
@log_queries()
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

# Fetch users while logging the query
users = fetch_all_users(query="SELECT * FROM users")
print(users)
