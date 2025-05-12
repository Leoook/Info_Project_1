from db_connection import DbConnection
import mysql.connector

class DailyProgram:
    def __init__(self, day):
        self.day = day  # Python datetime.date or similar
        self.activities = {}  # dict of Activity -> list of Student

    def add_activity(self, activity, participants):
        self.activities[activity] = participants

    def get_activities(self):
        return self.activities

    def get_participants(self, activity):
        return self.activities.get(activity, [])

    def remove_activity(self, activity):
        if activity in self.activities:
            del self.activities[activity]

    def save_to_database(self):
        connection = DbConnection.connect()
        if connection:
            try:
                sql = "INSERT INTO daily_program (day, activity_id) VALUES (%s, %s)"
                statement = connection.cursor()
                for activity, _ in self.activities.items():
                    statement.execute(sql, (self.day, activity.get_id()))
                connection.commit()
                print("Daily program saved to database.")
            except mysql.connector.Error as e:
                print(f"Error saving daily program to database: {e}")

    def __str__(self):
        return f"DailyProgram [day={self.day}, activities={self.activities}]"