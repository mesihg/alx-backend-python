import sqlite3

class DatabaseConnection:
    """Context manager that opens and closes a database connection."""
    def __init__(self, db_name="users.db"):
        self.db_name = db_name
        self.conn = None

    def __enter__(self):
        self.conn = sqlite3.connect(self.db_name)
        print(f"Database connection opened.")
        return self.conn 

    def __exit__(self, exc_type, exc_value, traceback):
        if self.conn:
            self.conn.close()
            print(f"Database connection closed.")
        return False
    
if __name__ == "__main__":
    query = "SELECT * FROM users"

    with DatabaseConnection() as conn:
        cursor = conn.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        results_list = [result for result in results]
        print(results_list)
