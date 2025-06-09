from PythonExpenseApp.db_connection import DbConnection
import mysql.connector

class Group:
    def __init__(self, name, common_activity, dietary_needs):
        """
        Initializes a new Group object with the given name, common activity, and dietary needs.

        :param name: str - The name of the group.
        :param common_activity: str - The activity that is common to all group members.
        :param dietary_needs: str - Any dietary needs or restrictions for the group.
        """
        # Unique identifier for the group (int or None if not saved to DB yet)
        self.id = None
        # Name of the group (string, e.g., "Group A")
        self.name = name # Added name attribute
        # List of members in the group (list of Student objects or IDs/names)
        self.members = [] # This will store Student objects if loaded, or IDs/names
        # The activity that is common to all group members (string)
        self.common_activity = common_activity
        # Dietary needs or restrictions for the group (string)
        self.dietary_needs = dietary_needs
        # Timestamp when the group was created (datetime or None if not set)
        self.created_at = None

    def add_member(self, student):
        """
        Adds a student to the group's members list.

        :param student: Student object or identifier to add to the group.
        :return: None
        """
        self.members.append(student)

    def remove_member(self, student):
        """
        Removes a student from the group's members list if present.

        :param student: Student object or identifier to remove from the group.
        :return: None
        """
        if student in self.members:
            self.members.remove(student)

    def get_members(self):
        """
        Returns the list of members in the group.

        :return: list - List of Student objects or identifiers.
        """
        return self.members

    def get_common_activity(self):
        """
        Returns the common activity for the group.

        :return: str - The group's common activity.
        """
        return self.common_activity

    def set_common_activity(self, common_activity):
        """
        Sets the common activity for the group.

        :param common_activity: str - The new common activity.
        :return: None
        """
        self.common_activity = common_activity

    def get_dietary_needs(self):
        """
        Returns the dietary needs for the group.

        :return: str - The group's dietary needs.
        """
        return self.dietary_needs

    def set_dietary_needs(self, dietary_needs):
        """
        Sets the dietary needs for the group.

        :param dietary_needs: str - The new dietary needs.
        :return: None
        """
        self.dietary_needs = dietary_needs

    def save_to_database(self):
        """
        Saves the group to the database using the DbConnection class.
        Sets the group's ID after successful insertion.

        :return: bool - True if saved successfully, False otherwise.
        """
        # Table creation is handled by DbConnection.create_tables_if_not_exist() or a setup script.
        
        query = "INSERT INTO groups (name, common_activity, dietary_needs) VALUES (%s, %s, %s)"
        params = (self.name, self.common_activity, self.dietary_needs) # Using self.name for group name
        
        success, result = DbConnection.execute_query(query, params) 
        if success:
            self.id = result
            print(f"Group saved to database with ID {self.id}")
            return True
        else:
            print(f"Error saving group to database: {result}")
            return False

    def add_member_to_database(self, student_id):
        """Add a member to the group in the database"""
        if not self.id:
            print("Error: Group must be saved to database first")
            return False
            
        # Table creation is handled by DbConnection.create_tables_if_not_exist() or a setup script.
        # Using 'student_groups' table name to match schema.
        
        query = "INSERT INTO student_groups (group_id, student_id) VALUES (%s, %s)"
        params = (self.id, student_id)
        
        success, result = DbConnection.execute_query(query, params)
        if success:
            print(f"Student {student_id} added to group {self.id}")
            return True
        else:
            print(f"Error adding member to group: {result}")
            return False

    @staticmethod
    def get_all_groups():
        """Get all groups from database"""
        query = "SELECT id, name, common_activity, dietary_needs, created_at FROM groups ORDER BY name"
        
        success, result = DbConnection.execute_query(query, fetch_all=True)
        if not success:
            print(f"Error retrieving groups: {result}")
            return []
            
        groups = []
        for row in result:
            group = Group(row[1], row[2], row[3]) # name, common_activity, dietary_needs
            group.id = row[0]
            group.created_at = row[4]
            groups.append(group)
            
        return groups

    def get_members_from_database(self):
        """Get all members of this group from database"""
        if not self.id:
            return []
            
        # Using 'student_groups' table name to match schema.
        query = """SELECT s.id, s.name, s.surname 
                   FROM students s
                   JOIN student_groups sg ON s.id = sg.student_id
                   WHERE sg.group_id = %s
                   ORDER BY s.surname, s.name"""
        
        success, result = DbConnection.execute_query(query, (self.id,), fetch_all=True)
        if success:
            return result
        return []

    def __str__(self): # String representation of the Group object
        return (f"Group [id={self.id}, name={self.name}, commonActivity={self.common_activity}, "  #added name attribute
                f"dietaryNeeds={self.dietary_needs}, membersCount={len(self.members)}]")  # Added members count for better representation
        # Note: This will not include members' details, just the count.