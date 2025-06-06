from PythonExpenseApp.db_connection import DbConnection

class Statistics:
    def __init__(self, activities=None, feedbacks=None):
        self.activities = activities or {}
        self.feedbacks = feedbacks or {}

    def get_total_participants(self):
        return sum(len(students) for students in self.activities.values())

    def get_most_popular_activity(self):
        if not self.activities:
            return None
        return max(self.activities, key=lambda act: len(self.activities[act]))

    def get_average_participants(self):
        if not self.activities:
            return 0.0
        return float(self.get_total_participants()) / len(self.activities)

    def fetch_statistics_from_database(self):
        """Fetch comprehensive statistics from database"""
        stats = {}
        
        # Total participants across all activities
        query = "SELECT COUNT(*) AS total_participants FROM student_activities"
        success, result = DbConnection.execute_query(query, fetch_one=True)
        if success and result:
            stats['total_participants'] = result[0]
        
        # Most popular activity
        query = """SELECT a.name, COUNT(sa.student_id) as participant_count
                   FROM activities a
                   LEFT JOIN student_activities sa ON a.id = sa.activity_id
                   GROUP BY a.id, a.name
                   ORDER BY participant_count DESC
                   LIMIT 1"""
        success, result = DbConnection.execute_query(query, fetch_one=True)
        if success and result:
            stats['most_popular_activity'] = {'name': result[0], 'participants': result[1]}
        
        # Activity participation statistics
        query = """SELECT a.name, COUNT(sa.student_id) as participants, a.max_participants
                   FROM activities a
                   LEFT JOIN student_activities sa ON a.id = sa.activity_id
                   GROUP BY a.id, a.name, a.max_participants
                   ORDER BY participants DESC"""
        success, result = DbConnection.execute_query(query, fetch_all=True)
        if success:
            stats['activity_participation'] = result
        
        # Average rating per activity
        query = """SELECT a.name, AVG(f.rating) as avg_rating, COUNT(f.id) as feedback_count
                   FROM activities a
                   LEFT JOIN feedback f ON a.id = f.activity_id
                   GROUP BY a.id, a.name
                   HAVING feedback_count > 0
                   ORDER BY avg_rating DESC"""
        success, result = DbConnection.execute_query(query, fetch_all=True)
        if success:
            stats['activity_ratings'] = result
        
        # Total expenses and debt statistics
        query = """SELECT 
                       SUM(amount) as total_expenses,
                       COUNT(*) as expense_count,
                       AVG(amount) as avg_expense
                   FROM expenses"""
        success, result = DbConnection.execute_query(query, fetch_one=True)
        if success and result:
            stats['expense_summary'] = {
                'total': result[0] if result[0] else 0,
                'count': result[1],
                'average': result[2] if result[2] else 0
            }
        
        # Outstanding debts summary
        query = """SELECT 
                       SUM(amount) as total_outstanding,
                       COUNT(*) as debt_count
                   FROM debts WHERE paid = FALSE"""
        success, result = DbConnection.execute_query(query, fetch_one=True)
        if success and result:
            stats['debt_summary'] = {
                'total_outstanding': result[0] if result[0] else 0,
                'count': result[1]
            }
        
        return stats

    def get_student_statistics(self, student_id):
        """Get statistics for a specific student"""
        stats = {}
        
        # Student's activities
        query = """SELECT COUNT(*) FROM student_activities WHERE student_id = %s"""
        success, result = DbConnection.execute_query(query, (student_id,), fetch_one=True)
        if success and result:
            stats['activities_count'] = result[0]
        
        # Student's expenses (as payer)
        query = """SELECT COUNT(*), SUM(amount) FROM expenses WHERE id_giver = %s"""
        success, result = DbConnection.execute_query(query, (student_id,), fetch_one=True)
        if success and result:
            stats['expenses_paid'] = {
                'count': result[0],
                'total': result[1] if result[1] else 0
            }
        
        # Money owed to student
        query = """SELECT SUM(amount) FROM debts WHERE payer_id = %s AND paid = FALSE"""
        success, result = DbConnection.execute_query(query, (student_id,), fetch_one=True)
        if success and result:
            stats['money_owed_to_student'] = result[0] if result[0] else 0
        
        # Money student owes
        query = """SELECT SUM(amount) FROM debts WHERE debtor_id = %s AND paid = FALSE"""
        success, result = DbConnection.execute_query(query, (student_id,), fetch_one=True)
        if success and result:
            stats['money_student_owes'] = result[0] if result[0] else 0
        
        # Student's feedback count
        query = """SELECT COUNT(*) FROM feedback WHERE student_id = %s"""
        success, result = DbConnection.execute_query(query, (student_id,), fetch_one=True)
        if success and result:
            stats['feedback_given'] = result[0]
        
        return stats

    def __str__(self):
        return (f"Statistics [Total Participants={self.get_total_participants()}, "
                f"Most Popular Activity={self.get_most_popular_activity()}, "
                f"Average Participants={self.get_average_participants()}]")