import sys
import os
_main_file_directory = os.path.dirname(os.path.abspath(__file__))
_project_root_directory = os.path.dirname(_main_file_directory)
if _project_root_directory not in sys.path:
    sys.path.insert(0, _project_root_directory)

import tkinter as tk
from tkinter import messagebox
from PythonExpenseApp.gui.expense_gui import ExpenseGUI
from PythonExpenseApp.gui.activity_form_gui import ActivityFormGUI
from PythonExpenseApp.gui.login_gui import LoginGUI
from PythonExpenseApp.gui.dashboard_gui import DashboardGUI
from PythonExpenseApp.db_connection import DbConnection

# Global variable to store the logged-in student
logged_in_student = None

def show_main_dashboard():
    """Show the main dashboard"""
    global logged_in_student
    if logged_in_student:
        on_login_success(logged_in_student)
    else:
        # If no logged in student, show login
        root = tk.Tk()
        login = LoginGUI(root, on_login_success)
        root.mainloop()

def show_expense_gui():
    """
    Launches the Expense GUI window.
    """
    root = tk.Tk()
    app = ExpenseGUI(root, logged_in_student, show_main_dashboard)
    root.mainloop()

def show_activity_form():
    """
    Launches the Activity Subscription GUI window.
    """
    global logged_in_student
    root = tk.Tk()
    app = ActivityFormGUI(root, logged_in_student, show_main_dashboard)
    root.mainloop()

def on_login_success(student):
    global logged_in_student
    logged_in_student = student

    # Main menu window - Now handled by DashboardGUI
    root = tk.Tk()
    # Pass the callbacks for showing other GUIs
    dashboard = DashboardGUI(root, student, show_expense_gui, show_activity_form)
    root.mainloop()

# Main entry point for the application
if __name__ == "__main__":
    # Check database connection before starting the GUI
    connection = DbConnection.connect()
    if not connection:
        temp_root = tk.Tk()
        temp_root.withdraw()
        messagebox.showerror("Database Error", "Could not connect to the database. Please check your connection settings.", parent=temp_root)
        temp_root.destroy()
        sys.exit(1)
    # Show login window first
    root = tk.Tk()
    login = LoginGUI(root, on_login_success)
    root.mainloop()