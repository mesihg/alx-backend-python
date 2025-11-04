import os
import sqlite3
import functools
from datetime import datetime

#### decorator to log SQL queries

def log_queries(func):
    """Decorator to log SQL queries or function execution"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        sql_query = kwargs.get('query') or (args[0] if args else None)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if sql_query:
            print(f"[{timestamp}] Executing Query: {sql_query}")
        else:
            print(f"[{timestamp}] Executing function: {func.__name__}")
        return func(*args, **kwargs)
    return wrapper

@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

#### fetch users while logging the query
users = fetch_all_users(query="SELECT * FROM users")
