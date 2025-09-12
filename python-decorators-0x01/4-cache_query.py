import time
import sqlite3
import functools

query_cache = {}

def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect("users.db")
        try:
            return func(conn, *args, **kwargs)
        finally:
            conn.close()
    return wrapper

def cache_query(expire=60):  # expire time in seconds
    def decorator(func):
        @functools.wraps(func)
        def wrapper(conn, query, *args, **kwargs):
            now = time.time()
            if query in query_cache:
                result, timestamp = query_cache[query]
                if now - timestamp < expire:
                    print(f"[CACHE] Using cached result for query: {query}")
                    return result
            # Execute the query and cache with timestamp
            result = func(conn, query, *args, **kwargs)
            query_cache[query] = (result, now)
            print(f"[CACHE] Caching result for query: {query}")
            return result
        return wrapper
    return decorator

@with_db_connection
@cache_query(expire=60)
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

# First call caches the result
users = fetch_users_with_cache(query="SELECT * FROM users")

# Second call uses cache if within 60 seconds
users_again = fetch_users_with_cache(query="SELECT * FROM users")
