import mysql.connector


DB_CONFIG = {
    'host': 'localhost',
    'user': 'root', 
    'password': 'password', 
    'database': 'ALX_prodev', 
}
TABLE_NAME = 'user_data'

def stream_users():
    """
    A generator that fetches rows one by one from the user_data table.
    """
    connection = mysql.connector.connect(**DB_CONFIG)
    if not connection:
        return 
    
    cursor = connection.cursor(dictionary=True, buffered=False)
    
    try:
        query = f"SELECT user_id, name, email, age FROM {TABLE_NAME}"
        cursor.execute(query)
        
        for row in cursor:
            yield row
            
    except mysql.connector.Error as err:
        print(f"Error during data streaming: {err}")
    finally:
        cursor.close()
        connection.close()
