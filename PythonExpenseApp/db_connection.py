import mysql.connector

class DbConnection:
    _connection = None

    @staticmethod
    def connect():
        if DbConnection._connection is None:
            try:
                DbConnection._connection = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="",
                    database="project"
                )
                print("Database connection established.")
            except mysql.connector.Error as e:
                print(f"Failed to connect to database: {e}")
                DbConnection._connection = None
        return DbConnection._connection

    @staticmethod
    def disconnect():
        if DbConnection._connection is not None:
            try:
                DbConnection._connection.close()
                DbConnection._connection = None
                print("Database connection closed.")
            except mysql.connector.Error as e:
                print(f"Failed to close the database connection: {e}")