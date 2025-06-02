from PythonExpenseApp.db_connection import DbConnection

class Feedback:
    def __init__(self, student_id, activity_id, rating, comment):
        self.id = None
        self.student_id = student_id
        self.activity_id = activity_id
        self.rating = rating
        self.comment = comment
        self.created_at = None

    def get_id(self):
        return self.id

    def get_student_id(self):
        return self.student_id

    def get_activity_id(self):
        return self.activity_id

    def get_rating(self):
        return self.rating

    def get_comment(self):
        return self.comment

    @staticmethod
    def can_student_leave_feedback(student_id, activity_id):
        """Check if a student can leave feedback for an activity"""
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
        """Validate feedback before saving to database"""
        can_leave, message = self.can_student_leave_feedback(self.student_id, self.activity_id)
        if not can_leave:
            return False, message
        return True, "Validation passed"

    def save_to_database(self):
        """Save feedback to database with validation"""
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
        """Update sentiment words for the activity after new feedback"""
        try:
            from PythonExpenseApp.statistics import Statistics
            stats = Statistics()
            stats.extract_and_analyze_sentiment_words(self.activity_id)
        except Exception as e:
            print(f"Error updating sentiment words: {e}")

    @staticmethod
    def get_feedback_sentiment_analysis(activity_id):
        """Get sentiment analysis for all feedback of an activity"""
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
        """Get all feedback for a specific activity"""
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
        """Get all feedback given by a specific student"""
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
        """Get average rating for an activity"""
        query = """SELECT AVG(rating), COUNT(*) FROM feedback WHERE activity_id = %s"""
        
        success, result = DbConnection.execute_query(query, (activity_id,), fetch_one=True)
        if success and result:
            return result[0], result[1]  # average, count
        return 0, 0

    def __str__(self):
        return f"Feedback(id={self.id}, rating={self.rating}, comment='{self.comment}')"

