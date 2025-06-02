from PythonExpenseApp.db_connection import DbConnection
import mysql.connector

class Activity:
    def __init__(self, id_, name, maxpart, location, duration, start, finish, participants=None, feedback=None):
        self.id = id_
        self.name = name
        self.maxpart = maxpart
        self.location = location
        self.duration = duration
        self.start = start
        self.finish = finish
        self.participants = participants or []
        self.activity_feedback = feedback or []
        self.day = None
        self.description = None

    def get_id(self):
        return self.id

    def set_id(self, id_):
        self.id = id_

    def is_full(self):
        return len(self.participants) >= self.maxpart

    def save_to_database(self):
        """Save activity to database using enhanced connection"""
        query = """INSERT INTO activities 
                   (name, day, start_time, finish_time, location, max_participants, 
                    duration, description)
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
        
        params = (self.name, self.day, self.start, self.finish, self.location,
                 self.maxpart, self.duration, self.description)
        
        success, result = DbConnection.execute_query(query, params)
        if success:
            self.id = result
            print(f"Activity '{self.name}' saved to database with ID {self.id}")
            return True
        else:
            print(f"Error saving activity to database: {result}")
            return False

    def update_in_database(self):
        """Update activity in database"""
        if not self.id:
            print("Error: Activity ID is required to update")
            return False
            
        query = """UPDATE activities 
                   SET name=%s, day=%s, start_time=%s, finish_time=%s, 
                       location=%s, max_participants=%s, duration=%s, description=%s
                   WHERE id=%s"""
        
        params = (self.name, self.day, self.start, self.finish, self.location,
                 self.maxpart, self.duration, self.description, self.id)
        
        success, result = DbConnection.execute_query(query, params)
        if success:
            print(f"Activity '{self.name}' updated in database")
            return True
        else:
            print(f"Error updating activity: {result}")
            return False

    @staticmethod
    def get_all_activities():
        """Get all activities from database"""
        query = """SELECT id, name, day, start_time, finish_time, location, 
                          max_participants, duration, description 
                   FROM activities ORDER BY day, start_time"""
        
        success, result = DbConnection.execute_query(query, fetch_all=True)
        if not success:
            print(f"Error retrieving activities: {result}")
            return []
            
        activities = []
        for row in result:
            activity = Activity(row[0], row[1], row[6], row[5], row[7], row[3], row[4])
            activity.day = row[2]
            activity.description = row[8]
            activities.append(activity)
            
        return activities

    @staticmethod
    def get_activity_by_id(activity_id):
        """Get specific activity by ID"""
        query = """SELECT id, name, day, start_time, finish_time, location, 
                          max_participants, duration, description 
                   FROM activities WHERE id=%s"""
        
        success, result = DbConnection.execute_query(query, (activity_id,), fetch_one=True)
        if not success or not result:
            return None
            
        activity = Activity(result[0], result[1], result[6], result[5], result[7], result[3], result[4])
        activity.day = result[2]
        activity.description = result[8]
        
        return activity

    def get_current_participants(self):
        """Get current number of participants for this activity"""
        if not self.id:
            return 0
            
        query = "SELECT COUNT(*) FROM student_activities WHERE activity_id=%s"
        success, result = DbConnection.execute_query(query, (self.id,), fetch_one=True)
        
        if success and result:
            return result[0]
        return 0

    def get_participant_list(self):
        """Get list of students participating in this activity"""
        if not self.id:
            return []
            
        query = """SELECT s.id, s.name, s.surname 
                   FROM students s
                   JOIN student_activities sa ON s.id = sa.student_id
                   WHERE sa.activity_id=%s
                   ORDER BY s.surname, s.name"""
        
        success, result = DbConnection.execute_query(query, (self.id,), fetch_all=True)
        if success:
            return result
        return []

    def get_detailed_ratings(self):
        """Get detailed rating information for this activity"""
        if not self.id:
            return None
            
        query = """SELECT average_rating, median_rating, total_ratings,
                          rating_1_count, rating_2_count, rating_3_count,
                          rating_4_count, rating_5_count
                   FROM activity_ratings WHERE activity_id = %s"""
        
        success, result = DbConnection.execute_query(query, (self.id,), fetch_one=True)
        if success and result:
            return {
                'average_rating': float(result[0]) if result[0] else 0.0,
                'median_rating': float(result[1]) if result[1] else 0.0,
                'total_ratings': result[2],
                'rating_distribution': {
                    1: result[3], 2: result[4], 3: result[5],
                    4: result[6], 5: result[7]
                }
            }
        return None

    def get_sentiment_words(self, limit=10):
        """Get most common sentiment words from feedback"""
        if not self.id:
            return []
        
        from PythonExpenseApp.statistics import Statistics
        stats = Statistics()
        return stats.get_sentiment_words_for_activity(self.id, limit)

    def update_sentiment_analysis(self):
        """Manually trigger sentiment analysis update for this activity"""
        if not self.id:
            return False
        
        try:
            from PythonExpenseApp.statistics import Statistics
            stats = Statistics()
            sentiment_words = stats.extract_and_analyze_sentiment_words(self.id)
            return len(sentiment_words) > 0
        except Exception as e:
            print(f"Error updating sentiment analysis: {e}")
            return False

    def get_sentiment_summary(self):
        """Get sentiment summary for this activity"""
        if not self.id:
            return {}
        
        from PythonExpenseApp.statistics import Statistics
        stats = Statistics()
        return stats.get_activity_sentiment_summary(self.id)

    def get_recent_feedback(self, limit=5):
        """Get recent feedback with student information"""
        if not self.id:
            return []
            
        query = """SELECT f.rating, f.comment, f.created_at, s.name, s.surname
                   FROM feedback f
                   JOIN students s ON f.student_id = s.id
                   WHERE f.activity_id = %s
                   ORDER BY f.created_at DESC
                   LIMIT %s"""
        
        success, result = DbConnection.execute_query(query, (self.id, limit), fetch_all=True)
        if success:
            return result
        return []

    def get_comprehensive_details(self):
        """Get all activity details including ratings, sentiment, and feedback"""
        if not self.id:
            return None
            
        details = {
            'basic_info': {
                'id': self.id,
                'name': self.name,
                'day': self.day,
                'start_time': self.start,
                'finish_time': self.finish,
                'location': self.location,
                'max_participants': self.maxpart,
                'duration': self.duration,
                'description': self.description
            },
            'participation': {
                'current_participants': self.get_current_participants(),
                'participant_list': self.get_participant_list()
            },
            'ratings': self.get_detailed_ratings(),
            'sentiment_words': self.get_sentiment_words(),
            'recent_feedback': self.get_recent_feedback()
        }
        
        return details

    def update_ratings(self):
        """Manually trigger rating update for this activity"""
        if not self.id:
            return False
            
        query = "CALL UpdateActivityRatings(%s)"
        success, result = DbConnection.execute_query(query, (self.id,))
        return success

    def update_sentiment_analysis(self):
        """Manually trigger sentiment analysis update for this activity"""
        if not self.id:
            return False
            
        query = "CALL UpdateSentimentWords(%s)"
        success, result = DbConnection.execute_query(query, (self.id,))
        return success

    @staticmethod
    def get_top_rated_activities(limit=5):
        """Get top-rated activities"""
        query = """SELECT a.id, a.name, ar.average_rating, ar.total_ratings
                   FROM activities a
                   JOIN activity_ratings ar ON a.id = ar.activity_id
                   WHERE ar.total_ratings >= 3
                   ORDER BY ar.average_rating DESC, ar.total_ratings DESC
                   LIMIT %s"""
        
        success, result = DbConnection.execute_query(query, (limit,), fetch_all=True)
        if success:
            return result
        return []

    @staticmethod
    def get_activities_by_rating_range(min_rating, max_rating):
        """Get activities within a specific rating range"""
        query = """SELECT a.id, a.name, ar.average_rating, ar.total_ratings
                   FROM activities a
                   JOIN activity_ratings ar ON a.id = ar.activity_id
                   WHERE ar.average_rating BETWEEN %s AND %s
                   ORDER BY ar.average_rating DESC"""
        
        success, result = DbConnection.execute_query(query, (min_rating, max_rating), fetch_all=True)
        if success:
            return result
        return []

    def __str__(self):
        return (f"Activity [id={self.id}, name={self.name}, maxpart={self.maxpart}, "
                f"location={self.location}, duration={self.duration}, start={self.start}, "
                f"finish={self.finish}, participants={self.participants}, "
                f"feedback={self.activity_feedback}]")
    
    def load_feedback_from_database(self):
        """
        Placeholder for loading feedback from the database. Implement as needed.
        """
        pass

    def can_student_leave_feedback(self, student_id):
        """Check if a student can leave feedback for this activity"""
        if not self.id:
            return False, "Activity not found"
        
        from PythonExpenseApp.feedback import Feedback
        return Feedback.can_student_leave_feedback(student_id, self.id)

    def get_students_who_can_leave_feedback(self):
        """Get list of students who participated but haven't left feedback"""
        if not self.id:
            return []
        
        query = """SELECT s.id, s.name, s.surname
                   FROM students s
                   JOIN student_activities sa ON s.id = sa.student_id
                   LEFT JOIN feedback f ON s.id = f.student_id AND f.activity_id = %s
                   WHERE sa.activity_id = %s AND f.id IS NULL
                   ORDER BY s.surname, s.name"""
        
        success, result = DbConnection.execute_query(query, (self.id, self.id), fetch_all=True)
        if success:
            return result
        return []

    def get_feedback_statistics(self):
        """Get feedback statistics for this activity"""
        if not self.id:
            return {}
        
        # Get participation and feedback counts
        participants_query = """SELECT COUNT(*) FROM student_activities WHERE activity_id = %s"""
        feedback_query = """SELECT COUNT(*) FROM feedback WHERE activity_id = %s"""
        
        success1, participants_result = DbConnection.execute_query(participants_query, (self.id,), fetch_one=True)
        success2, feedback_result = DbConnection.execute_query(feedback_query, (self.id,), fetch_one=True)
        
        if success1 and success2:
            participants_count = participants_result[0] if participants_result else 0
            feedback_count = feedback_result[0] if feedback_result else 0
            
            return {
                'total_participants': participants_count,
                'feedback_given': feedback_count,
                'feedback_pending': participants_count - feedback_count,
                'feedback_percentage': (feedback_count / participants_count * 100) if participants_count > 0 else 0
            }
        
        return {}
