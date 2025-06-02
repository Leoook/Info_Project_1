import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk, ImageDraw, ImageFilter
from PythonExpenseApp.db_connection import DbConnection
import mysql.connector

class ActivityFormGUI:
    """
    GUI for subscribing a student to an activity.
    The 'self' variable refers to the current instance of ActivityFormGUI.
    It is used to access instance variables (attributes) and methods throughout the class.
    For example, self.activities refers to the list of activities for this particular GUI window.
    """
    def __init__(self, root, student, main_callback=None):
        """
        Initializes the Activity Subscription GUI window and its widgets.
        - Loads all activities from the database and displays them in a listbox.
        - Provides a button to subscribe the student to the selected activity.
        """
        self.root = root
        self.student = student
        self.main_callback = main_callback
        self.root.title("Activity Subscription")
        self.root.geometry("1000x700")
        self.root.resizable(True, True)
        self.root.configure(bg='#f8fafc')
        
        # Main container
        main_container = tk.Frame(self.root, bg='#ffffff', relief='solid', bd=1)
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Header section with back button
        header_frame = tk.Frame(main_container, bg='#ffffff', height=100)
        header_frame.pack(fill=tk.X, padx=30, pady=(20, 10))
        header_frame.pack_propagate(False)
        
        # Back button
        if self.main_callback:
            back_btn = tk.Button(header_frame, text="← Back to Main", 
                                font=("Segoe UI", 12, "bold"), bg="#6b7280", fg="white",
                                relief='flat', bd=0, activebackground="#4b5563",
                                cursor="hand2", command=self.go_back_to_main)
            back_btn.pack(side=tk.LEFT, anchor='nw', pady=10)
        
        # Title section
        title_section = tk.Frame(header_frame, bg='#ffffff')
        title_section.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(20, 0))
        
        title_label = tk.Label(title_section, text="🎯 Activity Manager", 
                              font=("Segoe UI", 28, "bold"), bg="#ffffff", fg="#1e293b")
        title_label.pack(anchor='w')
        
        subtitle_label = tk.Label(title_section, text="Subscribe to activities and manage your schedule", 
                                 font=("Segoe UI", 14), bg="#ffffff", fg="#64748b")
        subtitle_label.pack(anchor='w', pady=(5, 0))
        
        # Student info on the right
        student_info = tk.Label(header_frame, text=f"Student: {student.name} {getattr(student, 'surname', '')}", 
                               font=("Segoe UI", 12, "bold"), bg="#ffffff", fg="#059669")
        student_info.pack(side=tk.RIGHT, anchor='ne', pady=10)
        
        # Content area
        content_frame = tk.Frame(main_container, bg='#ffffff')
        content_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=20)
        
        # Configure grid
        content_frame.grid_columnconfigure(0, weight=2)
        content_frame.grid_columnconfigure(1, weight=1)
        content_frame.grid_rowconfigure(0, weight=1)
        
        # Activities section
        activities_section = tk.LabelFrame(content_frame, text="Available Activities", 
                                          font=("Segoe UI", 16, "bold"), bg="#ffffff", 
                                          fg="#1e293b", relief='solid', bd=2)
        activities_section.grid(row=0, column=0, sticky="nsew", padx=(0, 10), pady=10)
        
        # Activities list container
        list_container = tk.Frame(activities_section, bg="#ffffff")
        list_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Scrollbar
        activities_scrollbar = tk.Scrollbar(list_container)
        activities_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.activity_listbox = tk.Listbox(list_container, font=("Segoe UI", 11), bg="#ffffff", 
                                          fg="#374151", relief='solid', bd=1,
                                          yscrollcommand=activities_scrollbar.set,
                                          selectbackground="#dbeafe", selectforeground="#1e40af")
        self.activity_listbox.pack(fill=tk.BOTH, expand=True)
        activities_scrollbar.config(command=self.activity_listbox.yview)
        
        # Action section
        action_section = tk.LabelFrame(content_frame, text="Actions", 
                                      font=("Segoe UI", 16, "bold"), bg="#ffffff", 
                                      fg="#1e293b", relief='solid', bd=2)
        action_section.grid(row=0, column=1, sticky="nsew", padx=(10, 0), pady=10)
        
        # Action buttons frame
        button_frame = tk.Frame(action_section, bg="#ffffff")
        button_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Subscribe button
        subscribe_btn = tk.Button(button_frame, text="Subscribe to Activity", 
                                 font=("Segoe UI", 12, "bold"), bg="#3b82f6", fg="#ffffff", 
                                 relief='flat', bd=0, activebackground="#2563eb", 
                                 activeforeground="#ffffff", cursor="hand2", 
                                 command=self.subscribe_to_activity)
        subscribe_btn.pack(fill=tk.X, pady=10, ipady=12)
        
        # View subscriptions button
        view_btn = tk.Button(button_frame, text="View My Activities", 
                            font=("Segoe UI", 12, "bold"), bg="#059669", fg="#ffffff", 
                            relief='flat', bd=0, activebackground="#047857", 
                            activeforeground="#ffffff", cursor="hand2", 
                            command=self.view_subscriptions)
        view_btn.pack(fill=tk.X, pady=10, ipady=12)
        
        # Refresh button
        refresh_btn = tk.Button(button_frame, text="Refresh Activities", 
                               font=("Segoe UI", 11), bg="#6b7280", fg="#ffffff", 
                               relief='flat', bd=0, activebackground="#4b5563", 
                               activeforeground="#ffffff", cursor="hand2", 
                               command=self.load_activities)
        refresh_btn.pack(fill=tk.X, pady=10, ipady=8)
        
        # View details button
        details_btn = tk.Button(button_frame, text="View Details", 
                               font=("Segoe UI", 12, "bold"), bg="#8b5cf6", fg="#ffffff", 
                               relief='flat', bd=0, activebackground="#7c3aed", 
                               activeforeground="#ffffff", cursor="hand2", 
                               command=self.view_activity_details)
        details_btn.pack(fill=tk.X, pady=10, ipady=12)
        
        # Feedback area
        feedback_frame = tk.Frame(main_container, bg='#ffffff', height=40)
        feedback_frame.pack(fill=tk.X, padx=30, pady=(0, 20))
        feedback_frame.pack_propagate(False)
        
        self.feedback_label = tk.Label(feedback_frame, text="", font=("Segoe UI", 12), 
                                      bg="#ffffff", fg="#dc2626")
        self.feedback_label.pack(anchor='center', pady=10)
        
        # Initialize data
        self.activities = []
        self.activity_ids = []
        self.activity_days = []
        self.load_activities()

    def load_activities(self):
        """Load all available activities from the database"""
        self.activity_listbox.delete(0, tk.END)
        self.activities = []
        self.activity_ids = []
        self.activity_days = []
        
        connection = DbConnection.connect()
        if connection:
            try:
                cursor = connection.cursor()
                cursor.execute("""SELECT id, name, day, start_time, finish_time, location, 
                                max_participants FROM activities ORDER BY day, start_time""")
                activities = cursor.fetchall()
                
                for activity in activities:
                    id, name, day, start, finish, location, max_part = activity
                    
                    # Get current subscription count
                    cursor.execute("SELECT COUNT(*) FROM student_activities WHERE activity_id=%s", (id,))
                    current_count = cursor.fetchone()[0]
                    
                    # Format display text
                    status = f"({current_count}/{max_part})" if max_part else f"({current_count})"
                    display_text = f"📅 {day} | ⏰ {start}:00-{finish}:00"
                    display_text += f"\n🎯 {name} @ {location} {status}"
                    display_text += f"\n{'🔴 FULL' if current_count >= max_part else '🟢 Available'}"
                    
                    self.activity_listbox.insert(tk.END, display_text)
                    self.activity_listbox.insert(tk.END, "")  # Separator
                    
                    self.activities.append(activity)
                    self.activity_ids.append(id)
                    self.activity_days.append((day, start, finish))
                    
                connection.close()
            except Exception as e:
                self.feedback_label.config(text=f"Error loading activities: {e}", fg="#dc2626")
        else:
            self.feedback_label.config(text="Could not connect to database", fg="#dc2626")

    def view_subscriptions(self):
        """Show current student subscriptions"""
        connection = DbConnection.connect()
        if connection:
            try:
                cursor = connection.cursor()
                cursor.execute("""SELECT a.name, a.day, a.start_time, a.finish_time, a.location
                                FROM student_activities sa 
                                JOIN activities a ON sa.activity_id = a.id 
                                WHERE sa.student_id = %s 
                                ORDER BY a.day, a.start_time""", (self.student.id,))
                subscriptions = cursor.fetchall()
                
                if subscriptions:
                    msg = "Your Current Activities:\n\n"
                    for name, day, start, finish, location in subscriptions:
                        msg += f"📅 {day} | ⏰ {start}:00-{finish}:00\n"
                        msg += f"🎯 {name} @ {location}\n\n"
                    messagebox.showinfo("My Activities", msg)
                else:
                    messagebox.showinfo("My Activities", "You are not subscribed to any activities yet.")
                    
                connection.close()
            except Exception as e:
                messagebox.showerror("Error", f"Could not load subscriptions: {e}")

    def subscribe_to_activity(self):
        """Subscribe to selected activity"""
        selection = self.activity_listbox.curselection()
        if not selection:
            messagebox.showerror("Error", "Please select an activity.")
            return
            
        # Get actual activity index (accounting for separators)
        selected_index = selection[0]
        activity_index = selected_index // 2  # Every other item is a separator
        
        if activity_index >= len(self.activity_ids):
            messagebox.showerror("Error", "Invalid selection.")
            return
            
        activity_id = self.activity_ids[activity_index]
        day, start_time, finish_time = self.activity_days[activity_index]
        
        connection = DbConnection.connect()
        if not connection:
            messagebox.showerror("Database Error", "Could not connect to the database.")
            return

        try:
            cursor = connection.cursor()
            
            # Check for time conflicts
            cursor.execute("""SELECT a.name, a.start_time, a.finish_time FROM student_activities sa
                            JOIN activities a ON sa.activity_id = a.id
                            WHERE sa.student_id=%s AND a.day=%s""", (self.student.id, day))
            
            for row in cursor.fetchall():
                existing_start, existing_finish = row[1], row[2]
                if not (finish_time <= existing_start or start_time >= existing_finish):
                    messagebox.showerror("Time Conflict", 
                                       f"You are already subscribed to '{row[0]}' at this time.")
                    return
            
            # Check if already subscribed
            cursor.execute("SELECT id FROM student_activities WHERE student_id=%s AND activity_id=%s", 
                          (self.student.id, activity_id))
            if cursor.fetchone():
                messagebox.showinfo("Already Subscribed", "You are already subscribed to this activity.")
                return
            
            # Check if activity is full
            cursor.execute("SELECT COUNT(*) FROM student_activities WHERE activity_id=%s", (activity_id,))
            count = cursor.fetchone()[0]
            cursor.execute("SELECT max_participants FROM activities WHERE id=%s", (activity_id,))
            max_part = cursor.fetchone()[0]
            
            if count >= max_part:
                messagebox.showerror("Full", "This activity is already full.")
                return
            
            # Subscribe
            cursor.execute("INSERT INTO student_activities (student_id, activity_id) VALUES (%s, %s)", 
                          (self.student.id, activity_id))
            connection.commit()
            
            self.feedback_label.config(text="Successfully subscribed to activity!", fg="#059669")
            messagebox.showinfo("Success", "You have been subscribed to the activity.")
            
            # Refresh the list to show updated counts
            self.load_activities()
            
        except Exception as e:
            messagebox.showerror("Error", f"Could not subscribe: {e}")
        finally:
            connection.close()

    def view_activity_details(self):
        """Show detailed activity information"""
        selection = self.activity_listbox.curselection()
        if not selection:
            messagebox.showerror("Error", "Please select an activity to view details.")
            return
            
        # Get actual activity index (accounting for separators)
        selected_index = selection[0]
        activity_index = selected_index // 2  # Every other item is a separator
        
        if activity_index >= len(self.activity_ids):
            messagebox.showerror("Error", "Invalid selection.")
            return
            
        activity_id = self.activity_ids[activity_index]
        
        # Create details window
        details_window = tk.Toplevel(self.root)
        from PythonExpenseApp.gui.activity_details_gui import ActivityDetailsGUI
        ActivityDetailsGUI(details_window, activity_id, self.student)

    def go_back_to_main(self):
        """Close this window and return to main dashboard"""
        self.root.destroy()
        if self.main_callback:
            self.main_callback()
