from PythonExpenseApp.db_connection import DbConnection
import mysql.connector
from datetime import datetime

class Expense:
    def __init__(self, amount, description, date_=None, giver_id=None, receiver_id=None, activity_id=None):
        self.amount = amount
        self.description = description
        self.date = date_ if date_ else datetime.now().strftime("%Y-%m-%d")
        self.giver_id = giver_id
        self.receiver_id = receiver_id
        self.activity_id = activity_id

    def get_amount(self):
        return self.amount

    def set_amount(self, amount):
        self.amount = amount

    def get_description(self):
        return self.description

    def set_description(self, description):
        self.description = description

    def get_date(self):
        return self.date

    def set_date(self, date_):
        self.date = date_

    def save_to_database(self):
        connection = DbConnection.connect()
        if connection:
            try:
                # If you have columns for giver_id, receiver_id, activity_id, adapt the query
                sql = """INSERT INTO expenses (amount, description, date, id_giver, id_receiver, id_activity)
                         VALUES (%s, %s, %s, %s, %s, %s)"""
                statement = connection.cursor()
                statement.execute(sql, (self.amount, self.description, self.date,
                                        self.giver_id, self.receiver_id, self.activity_id))
                connection.commit()
                print("Expense saved to database.")
            except mysql.connector.Error as e:
                print(f"Error saving expense to database: {e}")

    def __str__(self):
        return f"Expense(amount={self.amount}, description={self.description}, date={self.date})"