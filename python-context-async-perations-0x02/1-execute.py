import sqlite3

# Custom class-based context manager for executing queries
class ExecuteQuery:
    def __init__(self, query, params=None, db_name="users.db"):
        self.query = query
        self.params = params or ()
        self.db_name = db_name
        self.conn = None
        self.cursor = None
        self.results = None

    def __enter__(self):
        # Open the database connection
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        # Execute the query with parameters
        self.cursor.execute(self.query, self.params)
        self.results = self.cursor.fetchall()
        return self.results  # Return query results to the 'with' block

    def __exit__(self, exc_type, exc_value, traceback):
        # Close the connection
        if self.conn:
            self.conn.close()
        # Propagate exceptions if any
        return False

# Using the context manager
query = "SELECT * FROM users WHERE age > ?"
params = (25,)

with ExecuteQuery(query, params) as results:
    for row in results:
        print(row)
