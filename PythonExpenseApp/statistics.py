from PythonExpenseApp.db_connection import DbConnection

class Statistics:
    def __init__(self, activities=None, feedbacks=None):
        """
        Initializes the Statistics object with optional activities and feedbacks data.

        :param activities: dict - A dictionary mapping activity names/IDs to lists of student IDs or objects.
        :param feedbacks: dict - A dictionary mapping activity names/IDs to lists of feedback objects or ratings.
        """
        # Dictionary mapping activity names/IDs to lists of students participating in each activity.
        # Example: {'Football': [student1, student2], 'Chess': [student3]}
        self.activities = activities or {}
        # Dictionary mapping activity names/IDs to lists of feedbacks for each activity.
        # Example: {'Football': [feedback1, feedback2], 'Chess': [feedback3]}
        self.feedbacks = feedbacks or {}

    def get_total_participants(self):
        """
        Calculates the total number of participants across all activities.

        :return: int - The sum of all participants in all activities.
        """
        return sum(len(students) for students in self.activities.values())

    def get_most_popular_activity(self):
        """
        Determines the activity with the highest number of participants.

        :return: key (activity name/ID) or None if no activities exist.
        """
        if not self.activities:
            return None
        # Returns the activity with the maximum number of participants.
        return max(self.activities, key=lambda act: len(self.activities[act]))

    def get_average_participants(self):
        """
        Calculates the average number of participants per activity.

        :return: float - The average number of participants, or 0.0 if no activities exist.
        """
        if not self.activities:
            return 0.0
        return float(self.get_total_participants()) / len(self.activities)

    def fetch_statistics_from_database(self):
        """
        Fetches comprehensive statistics from the database, including:
        - Total participants across all activities.
        - Most popular activity and its participant count.
        - Participation statistics for each activity.
        - Average rating per activity (if feedback exists).
        - Total expenses, count, and average expense.
        - Outstanding debts summary.

        :return: dict - A dictionary containing various statistics.
        """
        stats = {}
        
        # Total participants across all activities (from student_activities table)
        query = "SELECT COUNT(*) AS total_participants FROM student_activities"
        success, result = DbConnection.execute_query(query, fetch_one=True)
        if success and result:
            stats['total_participants'] = result[0]
        
        # Most popular activity (from activities and student_activities tables)
        query = """SELECT a.name, COUNT(sa.student_id) as participant_count
                   FROM activities a
                   LEFT JOIN student_activities sa ON a.id = sa.activity_id
                   GROUP BY a.id, a.name
                   ORDER BY participant_count DESC
                   LIMIT 1"""
        success, result = DbConnection.execute_query(query, fetch_one=True)
        if success and result:
            stats['most_popular_activity'] = {'name': result[0], 'participants': result[1]}
        
        # Activity participation statistics (from activities and student_activities tables)
        query = """SELECT a.name, COUNT(sa.student_id) as participants, a.max_participants
                   FROM activities a
                   LEFT JOIN student_activities sa ON a.id = sa.activity_id
                   GROUP BY a.id, a.name, a.max_participants
                   ORDER BY participants DESC"""
        success, result = DbConnection.execute_query(query, fetch_all=True)
        if success:
            stats['activity_participation'] = result
        
        # Average rating per activity (from activities and feedback tables)
        query = """SELECT a.name, AVG(f.rating) as avg_rating, COUNT(f.id) as feedback_count
                   FROM activities a
                   LEFT JOIN feedback f ON a.id = f.activity_id
                   GROUP BY a.id, a.name
                   HAVING feedback_count > 0
                   ORDER BY avg_rating DESC"""
        success, result = DbConnection.execute_query(query, fetch_all=True)
        if success:
            stats['activity_ratings'] = result
        
        # Total expenses and debt statistics (from expenses and debts tables)
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
        
        # Outstanding debts summary (from debts table)
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
        """
        Get statistics for a specific student, including:
        - Number of activities the student is participating in.
        - Total expenses paid by the student.
        - Money owed to the student.
        - Money the student owes.
        - Feedback count given by the student.

        :param student_id: int or str - The ID of the student for whom statistics are to be fetched.
        :return: dict - A dictionary containing various statistics for the student.
        """
        stats = {}
        
        # Student's activities count (from student_activities table)
        query = """SELECT COUNT(*) FROM student_activities WHERE student_id = %s"""
        success, result = DbConnection.execute_query(query, (student_id,), fetch_one=True)
        if success and result:
            stats['activities_count'] = result[0]
        
        # Student's expenses (as payer) - count and total amount (from expenses table)
        query = """SELECT COUNT(*), SUM(amount) FROM expenses WHERE id_giver = %s"""
        success, result = DbConnection.execute_query(query, (student_id,), fetch_one=True)
        if success and result:
            stats['expenses_paid'] = {
                'count': result[0],
                'total': result[1] if result[1] else 0
            }
        
        # Money owed to student (from debts table)
        query = """SELECT SUM(amount) FROM debts WHERE payer_id = %s AND paid = FALSE"""
        success, result = DbConnection.execute_query(query, (student_id,), fetch_one=True)
        if success and result:
            stats['money_owed_to_student'] = result[0] if result[0] else 0
        
        # Money student owes (from debts table)
        query = """SELECT SUM(amount) FROM debts WHERE debtor_id = %s AND paid = FALSE"""
        success, result = DbConnection.execute_query(query, (student_id,), fetch_one=True)
        if success and result:
            stats['money_student_owes'] = result[0] if result[0] else 0
        
        # Student's feedback count (from feedback table)
        query = """SELECT COUNT(*) FROM feedback WHERE student_id = %s"""
        success, result = DbConnection.execute_query(query, (student_id,), fetch_one=True)
        if success and result:
            stats['feedback_given'] = result[0]
        
        return stats

    def __str__(self):
        """
        String representation of the Statistics object, displaying:
        - Total number of participants.
        - Most popular activity.
        - Average number of participants per activity.

        :return: str - A formatted string summarizing the statistics.
        """
        return (f"Statistics [Total Participants={self.get_total_participants()}, "
                f"Most Popular Activity={self.get_most_popular_activity()}, "
                f"Average Participants={self.get_average_participants()}]")