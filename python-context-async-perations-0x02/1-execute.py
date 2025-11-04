import sqlite3

class ExecuteQuery:
    """Context manager that opens and closes a database connection and query execution"""
    def __init__(self, query, params=None, db_name="users.db"):
        self.query = query
        self.params = params or ()
        self.db_name = db_name
        self.conn = None
        self.results = None

    def __enter__(self):
        # Open the connection
        self.conn = sqlite3.connect(self.db_name)
        print("Database connection opened.")

        # Execute the query
        cursor = self.conn.cursor()
        cursor.execute(self.query, self.params)
        self.results = cursor.fetchall()
        return self.results  

    def __exit__(self, exc_type, exc_value, traceback):
        # Close the connection
        if self.conn:
            self.conn.close()
            print("Database connection closed.")
        return False


if __name__ == "__main__":
    query = "SELECT * FROM users WHERE email =  ?"
    params = ('bob@example.com',)

    with ExecuteQuery(query, params) as results:
        results_list = [result for result in results]
        print(results_list)
