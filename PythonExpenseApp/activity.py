# ===================================================================
# ACTIVITY CLASS - CORE BUSINESS LOGIC FOR TRIP ACTIVITIES
# ===================================================================
# This file contains the Activity class which represents a single activity
# during the trip. It handles all business logic related to activities
# including participant management, feedback validation, and data retrieval.
#
# KEY RESPONSIBILITIES:
# 1. Activity data management (CRUD operations)
# 2. Participant enrollment tracking
# 3. Feedback system integration
# 4. Statistical data aggregation
# 5. Database interaction for activity-related queries
# ===================================================================

# Import the database connection module for all database operations
from PythonExpenseApp.db_connection import DbConnection
# Import datetime for handling date/time operations
from datetime import datetime

class Activity:
    """
    Represents a single trip activity with all its properties and behaviors.

    ATTRIBUTES:
        id (int): Unique database identifier (None for new activities)
        name (str): Activity name/title
        day (str/date): Date when activity occurs
        start (int): Starting hour in 24-hour format
        finish (int): Ending hour in 24-hour format  
        location (str): Where the activity takes place
        maxpart (int): Maximum participants (None = unlimited)
        duration (int): Duration in hours (optional)
        description (str): Detailed activity description
        participants (list): List of enrolled students (loaded from DB)
        activity_feedback (list): List of feedback entries (loaded from DB)
    """

    def __init__(self, name, day, start, finish, location, maxpart=None, duration=None, description=None):
        """
        Initialize a new Activity instance with the provided parameters.

        :param name: str - The name/title of the activity (required)
        :param day: str/date - The date when the activity occurs (required)
        :param start: int - Starting hour in 24-hour format, e.g., 14 for 2 PM (required)
        :param finish: int - Ending hour in 24-hour format (required)
        :param location: str - Physical location where activity takes place (required)
        :param maxpart: int, optional - Maximum number of participants. None means unlimited
        :param duration: int, optional - Duration in hours. Can be calculated from start/finish
        :param description: str, optional - Detailed description of what the activity involves

        USAGE EXAMPLE:
            museum_visit = Activity(
                name="National History Museum",
                day="2024-03-15", 
                start=9,
                finish=12,
                location="Downtown Museum District",
                maxpart=25,
                duration=3,
                description="Guided tour with interactive exhibits"
            )
        """
        # Database identifier - None for new activities, set when saved to DB
        self.id = None
        # Activity title/name (string)
        self.name = name
        # Date of activity (string or date)
        self.day = day
        # Start time (24-hour format, integer)
        self.start = start
        # End time (24-hour format, integer)
        self.finish = finish
        # Physical location (string)
        self.location = location
        # Maximum participants (integer or None for unlimited)
        self.maxpart = maxpart
        # Duration in hours (integer or None)
        self.duration = duration
        # Detailed description (string or None)
        self.description = description
        # List of enrolled students (populated from DB as needed)
        self.participants = []
        # List of feedback entries (populated from DB as needed)
        self.activity_feedback = []

    def get_current_participants(self):
        """
        Retrieve the current number of students enrolled in this activity.

        :return: int - Current number of enrolled participants

        - Queries the student_activities table for this activity's ID.
        - Returns 0 if the activity is not saved or on error.
        """
        # Check if activity has been saved to database (has an ID)
        if not self.id:
            return 0
            
        # Query to count enrolled participants for this activity
        query = "SELECT COUNT(*) FROM student_activities WHERE activity_id = %s"
        
        # Execute query safely with parameterized input
        success, result = DbConnection.execute_query(query, (self.id,), fetch_one=True)
        
        # Return count if successful, 0 if error
        if success and result:
            return result[0]  # result is a tuple, get first element (count)
        return 0

    def get_participant_list(self):
        """
        Get a detailed list of all students enrolled in this activity.

        :return: list of tuples (student_id, first_name, last_name)
        - Returns empty list if no participants or database error.
        - Joins student_activities and students tables.
        """
        # Check if activity exists in database
        if not self.id:
            return []
            
        # Complex query joining students and enrollment tables
        query = """SELECT s.id, s.name, s.surname
                   FROM students s
                   JOIN student_activities sa ON s.id = sa.student_id
                   WHERE sa.activity_id = %s
                   ORDER BY s.surname, s.name"""
        
        # Execute query and return results
        success, result = DbConnection.execute_query(query, (self.id,), fetch_all=True)
        if success:
            return result  # List of tuples: (id, name, surname)
        return []

    def can_student_leave_feedback(self, student_id):
        """
        Check if a specific student is allowed to leave feedback for this activity.

        :param student_id: int - The ID of the student wanting to leave feedback
        :return: tuple (can_leave_feedback: bool, reason_message: str)
        - Only participants can leave feedback.
        - One feedback per student per activity.
        """
        # Import Feedback class to use its validation logic
        from PythonExpenseApp.feedback import Feedback
        
        # Delegate to Feedback class which handles all validation logic
        return Feedback.can_student_leave_feedback(student_id, self.id)

    def get_rating_details(self):
        """
        Get comprehensive rating statistics for this activity.

        :return: dict or None - Dictionary with rating stats or None if no ratings.
        Keys: 'total_ratings', 'average_rating', 'median_rating', 'rating_distribution'
        """
        # Check if activity exists in database
        if not self.id: # Activity must be saved to have an ID
            return None
            
        # Query to get count of each rating value (1-5 stars)
        query = """SELECT rating, COUNT(*) as count
                   FROM feedback 
                   WHERE activity_id = %s
                   GROUP BY rating
                   ORDER BY rating"""
        
        success, rating_counts = DbConnection.execute_query(query, (self.id,), fetch_all=True)
        if not success:
            return None
        
        # Initialize rating distribution with all possible ratings (1-5)
        rating_distribution = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0} # Default distribution - all zero
        total_ratings = 0
        
        # Populate distribution with actual counts from database
        for rating, count in rating_counts: # rating is 1-5, count is number of feedback entries
            rating_distribution[rating] = count # Store count for this rating
            total_ratings += count # Increment total ratings count
        
        # Return None if no ratings exist
        if total_ratings == 0:
            return None
        
        # Calculate average rating
        query = """SELECT AVG(rating) as avg_rating
                   FROM feedback 
                   WHERE activity_id = %s"""
        
        success, avg_result = DbConnection.execute_query(query, (self.id,), fetch_one=True) # Fetch average rating
        average_rating = float(avg_result[0]) if avg_result and avg_result[0] else 0
        
        # Calculate median rating (approximate method using SQL)
        # This gets the middle value when ratings are sorted
        query = """SELECT rating
                   FROM feedback 
                   WHERE activity_id = %s
                   ORDER BY rating
                   LIMIT 1 OFFSET %s"""
        
        median_offset = total_ratings // 2  # Middle position for median
        success, median_result = DbConnection.execute_query(query, (self.id, median_offset), fetch_one=True) # Use OFFSET to get median
        median_rating = float(median_result[0]) if median_result else 0 # Ensure median is a float
        
        # Return comprehensive rating statistics
        return {
            'total_ratings': total_ratings, # Total number of ratings received
            'average_rating': average_rating, # Average rating value (float)
            'median_rating': median_rating, # Median rating value (float)
            'rating_distribution': rating_distribution # Distribution of ratings (1-5 stars)
        }

    def get_comprehensive_details(self): 
        """
        Retrieve all information needed for the activity details GUI.

        :return: dict or None - Complete activity information or None if not found.
        Keys: 'participation', 'ratings', 'recent_feedback'
        """
        # Ensure activity exists in database
        if not self.id:
            return None
        
        # Get participation information
        participant_list = self.get_participant_list() # List of tuples (student_id, name, surname)
        current_participants = len(participant_list) # Count of current participants
        
        # Structure participation data
        participation_data = {
            'current_participants': current_participants,
            'participant_list': participant_list
        }
        
        # Get rating statistics (may be None if no ratings)
        ratings_data = self.get_rating_details()
        
        # Get recent feedback with student information
        # This query joins feedback with students to get names
        query = """SELECT f.rating, f.comment, f.created_at, s.name, s.surname
                   FROM feedback f
                   JOIN students s ON f.student_id = s.id
                   WHERE f.activity_id = %s
                   ORDER BY f.created_at DESC
                   LIMIT 50"""
        
        success, recent_feedback = DbConnection.execute_query(query, (self.id,), fetch_all=True) #  Fetch last 50 feedback entries
        if not success:
            recent_feedback = []
        
        # Return comprehensive data structure
        return {
            'participation': participation_data,
            'ratings': ratings_data,
            'recent_feedback': recent_feedback
        }

    @staticmethod
    def get_all_activities():
        """
        Retrieve all activities from the database.

        :return: list of Activity objects loaded from database.
        - Returns empty list if no activities or database error.
        """
        # Query to get all activities in chronological order
        query = """SELECT id, name, day, start_time, finish_time, location, 
                          max_participants, duration, description
                   FROM activities 
                   ORDER BY day, start_time"""
        
        success, result = DbConnection.execute_query(query, fetch_all=True)
        if not success:
            return []
        
        # Convert database rows to Activity objects
        activities = []
        for row in result:
            # Create Activity object with data from database
            activity = Activity(row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8]) # row[0] is the ID
            activity.id = row[0]  # Set the database ID
            activities.append(activity) # Append to list
        
        return activities

    @staticmethod
    def get_activity_by_id(activity_id):
        """
        Retrieve a specific activity by its database ID.

        :param activity_id: int - The unique database ID of the activity to retrieve
        :return: Activity or None - Activity object if found, None if not found or error
        """
        # Query to get specific activity by ID
        query = """SELECT id, name, day, start_time, finish_time, location, 
                          max_participants, duration, description
                   FROM activities 
                   WHERE id = %s"""
        
        success, result = DbConnection.execute_query(query, (activity_id,), fetch_one=True)
        if not success or not result:
            return None
        
        # Create Activity object from database row
        activity = Activity(result[1], result[2], result[3], result[4], result[5], 
                           result[6], result[7], result[8])
        activity.id = result[0]  # Set the database ID
        return activity

    def save_to_database(self):
        """
        Save this activity to the database.

        :return: bool - True if saved successfully, False if error occurred.
        - Sets self.id to the new database ID if successful.
        """
        # SQL INSERT query for new activity
        query = """INSERT INTO activities (name, day, start_time, finish_time, location, 
                                          max_participants, duration, description)
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
        
        # Parameters tuple matching the query placeholders
        params = (self.name, self.day, self.start, self.finish, self.location,
                 self.maxpart, self.duration, self.description)
        
        # Execute the INSERT query
        success, result = DbConnection.execute_query(query, params)
        if success:
            self.id = result  # Store the new database ID
            return True
        return False

    def is_full(self):
        """
        Check if this activity has reached its participant capacity.

        :return: bool - True if activity is at capacity, False if it can accept more participants.
        - If maxpart is None (unlimited), always returns False.
        """
        current_participants = self.get_current_participants()
        # Cambiamento: controllo esplicito su None
        if self.maxpart is None:
            return False
        return current_participants >= self.maxpart

    def __str__(self):
        """
        Return a string representation of this activity.

        :return: str - Formatted string with key activity information.
        """
        return f"Activity(id={self.id}, name={self.name}, day={self.day}, participants={self.get_current_participants()})"
