import psycopg2 
from g import DB_HOST, DB_NAME, DB_USER, DB_PASSWORD


class Database:
    def __init__(self):
        self._conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST)
        # Creates a cursor object that allows us to execute SQL commands in python 
        self._cursor = self._conn.cursor()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    @property
    def connection(self):
        return self._conn

    @property
    def cursor(self):
        return self._cursor
    # Commit changes to the database
    def commit(self):
        self.connection.commit()
    # Close the connection to the database
    def close(self, commit=True):
        if commit:
            self.commit()
        self.connection.close()
    # Execute a SQL command
    def execute(self, sql, params=None):
        self.cursor.execute(sql, params or ())
    # Fetch all results from the cursor
    def fetchall(self):
        return self.cursor.fetchall()
    # Fetch one result from the cursor 
    def fetchone(self):
        return self.cursor.fetchone()
    # Query the database and return all results
    def query(self, sql, params=None):
        self.cursor.execute(sql, params or ())
        return self.fetchall()