#!/usr/bin/python3
seed = __import__('seed')


def stream_user_ages():
    connection = seed.connect_to_prodev() 
    if not connection:
        return 

    cursor = connection.cursor(dictionary=True, buffered=False)
    
    try:
        query = "SELECT age FROM user_data"
        cursor.execute(query)
        
        for row in cursor:
            yield float(row['age'])
            
    except Exception as err:
        print(f"Error during data streaming: {err}")
    finally:
        cursor.close()
        connection.close()


def calculate_average_age():
    total_age = 0.0
    user_count = 0
    
    for age in stream_user_ages():
        total_age += age
        user_count += 1
    
    if user_count > 0:
        average_age = total_age / user_count
        print(f"Average age of users: {average_age:.2f}")
    else:
        print("No users found to calculate the average age.")
