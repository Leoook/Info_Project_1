import tkinter as tk
from tkinter import messagebox
import mysql.connector
from PythonExpenseApp.db_connection import DbConnection
from PythonExpenseApp.expense import Expense

class ExpenseGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Expense Tracker")
        self.root.geometry("600x300")

        self.expenses = []

        # Input Panel
        input_frame = tk.Frame(self.root)
        input_frame.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

        tk.Label(input_frame, text="Amount:").grid(row=0, column=0, padx=5, pady=2)
        self.amount_entry = tk.Entry(input_frame)
        self.amount_entry.grid(row=0, column=1, padx=5, pady=2)

        tk.Label(input_frame, text="Description:").grid(row=0, column=2, padx=5, pady=2)
        self.description_entry = tk.Entry(input_frame)
        self.description_entry.grid(row=0, column=3, padx=5, pady=2)
        tk.Label(input_frame, text="Student Name:").grid(row=0, column=0, padx=5, pady=2)
        self.name_entry = tk.Entry(input_frame)
        self.name_entry.grid(row=0, column=1, padx=5, pady=2)

        tk.Label(input_frame, text="Surname:").grid(row=0, column=2, padx=5, pady=2)
        self.surname_var = tk.StringVar()
        self.surname_entry = tk.Entry(input_frame, textvariable=self.surname_var, state="readonly")
        self.surname_entry.grid(row=0, column=3, padx=5, pady=2)

        tk.Button(input_frame, text="Search Student", command=self.search_student).grid(row=0, column=6, padx=5, pady=2)
        add_button = tk.Button(input_frame, text="Add Expense", command=self.add_expense)
        add_button.grid(row=0, column=4, padx=5, pady=2)

        # Text area for expenses
        self.expense_list_area = tk.Text(self.root, state="normal")
        self.expense_list_area.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    def search_student(self):
        name = self.name_entry.get()
        if not name.strip():
            messagebox.showerror("Error", "Please enter a student name.")
            return

        connection = DbConnection.connect()
        if connection:
            try:
                sql = "SELECT id, surname FROM students WHERE name = %s LIMIT 1"
                statement = connection.cursor()
                statement.execute(sql, (name,))
                result = statement.fetchone()
                if result:
                    student_id, surname = result
                    self.student_id_var.set(student_id)
                    self.surname_var.set(surname)
                else:
                    messagebox.showinfo("Not found", "No student found with that name.")
            except mysql.connector.Error as e:
                messagebox.showerror("Error", f"Database error: {e}")

    def add_expense(self):
        amount_text = self.amount_entry.get()
        description = self.description_entry.get()
        if amount_text and description:
            try:
                amount = float(amount_text)
                expense = Expense(amount, description)
                self.expenses.append(expense)
                expense.save_to_database()
                self.update_expense_list()
                self.amount_entry.delete(0, tk.END)
                self.description_entry.delete(0, tk.END)
            except ValueError:
                messagebox.showerror("Error", "Amount must be a number.")
        else:
            messagebox.showerror("Error", "Please enter both amount and description.")

    def update_expense_list(self):
        self.expense_list_area.config(state="normal")
        self.expense_list_area.delete("1.0", tk.END)
        for exp in self.expenses:
            self.expense_list_area.insert(tk.END, str(exp) + "\n")
        self.expense_list_area.config(state="disabled")