import tkinter as tk
from tkinter import messagebox
import mysql.connector
from PythonExpenseApp.db_connection import DbConnection

class ActivityFormGUI:
    """
    GUI for subscribing a student to an activity.
    The 'self' variable refers to the current instance of ActivityFormGUI.
    It is used to access instance variables (attributes) and methods throughout the class.
    For example, self.activities refers to the list of activities for this particular GUI window.
    """
    def __init__(self, root):
        """
        Initializes the Activity Subscription GUI window and its widgets.
        - Loads all activities from the database and displays them in a listbox.
        - Provides input fields for student name, surname, and class.
        - Provides a button to subscribe the student to the selected activity.
        """
        self.root = root  # Reference to the Tkinter window for this GUI instance
        self.root.title("Activity Subscription")

        # List of activity display strings (e.g., "Basketball (max: 10)")
        self.activities = []
        # List of activity IDs corresponding to the activities
        self.activity_ids = []
        # Retrieve activities from the database
        connection = DbConnection.connect()
        if connection:
            try:
                sql = "SELECT id, name, max_participants FROM activities"
                statement = connection.cursor()
                statement.execute(sql)
                for (id_, name, maxp) in statement:
                    self.activities.append(f"{name} (max: {maxp})")
                    self.activity_ids.append(id_)
            except mysql.connector.Error as e:
                messagebox.showerror("Error", f"Error loading activities: {e}")

        # Listbox to select an activity
        tk.Label(self.root, text="Select Activity:").grid(row=0, column=0, padx=5, pady=5)
        self.activity_var = tk.StringVar()
        self.activity_listbox = tk.Listbox(self.root, listvariable=tk.StringVar(value=self.activities), height=6)
        self.activity_listbox.grid(row=0, column=1, padx=5, pady=5)

        # Entry for student name
        tk.Label(self.root, text="Name:").grid(row=1, column=0, padx=5, pady=5)
        self.name_var = tk.StringVar()
        self.name_entry = tk.Entry(self.root, textvariable=self.name_var)
        self.name_entry.grid(row=1, column=1, padx=5, pady=5)

        # Entry for student surname
        tk.Label(self.root, text="Surname:").grid(row=2, column=0, padx=5, pady=5)
        self.surname_var = tk.StringVar()
        self.surname_entry = tk.Entry(self.root, textvariable=self.surname_var)
        self.surname_entry.grid(row=2, column=1, padx=5, pady=5)

        # Entry for student class
        tk.Label(self.root, text="Class:").grid(row=3, column=0, padx=5, pady=5)
        self.class_var = tk.StringVar()
        self.class_entry = tk.Entry(self.root, textvariable=self.class_var)
        self.class_entry.grid(row=3, column=1, padx=5, pady=5)

        # Button to subscribe the student to the selected activity
        tk.Button(self.root, text="Subscribe", command=self.subscribe_student).grid(row=4, column=0, columnspan=2, pady=10)

    def subscribe_student(self):
        """
        Subscribes the student to the selected activity if possible.
        - Checks that all fields are filled.
        - Checks that the student exists in the database.
        - Checks that the activity is not full.
        - If all checks pass, inserts the subscription into the student_activities table.
        - Shows a message on success or error.
        Uses 'self' to access the current GUI's widgets and data.
        """
        # Get selected activity index from this instance's listbox
        selection = self.activity_listbox.curselection()
        if not selection:
            messagebox.showerror("Error", "Please select an activity.")
            return
        activity_idx = selection[0]
        activity_id = self.activity_ids[activity_idx]

        # Get student info from this instance's input fields
        name = self.name_var.get().strip()
        surname = self.surname_var.get().strip()
        class_ = self.class_var.get().strip()

        if not (name and surname and class_):
            messagebox.showerror("Error", "Please fill all student fields.")
            return

        connection = DbConnection.connect()
        if not connection:
            messagebox.showerror("Error", "Database connection error.")
            return

        try:
            # Check if the student exists in the database
            sql = "SELECT id FROM students WHERE name = %s AND surname = %s AND class = %s"
            statement = connection.cursor()
            statement.execute(sql, (name, surname, class_))
            student_row = statement.fetchone()
            if not student_row:
                messagebox.showerror("Error", "Student not found.")
                return
            student_id = student_row[0]

            # Check the activity's maximum capacity
            sql = "SELECT max_participants FROM activities WHERE id = %s"
            statement.execute(sql, (activity_id,))
            maxp_row = statement.fetchone()
            if not maxp_row:
                messagebox.showerror("Error", "Activity not found.")
                return
            max_participants = maxp_row[0]

            # Count current participants in the activity
            sql = "SELECT COUNT(*) FROM student_activities WHERE activity_id = %s"
            statement.execute(sql, (activity_id,))
            count_row = statement.fetchone()
            current_participants = count_row[0] if count_row else 0

            # If activity is full, show error
            if current_participants >= max_participants:
                messagebox.showerror("Error", "Activity is full.")
                return

            # Subscribe the student to the activity
            sql = "INSERT INTO student_activities (student_id, activity_id) VALUES (%s, %s)"
            statement.execute(sql, (student_id, activity_id))
            connection.commit()
            messagebox.showinfo("Success", "Student subscribed to activity.")
            self.root.destroy()
        except mysql.connector.Error as e:
            messagebox.showerror("Error", f"Database error: {e}")
