import tkinter as tk
from tkinter import ttk, messagebox
from db_connection import DbConnection
import datetime
from collections import defaultdict


class TeacherDashboard:
    def __init__(self, root, teacher, main_dashboard_callback):
        self.root = root
        self.teacher = teacher
        self.main_dashboard_callback = main_dashboard_callback
        
        self.root.title("Teacher Dashboard - Trip Manager")
        self.root.geometry("1400x900")
        self.root.configure(bg='#f8fafc')
        
        # Try to maximize window
        try:
            self.root.state('zoomed')
        except tk.TclError:
            pass
            
        self.setup_ui()
        self.load_data()

    def setup_ui(self):
        # Main container
        main_container = tk.Frame(self.root, bg='#ffffff', relief='solid', bd=1)
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Header section
        self.create_header(main_container)
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(main_container)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Create tabs
        self.create_activities_tab()
        self.create_participants_tab()
        self.create_schedule_tab()
        self.create_analytics_tab()
        
        # Footer with navigation
        self.create_footer(main_container)

    def create_header(self, parent):
        header_frame = tk.Frame(parent, bg='#ffffff', height=100)
        header_frame.pack(fill=tk.X, padx=30, pady=(30, 20))
        header_frame.pack_propagate(False)

        # Title
        title_label = tk.Label(header_frame, text="Teacher Dashboard",
                              font=("Segoe UI", 32, "bold"), bg="#ffffff", fg="#1e293b")
        title_label.pack(anchor='w')

        # Teacher info
        teacher_info = f"Teacher: {self.teacher.name} {getattr(self.teacher, 'surname', '')}"
        info_label = tk.Label(header_frame, text=teacher_info,
                             font=("Segoe UI", 16), bg="#ffffff", fg="#64748b")
        info_label.pack(anchor='w', pady=(5, 0))

        # Quick stats
        stats_frame = tk.Frame(header_frame, bg="#ffffff")
        stats_frame.pack(anchor='w', pady=(10, 0))
        
        self.stats_labels = {}
        
    def create_activities_tab(self):
        # Activities tab
        activities_frame = ttk.Frame(self.notebook)
        self.notebook.add(activities_frame, text="📋 Activities Overview")
        
        # Search and filter frame
        search_frame = tk.Frame(activities_frame, bg='#f8fafc')
        search_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Label(search_frame, text="Search Activities:", font=("Segoe UI", 12, "bold"),
                bg='#f8fafc').pack(side=tk.LEFT, padx=(0, 10))
        
        self.activity_search_var = tk.StringVar()
        self.activity_search_var.trace('w', self.filter_activities)
        search_entry = tk.Entry(search_frame, textvariable=self.activity_search_var,
                               font=("Segoe UI", 11), width=30)
        search_entry.pack(side=tk.LEFT, padx=(0, 20))
        
        # Day filter
        tk.Label(search_frame, text="Filter by Day:", font=("Segoe UI", 12, "bold"),
                bg='#f8fafc').pack(side=tk.LEFT, padx=(0, 10))
        
        self.day_filter_var = tk.StringVar(value="All Days")
        self.day_filter = ttk.Combobox(search_frame, textvariable=self.day_filter_var,
                                      state="readonly", width=15)
        self.day_filter.pack(side=tk.LEFT)
        self.day_filter.bind('<<ComboboxSelected>>', self.filter_activities)
        
        # Activities treeview
        tree_frame = tk.Frame(activities_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(tree_frame, orient="vertical")
        h_scrollbar = ttk.Scrollbar(tree_frame, orient="horizontal")
        
        self.activities_tree = ttk.Treeview(tree_frame, 
                                           columns=("day", "time", "location", "participants", "max_participants", "description"),
                                           show="tree headings",
                                           yscrollcommand=v_scrollbar.set,
                                           xscrollcommand=h_scrollbar.set)
        
        # Configure scrollbars
        v_scrollbar.config(command=self.activities_tree.yview)
        h_scrollbar.config(command=self.activities_tree.xview)
        
        # Grid layout for treeview and scrollbars
        self.activities_tree.grid(row=0, column=0, sticky="nsew")
        v_scrollbar.grid(row=0, column=1, sticky="ns")
        h_scrollbar.grid(row=1, column=0, sticky="ew")
        
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)
        
        # Configure columns
        self.activities_tree.heading("#0", text="Activity Name", anchor="w")
        self.activities_tree.heading("day", text="Day", anchor="center")
        self.activities_tree.heading("time", text="Time", anchor="center")
        self.activities_tree.heading("location", text="Location", anchor="w")
        self.activities_tree.heading("participants", text="Enrolled", anchor="center")
        self.activities_tree.heading("max_participants", text="Max", anchor="center")
        self.activities_tree.heading("description", text="Description", anchor="w")
        
        # Configure column widths
        self.activities_tree.column("#0", width=200, minwidth=150)
        self.activities_tree.column("day", width=100, minwidth=80)
        self.activities_tree.column("time", width=120, minwidth=100)
        self.activities_tree.column("location", width=150, minwidth=120)
        self.activities_tree.column("participants", width=80, minwidth=60)
        self.activities_tree.column("max_participants", width=60, minwidth=50)
        self.activities_tree.column("description", width=300, minwidth=200)
        
        # Bind double-click to show participants
        self.activities_tree.bind("<Double-1>", self.show_activity_participants)

    def create_participants_tab(self):
        # Participants tab
        participants_frame = ttk.Frame(self.notebook)
        self.notebook.add(participants_frame, text="👥 Students & Enrollment")
        
        # Search frame
        search_frame = tk.Frame(participants_frame, bg='#f8fafc')
        search_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Label(search_frame, text="Search Students:", font=("Segoe UI", 12, "bold"),
                bg='#f8fafc').pack(side=tk.LEFT, padx=(0, 10))
        
        self.student_search_var = tk.StringVar()
        self.student_search_var.trace('w', self.filter_students)
        search_entry = tk.Entry(search_frame, textvariable=self.student_search_var,
                               font=("Segoe UI", 11), width=30)
        search_entry.pack(side=tk.LEFT, padx=(0, 20))
        
        # Class filter
        tk.Label(search_frame, text="Filter by Class:", font=("Segoe UI", 12, "bold"),
                bg='#f8fafc').pack(side=tk.LEFT, padx=(0, 10))
        
        self.class_filter_var = tk.StringVar(value="All Classes")
        self.class_filter = ttk.Combobox(search_frame, textvariable=self.class_filter_var,
                                        state="readonly", width=15)
        self.class_filter.pack(side=tk.LEFT)
        self.class_filter.bind('<<ComboboxSelected>>', self.filter_students)
        
        # Students treeview
        tree_frame = tk.Frame(participants_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        v_scrollbar = ttk.Scrollbar(tree_frame, orient="vertical")
        h_scrollbar = ttk.Scrollbar(tree_frame, orient="horizontal")
        
        self.students_tree = ttk.Treeview(tree_frame,
                                         columns=("class", "email", "age", "activities_count", "special_needs"),
                                         show="tree headings",
                                         yscrollcommand=v_scrollbar.set,
                                         xscrollcommand=h_scrollbar.set)
        
        v_scrollbar.config(command=self.students_tree.yview)
        h_scrollbar.config(command=self.students_tree.xview)
        
        self.students_tree.grid(row=0, column=0, sticky="nsew")
        v_scrollbar.grid(row=0, column=1, sticky="ns")
        h_scrollbar.grid(row=1, column=0, sticky="ew")
        
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)
        
        # Configure columns
        self.students_tree.heading("#0", text="Student Name", anchor="w")
        self.students_tree.heading("class", text="Class", anchor="center")
        self.students_tree.heading("email", text="Email", anchor="w")
        self.students_tree.heading("age", text="Age", anchor="center")
        self.students_tree.heading("activities_count", text="Activities", anchor="center")
        self.students_tree.heading("special_needs", text="Special Needs", anchor="w")
        
        # Configure column widths
        self.students_tree.column("#0", width=200, minwidth=150)
        self.students_tree.column("class", width=80, minwidth=60)
        self.students_tree.column("email", width=200, minwidth=150)
        self.students_tree.column("age", width=60, minwidth=50)
        self.students_tree.column("activities_count", width=80, minwidth=60)
        self.students_tree.column("special_needs", width=300, minwidth=200)
        
        # Bind double-click to show student activities
        self.students_tree.bind("<Double-1>", self.show_student_activities)

    def create_schedule_tab(self):
        # Daily schedule tab
        schedule_frame = ttk.Frame(self.notebook)
        self.notebook.add(schedule_frame, text="📅 Daily Schedule")
        
        # Date selection frame
        date_frame = tk.Frame(schedule_frame, bg='#f8fafc')
        date_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Label(date_frame, text="Select Date:", font=("Segoe UI", 12, "bold"),
                bg='#f8fafc').pack(side=tk.LEFT, padx=(0, 10))
        
        self.selected_date_var = tk.StringVar()
        self.date_combo = ttk.Combobox(date_frame, textvariable=self.selected_date_var,
                                      state="readonly", width=20)
        self.date_combo.pack(side=tk.LEFT, padx=(0, 20))
        self.date_combo.bind('<<ComboboxSelected>>', self.load_daily_schedule)
        
        # Today button
        today_btn = tk.Button(date_frame, text="Today", font=("Segoe UI", 10, "bold"),
                             bg="#3b82f6", fg="white", relief='flat',
                             command=self.select_today)
        today_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Schedule display frame
        self.schedule_display_frame = tk.Frame(schedule_frame, bg='#ffffff')
        self.schedule_display_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def create_analytics_tab(self):
        # Analytics tab
        analytics_frame = ttk.Frame(self.notebook)
        self.notebook.add(analytics_frame, text="📊 Analytics")
        
        # Create analytics widgets
        self.create_analytics_widgets(analytics_frame)

    def create_analytics_widgets(self, parent):
        # Statistics frame
        stats_frame = tk.LabelFrame(parent, text="Trip Statistics", font=("Segoe UI", 14, "bold"),
                                   bg='#ffffff', fg='#1e293b', relief='solid', bd=2)
        stats_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Create grid for statistics
        stats_grid = tk.Frame(stats_frame, bg='#ffffff')
        stats_grid.pack(fill=tk.X, padx=20, pady=20)
        
        self.stats_widgets = {}
        
        # Popular activities frame
        popular_frame = tk.LabelFrame(parent, text="Most Popular Activities", 
                                     font=("Segoe UI", 14, "bold"),
                                     bg='#ffffff', fg='#1e293b', relief='solid', bd=2)
        popular_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Popular activities listbox
        popular_container = tk.Frame(popular_frame, bg='#ffffff')
        popular_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        scrollbar = tk.Scrollbar(popular_container)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.popular_activities_list = tk.Listbox(popular_container, 
                                                 font=("Segoe UI", 11),
                                                 bg='#ffffff', fg='#374151',
                                                 yscrollcommand=scrollbar.set)
        self.popular_activities_list.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.popular_activities_list.yview)

    def create_footer(self, parent):
        footer_frame = tk.Frame(parent, bg='#e5e7eb', height=60)
        footer_frame.pack(fill=tk.X, side=tk.BOTTOM)
        footer_frame.pack_propagate(False)
        
        # Back button
        back_btn = tk.Button(footer_frame, text="← Back to Main Dashboard",
                            font=("Segoe UI", 12, "bold"), bg="#6b7280", fg="white",
                            relief='flat', bd=0, activebackground="#4b5563",
                            cursor="hand2", command=self.go_back)
        back_btn.pack(side=tk.LEFT, padx=20, pady=15)
        
        # Status label
        self.status_label = tk.Label(footer_frame, text="Ready",
                                    font=("Segoe UI", 10), bg="#e5e7eb", fg="#64748b")
        self.status_label.pack(side=tk.RIGHT, padx=20, pady=15)

    def load_data(self):
        """Load all data from database"""
        self.update_status("Loading data...")
        
        connection = DbConnection.connect()
        if not connection:
            messagebox.showerror("Database Error", "Could not connect to database")
            return
            
        try:
            cursor = connection.cursor()
            # Load all activities with participant counts
            cursor.execute("""
                SELECT a.id, a.name, a.day, a.start_time, a.finish_time, 
                       a.location, a.max_participants, a.description,
                       (SELECT COUNT(*) FROM student_activities sa WHERE sa.activity_id = a.id) as participant_count
                FROM activities a
                ORDER BY a.day, a.start_time
            """)
            self.activities_data = cursor.fetchall()
            
            # Load all students with activity counts
            cursor.execute("""
                SELECT s.id, s.name, s.surname, s.class, s.email, s.age, 
                       s.special_needs, 
                       (SELECT COUNT(*) FROM student_activities sa WHERE sa.student_id = s.id) as activity_count
                FROM students s
                WHERE s.role = 'student'
                ORDER BY s.class, s.surname, s.name
            """)
            self.students_data = cursor.fetchall()
            
            # Load unique days and classes for filters
            cursor.execute("SELECT DISTINCT day FROM activities ORDER BY day")
            self.unique_days = [row[0] for row in cursor.fetchall()]
            
            cursor.execute("SELECT DISTINCT class FROM students WHERE role = 'student' ORDER BY class")
            self.unique_classes = [row[0] for row in cursor.fetchall()]
            
            connection.close()
            
            # Populate UI
            self.populate_activities()
            self.populate_students()
            self.setup_filters()
            self.load_analytics()
            self.setup_schedule_dates()
            self.update_quick_stats()
            
            self.update_status("Data loaded successfully")
            
        except Exception as e:
            connection.close()
            messagebox.showerror("Error", f"Error loading data: {str(e)}")
            self.update_status("Error loading data")

    def populate_activities(self):
        """Populate activities treeview"""
        # Clear existing items
        for item in self.activities_tree.get_children():
            self.activities_tree.delete(item)
        for activity in self.activities_data:
            activity_id, name, day, start_time, finish_time, location, max_participants, description, participant_count = activity
            start_hour = start_time // 60
            start_min = start_time % 60
            finish_hour = finish_time // 60
            finish_min = finish_time % 60
            time_str = f"{start_hour:02d}:{start_min:02d} - {finish_hour:02d}:{finish_min:02d}"
            max_str = str(max_participants) if max_participants else "∞"
            day_str = day.strftime("%Y-%m-%d") if hasattr(day, 'strftime') else str(day)
            self.activities_tree.insert("", "end", text=name,
                                       values=(day_str, time_str, location, 
                                              participant_count, max_str, description or ""))

    def populate_students(self):
        """Populate students treeview"""
        # Clear existing items
        for item in self.students_tree.get_children():
            self.students_tree.delete(item)
        for student in self.students_data:
            student_id, name, surname, class_name, email, age, special_needs, activity_count = student
            full_name = f"{name} {surname}"
            age_str = str(age) if age else "N/A"
            special_needs_str = special_needs or "None"
            self.students_tree.insert("", "end", text=full_name,
                                     values=(class_name, email, age_str, 
                                            activity_count, special_needs_str))

    def setup_filters(self):
        """Setup filter comboboxes"""
        # Day filter
        day_values = ["All Days"] + [day.strftime("%Y-%m-%d") for day in self.unique_days]
        self.day_filter['values'] = day_values
        
        # Class filter  
        class_values = ["All Classes"] + self.unique_classes
        self.class_filter['values'] = class_values

    def setup_schedule_dates(self):
        """Setup date selection for schedule"""
        date_values = [day.strftime("%Y-%m-%d") for day in self.unique_days]
        self.date_combo['values'] = date_values
        
        # Set today as default if available
        today = datetime.date.today().strftime("%Y-%m-%d")
        if today in date_values:
            self.selected_date_var.set(today)
            self.load_daily_schedule()
        elif date_values:
            self.selected_date_var.set(date_values[0])
            self.load_daily_schedule()

    def filter_activities(self, *args):
        """Filter activities based on search and day filter"""
        search_term = self.activity_search_var.get().lower()
        day_filter = self.day_filter_var.get()
        
        # Clear existing items
        for item in self.activities_tree.get_children():
            self.activities_tree.delete(item)
            
        for activity in self.activities_data:
            activity_id, name, day, start_time, finish_time, location, max_participants, description, participant_count = activity
            
            # Check search term
            if search_term and search_term not in name.lower() and search_term not in location.lower():
                continue
                
            # Check day filter
            day_str = day.strftime("%Y-%m-%d") if day else "N/A"
            if day_filter != "All Days" and day_filter != day_str:
                continue
                
            # Add item
            start_hour = start_time // 60
            start_min = start_time % 60
            finish_hour = finish_time // 60
            finish_min = finish_time % 60
            time_str = f"{start_hour:02d}:{start_min:02d} - {finish_hour:02d}:{finish_min:02d}"
            
            max_str = str(max_participants) if max_participants else "∞"
            
            self.activities_tree.insert("", "end", text=name,
                                       values=(day_str, time_str, location,
                                              participant_count, max_str, description or ""))

    def filter_students(self, *args):
        """Filter students based on search and class filter"""
        search_term = self.student_search_var.get().lower()
        class_filter = self.class_filter_var.get()
        
        # Clear existing items
        for item in self.students_tree.get_children():
            self.students_tree.delete(item)
            
        for student in self.students_data:
            student_id, name, surname, class_name, email, age, special_needs, activity_count = student
            
            full_name = f"{name} {surname}"
            
            # Check search term
            if search_term and (search_term not in full_name.lower() and 
                               search_term not in email.lower()):
                continue
                
            # Check class filter
            if class_filter != "All Classes" and class_filter != class_name:
                continue
                
            # Add item
            age_str = str(age) if age else "N/A"
            special_needs_str = special_needs or "None"
            
            self.students_tree.insert("", "end", text=full_name,
                                     values=(class_name, email, age_str,
                                            activity_count, special_needs_str))

    def show_activity_participants(self, event):
        """Show participants for selected activity"""
        selection = self.activities_tree.selection()
        if not selection:
            return
            
        item = selection[0]
        activity_name = self.activities_tree.item(item, "text")
        
        # Find activity in data
        activity_data = None
        for activity in self.activities_data:
            if activity[1] == activity_name:  # name is at index 1
                activity_data = activity
                break
                
        if not activity_data:
            return
            
        # Get participants from database
        connection = DbConnection.connect()
        if not connection:
            return
            
        try:
            cursor = connection.cursor()
            cursor.execute("""
                SELECT s.name, s.surname, s.class, s.email
                FROM students s
                JOIN student_activities sa ON s.id = sa.student_id
                WHERE sa.activity_id = %s
                ORDER BY s.class, s.surname, s.name
            """, (activity_data[0],))  # activity_id is at index 0
            
            participants = cursor.fetchall()
            connection.close()
            
            # Show participants window
            self.show_participants_window(activity_name, participants)
            
        except Exception as e:
            connection.close()
            messagebox.showerror("Error", f"Error loading participants: {str(e)}")

    def show_student_activities(self, event):
        """Show activities for selected student"""
        selection = self.students_tree.selection()
        if not selection:
            return
            
        item = selection[0]
        student_name = self.students_tree.item(item, "text")
        
        # Find student in data
        student_data = None
        for student in self.students_data:
            full_name = f"{student[1]} {student[2]}"  # name and surname
            if full_name == student_name:
                student_data = student
                break
                
        if not student_data:
            return
            
        # Get activities from database
        connection = DbConnection.connect()
        if not connection:
            return
            
        try:
            cursor = connection.cursor()
            cursor.execute("""
                SELECT a.name, a.day, a.start_time, a.finish_time, a.location
                FROM activities a
                JOIN student_activities sa ON a.id = sa.activity_id
                WHERE sa.student_id = %s
                ORDER BY a.day, a.start_time
            """, (student_data[0],))  # student_id is at index 0
            
            activities = cursor.fetchall()
            connection.close()
            
            # Show activities window
            self.show_student_activities_window(student_name, activities)
            
        except Exception as e:
            connection.close()
            messagebox.showerror("Error", f"Error loading student activities: {str(e)}")

    def show_participants_window(self, activity_name, participants):
        """Show participants in a popup window"""
        popup = tk.Toplevel(self.root)
        popup.title(f"Participants - {activity_name}")
        popup.geometry("600x400")
        popup.configure(bg='#ffffff')
        
        # Header
        header_label = tk.Label(popup, text=f"Participants in: {activity_name}",
                               font=("Segoe UI", 16, "bold"), bg='#ffffff', fg='#1e293b')
        header_label.pack(pady=20)
        
        # Participants list
        frame = tk.Frame(popup, bg='#ffffff')
        frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        scrollbar = tk.Scrollbar(frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        participants_list = tk.Listbox(frame, font=("Segoe UI", 11),
                                      yscrollcommand=scrollbar.set)
        participants_list.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=participants_list.yview)
        
        if participants:
            for name, surname, class_name, email in participants:
                participants_list.insert(tk.END, f"{name} {surname} ({class_name}) - {email}")
        else:
            participants_list.insert(tk.END, "No participants enrolled")
            
        # Close button
        close_btn = tk.Button(popup, text="Close", font=("Segoe UI", 12),
                             bg='#6b7280', fg='white', command=popup.destroy)
        close_btn.pack(pady=20)

    def show_student_activities_window(self, student_name, activities):
        """Show student activities in a popup window"""
        popup = tk.Toplevel(self.root)
        popup.title(f"Activities - {student_name}")
        popup.geometry("700x400")
        popup.configure(bg='#ffffff')
        
        # Header
        header_label = tk.Label(popup, text=f"Activities for: {student_name}",
                               font=("Segoe UI", 16, "bold"), bg='#ffffff', fg='#1e293b')
        header_label.pack(pady=20)
        
        # Activities list
        frame = tk.Frame(popup, bg='#ffffff')
        frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        scrollbar = tk.Scrollbar(frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        activities_list = tk.Listbox(frame, font=("Segoe UI", 11),
                                    yscrollcommand=scrollbar.set)
        activities_list.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=activities_list.yview)
        
        if activities:
            for name, day, start_time, finish_time, location in activities:
                start_hour = start_time // 60
                start_min = start_time % 60
                finish_hour = finish_time // 60
                finish_min = finish_time % 60
                time_str = f"{start_hour:02d}:{start_min:02d} - {finish_hour:02d}:{finish_min:02d}"
                day_str = day.strftime("%Y-%m-%d")
                
                activities_list.insert(tk.END, f"{name} | {day_str} {time_str} | {location}")
        else:
            activities_list.insert(tk.END, "No activities enrolled")
            
        # Close button
        close_btn = tk.Button(popup, text="Close", font=("Segoe UI", 12),
                             bg='#6b7280', fg='white', command=popup.destroy)
        close_btn.pack(pady=20)

    def load_daily_schedule(self, event=None):
        """Load schedule for selected date"""
        selected_date = self.selected_date_var.get()
        if not selected_date:
            return
            
        # Clear existing schedule
        for widget in self.schedule_display_frame.winfo_children():
            widget.destroy()
            
        # Get activities for selected date
        connection = DbConnection.connect()
        if not connection:
            return
            
        try:
            cursor = connection.cursor()
            cursor.execute("""
                SELECT a.name, a.start_time, a.finish_time, a.location, a.description,
                       COUNT(sa.student_id) as participant_count, a.max_participants
                FROM activities a
                LEFT JOIN student_activities sa ON a.id = sa.activity_id
                WHERE a.day = %s
                GROUP BY a.id
                ORDER BY a.start_time
            """, (selected_date,))
            
            daily_activities = cursor.fetchall()
            connection.close()
            
            if not daily_activities:
                no_activities_label = tk.Label(self.schedule_display_frame,
                                              text="No activities scheduled for this date",
                                              font=("Segoe UI", 16), bg='#ffffff', fg='#64748b')
                no_activities_label.pack(expand=True)
                return
                
            # Create schedule display
            canvas = tk.Canvas(self.schedule_display_frame, bg='#ffffff')
            scrollbar = ttk.Scrollbar(self.schedule_display_frame, orient="vertical", command=canvas.yview)
            scrollable_frame = ttk.Frame(canvas)
            
            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
            )
            
            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)
            
            # Add activities to schedule
            for i, activity in enumerate(daily_activities):
                name, start_time, finish_time, location, description, participant_count, max_participants = activity
                
                # Create activity card
                card_frame = tk.Frame(scrollable_frame, bg='#f8fafc', relief='solid', bd=1)
                card_frame.pack(fill=tk.X, padx=10, pady=5)
                
                # Time and title
                start_hour = start_time // 60
                start_min = start_time % 60
                finish_hour = finish_time // 60
                finish_min = finish_time % 60
                time_str = f"{start_hour:02d}:{start_min:02d} - {finish_hour:02d}:{finish_min:02d}"
                
                header_frame = tk.Frame(card_frame, bg='#f8fafc')
                header_frame.pack(fill=tk.X, padx=15, pady=10)
                
                time_label = tk.Label(header_frame, text=time_str,
                                     font=("Segoe UI", 14, "bold"), bg='#f8fafc', fg='#3b82f6')
                time_label.pack(side=tk.LEFT)
                
                title_label = tk.Label(header_frame, text=name,
                                      font=("Segoe UI", 16, "bold"), bg='#f8fafc', fg='#1e293b')
                title_label.pack(side=tk.LEFT, padx=(20, 0))
                
                # Participants count
                max_str = str(max_participants) if max_participants else "∞"
                participants_label = tk.Label(header_frame, text=f"👥 {participant_count}/{max_str}",
                                             font=("Segoe UI", 12), bg='#f8fafc', fg='#059669')
                participants_label.pack(side=tk.RIGHT)
                
                # Location and description
                details_frame = tk.Frame(card_frame, bg='#f8fafc')
                details_frame.pack(fill=tk.X, padx=15, pady=(0, 10))
                
                location_label = tk.Label(details_frame, text=f"📍 {location}",
                                         font=("Segoe UI", 12), bg='#f8fafc', fg='#64748b')
                location_label.pack(anchor='w')
                
                if description:
                    desc_label = tk.Label(details_frame, text=f"ℹ️ {description}",
                                         font=("Segoe UI", 11), bg='#f8fafc', fg='#64748b',
                                         wraplength=600, justify='left')
                    desc_label.pack(anchor='w', pady=(5, 0))
            
            canvas.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")
            
        except Exception as e:
            connection.close()
            error_label = tk.Label(self.schedule_display_frame,
                                  text=f"Error loading schedule: {str(e)}",
                                  font=("Segoe UI", 12), bg='#ffffff', fg='#dc2626')
            error_label.pack(expand=True)

    def select_today(self):
        """Select today's date in schedule"""
        today = datetime.date.today().strftime("%Y-%m-%d")
        if today in self.date_combo['values']:
            self.selected_date_var.set(today)
            self.load_daily_schedule()

    def load_analytics(self):
        """Load analytics data"""
        connection = DbConnection.connect()
        if not connection:
            return
            
        try:
            cursor = connection.cursor()
            
            # Get popular activities
            cursor.execute("""
                SELECT a.name, COUNT(sa.student_id) as participant_count
                FROM activities a
                LEFT JOIN student_activities sa ON a.id = sa.activity_id
                GROUP BY a.id
                ORDER BY participant_count DESC, a.name
                LIMIT 10
            """)
            
            popular_activities = cursor.fetchall()
            
            # Clear and populate popular activities list
            self.popular_activities_list.delete(0, tk.END)
            for i, (name, count) in enumerate(popular_activities, 1):
                self.popular_activities_list.insert(tk.END, f"{i}. {name} ({count} participants)")
                
            connection.close()
            
        except Exception as e:
            connection.close()
            self.popular_activities_list.delete(0, tk.END)
            self.popular_activities_list.insert(tk.END, f"Error loading analytics: {str(e)}")

    def update_quick_stats(self):
        """Update quick statistics in header"""
        total_activities = len(self.activities_data)
        total_students = len(self.students_data)
        
        # Calculate total enrollments
        total_enrollments = sum(activity[8] for activity in self.activities_data)  # participant_count
        
        # Create stats if not exists
        if not hasattr(self, 'stats_frame'):
            self.stats_frame = tk.Frame(self.root.children[list(self.root.children.keys())[0]], bg="#ffffff")
            
        stats_text = f"📋 {total_activities} Activities  |  👥 {total_students} Students  |  ✅ {total_enrollments} Total Enrollments"
        
        # Remove old stats if exists
        for child in self.stats_frame.winfo_children():
            child.destroy()
            
        stats_label = tk.Label(self.stats_frame, text=stats_text,
                              font=("Segoe UI", 12), bg="#ffffff", fg="#059669")
        stats_label.pack()

    def update_status(self, message):
        """Update status message"""
        if hasattr(self, 'status_label'):
            self.status_label.config(text=message)
            self.root.update_idletasks()

    def go_back(self):
        """Return to main dashboard"""
        self.root.destroy()
        self.main_dashboard_callback()


if __name__ == "__main__":
    # Test the teacher dashboard
    class MockTeacher:
        def __init__(self):
            self.name = "Dr. Smith"
            self.surname = "Johnson"
            self.role = "teacher"
    
    def mock_callback():
        print("Back to main dashboard")
    
    root = tk.Tk()
    teacher = MockTeacher()
    app = TeacherDashboard(root, teacher, mock_callback)
    root.mainloop()