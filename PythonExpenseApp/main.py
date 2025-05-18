import tkinter as tk
from tkinter import messagebox
from PythonExpenseApp.gui.expense_gui import ExpenseGUI
from PythonExpenseApp.gui.activity_form_gui import ActivityFormGUI
import sys
from PythonExpenseApp.activity import Activity
from PythonExpenseApp.db_connection import DbConnection
import mysql.connector

def show_expense_gui():
    root = tk.Tk()
    app = ExpenseGUI(root)
    root.mainloop()

def show_activity_form():
    root = tk.Tk()
    app = ActivityFormGUI(root)
    root.mainloop()

# Replaces old console approach with a simple GUI
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Main Menu")
    root.geometry("300x150")

    tk.Label(root, text="Select mode:").pack(pady=10)
    tk.Button(root, text="Expense GUI", command=lambda: [root.destroy(), show_expense_gui()]).pack(pady=5)
    tk.Button(root, text="Activity Form", command=lambda: [root.destroy(), show_activity_form()]).pack(pady=5)

    root.mainloop()