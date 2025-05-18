import tkinter as tk
from tkinter import messagebox
import mysql.connector
from PythonExpenseApp.db_connection import DbConnection

class ActivityFormGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Activity Subscription")

        # Retrieve activities from DB
        self.activities = []
        self.activity_ids = []
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

        tk.Label(self.root, text="Select Activity:").grid(row=0, column=0, padx=5, pady=5)
        self.activity_var = tk.StringVar()
        self.activity_listbox = tk.Listbox(self.root, listvariable=tk.StringVar(value=self.activities), height=6)
        self.activity_listbox.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.root, text="Name:").grid(row=1, column=0, padx=5, pady=5)
        self.name_var = tk.StringVar()
        self.name_entry = tk.Entry(self.root, textvariable=self.name_var)
        self.name_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(self.root, text="Surname:").grid(row=2, column=0, padx=5, pady=5)
        self.surname_var = tk.StringVar()
        self.surname_entry = tk.Entry(self.root, textvariable=self.surname_var)
        self.surname_entry.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(self.root, text="Class:").grid(row=3, column=0, padx=5, pady=5)
        self.class_var = tk.StringVar()
        self.class_entry = tk.Entry(self.root, textvariable=self.class_var)
        self.class_entry.grid(row=3, column=1, padx=5, pady=5)

        tk.Button(self.root, text="Subscribe", command=self.subscribe_student).grid(row=4, column=0, columnspan=2, pady=10)

    def subscribe_student(self):
        selection = self.activity_listbox.curselection()
        if not selection:
            messagebox.showerror("Error", "Please select an activity.")
            return
        activity_idx = selection[0]
        activity_id = self.activity_ids[activity_idx]

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
            sql = "SELECT id FROM students WHERE name = %s AND surname = %s AND class = %s"
            statement = connection.cursor()
            statement.execute(sql, (name, surname, class_))
            student_row = statement.fetchone()
            if not student_row:
                messagebox.showerror("Error", "Student not found.")
                return
            student_id = student_row[0]

            sql = "SELECT max_participants FROM activities WHERE id = %s"
            statement.execute(sql, (activity_id,))
            maxp_row = statement.fetchone()
            if not maxp_row:
                messagebox.showerror("Error", "Activity not found.")
                return
            max_participants = maxp_row[0]

            sql = "SELECT COUNT(*) FROM student_activities WHERE activity_id = %s"
            statement.execute(sql, (activity_id,))
            count_row = statement.fetchone()
            current_participants = count_row[0] if count_row else 0

            if current_participants >= max_participants:
                messagebox.showerror("Error", "Activity is full.")
                return

            sql = "INSERT INTO student_activities (student_id, activity_id) VALUES (%s, %s)"
            statement.execute(sql, (student_id, activity_id))
            connection.commit()
            messagebox.showinfo("Success", "Student subscribed to activity.")
            self.root.destroy()
        except mysql.connector.Error as e:
            messagebox.showerror("Error", f"Database error: {e}")
