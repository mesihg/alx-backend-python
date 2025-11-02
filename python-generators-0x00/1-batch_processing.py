import mysql.connector
import sys


DB_CONFIG = {
    'host': 'localhost',
    'user': 'root', 
    'password': 'password', 
    'database': 'ALX_prodev', 
}
TABLE_NAME = 'user_data'


def stream_users_in_batches(batch_size: int):
    """
    Generator function that fetches rows from the user_data table 
    in batches using the specified batch size.
    """
    connection = mysql.connector.connect(**DB_CONFIG)
    if not connection:
        return 

    cursor = connection.cursor(dictionary=True)
    offset = 0

    while True:
        cursor.execute(
            f"SELECT * FROM {TABLE_NAME} LIMIT %s OFFSET %s", (batch_size, offset)
        )
        rows = cursor.fetchall()
        if not rows:
            break
        yield rows
        offset += batch_size

    cursor.close()
    connection.close()


def batch_processing(batch_size: int):
    """
    Processes each batch of user data to filter users over the age of 25 
    and prints the results.
    """
    for batch in stream_users_in_batches(batch_size):
        for user in batch:
            if float(user['age']) > 25:
                print(user)
