import sqlite3
import functools
from datetime import datetime

def with_db_connection(func):
    """Decorator that opens and closes a database connection."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] Opening database connection...")

        conn = sqlite3.connect("database.db")
        try:
            result = func(conn, *args, **kwargs)
            print(f"[{timestamp}] Query executed successfully.")
            return result
        except Exception as e:
            print(f"[{timestamp}] Error: {e}")
            raise
        finally:
            conn.close()
            print(f"[{timestamp}] Database connection closed.")
    return wrapper

@with_db_connection 
def get_user_by_id(conn, user_id): 
cursor = conn.cursor() 
cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,)) 
return cursor.fetchone() 
#### Fetch user by ID with automatic connection handling 

user = get_user_by_id(user_id=1)
print(user)
