from PythonExpenseApp.db_connection import DbConnection
import mysql.connector

class Student:
    # Student class represents a student with personal data, activities, and financial info

    def __init__(self, name, surname, age, special_needs):
        # Student's first name
        self.name = name
        # Student's surname
        self.surname = surname
        # Student's age
        self.age = age
        # Special needs (string, can be empty)
        self.special_needs = special_needs
        # List of Activity objects the student has selected
        self.selected_activities = []
        # Total expenses incurred by the student
        self.total_expenses = 0.0
        # The student's share of the total fee
        self.fee_share = 0.0
        # The balance the student needs to pay or receive
        self.balance = 0.0

    def add_activity(self, activity):
        """
        Adds an activity to the student's selected activities if not full.
        :param activity: Activity object
        """
        try:
            if activity.is_full():
                print(f"Activity '{activity.name}' is already full.")
                return
        except Exception as e:
            print(f"Error checking activity capacity: {e}")
        self.selected_activities.append(activity)

    def get_selected_activities(self):
        """
        Returns the list of selected activities.
        """
        return self.selected_activities

    def add_expense(self, amount):
        """
        Adds an expense to the student's total expenses.
        :param amount: float
        """
        self.total_expenses += amount

    def get_total_expenses(self):
        """
        Returns the total expenses of the student.
        """
        return self.total_expenses

    def set_fee_share(self, fee_share):
        """
        Sets the student's share of the fee.
        :param fee_share: float
        """
        self.fee_share = fee_share

    def get_fee_share(self):
        """
        Returns the student's share of the fee.
        """
        return self.fee_share

    def set_balance(self, balance):
        """
        Sets the student's balance.
        :param balance: float
        """
        self.balance = balance

    def get_balance(self):
        """
        Returns the student's balance.
        """
        return self.balance

    def save_to_database(self):
        """
        Saves the student to the database.
        """
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
        """
        Updates the student's financial data in the database.
        """
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
        """
        Retrieves all students from the database and returns them as a list of Student objects.
        """
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
        """
        Returns a string representation of the student.
        """
        return (f"Student [name={self.name}, surname={self.surname}, age={self.age}, "
                f"specialNeeds={self.special_needs}, selectedActivities={self.selected_activities}, "
                f"totalExpenses={self.total_expenses}, feeShare={self.fee_share}, "
                f"balance={self.balance}]")