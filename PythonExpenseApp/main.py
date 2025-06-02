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
from PythonExpenseApp.activity import Activity
from PythonExpenseApp.db_connection import DbConnection
import mysql.connector
from PIL import Image, ImageTk, ImageDraw, ImageFilter

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

    # Main menu window - Clean rectangular design
    root = tk.Tk()
    root.title("Trip Manager Dashboard")
    root.geometry("1200x800")
    root.resizable(True, True)
    root.configure(bg='#f8fafc')
    
    # Set window icon and properties
    try:
        root.state('zoomed')  # Maximize on Windows
    except:
        pass
    
    # Main container with clean design
    main_container = tk.Frame(root, bg='#ffffff', relief='solid', bd=1)
    main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
    
    # Header section
    header_frame = tk.Frame(main_container, bg='#ffffff', height=100)
    header_frame.pack(fill=tk.X, padx=30, pady=(30, 20))
    header_frame.pack_propagate(False)
    
    # Title and greeting
    title_label = tk.Label(header_frame, text="Trip Manager Dashboard", 
                          font=("Segoe UI", 32, "bold"), bg="#ffffff", fg="#1e293b")
    title_label.pack(anchor='w')
    
    greeting = f"Welcome, {student.name} | Class {getattr(student, 'class_', getattr(student, 'class', ''))}"
    greeting_label = tk.Label(header_frame, text=greeting, 
                             font=("Segoe UI", 14), bg="#ffffff", fg="#64748b")
    greeting_label.pack(anchor='w', pady=(5, 0))
    
    subtitle_label = tk.Label(header_frame, text="Manage your expenses and activities efficiently", 
                             font=("Segoe UI", 16), bg="#ffffff", fg="#64748b")
    subtitle_label.pack(anchor='w', pady=(5, 0))

    # Content area with grid layout
    content_frame = tk.Frame(main_container, bg='#ffffff')
    content_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=20)
    
    # Configure grid
    content_frame.grid_columnconfigure(0, weight=1)
    content_frame.grid_columnconfigure(1, weight=1)
    content_frame.grid_rowconfigure(0, weight=1)

    # Actions section
    actions_frame = tk.LabelFrame(content_frame, text="Quick Actions", 
                                 font=("Segoe UI", 18, "bold"), bg="#ffffff", 
                                 fg="#1e293b", relief='solid', bd=2)
    actions_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10), pady=10)
    
    # Action buttons with clean design
    def create_action_button(parent, text, icon, description, command, bg_color="#3b82f6"):
        btn_frame = tk.Frame(parent, bg="#ffffff", relief='solid', bd=1)
        btn_frame.pack(fill=tk.X, padx=20, pady=15)
        
        # Button content
        btn_content = tk.Frame(btn_frame, bg="#ffffff")
        btn_content.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Icon and text
        icon_label = tk.Label(btn_content, text=icon, font=("Segoe UI", 24), 
                             bg="#ffffff", fg=bg_color)
        icon_label.pack(side=tk.LEFT, padx=(0, 15))
        
        text_frame = tk.Frame(btn_content, bg="#ffffff")
        text_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        title_label = tk.Label(text_frame, text=text, font=("Segoe UI", 16, "bold"), 
                              bg="#ffffff", fg="#1e293b", anchor='w')
        title_label.pack(anchor='w')
        
        desc_label = tk.Label(text_frame, text=description, font=("Segoe UI", 12), 
                             bg="#ffffff", fg="#64748b", anchor='w')
        desc_label.pack(anchor='w')
        
        # Action button
        action_btn = tk.Button(btn_content, text="Open →", font=("Segoe UI", 12, "bold"),
                              bg=bg_color, fg="white", relief='flat', bd=0,
                              activebackground="#2563eb", cursor="hand2",
                              command=command)
        action_btn.pack(side=tk.RIGHT, padx=(15, 0), pady=10)
        
        # Hover effects
        def on_enter(e):
            btn_frame.config(relief='solid', bd=2)
        def on_leave(e):
            btn_frame.config(relief='solid', bd=1)
            
        btn_frame.bind("<Enter>", on_enter)
        btn_frame.bind("<Leave>", on_leave)
    
    create_action_button(actions_frame, "Expense Tracker", "💰", 
                        "Track and manage all trip expenses", 
                        lambda: [root.destroy(), show_expense_gui()], "#3b82f6")
    
    create_action_button(actions_frame, "Activity Manager", "🎯", 
                        "Subscribe to activities and manage schedule", 
                        lambda: [root.destroy(), show_activity_form()], "#059669")

    # Schedule section
    schedule_frame = tk.LabelFrame(content_frame, text="Today's Schedule", 
                                  font=("Segoe UI", 18, "bold"), bg="#ffffff", 
                                  fg="#1e293b", relief='solid', bd=2)
    schedule_frame.grid(row=0, column=1, sticky="nsew", padx=(10, 0), pady=10)
    
    # Schedule listbox
    schedule_container = tk.Frame(schedule_frame, bg="#ffffff")
    schedule_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
    
    # Scrollbar for schedule
    schedule_scrollbar = tk.Scrollbar(schedule_container)
    schedule_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    schedule_list = tk.Listbox(schedule_container, font=("Segoe UI", 12), bg="#ffffff", 
                              fg="#374151", relief='solid', bd=1,
                              yscrollcommand=schedule_scrollbar.set,
                              selectbackground="#dbeafe", selectforeground="#1e40af")
    schedule_list.pack(fill=tk.BOTH, expand=True)
    schedule_scrollbar.config(command=schedule_list.yview)
    
    # Load schedule data
    from datetime import date
    today = date.today().isoformat()
    connection = DbConnection.connect()
    if connection:
        cursor = connection.cursor()
        cursor.execute("SELECT name, start_time, finish_time, location FROM activities WHERE day=%s ORDER BY start_time", (today,))
        activities = cursor.fetchall()
        if not activities:
            schedule_list.insert(tk.END, "📌 No activities scheduled for today")
            schedule_list.insert(tk.END, "")
            schedule_list.insert(tk.END, "✨ Enjoy your free day!")
        else:
            for name, start, finish, location in activities:
                schedule_list.insert(tk.END, f"🕐 {start}:00 - {finish}:00")
                schedule_list.insert(tk.END, f"📍 {name} @ {location}")
                schedule_list.insert(tk.END, "")
        connection.close()
    else:
        schedule_list.insert(tk.END, "❌ Could not load schedule")

    # Status bar
    status_frame = tk.Frame(root, bg='#e5e7eb', height=30)
    status_frame.pack(fill=tk.X, side=tk.BOTTOM)
    status_frame.pack_propagate(False)
    
    status_label = tk.Label(status_frame, text="Trip Manager © 2025 - Ready", 
                           font=("Segoe UI", 10), bg="#e5e7eb", fg="#64748b")
    status_label.pack(side=tk.LEFT, padx=10, pady=5)

    root.mainloop()

# Main entry point for the application
if __name__ == "__main__":
    # Check database connection before starting the GUI
    connection = DbConnection.connect()
    if not connection:
        tk.Tk().withdraw()  # Hide the root window
        messagebox.showerror("Database Error", "Could not connect to the database. Please check your connection settings.")
        sys.exit(1)
    # Show login window first
    root = tk.Tk()
    login = LoginGUI(root, on_login_success)
    root.mainloop()