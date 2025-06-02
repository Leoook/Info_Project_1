from PythonExpenseApp.db_connection import DbConnection
import mysql.connector

class Group:
    def __init__(self, common_activity, dietary_needs):
        self.id = None
        self.members = []
        self.common_activity = common_activity
        self.dietary_needs = dietary_needs
        self.created_at = None

    def add_member(self, student):
        self.members.append(student)

    def remove_member(self, student):
        if student in self.members:
            self.members.remove(student)

    def get_members(self):
        return self.members

    def get_common_activity(self):
        return self.common_activity

    def set_common_activity(self, common_activity):
        self.common_activity = common_activity

    def get_dietary_needs(self):
        return self.dietary_needs

    def set_dietary_needs(self, dietary_needs):
        self.dietary_needs = dietary_needs

    def save_to_database(self):
        """Save group to database using enhanced connection"""
        # First, create the groups table if it doesn't exist
        create_table_query = """
            CREATE TABLE IF NOT EXISTS groups (
                id INT AUTO_INCREMENT PRIMARY KEY,
                common_activity VARCHAR(200),
                dietary_needs TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """
        
        # Create table first
        DbConnection.execute_query(create_table_query)
        
        # Insert group
        query = "INSERT INTO groups (common_activity, dietary_needs) VALUES (%s, %s)"
        params = (self.common_activity, self.dietary_needs)
        
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
            
        # Create group_members table if it doesn't exist
        create_table_query = """
            CREATE TABLE IF NOT EXISTS group_members (
                id INT AUTO_INCREMENT PRIMARY KEY,
                group_id INT NOT NULL,
                student_id INT NOT NULL,
                joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (group_id) REFERENCES groups(id) ON DELETE CASCADE,
                FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE,
                UNIQUE KEY unique_group_member (group_id, student_id)
            )
        """
        
        DbConnection.execute_query(create_table_query)
        
        # Add member
        query = "INSERT INTO group_members (group_id, student_id) VALUES (%s, %s)"
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
        query = "SELECT id, common_activity, dietary_needs, created_at FROM groups ORDER BY created_at DESC"
        
        success, result = DbConnection.execute_query(query, fetch_all=True)
        if not success:
            print(f"Error retrieving groups: {result}")
            return []
            
        groups = []
        for row in result:
            group = Group(row[1], row[2])
            group.id = row[0]
            group.created_at = row[3]
            groups.append(group)
            
        return groups

    def get_members_from_database(self):
        """Get all members of this group from database"""
        if not self.id:
            return []
            
        query = """SELECT s.id, s.name, s.surname 
                   FROM students s
                   JOIN group_members gm ON s.id = gm.student_id
                   WHERE gm.group_id = %s
                   ORDER BY s.surname, s.name"""
        
        success, result = DbConnection.execute_query(query, (self.id,), fetch_all=True)
        if success:
            return result
        return []

    def __str__(self):
        return (f"Group [commonActivity={self.common_activity}, "
                f"dietaryNeeds={self.dietary_needs}, members={self.members}]")