from db_connection import DbConnection
import mysql.connector

class Group:
    def __init__(self, common_activity, dietary_needs):
        self.members = []
        self.common_activity = common_activity
        self.dietary_needs = dietary_needs

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
        connection = DbConnection.connect()
        if connection:
            try:
                sql = "INSERT INTO groups (common_activity, dietary_needs) VALUES (%s, %s)"
                statement = connection.cursor()
                statement.execute(sql, (self.common_activity, self.dietary_needs))
                connection.commit()
                print("Group saved to database.")
            except mysql.connector.Error as e:
                print(f"Error saving group to database: {e}")

    def __str__(self):
        return (f"Group [commonActivity={self.common_activity}, "
                f"dietaryNeeds={self.dietary_needs}, members={self.members}]")