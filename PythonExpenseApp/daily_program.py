# ===================================================================
# DAILY PROGRAM MODULE - SCHEDULE MANAGEMENT AND CONFLICT DETECTION
# ===================================================================
# This module handles daily schedule management for trip activities,
# including conflict detection, time slot validation, and schedule
# optimization for students and activities.
#
# KEY RESPONSIBILITIES:
# 1. Managing daily activity schedules
# 2. Detecting time conflicts for students
# 3. Validating activity time slots
# 4. Generating optimized schedules
# 5. Providing schedule analytics and reporting
# ===================================================================

# Import required modules for database operations and date handling
from PythonExpenseApp.db_connection import DbConnection  # For database interactions
from datetime import datetime, date, time, timedelta    # For date and time manipulations
import calendar  # For calendar-related functions (though not explicitly used in current methods)

class DailyProgram:
    """
    Manages daily activity schedules and handles conflict detection.

    ATTRIBUTES:
        date (date): The specific date this program instance represents.
        activities (list): List of Activity objects scheduled for this date.
        conflicts (dict): Tracks scheduling conflicts for students.
        time_slots (dict): Maps each hour of the day (0-23) to a list of Activity objects.
        student_schedules (dict): Caches student schedules for the day.

    USAGE:
        program = DailyProgram("2024-03-15")
        student_conflicts = program.detect_student_conflicts(student_id=1)
        schedule_display_text = program.get_formatted_schedule(format_type="detailed")
    """

    def __init__(self, program_date=None):
        """
        Initialize a DailyProgram for a specific date.

        :param program_date: str or date, optional. The date for this program.
                             Can be a string in "YYYY-MM-DD" format or a Python `date` object.
                             Defaults to `date.today()` if not provided.

        Initializes:
            - self.date: The date for which the schedule is managed.
            - self.activities: List of Activity objects for the date.
            - self.conflicts: Dict for student_id -> list of conflicting activities.
            - self.time_slots: Dict for hour -> list of activities at that hour.
            - self.student_schedules: Dict for student_id -> list of their activities for the day.

        Raises:
            ValueError: If `program_date` string is not in "YYYY-MM-DD" format.
            TypeError: If `program_date` is not a string, `date` object, or None.
        """
        # Parse and store the program date
        if program_date is None:
            self.date = date.today()  # Use today's date if no date is specified
        elif isinstance(program_date, str):
            # Parse string date, expecting "YYYY-MM-DD" format
            try:
                self.date = datetime.strptime(program_date, "%Y-%m-%d").date()
            except ValueError:
                # Raise an error if the date string format is incorrect
                raise ValueError(f"Invalid date format: {program_date}. Use YYYY-MM-DD format.")
        elif isinstance(program_date, date):
            self.date = program_date  # Use the provided date object directly
        else:
            # Raise an error if the type of program_date is unexpected
            raise TypeError(f"Date must be string or date object, got {type(program_date)}")
        
        # Initialize data structures for managing schedule information
        self.activities = []          # List to store Activity objects for this date
        self.conflicts = {}          # Dict to store student_id -> list of conflicting activities
        self.time_slots = {}         # Dict to map hour -> list of activities at that time
        self.student_schedules = {}  # Dict to cache student_id -> list of their activities for the day
        
        # Load activities for this specific date from the database
        self.load_activities_for_date()
        
        # Build a mapping of time slots to activities for efficient conflict detection
        self.build_time_slot_mapping()

    def load_activities_for_date(self):
        """
        Load all activities scheduled for the program's date from the database.

        - Queries the `activities` table for all activities on self.date.
        - Converts each row into an Activity object and stores in self.activities.
        - Prints status messages on success or failure.
        - If no activities found, self.activities is empty.
        """
        # Import Activity class locally to avoid circular dependencies at module level
        from PythonExpenseApp.activity import Activity
        
        # SQL query to select activities for the specific date, ordered by start time
        query = """SELECT id, name, day, start_time, finish_time, location, 
                          max_participants, duration, description
                   FROM activities 
                   WHERE day = %s
                   ORDER BY start_time, name"""
        
        # Execute the query using the DbConnection class
        # (self.date,) is a tuple containing the date parameter for the query
        success, result = DbConnection.execute_query(query, (self.date,), fetch_all=True)
        
        if success and result:
            # If the query was successful and returned data
            # Convert each database row into an Activity object
            for row in result:
                # Create an Activity object using data from the current row
                activity = Activity(
                    name=row[1],           # Activity name (index 1 in the row tuple)
                    day=row[2],            # Activity date
                    start=row[3],          # Start hour
                    finish=row[4],         # Finish hour
                    location=row[5],       # Location
                    maxpart=row[6],        # Max participants
                    duration=row[7],       # Duration in hours
                    description=row[8]     # Detailed description
                )
                activity.id = row[0]       # Set the database ID for the Activity object
                self.activities.append(activity) # Add the new Activity object to the list
            
            # Print a success message to the console
            print(f"Loaded {len(self.activities)} activities for {self.date}")
        else:
            # Handle cases where the query failed or no activities were found
            if not success:
                # If the query execution itself failed
                print(f"Database error loading activities for {self.date}: {result}")
            else:
                # If the query was successful but returned no results
                print(f"No activities found for {self.date}")
            self.activities = [] # Ensure self.activities is an empty list

    def build_time_slot_mapping(self):
        """
        Build a mapping of time slots (hours) to activities for efficient conflict detection.

        - Iterates through all loaded activities and populates self.time_slots.
        - Each hour (0-23) maps to a list of activities scheduled during that hour.
        - Used for fast conflict detection and slot availability checks.
        """
        # Initialize or clear the time_slots dictionary
        self.time_slots = {}
        
        # Process each activity loaded for the day
        for activity in self.activities:
            # Get the start and finish hours for the current activity
            start_hour = activity.start   # e.g., 9
            finish_hour = activity.finish # e.g., 12
            
            # Add this activity to each hour slot it occupies
            # range(start_hour, finish_hour) will produce [9, 10, 11] for the example
            for hour in range(start_hour, finish_hour):
                # If this hour slot hasn't been seen before, initialize it with an empty list
                if hour not in self.time_slots:
                    self.time_slots[hour] = []
                
                # Add the current activity to the list of activities for this hour
                self.time_slots[hour].append(activity)
        
        # Print a status message indicating the mapping is built
        print(f"Built time slot mapping with {len(self.time_slots)} occupied hours")

    def detect_student_conflicts(self, student_id):
        """
        Detect scheduling conflicts for a specific student on the program's date.

        :param student_id: int. The database ID of the student.
        :return: list. Each element is a list of Activity objects that conflict with each other.

        - Retrieves all activities the student is enrolled in for self.date.
        - Checks all pairs for time overlaps.
        - Returns a list of conflict groups (each group is a list of conflicting activities).
        """
        # Get all activities the student is enrolled in for this specific date
        student_activities = self.get_student_activities_for_date(student_id)
        
        # If the student has 0 or 1 activity, no conflicts are possible
        if len(student_activities) <= 1:
            return []
        
        # List to store groups of conflicting activities
        conflicts = []
        # Set to keep track of pairs of activities already checked to avoid redundant checks
        checked_pairs = set()
        
        # Iterate through each activity the student is enrolled in
        for i, activity1 in enumerate(student_activities):
            # Start a new potential conflict group with the current activity
            current_conflict_group = {activity1} # Use a set for easy addition and uniqueness
            
            # Compare activity1 with every other activity the student is enrolled in
            for j, activity2 in enumerate(student_activities):
                if i == j: # Don't compare an activity with itself
                    continue
                
                # Check if these two activities overlap in time
                if self.activities_overlap(activity1, activity2):
                    current_conflict_group.add(activity2) # Add to the current conflict set
            
            # If the conflict group has more than one activity, it's a valid conflict
            if len(current_conflict_group) > 1:
                # Sort activities in the group by ID to ensure consistent representation
                # This helps in identifying duplicate conflict groups
                sorted_conflict_group = sorted(list(current_conflict_group), key=lambda act: act.id)
                
                # Check if this exact conflict group (or a permutation) is already in conflicts list
                is_duplicate = False
                for existing_group in conflicts:
                    # Compare sets of activity IDs for equality
                    if set(act.id for act in sorted_conflict_group) == set(act.id for act in existing_group):
                        is_duplicate = True
                        break
                
                if not is_duplicate:
                    conflicts.append(sorted_conflict_group) # Add the new, unique conflict group
        
        return conflicts

    def activities_overlap(self, activity1, activity2):
        """
        Check if two activities have overlapping time slots.

        :param activity1: Activity object.
        :param activity2: Activity object.
        :return: bool. True if the activities' time slots overlap, False otherwise.

        - Uses interval overlap logic: [start1, end1) and [start2, end2) overlap if start1 < end2 and start2 < end1.
        """
        # Get the start and finish hours for both activities
        start1, end1 = activity1.start, activity1.finish
        start2, end2 = activity2.start, activity2.finish
        
        # Standard interval overlap condition:
        # Two intervals [s1, e1] and [s2, e2] overlap if s1 < e2 AND s2 < e1.
        overlap_exists = (start1 < end2) and (start2 < end1)
        
        return overlap_exists

    def get_student_activities_for_date(self, student_id):
        """
        Get all activities a student is enrolled in for this program's date.

        :param student_id: int. The database ID of the student.
        :return: list of Activity objects for self.date.

        - Queries the database for all activities for the student on self.date.
        - Caches results in self.student_schedules for efficiency.
        """
        # Check cache first
        if student_id in self.student_schedules:
            return self.student_schedules[student_id]

        # SQL query to get activities for a student on a specific date
        query = """SELECT a.id, a.name, a.day, a.start_time, a.finish_time, a.location,
                          a.max_participants, a.duration, a.description
                   FROM activities a
                   JOIN student_activities sa ON a.id = sa.activity_id
                   WHERE sa.student_id = %s AND a.day = %s
                   ORDER BY a.start_time""" # Order by start time for a chronological list
        
        # Execute the query with student_id and self.date as parameters
        success, result = DbConnection.execute_query(query, (student_id, self.date), fetch_all=True)
        
        student_activities_list = []
        if success and result:
            # Import Activity class locally
            from PythonExpenseApp.activity import Activity
            
            # Convert each database row to an Activity object
            for row in result:
                activity = Activity(
                    name=row[1], day=row[2], start=row[3], finish=row[4],
                    location=row[5], maxpart=row[6], duration=row[7], description=row[8]
                )
                activity.id = row[0] # Set the database ID
                student_activities_list.append(activity)
        
        # Cache the result
        self.student_schedules[student_id] = student_activities_list
        return student_activities_list

    def get_available_time_slots(self, duration_hours=1):
        """
        Find available time slots on self.date for an activity of a given duration.

        :param duration_hours: int, optional. Required duration in hours. Defaults to 1.
        :return: list of (start_hour, end_hour) tuples representing available slots.

        - Scans the day for continuous blocks of free time at least duration_hours long.
        - Returns all such available slots.
        """
        available_slots = []
        
        # Define a reasonable range of hours for scheduling activities (e.g., 6 AM to 11 PM)
        earliest_scheduling_hour = 6   # 6:00 AM
        latest_scheduling_hour = 23    # 11:00 PM (activities must end by this hour)
        
        # Iterate through possible start hours for the new activity
        # The loop ensures that an activity of `duration_hours` can fit before `latest_scheduling_hour`
        for start_hour_candidate in range(earliest_scheduling_hour, latest_scheduling_hour - duration_hours + 1):
            is_slot_available = True # Assume the slot is available initially
            
            # Check each hour within the proposed duration
            for hour_offset in range(duration_hours):
                current_hour_to_check = start_hour_candidate + hour_offset
                # If the current hour is already in time_slots and has activities, it's occupied
                if current_hour_to_check in self.time_slots and len(self.time_slots[current_hour_to_check]) > 0:
                    is_slot_available = False # This slot is not available
                    break # No need to check further hours for this start_hour_candidate
            
            if is_slot_available:
                # If all hours in the duration are free, this is an available slot
                end_hour_candidate = start_hour_candidate + duration_hours
                available_slots.append((start_hour_candidate, end_hour_candidate))
        
        return available_slots

    def get_formatted_schedule(self, format_type="simple"):
        """
        Generate a human-readable, formatted schedule display for self.date.

        :param format_type: str, optional. "simple", "detailed", or "timeline".
        :return: str. Formatted schedule.

        - "simple": Basic list with times and activity names.
        - "detailed": Includes location, duration, and participant info.
        - "timeline": Hour-by-hour view of activities.
        """
        # If there are no activities for the day, return a simple message
        if not self.activities:
            return f"No activities scheduled for {self.date.strftime('%A, %B %d, %Y')}"
        
        # Prepare the header with the day's date
        day_name = self.date.strftime('%A') # Full weekday name (e.g., "Monday")
        formatted_date_str = self.date.strftime('%B %d, %Y') # e.g., "March 15, 2024"
        schedule_text_parts = [f"=== {day_name}, {formatted_date_str} ===\n"]
        
        # Sort activities by start time for chronological display
        sorted_activities = sorted(self.activities, key=lambda act: act.start)
        
        if format_type == "simple":
            # Simple format: "HH:00 - HH:00: Activity Name"
            for activity in sorted_activities:
                start_time_str = f"{activity.start:02d}:00" # Format hour as HH
                end_time_str = f"{activity.finish:02d}:00"
                schedule_text_parts.append(f"{start_time_str} - {end_time_str}: {activity.name}")
        
        elif format_type == "detailed":
            # Detailed format: includes location, participants, and description
            for activity in sorted_activities:
                start_time_str = f"{activity.start:02d}:00"
                end_time_str = f"{activity.finish:02d}:00"
                
                # Get current participant count for the activity
                current_participants = activity.get_current_participants()
                capacity_info_str = f"{current_participants}"
                if activity.maxpart: # If max participants is set
                    capacity_info_str += f"/{activity.maxpart}"
                capacity_info_str += " participants"
                
                schedule_text_parts.append(f"{start_time_str} - {end_time_str}: {activity.name}")
                schedule_text_parts.append(f"  📍 Location: {activity.location}")
                schedule_text_parts.append(f"  👥 {capacity_info_str}")
                if activity.description:
                    # Truncate long descriptions for brevity
                    desc_preview = activity.description[:100] + "..." if len(activity.description) > 100 else activity.description
                    schedule_text_parts.append(f"  📝 {desc_preview}")
                schedule_text_parts.append("") # Add a blank line for spacing
        
        elif format_type == "timeline":
            # Timeline format: Hour-by-hour view
            # Determine the range of hours to display based on occupied slots
            occupied_hours_keys = sorted(self.time_slots.keys())
            if occupied_hours_keys:
                min_hour = min(occupied_hours_keys)
                max_hour = max(occupied_hours_keys) # Last hour an activity is in
                
                # Iterate from the earliest activity start to the end of the latest activity
                for hour in range(min_hour, max_hour + 1):
                    time_label_str = f"{hour:02d}:00"
                    
                    if hour in self.time_slots and self.time_slots[hour]:
                        # If there are activities in this hour slot
                        activities_at_this_hour = self.time_slots[hour]
                        activity_names_str = ', '.join([act.name for act in activities_at_this_hour])
                        schedule_text_parts.append(f"{time_label_str} | {activity_names_str}")
                    else:
                        # If the hour slot is free
                        schedule_text_parts.append(f"{time_label_str} | (Free time)")
            else: # Should not happen if self.activities is not empty, but as a fallback
                schedule_text_parts.append("No scheduled activities to display in timeline.")
        
        return "\n".join(schedule_text_parts) # Join all parts with newlines

    def get_schedule_statistics(self):
        """
        Generate statistical information about the day's schedule.

        :return: dict. Contains keys like 'total_activities', 'total_scheduled_hours', 'average_duration', etc.

        - Analyzes the schedule for insights such as total activities, scheduled hours, busiest hours, and participant summary.
        """
        # Initialize statistics dictionary with default values
        stats = {
            'date': self.date.isoformat(), # ISO format date string (YYYY-MM-DD)
            'total_activities': len(self.activities),
            'total_scheduled_hours': 0,
            'average_duration': 0.0,
            'busiest_hours': [], # List of hours with the most concurrent activities
            'schedule_utilization': 0.0, # Percentage of the day (or scheduling window) occupied
            'activity_types': {}, # Placeholder for future categorization
            'participant_summary': {} # Summary of participant numbers
        }
        
        # If there are no activities, return the default stats
        if not self.activities:
            return stats
        
        # Calculate total scheduled hours and average duration
        total_duration_sum = sum(activity.finish - activity.start for activity in self.activities)
        stats['total_scheduled_hours'] = total_duration_sum
        if len(self.activities) > 0:
            stats['average_duration'] = total_duration_sum / len(self.activities)
        
        # Find busiest hours (hours with the maximum number of concurrent activities)
        hour_activity_counts = {} # Store count of activities per hour
        for hour, activities_in_hour in self.time_slots.items():
            hour_activity_counts[hour] = len(activities_in_hour)
        
        if hour_activity_counts:
            max_concurrent_activities = max(hour_activity_counts.values())
            stats['busiest_hours'] = [
                hour for hour, count in hour_activity_counts.items() 
                if count == max_concurrent_activities
            ]
        
        # Calculate schedule utilization (e.g., percentage of a 24-hour day occupied)
        # This could be refined to use a specific scheduling window (e.g., 8 AM - 10 PM)
        occupied_unique_hours = len(self.time_slots) # Number of unique hours that have at least one activity
        total_hours_in_day = 24 
        if total_hours_in_day > 0:
            stats['schedule_utilization'] = (occupied_unique_hours / total_hours_in_day) * 100
        
        # Participant summary statistics
        total_enrollments = 0
        for activity in self.activities:
            total_enrollments += activity.get_current_participants()
        
        stats['participant_summary'] = {
            'total_enrollments': total_enrollments, # Sum of participants across all activities
            'average_enrollment_per_activity': total_enrollments / len(self.activities) if self.activities else 0.0
        }
        
        return stats

    def validate_new_activity(self, start_hour, finish_hour, max_participants=None):
        """
        Validate if a new activity can be scheduled at the specified time on self.date.

        :param start_hour: int. Proposed start hour (0-23).
        :param finish_hour: int. Proposed finish hour (1-24).
        :param max_participants: int, optional. Not used in validation here.
        :return: tuple (is_valid, validation_messages).

        - Checks for time integrity, hour range, minimum duration, and conflicts with existing activities.
        - Returns True and empty list if valid, otherwise False and list of issues.
        """
        validation_messages = []
        is_valid = True
        
        # 1. Basic time integrity check
        if start_hour >= finish_hour:
            validation_messages.append("Start time must be before finish time.")
            is_valid = False
        
        # 2. Hour range validation
        if not (0 <= start_hour <= 23 and 1 <= finish_hour <= 24):
            validation_messages.append("Hours must be within valid range (start: 0-23, finish: 1-24).")
            is_valid = False
        
        # 3. Minimum duration check (assuming valid start/finish from above checks)
        if is_valid and (finish_hour - start_hour < 1): # Check is_valid to avoid error with bad start/finish
            validation_messages.append("Activity must be at least 1 hour long.")
            is_valid = False
        
        # If basic time checks failed, no point in checking conflicts
        if not is_valid:
            return False, validation_messages

        # 4. Conflict detection with existing activities
        conflicting_activity_objects = []
        for hour_to_check in range(start_hour, finish_hour):
            if hour_to_check in self.time_slots and self.time_slots[hour_to_check]:
                # If this hour is already occupied, collect conflicting activities
                for existing_activity in self.time_slots[hour_to_check]:
                    if existing_activity not in conflicting_activity_objects:
                        conflicting_activity_objects.append(existing_activity)
        
        if conflicting_activity_objects:
            conflicting_names = [act.name for act in conflicting_activity_objects]
            validation_messages.append(f"Time conflict with existing activities: {', '.join(conflicting_names)}.")
            is_valid = False
        
        # 5. Reasonable scheduling hours warning (e.g., not too early or too late)
        # This is a soft validation - it adds a message but doesn't set is_valid to False.
        if start_hour < 6 or finish_hour > 23: # Example: 6 AM to 11 PM
            validation_messages.append("Warning: Activity is scheduled outside typical hours (6:00 AM - 11:00 PM).")
            # is_valid remains unchanged by this warning
        
        return is_valid, validation_messages

    def export_schedule(self, file_format="txt", file_path=None):
        """
        Export the schedule for self.date to a file in the specified format.

        :param file_format: str, optional. "txt", "csv", or "json". Defaults to "txt".
        :param file_path: str, optional. Path to save the file. Defaults to "schedule_YYYY-MM-DD.format".
        :return: str. Absolute path to the created file.

        - Exports schedule in human-readable text, CSV, or JSON format.
        - Raises ValueError for unsupported formats.
        """
        import json # For JSON export
        import csv  # For CSV export
        import os   # For path manipulation
        
        # Generate a default filename if file_path is not provided
        if file_path is None:
            date_str = self.date.strftime("%Y-%m-%d")
            # Default filename in the current working directory
            file_path = os.path.abspath(f"schedule_{date_str}.{file_format.lower()}")
        
        # Ensure the directory for the file_path exists
        output_directory = os.path.dirname(file_path)
        if output_directory and not os.path.exists(output_directory):
            os.makedirs(output_directory) # Create directory if it doesn't exist

        if file_format.lower() == "txt":
            # Text format export
            # Get detailed schedule and statistics
            schedule_content = self.get_formatted_schedule("detailed")
            stats_content = self.get_schedule_statistics()
            
            # Combine into a single string
            full_content = schedule_content + "\n\n" + "="*50 + "\n"
            full_content += "SCHEDULE STATISTICS\n" + "="*50 + "\n"
            for key, value in stats_content.items():
                full_content += f"{key.replace('_', ' ').title()}: {value}\n"
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(full_content)
        
        elif file_format.lower() == "csv":
            # CSV format export
            with open(file_path, 'w', newline='', encoding='utf-8') as f:
                csv_writer = csv.writer(f)
                
                # CSV Header row
                header = ['Date', 'Activity ID', 'Activity Name', 'Start Time (HH:00)', 
                          'End Time (HH:00)', 'Location', 'Current Participants', 
                          'Max Participants', 'Duration (Hours)', 'Description']
                csv_writer.writerow(header)
                
                # Write data for each activity
                for activity in sorted(self.activities, key=lambda act: act.start):
                    row_data = [
                        self.date.isoformat(),
                        activity.id,
                        activity.name,
                        f"{activity.start:02d}:00",
                        f"{activity.finish:02d}:00",
                        activity.location,
                        activity.get_current_participants(),
                        activity.maxpart if activity.maxpart is not None else 'Unlimited',
                        activity.duration if activity.duration is not None else (activity.finish - activity.start),
                        activity.description if activity.description else ''
                    ]
                    csv_writer.writerow(row_data)
        
        elif file_format.lower() == "json":
            # JSON format export
            # Prepare data structure for JSON
            json_output_data = {
                'schedule_date': self.date.isoformat(),
                'activities_list': [],
                'schedule_statistics': self.get_schedule_statistics() # Get stats as a dict
            }
            
            for activity in sorted(self.activities, key=lambda act: act.start):
                activity_dict = {
                    'id': activity.id,
                    'name': activity.name,
                    'start_hour': activity.start,
                    'finish_hour': activity.finish,
                    'location': activity.location,
                    'current_participants': activity.get_current_participants(),
                    'max_participants': activity.maxpart,
                    'duration_hours': activity.duration if activity.duration is not None else (activity.finish - activity.start),
                    'description': activity.description
                }
                json_output_data['activities_list'].append(activity_dict)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                # Dump data to JSON file with indentation for readability
                json.dump(json_output_data, f, indent=4, ensure_ascii=False)
        else:
            # Handle unsupported format
            raise ValueError(f"Unsupported file format: {file_format}. Supported formats: txt, csv, json.")
            
        print(f"Schedule exported successfully to: {file_path}")
        return file_path

    def __str__(self):
        """
        Return a string representation of the DailyProgram instance.

        :return: str. Format: "DailyProgram(date=YYYY-MM-DD, activities=N)".
        """
        return f"DailyProgram(date={self.date.isoformat()}, activities={len(self.activities)})"

    def __repr__(self):
        """
        Return a detailed string representation of the DailyProgram instance.

        :return: str. Includes date, number of activities, and a preview of activities.
        """
        if not self.activities:
            activities_preview = "No activities loaded."
        else:
            # Show a preview of the first few activities (up to 3) with their times
            activities_preview = ", ".join([f"{act.name} ({act.start:02d}:00-{act.finish:02d}:00)" for act in self.activities[:3]])
            if len(self.activities) > 3:
                activities_preview += ", ..." # Indicate that there are more activities
            
        return (f"DailyProgram(date={self.date.isoformat()}, "
                f"activities_count={len(self.activities)}, "
                f"activities_preview=[{activities_preview}])")