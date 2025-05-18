from PythonExpenseApp.db_connection import DbConnection
import mysql.connector
import re

class Statistics:
    def __init__(self, activities, feedbacks):
        # activities: dict of Activity -> list of Student
        # feedbacks: dict of Activity -> list of strings
        self.activities = activities
        self.feedbacks = feedbacks

    def get_total_participants(self):
        return sum(len(students) for students in self.activities.values())

    def get_most_popular_activity(self):
        if not self.activities:
            return None
        return max(self.activities, key=lambda act: len(self.activities[act]))

    def highlight_sentimental_words(self, activity, sentimental_words):
        feedback_list = self.feedbacks.get(activity, [])
        highlighted = []
        for feedback in feedback_list:
            highlighted_feedback = feedback
            for word in sentimental_words:
                # Add asterisks around matching words
                pattern = r"\b" + re.escape(word) + r"\b"
                highlighted_feedback = re.sub(pattern, f"*{word}*", highlighted_feedback)
            highlighted.append(highlighted_feedback)
        return highlighted

    def get_average_participants(self):
        if not self.activities:
            return 0.0
        return float(self.get_total_participants()) / len(self.activities)

    def fetch_statistics_from_database(self):
        connection = DbConnection.connect()
        if connection:
            try:
                sql = "SELECT COUNT(*) AS total_participants FROM student_activities"
                statement = connection.cursor()
                statement.execute(sql)
                result = statement.fetchone()
                if result:
                    print(f"Total Participants: {result[0]}")
            except mysql.connector.Error as e:
                print(f"Error fetching statistics from database: {e}")

    def __str__(self):
        return (f"Statistics [Total Participants={self.get_total_participants()}, "
                f"Most Popular Activity={self.get_most_popular_activity()}, "
                f"Average Participants={self.get_average_participants()}]")