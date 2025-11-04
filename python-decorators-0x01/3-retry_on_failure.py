import time
import sqlite3
import functools
from datetime import datetime

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

def retry_on_failure(retries=3, delay=2):
    """Decorator to retry a function if it raises an exception."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempt = 1
            while attempt <= retries:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                try:
                    print(f"[{timestamp}] Attempt {attempt} for {func.__name__}...")
                    return func(*args, **kwargs)
                except Exception as e:
                    print(f"[{timestamp}] Attempt {attempt} failed: {e}")
                    if attempt == retries:
                        print(f"[{timestamp}] All {retries} attempts failed.")
                        raise
                    else:
                        print(f"[{timestamp}] Retrying in {delay} seconds...")
                        time.sleep(delay)
                        attempt += 1
        return wrapper
    return decorator

@with_db_connection
@retry_on_failure(retries=3, delay=1)
def fetch_users_with_retry(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()

users = fetch_users_with_retry()
print(users)
