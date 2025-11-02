import mysql.connector
import csv
import uuid
import sys


DB_CONFIG = {
    'host': 'localhost',
    'user': 'root', 
    'password': 'password', 
}
DB_NAME = 'ALX_prodev'
TABLE_NAME = 'user_data'
CSV_FILE = 'user_data.csv'


def connect_db() -> mysql.connector.MySQLConnection:
    """Connects to the MySQL database server."""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        print("connection successful")
        return connection
    except mysql.connector.Error as err:
        print(f"Error connecting to MySQL: {err}")
        sys.exit(1)

def connect_to_prodev() -> mysql.connector.MySQLConnection:
    """Connects to the specified ALX_prodev database."""
    config_with_db = {**DB_CONFIG, 'database': DB_NAME}
    try:
        connection = mysql.connector.connect(**config_with_db)
        return connection
    except mysql.connector.Error as err:
        print(f"Error connecting to database: {err}")
        return None

def create_database(connection: mysql.connector.MySQLConnection):
    """Creates the database ALX_prodev if it does not exist."""
    cursor = connection.cursor()
    try:
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
    except mysql.connector.Error as err:
        print(f"Failed creating database: {err}")
    finally:
        cursor.close()

def create_table(connection: mysql.connector.MySQLConnection):
    """Creates a table user_data if it does not exists with the required fields."""
    cursor = connection.cursor()

    create_table_query = f"""
    CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
        user_id CHAR(36) PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL,
        age DECIMAL(5, 2) NOT NULL,
        INDEX idx_user_id (user_id)
    );
    """
    try:
        cursor.execute(create_table_query)
        connection.commit()
        print("Table user_data created successfully")
    except mysql.connector.Error as err:
        print(f"Failed to create table: {err}")
    finally:
        cursor.close()

def load_csv_data(filepath: str) -> list[tuple]:
    """Reads CSV data and formats it for insertion, generating UUIDs."""
    data = []
    try:
        with open(filepath, mode='r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Generate a UUID, then cast data types correctly
                new_uuid = str(uuid.uuid4())
                name = row['name']
                email = row['email']
                age = float(row['age']) # Convert age to float for DECIMAL compatibility
                data.append((new_uuid, name, email, age))
        print(f"Successfully loaded {len(data)} records from {filepath}.")
        return data
    except FileNotFoundError:
        print(f"Error: CSV file not found at {filepath}")
        return []
    except Exception as e:
        print(f"An error occurred while processing CSV data: {e}")
        return []

def insert_data(connection: mysql.connector.MySQLConnection, csv_file: str):
    """Inserts data into the user_data table if it does not exist."""
    cursor = connection.cursor()
    with open(csv_file, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            user_id = row.get('user_id') or str(uuid.uuid4())
            name = row['name']
            email = row['email']
            age = row['age']
            try:
                cursor.execute(f"""
                    INSERT IGNORE INTO {TABLE_NAME} (user_id, name, email, age)
                    VALUES (%s, %s, %s, %s)
                """, (user_id, name, email, age))
            except mysql.connector.Error as err:
                print(f"Error inserting row: {err}")
    connection.commit()
    cursor.close()
