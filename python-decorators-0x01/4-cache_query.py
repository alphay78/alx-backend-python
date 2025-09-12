import sqlite3
import functools

# Simple in-memory cache
query_cache = {}

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

# Decorator to cache query results
def cache_query(func):
    @functools.wraps(func)
    def wrapper(conn, query, *args, **kwargs):
        if query in query_cache:
            print(f"[CACHE] Using cached result for query: {query}")
            return query_cache[query]
        # Execute the query and cache the result
        result = func(conn, query, *args, **kwargs)
        query_cache[query] = result
        print(f"[CACHE] Caching result for query: {query}")
        return result
    return wrapper

# Example usage
@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

# First call will execute the query and cache the result
users = fetch_users_with_cache(query="SELECT * FROM users")
print(users)

# Second call will use the cached result
users_again = fetch_users_with_cache(query="SELECT * FROM users")
print(users_again)
