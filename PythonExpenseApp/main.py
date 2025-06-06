import sys
import os
# _main_file_directory: The directory where this main.py file is located.
_main_file_directory = os.path.dirname(os.path.abspath(__file__))
# _project_root_directory: The root directory of the project, one level above main.py.
_project_root_directory = os.path.dirname(_main_file_directory)
# Ensure the project root directory is in sys.path for module imports.
if _project_root_directory not in sys.path:
    sys.path.insert(0, _project_root_directory)

import tkinter as tk
from tkinter import messagebox
from gui.expense_gui import ExpenseGUI
from gui.activity_form_gui import ActivityFormGUI
from gui.login_gui import LoginGUI
from gui.dashboard_gui import DashboardGUI
from gui.teacher_dashboard import TeacherDashboard
from db_connection import DbConnection

# Global variable to store the currently logged-in student object.
# This variable is updated after a successful login and is used throughout the session.
logged_in_student = None

def show_main_dashboard():
    """
    Displays the main dashboard window.
    If a student is already logged in, it calls on_login_success to show the appropriate dashboard.
    Otherwise, it launches the login window.
    """
    global logged_in_student
    if logged_in_student:
        on_login_success(logged_in_student)
    else:
        # If no logged in student, show login window.
        root = tk.Tk()
        login = LoginGUI(root, on_login_success)
        root.mainloop()

def show_expense_gui():
    """
    Launches the Expense GUI window for the logged-in student.
    This window allows the student to manage and view their expenses.
    """
    root = tk.Tk()
    app = ExpenseGUI(root, logged_in_student, show_main_dashboard)
    root.mainloop()

def show_activity_form():
    """
    Launches the Activity Subscription GUI window for the logged-in student.
    This window allows the student to subscribe to or manage activities.
    """
    global logged_in_student
    root = tk.Tk()
    app = ActivityFormGUI(root, logged_in_student, show_main_dashboard)
    root.mainloop()

def on_login_success(student):
    """
    Callback function called after a successful login.
    Sets the global logged_in_student variable and launches the appropriate dashboard
    based on the user's role (student or teacher).

    :param student: Student object - The student who has logged in.
    """
    global logged_in_student
    logged_in_student = student

    # Check if user is a teacher and redirect to teacher dashboard
    if hasattr(student, 'role') and student.role == 'teacher':
        # Launch the teacher dashboard GUI for users with the 'teacher' role.
        root = tk.Tk()
        teacher_dashboard = TeacherDashboard(root, student, show_main_dashboard)
        root.mainloop()
    else:
        # Launch the regular student dashboard GUI for students.
        root = tk.Tk()
        # Pass the callbacks for showing other GUIs (expenses, activities).
        dashboard = DashboardGUI(root, student, show_expense_gui, show_activity_form)
        root.mainloop()

# Main entry point for the application
if __name__ == "__main__":
    # Check database connection before starting the GUI.
    # If the connection fails, show an error message and exit.
    connection = DbConnection.connect()
    if not connection:
        temp_root = tk.Tk()
        temp_root.withdraw()
        messagebox.showerror(
            "Database Error",
            "Could not connect to the database. Please check your connection settings.",
            parent=temp_root
        )
        temp_root.destroy()
        sys.exit(1)
    # Show login window first.
    root = tk.Tk()
    login = LoginGUI(root, on_login_success)
    root.mainloop()

# No changes needed in this file based on the current request,
# as the student object passed around will implicitly carry the role.
# The logic for handling the role is within the individual GUI classes.