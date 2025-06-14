from db_connection import DbConnection

class Student:
    # Student class represents a student with personal data, activities, and financial info

    def __init__(self, name, surname, age, special_needs):
        """
        Initialize a new Student object with personal and default financial/activity data.

        :param name: str - The first name of the student.
        :param surname: str - The surname (last name) of the student.
        :param age: int - The age of the student.
        :param special_needs: str - Any special needs or requirements the student has (can be empty string).
        """
        # Student's first name (string)
        self.name = name
        # Student's surname (string)
        self.surname = surname
        # Student's age (integer)
        self.age = age
        # Special needs (string, can be empty if no special needs)
        self.special_needs = special_needs
        # List of Activity objects the student has selected (list of Activity)
        self.selected_activities = []
        # Total expenses incurred by the student (float, sum of all expenses)
        self.total_expenses = 0.0
        # The student's share of the total fee (float, calculated externally)
        self.fee_share = 0.0
        # The balance the student needs to pay or receive (float, positive means owes money, negative means to be reimbursed)
        self.balance = 0.0
        # Student ID, set after saving to database (int or None if not saved)
        self.id = None
        # Username for student login (string, must be set before saving to DB)
        self.username = None
        # Class of the student (string, e.g., "10A", can be None if not set)
        self.class_ = None

    def add_activity(self, activity):
        """
        Adds an activity to the student's selected activities if the activity is not full.

        :param activity: Activity object - The activity to add to the student's list.
        :return: None
        """
        try:
            # Check if the activity is already at capacity before adding
            if activity.is_full():
                print(f"Activity '{activity.name}' is already full.")
                return
        except Exception as e:
            # Handle any errors that occur when checking activity capacity
            print(f"Error checking activity capacity: {e}")
        # Add the activity to the student's selected activities list
        self.selected_activities.append(activity)

    def get_selected_activities(self):
        """
        Returns the list of activities the student has selected.

        :return: list - List of Activity objects selected by the student.
        """
        return self.selected_activities

    def add_expense(self, amount):
        """
        Adds an expense to the student's total expenses.

        :param amount: float - The amount to add to the student's expenses.
        :return: None
        """
        self.total_expenses += amount

    def get_total_expenses(self):
        """
        Returns the total expenses incurred by the student.

        :return: float - The total expenses.
        """
        return self.total_expenses

    def set_fee_share(self, fee_share):
        """
        Sets the student's share of the total fee.

        :param fee_share: float - The calculated share of the fee for this student.
        :return: None
        """
        self.fee_share = fee_share

    def get_fee_share(self):
        """
        Returns the student's share of the total fee.

        :return: float - The student's fee share.
        """
        return self.fee_share

    def set_balance(self, balance):
        """
        Sets the student's balance (amount to pay or receive).

        :param balance: float - The balance to set for the student.
        :return: None
        """
        self.balance = balance

    def get_balance(self):
        """
        Returns the student's current balance.

        :return: float - The student's balance.
        """
        return self.balance

    def save_to_database(self):
        """
        Saves the student to the database using the DbConnection class.
        Requires the username to be set before calling.
        Sets the student's ID after successful insertion.

        :return: bool - True if saved successfully, False otherwise.
        """
        if not self.username:
            print("Error: Username is required to save student")
            return False
            
        query = """INSERT INTO students 
                   (name, surname, username, password, class, age, special_needs, 
                    total_expenses, fee_share, balance)
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        
        # Default password - should be changed in production
        default_password = f"{self.surname.lower()}{self.age}"
        
        params = (self.name, self.surname, self.username, default_password, 
                 getattr(self, 'class_', ''), self.age, self.special_needs,
                 self.total_expenses, self.fee_share, self.balance)
        
        # Execute the insert query and get the result
        success, result = DbConnection.execute_query(query, params)
        if success:
            # Set the student ID to the inserted row's ID
            self.id = result
            print(f"Student {self.name} {self.surname} saved to database with ID {self.id}")
            return True
        else:
            print(f"Error saving student to database: {result}")
            return False

    def update_in_database(self):
        """
        Updates the student's data in the database.
        Requires the student to have a valid ID.

        :return: bool - True if updated successfully, False otherwise.
        """
        if not self.id:
            print("Error: Student ID is required to update")
            return False
            
        query = """UPDATE students 
                   SET name=%s, surname=%s, age=%s, special_needs=%s,
                       total_expenses=%s, fee_share=%s, balance=%s, class=%s
                   WHERE id=%s"""
        
        params = (self.name, self.surname, self.age, self.special_needs,
                 self.total_expenses, self.fee_share, self.balance,
                 getattr(self, 'class_', ''), self.id)
        
        # Execute the update query and get the result
        success, result = DbConnection.execute_query(query, params)
        if success:
            print(f"Student {self.name} {self.surname} updated in database")
            return True
        else:
            print(f"Error updating student in database: {result}")
            return False

    @staticmethod
    def get_all_students():
        """
        Retrieves all students from the database and returns them as a list of Student objects.
        Each Student object is populated with data from the database.

        :return: list - List of Student objects.
        """
        query = """SELECT id, name, surname, username, class, age, special_needs, 
                          total_expenses, fee_share, balance 
                   FROM students ORDER BY surname, name"""
        
        # Execute the select query to fetch all students
        success, result = DbConnection.execute_query(query, fetch_all=True)
        if not success:
            print(f"Error retrieving students: {result}")
            return []
            
        students = []
        for row in result:
            # Create a Student object for each row and populate its fields
            student = Student(row[1], row[2], row[5], row[6])
            student.id = row[0]
            student.username = row[3]
            student.class_ = row[4]
            student.total_expenses = float(row[7]) if row[7] else 0.0
            student.fee_share = float(row[8]) if row[8] else 0.0
            student.balance = float(row[9]) if row[9] else 0.0
            students.append(student)
            
        return students

    @staticmethod
    def get_student_by_id(student_id):
        """
        Retrieves a specific student from the database by their ID.
        Returns a Student object if found, otherwise None.

        :param student_id: int - The ID of the student to retrieve.
        :return: Student or None
        """
        query = """SELECT id, name, surname, username, class, age, special_needs, 
                          total_expenses, fee_share, balance 
                   FROM students WHERE id=%s"""
        
        # Execute the select query to fetch the student by ID
        success, result = DbConnection.execute_query(query, (student_id,), fetch_one=True)
        if not success or not result:
            return None
            
        student = Student(result[1], result[2], result[5], result[6])
        student.id = result[0]
        student.username = result[3]
        student.class_ = result[4]
        student.total_expenses = float(result[7]) if result[7] else 0.0
        student.fee_share = float(result[8]) if result[8] else 0.0
        student.balance = float(result[9]) if result[9] else 0.0
        
        return student

    @staticmethod
    def authenticate(email, password):
        """
        Authenticates a student login using email and password.
        Returns a Student object if authentication is successful, otherwise None.

        :param email: str - The email address of the student.
        :param password: str - The password for the student.
        :return: Student or None
        """
        query = """SELECT id, name, surname, email, class, age, special_needs, role 
                   FROM students WHERE email=%s AND password=%s"""
        
        # Execute the select query to authenticate the student
        success, result = DbConnection.execute_query(query, (email, password), fetch_one=True)
        if not success or not result:
            return None
            
        student = Student(result[1], result[2], result[5], result[6])
        student.id = result[0]
        student.email = result[3]
        student.class_ = result[4]
        # Role is optional, default to 'student' if not present
        student.role = result[7] if len(result) > 7 else 'student'
        
        return student

    def get_participated_activities(self):
        """
        Retrieves a list of activities the student has participated in.
        Returns a list of tuples with activity details.

        :return: list - List of tuples (activity_id, name, day, start_time, finish_time, location)
        """
        if not self.id:
            return []
            
        query = """SELECT a.id, a.name, a.day, a.start_time, a.finish_time, a.location
                   FROM activities a
                   JOIN student_activities sa ON a.id = sa.activity_id
                   WHERE sa.student_id = %s
                   ORDER BY a.day, a.start_time"""
        
        # Execute the select query to fetch participated activities
        success, result = DbConnection.execute_query(query, (self.id,), fetch_all=True)
        if success:
            return result
        return []

    def has_participated_in_activity(self, activity_id):
        """
        Checks if the student has participated in a specific activity.

        :param activity_id: int - The ID of the activity to check.
        :return: bool - True if participated, False otherwise.
        """
        if not self.id:
            return False
            
        query = """SELECT COUNT(*) FROM student_activities 
                   WHERE student_id = %s AND activity_id = %s"""
        
        # Execute the select query to check participation
        success, result = DbConnection.execute_query(query, (self.id, activity_id), fetch_one=True)
        if success and result:
            return result[0] > 0
        return False

    def has_given_feedback_for_activity(self, activity_id):
        """
        Checks if the student has already given feedback for a specific activity.

        :param activity_id: int - The ID of the activity to check.
        :return: bool - True if feedback has been given, False otherwise.
        """
        if not self.id:
            return False
            
        query = """SELECT COUNT(*) FROM feedback 
                   WHERE student_id = %s AND activity_id = %s"""
        
        # Execute the select query to check feedback
        success, result = DbConnection.execute_query(query, (self.id, activity_id), fetch_one=True)
        if success and result:
            return result[0] > 0
        return False

    def can_leave_feedback_for_activity(self, activity_id):
        """
        Determines if the student can leave feedback for a specific activity.
        The student can leave feedback only if they participated and haven't already given feedback.

        :param activity_id: int - The ID of the activity.
        :return: bool - True if feedback can be left, False otherwise.
        """
        # Verifica se lo studente ha partecipato all'attività e non ha già lasciato un feedback
        return (self.has_participated_in_activity(activity_id) and 
                not self.has_given_feedback_for_activity(activity_id))

    def __str__(self):
        """
        Returns a string representation of the student, including all key attributes.

        :return: str - Human-readable string describing the student.
        """
        # Restituisce una stringa leggibile con tutti gli attributi principali dello studente
        return (f"Student [name={self.name}, surname={self.surname}, age={self.age}, "
                f"specialNeeds={self.special_needs}, selectedActivities={self.selected_activities}, "
                f"totalExpenses={self.total_expenses}, feeShare={self.fee_share}, "
                f"balance={self.balance}]")