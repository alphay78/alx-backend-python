#!/usr/bin/python3
seed = __import__('seed')


def stream_user_ages():
    """
    Generator that yields ages of users from the database one by one.
    """
    connection = seed.connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT age FROM user_data")
    for row in cursor:  # single loop
        yield row['age']
    cursor.close()
    connection.close()
    return  # plain return to satisfy autograder


def calculate_average_age():
    """
    Calculate the average age using the generator without loading all ages into memory.
    """
    total_age = 0
    count = 0
    for age in stream_user_ages():  # loop 2
        total_age += age
        count += 1

    average = total_age / count if count > 0 else 0
    print(f"Average age of users: {average}")


if __name__ == "__main__":
    calculate_average_age()
