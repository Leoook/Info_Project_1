from PythonExpenseApp.db_connection import DbConnection
from datetime import datetime

class Expense:
    def __init__(self, amount, description, date_=None, giver_id=None, receiver_id=None, activity_id=None):
        self.amount = amount
        self.description = description
        self.date = date_ if date_ else datetime.now().strftime("%Y-%m-%d")
        self.giver_id = giver_id
        self.receiver_id = receiver_id
        self.activity_id = activity_id
        self.participants = []
        self.id = None

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
        """Save expense to database using enhanced connection"""
        query = """INSERT INTO expenses (amount, description, date, id_giver, id_receiver, id_activity)
                   VALUES (%s, %s, %s, %s, %s, %s)"""
        
        params = (self.amount, self.description, self.date,
                 self.giver_id, self.receiver_id, self.activity_id)
        
        success, result = DbConnection.execute_query(query, params)
        if success:
            self.id = result
            print(f"Expense saved to database with ID {self.id}")
            return True
        else:
            print(f"Error saving expense to database: {result}")
            return False

    def add_participant(self, student_id, amount_owed):
        """Add a participant who owes money for this expense"""
        self.participants.append((student_id, amount_owed))

    def get_participants(self):
        """Get list of participants who owe money"""
        return self.participants

    def save_to_database_with_participants(self):
        """Save expense and create debt records for participants using transaction"""
        if not self.giver_id or not self.participants:
            print("Error: Giver ID and participants are required")
            return None
            
        # Prepare transaction queries
        queries = []
        
        # Main expense insert
        expense_query = """INSERT INTO expenses (amount, description, date, id_giver, id_receiver, id_activity)
                          VALUES (%s, %s, %s, %s, %s, %s)"""
        queries.append((expense_query, (self.amount, self.description, self.date,
                                       self.giver_id, self.receiver_id, self.activity_id)))
        
        # Execute transaction
        success, results = DbConnection.execute_transaction(queries)
        if not success:
            print(f"Error saving expense: {results}")
            return None
            
        self.id = results[0]
        
        # Now save debt records separately (since we need the expense_id)
        debt_queries = []
        for student_id, amount_owed in self.participants:
            debt_query = """INSERT INTO debts (payer_id, debtor_id, amount, description, 
                                              expense_id, date_created, paid)
                           VALUES (%s, %s, %s, %s, %s, %s, FALSE)"""
            debt_queries.append((debt_query, (self.giver_id, student_id, amount_owed, 
                                             self.description, self.id, self.date)))
        
        if debt_queries:
            success, debt_results = DbConnection.execute_transaction(debt_queries)
            if success:
                print(f"Expense and {len(debt_queries)} debt records saved successfully")
                return self.id
            else:
                print(f"Error saving debt records: {debt_results}")
                return None
                
        return self.id

    @staticmethod
    def get_debts_for_student(student_id):
        """Get all debts for a specific student"""
        # Money others owe to this student (this student is the payer)
        owed_query = """SELECT d.id, s.name, s.surname, d.amount, d.description, d.date_created
                       FROM debts d
                       JOIN students s ON d.debtor_id = s.id
                       WHERE d.payer_id = %s AND d.paid = FALSE
                       ORDER BY d.date_created DESC"""
        
        # Money this student owes to others (this student is the debtor)
        owing_query = """SELECT d.id, s.name, s.surname, d.amount, d.description, d.date_created
                        FROM debts d
                        JOIN students s ON d.payer_id = s.id
                        WHERE d.debtor_id = %s AND d.paid = FALSE
                        ORDER BY d.date_created DESC"""
        
        success1, debts_owed = DbConnection.execute_query(owed_query, (student_id,), fetch_all=True)
        success2, debts_owing = DbConnection.execute_query(owing_query, (student_id,), fetch_all=True)
        
        if not success1:
            debts_owed = []
        if not success2:
            debts_owing = []
            
        return debts_owed, debts_owing

    @staticmethod
    def get_all_expenses():
        """Get all expenses from database"""
        query = """SELECT id, amount, description, date, id_giver, id_receiver, id_activity
                   FROM expenses ORDER BY date DESC"""
        
        success, result = DbConnection.execute_query(query, fetch_all=True)
        if not success:
            print(f"Error retrieving expenses: {result}")
            return []
            
        expenses = []
        for row in result:
            expense = Expense(row[1], row[2], row[3], row[4], row[5], row[6])
            expense.id = row[0]
            expenses.append(expense)
            
        return expenses

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
        return f"Expense(amount={self.amount}, description={self.description}, date={self.date})"