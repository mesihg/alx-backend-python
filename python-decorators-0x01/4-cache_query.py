import sqlite3
import functools
from datetime import datetime


query_cache = {}

def with_db_connection(func):
    """Decorator that opens and closes a database connection."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] Opening database connection...")
        conn = sqlite3.connect("users.db")
        try:
            result = func(conn, *args, **kwargs)
            return result
        except Exception as e:
            print(f"[{timestamp}] Error: {e}")
            raise
        finally:
            conn.close()
            print(f"[{timestamp}] Database connection closed.")
    return wrapper

def cache_query(func):
    """Decorator that caches query results based on the SQL query string."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        query = kwargs.get('query') or (args[1] if len(args) > 1 else None)
        if query is None:
            raise ValueError("Query string must be provided as a positional or keyword argument")

        if query in query_cache:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"[{timestamp}] Using cached result for query: {query}")
            return query_cache[query]

        # Execute query and cache result
        result = func(*args, **kwargs)
        query_cache[query] = result
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] Caching result for query: {query}")
        return result

    return wrapper

@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

#### First call will cache the result
users = fetch_users_with_cache(query="SELECT * FROM users")

#### Second call will use the cached result
users_again = fetch_users_with_cache(query="SELECT * FROM users")
