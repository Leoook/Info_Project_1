from db_connection import DbConnection
import mysql.connector

class Activity:
    def __init__(self, id_, name, maxpart, location, duration, start, finish, participants, feedback):
        self.id = id_
        self.name = name
        self.maxpart = maxpart
        self.location = location
        self.duration = duration
        self.start = start
        self.finish = finish
        self.participants = participants  # list
        self.activity_feedback = feedback # list

    def get_id(self):
        return self.id

    def set_id(self, id_):
        self.id = id_

    def is_full(self):
        return len(self.participants) >= self.maxpart

    def save_to_database(self):
        connection = DbConnection.connect()
        if connection:
            try:
                sql = """INSERT INTO activities
                         (name, max_participants, location, duration, start_time, finish_time)
                         VALUES (%s, %s, %s, %s, %s, %s)"""
                statement = connection.cursor()
                statement.execute(sql, (self.name, self.maxpart, self.location,
                                        self.duration, self.start, self.finish))
                connection.commit()
                print("Activity saved to database.")
            except mysql.connector.Error as e:
                print(f"Error saving activity to database: {e}")

    def __str__(self):
        return (f"Activity [id={self.id}, name={self.name}, maxpart={self.maxpart}, "
                f"location={self.location}, duration={self.duration}, start={self.start}, "
                f"finish={self.finish}, participants={self.participants}, "
                f"feedback={self.activity_feedback}]")