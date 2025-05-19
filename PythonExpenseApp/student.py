from PythonExpenseApp.db_connection import DbConnection
import mysql.connector

class Student:
    def __init__(self, name, surname, age, special_needs):
        self.name = name
        self.surname = surname
        self.age = age
        self.special_needs = special_needs
        self.selected_activities = []  # list of Activity
        self.total_expenses = 0.0
        self.fee_share = 0.0
        self.balance = 0.0

    def add_activity(self, activity):
        try:
            if activity.is_full():
                print(f"Activity '{activity.name}' is already full.")
                return
        except Exception as e:
            print(f"Error checking activity capacity: {e}")
        self.selected_activities.append(activity)

    def get_selected_activities(self):
        return self.selected_activities

    def add_expense(self, amount):
        self.total_expenses += amount

    def get_total_expenses(self):
        return self.total_expenses

    def set_fee_share(self, fee_share):
        self.fee_share = fee_share

    def get_fee_share(self):
        return self.fee_share

    def set_balance(self, balance):
        self.balance = balance

    def get_balance(self):
        return self.balance
    
    def __init__(self, id):
        self.id = id

    def save_to_database(self):
        connection = DbConnection.connect()
        if connection:
            try:
                sql = """INSERT INTO students
                         (name, surname, age, special_needs, total_expenses, fee_share, balance)
                         VALUES (%s, %s, %s, %s, %s, %s, %s)"""
                statement = connection.cursor()
                statement.execute(sql, (self.name, self.surname, self.age, self.special_needs,
                                        self.total_expenses, self.fee_share, self.balance))
                connection.commit()
                print("Student saved to database.")
            except mysql.connector.Error as e:
                print(f"Error saving student to database: {e}")

    def update_in_database(self):
        connection = DbConnection.connect()
        if connection:
            try:
                sql = """UPDATE students
                         SET total_expenses = %s, fee_share = %s, balance = %s
                         WHERE name = %s AND surname = %s"""
                statement = connection.cursor()
                statement.execute(sql, (self.total_expenses, self.fee_share, self.balance,
                                        self.name, self.surname))
                connection.commit()
                print("Student updated in database.")
            except mysql.connector.Error as e:
                print(f"Error updating student in database: {e}")

    @staticmethod
    def get_all_students():
        students = []
        connection = DbConnection.connect()
        if connection:
            try:
                sql = """SELECT name, surname, age, special_needs, total_expenses,
                                fee_share, balance FROM students"""
                statement = connection.cursor()
                statement.execute(sql)
                for (name, surname, age, special_needs, total_expenses, fee_share, balance) in statement:
                    stu = Student(name, surname, age, special_needs)
                    stu.add_expense(total_expenses)
                    stu.set_fee_share(fee_share)
                    stu.set_balance(balance)
                    students.append(stu)
            except mysql.connector.Error as e:
                print(f"Error retrieving students from database: {e}")
        return students

    def __str__(self):
        return (f"Student [name={self.name}, surname={self.surname}, age={self.age}, "
                f"specialNeeds={self.special_needs}, selectedActivities={self.selected_activities}, "
                f"totalExpenses={self.total_expenses}, feeShare={self.fee_share}, "
                f"balance={self.balance}]")