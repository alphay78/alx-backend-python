import sqlite3

# Custom class-based context manager
class DatabaseConnection:
    def __init__(self, db_name="users.db"):
        self.db_name = db_name
        self.conn = None

    def __enter__(self):
        # Open the database connection
        self.conn = sqlite3.connect(self.db_name)
        return self.conn  # The connection object is returned to the 'with' block

    def __exit__(self, exc_type, exc_value, traceback):
        # Close the connection when exiting the 'with' block
        if self.conn:
            self.conn.close()
        # Optional: handle exceptions if needed
        # Returning False propagates any exception that occurs
        return False

# Using the custom context manager
with DatabaseConnection() as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    results = cursor.fetchall()
    for row in results:
        print(row)
