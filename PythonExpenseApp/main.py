import tkinter as tk
from tkinter import messagebox
from PythonExpenseApp.gui.expense_gui import ExpenseGUI
from PythonExpenseApp.gui.activity_form_gui import ActivityFormGUI
import sys
from PythonExpenseApp.activity import Activity
from PythonExpenseApp.db_connection import DbConnection
import mysql.connector

def show_expense_gui():
    """
    Launches the Expense GUI window.
    """
    root = tk.Tk()
    app = ExpenseGUI(root)
    root.mainloop()

def show_activity_form():
    """
    Launches the Activity Subscription GUI window.
    """
    root = tk.Tk()
    app = ActivityFormGUI(root)
    root.mainloop()

# Main entry point for the application
if __name__ == "__main__":
    # Main menu window
    root = tk.Tk()
    root.title("Main Menu")
    root.geometry("300x150")

    # Label for mode selection
    tk.Label(root, text="Select mode:").pack(pady=10)
    # Button to open Expense GUI
    tk.Button(root, text="Expense GUI", command=lambda: [root.destroy(), show_expense_gui()]).pack(pady=5)
    # Button to open Activity Form GUI
    tk.Button(root, text="Activity Form", command=lambda: [root.destroy(), show_activity_form()]).pack(pady=5)

    root.mainloop()