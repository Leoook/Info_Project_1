from PythonExpenseApp.db_connection import DbConnection

class Feedback:
    def __init__(self, student_id, activity_id, rating, comment):
        """
        Initializes a new Feedback object with the given student, activity, rating, and comment.

        :param student_id: int - The ID of the student leaving the feedback.
        :param activity_id: int - The ID of the activity for which feedback is left.
        :param rating: int or float - The rating given by the student (e.g., 1-5).
        :param comment: str - The textual comment provided by the student.
        """
        # Unique identifier for the feedback (int or None if not saved to DB yet)
        self.id = None
        # The ID of the student who left the feedback (int)
        self.student_id = student_id
        # The ID of the activity the feedback is for (int)
        self.activity_id = activity_id
        # The rating given by the student (int or float, e.g., 1-5)
        self.rating = rating
        # The comment text provided by the student (string)
        self.comment = comment
        # Timestamp when the feedback was created (datetime or None if not set)
        self.created_at = None

    def get_id(self):
        """
        Returns the unique ID of the feedback.

        :return: int or None - Feedback ID.
        """
        return self.id

    def get_student_id(self):
        """
        Returns the ID of the student who left the feedback.

        :return: int - Student ID.
        """
        return self.student_id

    def get_activity_id(self):
        """
        Returns the ID of the activity for which the feedback was left.

        :return: int - Activity ID.
        """
        return self.activity_id

    def get_rating(self):
        """
        Returns the rating given in the feedback.

        :return: int or float - Rating value.
        """
        return self.rating

    def get_comment(self):
        """
        Returns the comment text of the feedback.

        :return: str - Feedback comment.
        """
        return self.comment

    @staticmethod
    def can_student_leave_feedback(student_id, activity_id):
        """
        Checks if a student is eligible to leave feedback for a specific activity.
        The student must have participated in the activity and not have already left feedback.

        :param student_id: int - The ID of the student.
        :param activity_id: int - The ID of the activity.
        :return: tuple (bool, str) - (Eligibility, Message explaining result)
        """
        # Check if student participated in the activity
        participation_query = """SELECT COUNT(*) FROM student_activities 
                                WHERE student_id = %s AND activity_id = %s"""
        
        success, result = DbConnection.execute_query(participation_query, (student_id, activity_id), fetch_one=True)
        if not success or not result or result[0] == 0:
            return False, "You must participate in an activity before leaving feedback."
        
        # Check if student has already given feedback
        feedback_query = """SELECT COUNT(*) FROM feedback 
                           WHERE student_id = %s AND activity_id = %s"""
        
        success, result = DbConnection.execute_query(feedback_query, (student_id, activity_id), fetch_one=True)
        if not success:
            return False, "Error checking existing feedback."
        
        if result[0] > 0:
            return False, "You have already left feedback for this activity."
        
        return True, "You can leave feedback for this activity."

    def validate_before_save(self):
        """
        Validates the feedback before saving to the database.
        Checks if the student can leave feedback for the activity.

        :return: tuple (bool, str) - (Validation result, Message)
        """
        can_leave, message = self.can_student_leave_feedback(self.student_id, self.activity_id)
        if not can_leave:
            return False, message
        return True, "Validation passed"

    def save_to_database(self):
        """
        Saves the feedback to the database after validation.
        Sets the feedback's ID after successful insertion.
        Also triggers sentiment analysis update for the activity.

        :return: tuple (bool, str) - (Success, Message)
        """
        # Validate before saving
        is_valid, validation_message = self.validate_before_save()
        if not is_valid:
            print(f"Feedback validation failed: {validation_message}")
            return False, validation_message
        
        query = """INSERT INTO feedback (student_id, activity_id, rating, comment) 
                   VALUES (%s, %s, %s, %s)"""
        
        params = (self.student_id, self.activity_id, self.rating, self.comment)
        
        success, result = DbConnection.execute_query(query, params)
        if success:
            self.id = result
            print(f"Feedback saved to database with ID {self.id}")
            
            # Trigger sentiment analysis update for the activity
            self._update_activity_sentiment_words()
            
            return True, "Feedback saved successfully"
        else:
            print(f"Error saving feedback to database: {result}")
            return False, f"Error saving feedback: {result}"

    def _update_activity_sentiment_words(self):
        """
        Updates sentiment words for the activity after new feedback is saved.
        This may trigger additional analysis or statistics updates.
        """
        try:
            from PythonExpenseApp.statistics import Statistics
            stats = Statistics()
            stats.extract_and_analyze_sentiment_words(self.activity_id)
        except Exception as e:
            print(f"Error updating sentiment words: {e}")

    @staticmethod
    def get_feedback_sentiment_analysis(activity_id):
        """
        Retrieves sentiment analysis for all feedback of a specific activity.
        Returns both the sentiment words and a summary.

        :param activity_id: int - The ID of the activity.
        :return: dict - {'sentiment_words': ..., 'sentiment_summary': ...}
        """
        from PythonExpenseApp.statistics import Statistics
        stats = Statistics()
        
        # Get sentiment words
        sentiment_words = stats.get_sentiment_words_for_activity(activity_id)
        
        # Get sentiment summary
        sentiment_summary = stats.get_activity_sentiment_summary(activity_id)
        
        return {
            'sentiment_words': sentiment_words,
            'sentiment_summary': sentiment_summary
        }

    @staticmethod
    def get_feedback_for_activity(activity_id):
        """
        Retrieves all feedback entries for a specific activity.
        Returns a list of tuples with feedback and student details.

        :param activity_id: int - The ID of the activity.
        :return: list - List of tuples (feedback_id, student_id, student_name, student_surname, rating, comment, created_at)
        """
        query = """SELECT f.id, f.student_id, s.name, s.surname, f.rating, f.comment, f.created_at
                   FROM feedback f
                   JOIN students s ON f.student_id = s.id
                   WHERE f.activity_id = %s
                   ORDER BY f.created_at DESC"""
        
        success, result = DbConnection.execute_query(query, (activity_id,), fetch_all=True)
        if success:
            return result
        else:
            print(f"Error retrieving feedback: {result}")
            return []

    @staticmethod
    def get_feedback_by_student(student_id):
        """
        Retrieves all feedback entries given by a specific student.
        Returns a list of tuples with feedback and activity details.

        :param student_id: int - The ID of the student.
        :return: list - List of tuples (feedback_id, activity_id, activity_name, rating, comment, created_at)
        """
        query = """SELECT f.id, f.activity_id, a.name, f.rating, f.comment, f.created_at
                   FROM feedback f
                   JOIN activities a ON f.activity_id = a.id
                   WHERE f.student_id = %s
                   ORDER BY f.created_at DESC"""
        
        success, result = DbConnection.execute_query(query, (student_id,), fetch_all=True)
        if success:
            return result
        else:
            print(f"Error retrieving feedback: {result}")
            return []

    @staticmethod
    def get_average_rating_for_activity(activity_id):
        """
        Calculates the average rating and count of feedback for a specific activity.

        :param activity_id: int - The ID of the activity.
        :return: tuple (average, count) - Average rating (float), number of feedbacks (int)
        """
        query = """SELECT AVG(rating), COUNT(*) FROM feedback WHERE activity_id = %s"""
        
        success, result = DbConnection.execute_query(query, (activity_id,), fetch_one=True)
        if success and result:
            return result[0], result[1]  # average, count
        return 0, 0

    def __str__(self):
        """
        Returns a string representation of the feedback object, including ID, rating, and comment.

        :return: str - Human-readable string describing the feedback.
        """
        return f"Feedback(id={self.id}, rating={self.rating}, comment='{self.comment}')"

