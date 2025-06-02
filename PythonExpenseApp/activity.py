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
    
    This class encapsulates all data and functionality related to a trip activity,
    including scheduling, participant management, feedback collection, and
    statistical analysis.
    
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
        
        This constructor creates a new activity object that can be saved to the database
        or represents an existing activity loaded from the database.
        
        PARAMETERS:
            name (str): The name/title of the activity (required)
            day (str/date): The date when the activity occurs (required)
            start (int): Starting hour in 24-hour format, e.g., 14 for 2 PM (required)
            finish (int): Ending hour in 24-hour format (required)
            location (str): Physical location where activity takes place (required)
            maxpart (int, optional): Maximum number of participants. None means unlimited
            duration (int, optional): Duration in hours. Can be calculated from start/finish
            description (str, optional): Detailed description of what the activity involves
            
        USAGE EXAMPLE:
            # Create a new museum visit activity
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
        
        # Core activity properties (required fields)
        self.name = name                    # Activity title/name
        self.day = day                      # Date of activity
        self.start = start                  # Start time (24-hour format)
        self.finish = finish                # End time (24-hour format)
        self.location = location            # Physical location
        
        # Optional properties
        self.maxpart = maxpart              # Maximum participants (None = unlimited)
        self.duration = duration            # Duration in hours
        self.description = description      # Detailed description
        
        # Runtime collections (loaded from database when needed)
        self.participants = []              # List of enrolled students
        self.activity_feedback = []         # List of feedback entries

    def get_current_participants(self):
        """
        Retrieve the current number of students enrolled in this activity.
        
        This method queries the database to get the real-time count of participants.
        It's used for capacity checking and statistical reporting.
        
        RETURNS:
            int: Current number of enrolled participants
            
        DATABASE QUERY:
            Counts records in student_activities table for this activity
            
        USAGE:
            current_count = activity.get_current_participants()
            if current_count >= activity.maxpart:
                print("Activity is full!")
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
        
        This method retrieves full participant information including names,
        which is useful for displaying enrollment lists and managing participants.
        
        RETURNS:
            list: List of tuples containing (student_id, first_name, last_name)
            Empty list if no participants or database error
            
        DATABASE QUERY:
            Joins student_activities with students table to get participant details
            Orders results alphabetically by last name, then first name
            
        USAGE:
            participants = activity.get_participant_list()
            for student_id, first_name, last_name in participants:
                print(f"{first_name} {last_name} is enrolled")
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
        
        This method enforces business rules for feedback:
        1. Student must have participated in the activity
        2. Student can only leave one feedback per activity
        
        PARAMETERS:
            student_id (int): The ID of the student wanting to leave feedback
            
        RETURNS:
            tuple: (can_leave_feedback, reason_message)
                - can_leave_feedback (bool): True if allowed, False if not
                - reason_message (str): Explanation of why feedback is/isn't allowed
                
        BUSINESS LOGIC:
            - Only participants can leave feedback (ensures authenticity)
            - One feedback per student per activity (prevents spam)
            
        USAGE:
            can_feedback, message = activity.can_student_leave_feedback(student.id)
            if can_feedback:
                show_feedback_form()
            else:
                show_error_message(message)
        """
        # Import Feedback class to use its validation logic
        from PythonExpenseApp.feedback import Feedback
        
        # Delegate to Feedback class which handles all validation logic
        return Feedback.can_student_leave_feedback(student_id, self.id)

    def get_rating_details(self):
        """
        Get comprehensive rating statistics for this activity.
        
        This method calculates detailed statistics about all ratings received,
        including distribution of ratings, averages, and counts. Used for
        analytics and displaying rating information in the GUI.
        
        RETURNS:
            dict or None: Dictionary containing rating statistics or None if no ratings
            Dictionary structure:
            {
                'total_ratings': int,           # Total number of ratings
                'average_rating': float,        # Average of all ratings
                'median_rating': float,         # Median rating value
                'rating_distribution': dict     # Count of each rating (1-5)
            }
            
        CALCULATIONS:
            - Rating distribution: Count of 1-star, 2-star, etc. ratings
            - Average: Mathematical mean of all ratings
            - Median: Middle value when ratings are sorted
            
        USAGE:
            rating_data = activity.get_rating_details()
            if rating_data:
                print(f"Average rating: {rating_data['average_rating']:.2f}")
                print(f"Total reviews: {rating_data['total_ratings']}")
        """
        # Check if activity exists in database
        if not self.id:
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
        rating_distribution = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
        total_ratings = 0
        
        # Populate distribution with actual counts from database
        for rating, count in rating_counts:
            rating_distribution[rating] = count
            total_ratings += count
        
        # Return None if no ratings exist
        if total_ratings == 0:
            return None
        
        # Calculate average rating
        query = """SELECT AVG(rating) as avg_rating
                   FROM feedback 
                   WHERE activity_id = %s"""
        
        success, avg_result = DbConnection.execute_query(query, (self.id,), fetch_one=True)
        average_rating = float(avg_result[0]) if avg_result and avg_result[0] else 0
        
        # Calculate median rating (approximate method using SQL)
        # This gets the middle value when ratings are sorted
        query = """SELECT rating
                   FROM feedback 
                   WHERE activity_id = %s
                   ORDER BY rating
                   LIMIT 1 OFFSET %s"""
        
        median_offset = total_ratings // 2  # Middle position for median
        success, median_result = DbConnection.execute_query(query, (self.id, median_offset), fetch_one=True)
        median_rating = float(median_result[0]) if median_result else 0
        
        # Return comprehensive rating statistics
        return {
            'total_ratings': total_ratings,
            'average_rating': average_rating,
            'median_rating': median_rating,
            'rating_distribution': rating_distribution
        }

    def get_comprehensive_details(self):
        """
        Retrieve all information needed for the activity details GUI.
        
        This method aggregates all activity-related data into a single structure
        that the GUI can use to display comprehensive activity information.
        It's the main data provider for the ActivityDetailsGUI class.
        
        RETURNS:
            dict or None: Complete activity information or None if activity doesn't exist
            Dictionary structure:
            {
                'participation': {
                    'current_participants': int,    # Current enrollment count
                    'participant_list': list        # List of enrolled students
                },
                'ratings': dict,                    # Rating statistics (from get_rating_details)
                'recent_feedback': list             # Recent feedback entries with student info
            }
            
        DATA SOURCES:
            - Participation data from student_activities table
            - Rating statistics from feedback table
            - Recent feedback with student names joined
            
        USAGE:
            details = activity.get_comprehensive_details()
            if details:
                display_activity_details(details)
            else:
                show_error("Activity not found")
        """
        # Ensure activity exists in database
        if not self.id:
            return None
        
        # Get participation information
        participant_list = self.get_participant_list()
        current_participants = len(participant_list)
        
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
        
        success, recent_feedback = DbConnection.execute_query(query, (self.id,), fetch_all=True)
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
        
        This static method loads all activities from the database and returns them
        as a list of Activity objects. Used for displaying activity lists in the GUI.
        
        RETURNS:
            list: List of Activity objects loaded from database
            Empty list if no activities or database error
            
        DATABASE QUERY:
            Selects all activities ordered by day and start time for logical display
            
        USAGE:
            activities = Activity.get_all_activities()
            for activity in activities:
                print(f"{activity.name} on {activity.day}")
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
            activity = Activity(row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8])
            activity.id = row[0]  # Set the database ID
            activities.append(activity)
        
        return activities

    @staticmethod
    def get_activity_by_id(activity_id):
        """
        Retrieve a specific activity by its database ID.
        
        This static method loads a single activity from the database using its
        unique identifier. Used when displaying detailed activity information.
        
        PARAMETERS:
            activity_id (int): The unique database ID of the activity to retrieve
            
        RETURNS:
            Activity or None: Activity object if found, None if not found or error
            
        DATABASE QUERY:
            Selects single activity by ID
            
        USAGE:
            activity = Activity.get_activity_by_id(5)
            if activity:
                display_activity_details(activity)
            else:
                show_error("Activity not found")
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
        
        This method inserts a new activity record into the database. Used when
        creating new activities through the application.
        
        RETURNS:
            bool: True if saved successfully, False if error occurred
            
        DATABASE OPERATION:
            INSERT into activities table with all activity properties
            
        SIDE EFFECTS:
            Sets self.id to the new database ID if successful
            
        USAGE:
            new_activity = Activity("Museum Visit", "2024-03-15", 9, 12, "Museum")
            if new_activity.save_to_database():
                print(f"Activity saved with ID: {new_activity.id}")
            else:
                print("Failed to save activity")
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
        
        This method determines if the activity can accept more participants
        based on the maximum capacity setting.
        
        RETURNS:
            bool: True if activity is at capacity, False if it can accept more participants
            
        LOGIC:
            - If maxpart is None (unlimited), always returns False
            - If maxpart is set, compares current participants to maximum
            
        USAGE:
            if activity.is_full():
                show_message("Sorry, this activity is full")
            else:
                allow_registration()
        """
        # Activities with no maximum capacity are never full
        if not self.maxpart:
            return False
        
        # Compare current participants to maximum capacity
        return self.get_current_participants() >= self.maxpart

    def __str__(self):
        """
        Return a string representation of this activity.
        
        This method provides a human-readable representation of the activity
        for debugging and logging purposes.
        
        RETURNS:
            str: Formatted string with key activity information
            
        USAGE:
            print(activity)  # Automatically calls __str__()
            logger.info(f"Processing {activity}")
        """
        return f"Activity(id={self.id}, name={self.name}, day={self.day}, participants={self.get_current_participants()})"
