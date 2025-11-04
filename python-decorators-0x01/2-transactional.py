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

def transactional(func):
    """Decorator to commit or roll back database transactions."""
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            result = func(conn, *args, **kwargs)
            conn.commit()
            print(f"[{timestamp}] Transaction committed successfully.")
            return result
        except Exception as e:
            conn.rollback()
            print(f"[{timestamp}] Transaction rolled back due to error: {e}")
            raise
    return wrapper

@with_db_connection 
@transactional 
def update_user_email(conn, user_id, new_email): 
    cursor = conn.cursor() 
    cursor.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id)) 

update_user_email(user_id=1, new_email='Crawford_Cartwright@hotmail.com')
