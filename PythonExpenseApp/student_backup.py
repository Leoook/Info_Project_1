from PythonExpenseApp.db_connection import DbConnection

class Student:
    # Student class represents a student with personal data, activities, and financial info

    def __init__(self, name, surname, age, special_needs, is_teacher=False):
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
        # Student ID, set after saving to database
        self.id = None
        # Username for student login
        self.username = None
        # Class of the student
        self.class_ = None        # Whether this user is a teacher
        self.is_teacher = is_teacher

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
        Saves the student to the database using enhanced connection
        """
        if not self.username:
            print("Error: Username is required to save student")
            return False
              query = """INSERT INTO students 
                   (name, surname, username, password, class, age, special_needs, 
                    total_expenses, fee_share, balance, is_teacher)
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        
        # Default password - should be changed in production
        default_password = f"{self.surname.lower()}{self.age}"
        
        params = (self.name, self.surname, self.username, default_password, 
                 getattr(self, 'class_', ''), self.age, self.special_needs,
                 self.total_expenses, self.fee_share, self.balance, self.is_teacher)
        
        success, result = DbConnection.execute_query(query, params)
        if success:
            self.id = result  # Get the inserted ID
            print(f"Student {self.name} {self.surname} saved to database with ID {self.id}")
            return True
        else:
            print(f"Error saving student to database: {result}")
            return False    def update_in_database(self):
        """
        Updates the student's data in the database
        """
        if not self.id:
            print("Error: Student ID is required to update")
            return False
            
        query = """UPDATE students 
                   SET name=%s, surname=%s, age=%s, special_needs=%s,
                       total_expenses=%s, fee_share=%s, balance=%s, class=%s, is_teacher=%s
                   WHERE id=%s"""
        
        params = (self.name, self.surname, self.age, self.special_needs,
                 self.total_expenses, self.fee_share, self.balance,
                 getattr(self, 'class_', ''), self.is_teacher, self.id)
        
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
        """        query = """SELECT id, name, surname, username, class, age, special_needs, 
                          total_expenses, fee_share, balance, is_teacher 
                   FROM students ORDER BY surname, name"""
        
        success, result = DbConnection.execute_query(query, fetch_all=True)
        if not success:
            print(f"Error retrieving students: {result}")
            return []
            
        students = []
        for row in result:
            student = Student(row[1], row[2], row[5], row[6], row[10] if len(row) > 10 else False)
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
        Get a specific student by ID
        """        query = """SELECT id, name, surname, username, class, age, special_needs, 
                          total_expenses, fee_share, balance, is_teacher 
                   FROM students WHERE id=%s"""
        
        success, result = DbConnection.execute_query(query, (student_id,), fetch_one=True)
        if not success or not result:
            return None
            
        student = Student(result[1], result[2], result[5], result[6], result[10] if len(result) > 10 else False)
        student.id = result[0]
        student.username = result[3]
        student.class_ = result[4]
        student.total_expenses = float(result[7]) if result[7] else 0.0
        student.fee_share = float(result[8]) if result[8] else 0.0
        student.balance = float(result[9]) if result[9] else 0.0
        
        return student

    @staticmethod
    def authenticate(username, password):
        """
        Authenticate a student login
        """        query = """SELECT id, name, surname, username, class, age, special_needs, is_teacher 
                   FROM students WHERE username=%s AND password=%s"""
        
        success, result = DbConnection.execute_query(query, (username, password), fetch_one=True)
        if not success or not result:
            return None
            
        student = Student(result[1], result[2], result[5], result[6], result[7] if len(result) > 7 else False)
        student.id = result[0]
        student.username = result[3]
        student.class_ = result[4]
        
        return student

    def get_participated_activities(self):
        """Get list of activities the student has participated in"""
        if not self.id:
            return []
            
        query = """SELECT a.id, a.name, a.day, a.start_time, a.finish_time, a.location
                   FROM activities a
                   JOIN student_activities sa ON a.id = sa.activity_id
                   WHERE sa.student_id = %s
                   ORDER BY a.day, a.start_time"""
        
        success, result = DbConnection.execute_query(query, (self.id,), fetch_all=True)
        if success:
            return result
        return []

    def has_participated_in_activity(self, activity_id):
        """Check if student has participated in a specific activity"""
        if not self.id:
            return False
            
        query = """SELECT COUNT(*) FROM student_activities 
                   WHERE student_id = %s AND activity_id = %s"""
        
        success, result = DbConnection.execute_query(query, (self.id, activity_id), fetch_one=True)
        if success and result:
            return result[0] > 0
        return False

    def has_given_feedback_for_activity(self, activity_id):
        """Check if student has already given feedback for a specific activity"""
        if not self.id:
            return False
            
        query = """SELECT COUNT(*) FROM feedback 
                   WHERE student_id = %s AND activity_id = %s"""
        
        success, result = DbConnection.execute_query(query, (self.id, activity_id), fetch_one=True)
        if success and result:
            return result[0] > 0
        return False

    def can_leave_feedback_for_activity(self, activity_id):
        """Check if student can leave feedback for an activity"""
        return (self.has_participated_in_activity(activity_id) and 
                not self.has_given_feedback_for_activity(activity_id))

    def __str__(self):
        """
        Returns a string representation of the student.
        """
        return (f"Student [name={self.name}, surname={self.surname}, age={self.age}, "
                f"specialNeeds={self.special_needs}, selectedActivities={self.selected_activities}, "
                f"totalExpenses={self.total_expenses}, feeShare={self.fee_share}, "
                f"balance={self.balance}, isTeacher={self.is_teacher}]")