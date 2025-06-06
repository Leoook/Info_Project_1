import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk, ImageDraw, ImageFilter
from PythonExpenseApp.db_connection import DbConnection
from PythonExpenseApp.gui.expense_gui import ExpenseGUI
from PythonExpenseApp.gui.activity_form_gui import ActivityFormGUI
import datetime

class DashboardGUI:
    def __init__(self, root, student, show_expense_gui_callback, show_activity_form_callback):
        self.root = root
        self.student = student
        self.show_expense_gui_callback = show_expense_gui_callback
        self.show_activity_form_callback = show_activity_form_callback
        self.logged_in_student = student # Keep a reference if needed by other methods

        self.root.title("Trip Manager Dashboard")
        self.root.geometry("1200x800")
        self.root.resizable(True, True)
        self.root.configure(bg='#f8fafc')

        # Set window icon and properties
        try:
            self.root.state('zoomed')  # Maximize on Windows
        except tk.TclError: # Handle cases where 'zoomed' might not be available (e.g. some Linux WMs)
            pass # Or implement alternative like self.root.attributes('-fullscreen', True) if desired

        # Main container with clean design
        main_container = tk.Frame(self.root, bg='#ffffff', relief='solid', bd=1)
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Header section
        header_frame = tk.Frame(main_container, bg='#ffffff', height=100)
        header_frame.pack(fill=tk.X, padx=30, pady=(30, 20))
        header_frame.pack_propagate(False)

        # Title and greeting
        title_label = tk.Label(header_frame, text="Trip Manager Dashboard",
                              font=("Segoe UI", 32, "bold"), bg="#ffffff", fg="#1e293b")
        title_label.pack(anchor='w')

        greeting = f"Welcome, {self.student.name} | Class {getattr(self.student, 'class_', getattr(self.student, 'class', ''))}"
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

        self._create_action_buttons(actions_frame)

        # Schedule section
        schedule_frame = tk.LabelFrame(content_frame, text="Today's Schedule",
                                      font=("Segoe UI", 18, "bold"), bg="#ffffff",
                                      fg="#1e293b", relief='solid', bd=2)
        schedule_frame.grid(row=0, column=1, sticky="nsew", padx=(10, 0), pady=10)

        self._create_schedule_section(schedule_frame)

        # Status bar
        status_frame = tk.Frame(self.root, bg='#e5e7eb', height=30)
        status_frame.pack(fill=tk.X, side=tk.BOTTOM)
        status_frame.pack_propagate(False)

        status_label = tk.Label(status_frame, text="Trip Manager © 2025 - Ready",
                               font=("Segoe UI", 10), bg="#e5e7eb", fg="#64748b")
        status_label.pack(side=tk.LEFT, padx=10, pady=5)

    def _create_action_button(self, parent, text, icon, description, command, bg_color="#3b82f6"):
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

    def _create_action_buttons(self, actions_frame):
        self._create_action_button(actions_frame, "Expense Tracker", "💰",
                                "Track and manage all trip expenses",
                                lambda: [self.root.destroy(), self.show_expense_gui_callback()], "#3b82f6")

        self._create_action_button(actions_frame, "Activity Manager", "🎯",
                                "Subscribe to activities and manage schedule",
                                lambda: [self.root.destroy(), self.show_activity_form_callback()], "#059669")

    def _create_schedule_section(self, schedule_frame):
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
        today = datetime.date.today().isoformat()
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

if __name__ == '__main__':
    # This is for testing the DashboardGUI directly
    # You'll need to mock or provide a student object and callback functions
    class MockStudent:
        def __init__(self, name, class_):
            self.name = name
            self.class_ = class_

    def mock_show_expense():
        print("Show expense GUI (mock)")

    def mock_show_activity():
        print("Show activity form GUI (mock)")

    # Example:
    # Check database connection before starting the GUI
    # This part is similar to main.py's __main__ block
    # You might want to centralize DB check if running GUIs independently
    connection = DbConnection.connect()
    if not connection:
        root = tk.Tk()
        root.withdraw()  # Hide the root window
        messagebox.showerror("Database Error", "Could not connect to the database. Please check your connection settings.")
        sys.exit(1) # Make sure to import sys if you use sys.exit

    test_student = MockStudent("Test User", "6A")
    main_root = tk.Tk()
    app = DashboardGUI(main_root, test_student, mock_show_expense, mock_show_activity)
    main_root.mainloop()
