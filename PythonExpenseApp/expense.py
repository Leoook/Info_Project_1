# ===================================================================
# EXPENSE CLASS - FINANCIAL TRANSACTION MANAGEMENT
# ===================================================================
# This file contains the Expense class which handles all financial
# transactions during the trip. It manages expense recording, debt
# calculation, and splitting costs among multiple participants.
#
# KEY RESPONSIBILITIES:
# 1. Recording individual expenses and shared costs
# 2. Calculating debt splits among participants
# 3. Creating individual debt records for each participant
# 4. Managing financial relationships between students
# 5. Providing financial reporting and statistics
# ===================================================================

# Import database connection module for all database operations
from PythonExpenseApp.db_connection import DbConnection
# Import datetime for handling date/time operations and timestamps
from datetime import datetime

class Expense:
    """
    Represents a financial transaction or expense during the trip.
    
    This class handles all aspects of expense management including recording
    who paid, how much was spent, what it was for, and how costs should be
    split among participants. It automatically creates debt records when
    expenses are shared among multiple people.
    
    ATTRIBUTES:
        id (int): Unique database identifier (None for new expenses)
        amount (float): Total amount of the expense in currency units
        description (str): What the money was spent on (required)
        date (str/date): When the expense occurred
        id_giver (int): Student ID who paid the money (the payer)
        id_receiver (int): Student ID who received money (for direct transfers)
        id_activity (int): Activity ID this expense is related to (optional)
        created_at (datetime): When this expense record was created
    
    EXPENSE TYPES:
        1. Shared Expenses: One person pays, multiple people owe money
        2. Direct Transfers: One person pays another person directly
        3. Activity Expenses: Costs associated with specific activities
        4. General Expenses: Miscellaneous costs not tied to activities
    """

    def __init__(self, amount=0.0, description="", date=None, id_giver=None, id_receiver=None, id_activity=None):
        """
        Initialize a new Expense instance.
        
        Creates a new expense object that can represent various types of
        financial transactions during the trip.
        
        PARAMETERS:
            amount (float): Total expense amount (must be positive)
            description (str): Description of what was purchased/paid for
            date (str/date): Date when expense occurred (defaults to today)
            id_giver (int): Student ID of person who paid the money
            id_receiver (int): Student ID of person who received money (for direct transfers)
            id_activity (int): Activity ID if expense is activity-related
            
        VALIDATION:
            - Amount must be positive (enforced by business logic)
            - Description is required for clarity
            - Date defaults to current date if not provided
            
        USAGE EXAMPLES:
            # Shared meal expense
            lunch = Expense(45.50, "Group lunch at restaurant", "2024-03-15", payer_id)
            
            # Direct money transfer
            transfer = Expense(20.00, "Bus fare reimbursement", "2024-03-15", 
                             payer_id, receiver_id)
            
            # Activity-related expense
            tickets = Expense(75.00, "Museum entrance tickets", "2024-03-15", 
                            payer_id, None, activity_id)
        """
        # Database identifier - None for new expenses, set when saved
        self.id = None
        
        # Core expense properties
        self.amount = float(amount)          # Total expense amount
        self.description = description       # What the money was spent on
        self.date = date or datetime.now().date()  # Date of expense (default to today)
        
        # Participant information
        self.id_giver = id_giver            # Who paid the money
        self.id_receiver = id_receiver      # Who received money (for direct transfers)
        self.id_activity = id_activity      # Related activity (optional)
        
        # Audit information
        self.created_at = None              # Set when saved to database

    def calculate_equal_split(self, participant_ids):
        """
        Calculate how much each participant owes for an equally split expense.
        
        This method divides the total expense amount equally among all participants.
        It's used for shared expenses like meals, transportation, or activities
        where everyone benefits equally.
        
        PARAMETERS:
            participant_ids (list): List of student IDs who should split the cost
            
        RETURNS:
            float: Amount each participant owes (rounded to 2 decimal places)
            
        CALCULATIONS:
            per_person_cost = total_amount / number_of_participants
            Rounded to 2 decimal places for currency precision
            
        VALIDATION:
            - participant_ids list cannot be empty
            - Returns 0 if no participants provided
            
        USAGE:
            participants = [1, 2, 3, 4]  # Student IDs
            per_person = expense.calculate_equal_split(participants)
            print(f"Each person owes: ${per_person:.2f}")
        """
        # Validate input
        if not participant_ids or len(participant_ids) == 0:
            return 0.0
        
        # Calculate equal split amount
        per_person_amount = self.amount / len(participant_ids)
        
        # Round to 2 decimal places for currency precision
        return round(per_person_amount, 2)

    def create_debt_records(self, participant_ids, split_method="equal", custom_amounts=None):
        """
        Create individual debt records for each participant in a shared expense.
        
        This method generates debt records that track who owes money to whom.
        Each participant who didn't pay gets a debt record showing they owe
        money to the person who paid.
        
        PARAMETERS:
            participant_ids (list): Student IDs of people who should split the cost
            split_method (str): How to split the cost ("equal" or "custom")
            custom_amounts (dict): Custom amounts per participant (for unequal splits)
            
        RETURNS:
            tuple: (success, message) indicating if debt records were created successfully
            
        DATABASE OPERATIONS:
            Inserts multiple records into the debts table, one for each participant
            
        BUSINESS LOGIC:
            - The payer (id_giver) doesn't owe money to themselves
            - Each other participant gets a debt record
            - All debts start as unpaid (paid=FALSE)
            
        USAGE:
            # Equal split among 4 people
            participants = [1, 2, 3, 4]
            success, msg = expense.create_debt_records(participants)
            
            # Custom split with specific amounts
            custom = {1: 10.00, 2: 15.00, 3: 20.50}
            success, msg = expense.create_debt_records([1,2,3], "custom", custom)
        """
        # Validation checks
        if not self.id:
            return False, "Expense must be saved to database before creating debt records"
        
        if not participant_ids:
            return False, "No participants provided for debt splitting"
        
        if not self.id_giver:
            return False, "No payer specified for this expense"
        
        # Calculate amounts based on split method
        if split_method == "equal":
            # Equal split: everyone pays the same amount
            per_person_amount = self.calculate_equal_split(participant_ids)
            debt_amounts = {pid: per_person_amount for pid in participant_ids}
        elif split_method == "custom" and custom_amounts:
            # Custom split: use provided amounts
            debt_amounts = custom_amounts
        else:
            return False, "Invalid split method or missing custom amounts"
        
        # Create debt records for each participant (except the payer)
        debt_records = []
        for participant_id in participant_ids:
            # Skip the payer - they don't owe money to themselves
            if participant_id == self.id_giver:
                continue
            
            # Get the amount this participant owes
            amount_owed = debt_amounts.get(participant_id, 0)
            if amount_owed <= 0:
                continue  # Skip if no debt
            
            # Create debt record query
            debt_query = """INSERT INTO debts (payer_id, debtor_id, amount, description, 
                                              expense_id, paid, date_created)
                           VALUES (%s, %s, %s, %s, %s, FALSE, %s)"""
            
            debt_params = (
                self.id_giver,          # Who is owed money (the payer)
                participant_id,         # Who owes money (the participant)
                amount_owed,            # How much is owed
                self.description,       # Description of what the debt is for
                self.id,               # Reference to original expense
                self.date              # Date the debt was created
            )
            
            debt_records.append((debt_query, debt_params))
        
        # Execute all debt record insertions in a transaction
        if debt_records:
            success, result = DbConnection.execute_transaction(debt_records)
            if success:
                return True, f"Created {len(debt_records)} debt records successfully"
            else:
                return False, f"Failed to create debt records: {result}"
        else:
            return True, "No debt records needed (payer was only participant)"

    def save_to_database(self):
        """
        Save this expense to the database.
        
        This method inserts the expense record into the database and sets
        the expense ID for future reference.
        
        RETURNS:
            tuple: (success, message) indicating if save was successful
            
        DATABASE OPERATION:
            INSERT into expenses table with all expense properties
            
        VALIDATION:
            - Amount must be positive
            - Description cannot be empty
            - Date must be valid
            
        SIDE EFFECTS:
            Sets self.id to the new database ID if successful
            Sets self.created_at to current timestamp
            
        USAGE:
            expense = Expense(25.50, "Taxi fare", "2024-03-15", payer_id)
            success, message = expense.save_to_database()
            if success:
                print(f"Expense saved with ID: {expense.id}")
            else:
                print(f"Save failed: {message}")
        """
        # Validation checks before saving
        if self.amount <= 0:
            return False, "Expense amount must be positive"
        
        if not self.description or self.description.strip() == "":
            return False, "Expense description is required"
        
        # SQL INSERT query for new expense
        query = """INSERT INTO expenses (amount, description, date, id_giver, id_receiver, id_activity)
                   VALUES (%s, %s, %s, %s, %s, %s)"""
        
        # Parameters tuple matching the query placeholders
        params = (
            self.amount,           # Total expense amount
            self.description,      # What was purchased
            self.date,            # Date of expense
            self.id_giver,        # Who paid
            self.id_receiver,     # Who received (for direct transfers)
            self.id_activity      # Related activity (optional)
        )
        
        # Execute the INSERT query
        success, result = DbConnection.execute_query(query, params)
        if success:
            self.id = result                        # Store the new database ID
            self.created_at = datetime.now()        # Record creation timestamp
            return True, "Expense saved successfully"
        else:
            return False, f"Failed to save expense: {result}"

    @staticmethod
    def get_all_expenses():
        """
        Retrieve all expenses from the database.
        
        This static method loads all expense records and returns them as
        Expense objects. Used for financial reporting and expense browsing.
        
        RETURNS:
            list: List of Expense objects loaded from database
            Empty list if no expenses or database error
            
        DATABASE QUERY:
            Selects all expenses ordered by date (most recent first)
            
        USAGE:
            expenses = Expense.get_all_expenses()
            total = sum(exp.amount for exp in expenses)
            print(f"Total expenses: ${total:.2f}")
        """
        # Query to get all expenses ordered by date
        query = """SELECT id, amount, description, date, id_giver, id_receiver, 
                          id_activity, created_at
                   FROM expenses 
                   ORDER BY date DESC, created_at DESC"""
        
        success, result = DbConnection.execute_query(query, fetch_all=True)
        if not success:
            return []
        
        # Convert database rows to Expense objects
        expenses = []
        for row in result:
            # Create Expense object with data from database
            expense = Expense(row[1], row[2], row[3], row[4], row[5], row[6])
            expense.id = row[0]           # Set database ID
            expense.created_at = row[7]   # Set creation timestamp
            expenses.append(expense)
        
        return expenses

    @staticmethod
    def get_expenses_by_student(student_id):
        """
        Get all expenses where a specific student was involved as payer or receiver.
        
        This method retrieves expenses relevant to a particular student,
        either as the person who paid or received money.
        
        PARAMETERS:
            student_id (int): The ID of the student to get expenses for
            
        RETURNS:
            list: List of Expense objects involving the specified student
            
        DATABASE QUERY:
            Selects expenses where student is either giver or receiver
            
        USAGE:
            student_expenses = Expense.get_expenses_by_student(student_id)
            paid_out = sum(exp.amount for exp in student_expenses if exp.id_giver == student_id)
        """
        # Query for expenses involving the specified student
        query = """SELECT id, amount, description, date, id_giver, id_receiver, 
                          id_activity, created_at
                   FROM expenses 
                   WHERE id_giver = %s OR id_receiver = %s
                   ORDER BY date DESC, created_at DESC"""
        
        success, result = DbConnection.execute_query(query, (student_id, student_id), fetch_all=True)
        if not success:
            return []
        
        # Convert to Expense objects
        expenses = []
        for row in result:
            expense = Expense(row[1], row[2], row[3], row[4], row[5], row[6])
            expense.id = row[0]
            expense.created_at = row[7]
            expenses.append(expense)
        
        return expenses

    @staticmethod
    def get_total_expenses():
        """
        Calculate the total amount of all expenses in the database.
        
        This method provides a quick summary statistic for financial reporting.
        
        RETURNS:
            float: Total sum of all expense amounts
            
        DATABASE QUERY:
            Uses SUM aggregation function on expense amounts
            
        USAGE:
            total = Expense.get_total_expenses()
            print(f"Total trip expenses: ${total:.2f}")
        """
        query = "SELECT SUM(amount) FROM expenses"
        success, result = DbConnection.execute_query(query, fetch_one=True)
        
        if success and result and result[0]:
            return float(result[0])
        return 0.0

    @staticmethod
    def mark_debt_as_paid(debt_id):
        """Mark a specific debt as paid"""
        query = """UPDATE debts SET paid=TRUE, date_paid=CURDATE() WHERE id=%s"""
        
        success, result = DbConnection.execute_query(query, (debt_id,))
        if success:
            print(f"Debt {debt_id} marked as paid")
            return True
        else:
            print(f"Error marking debt as paid: {result}")
            return False

    def __str__(self):
        """
        Return a string representation of this expense.
        
        This method provides a human-readable representation for debugging
        and logging purposes.
        
        RETURNS:
            str: Formatted string with key expense information
            
        USAGE:
            print(expense)  # Automatically calls __str__()
            logger.info(f"Processing {expense}")
        """
        return f"Expense(id={self.id}, amount=${self.amount:.2f}, description='{self.description}', date={self.date})"