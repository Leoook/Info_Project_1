import tkinter as tk
from tkinter import ttk, messagebox
from PythonExpenseApp.activity import Activity
from PythonExpenseApp.feedback import Feedback

# Try to import matplotlib, but provide fallback if not available
try:
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    import numpy as np
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False
    print("Matplotlib not available. Charts will be displayed as text.")

class ActivityDetailsGUI:
    def __init__(self, root, activity_id, student=None, main_callback=None):
        self.root = root
        self.activity_id = activity_id
        self.student = student
        self.main_callback = main_callback
        self.activity = Activity.get_activity_by_id(activity_id)
        
        if not self.activity:
            messagebox.showerror("Error", "Activity not found")
            root.destroy()
            return
            
        self.setup_window()
        self.create_interface()
        self.load_activity_details()

    def setup_window(self):
        self.root.title(f"Activity Details - {self.activity.name}")
        self.root.geometry("1200x800")
        self.root.configure(bg='#f8fafc')
        
        # Make window resizable
        self.root.resizable(True, True)

    def create_interface(self):
        # Main container
        main_container = tk.Frame(self.root, bg='#ffffff', relief='solid', bd=1)
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Header with back button
        self.create_header(main_container)
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(main_container)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create tabs (removed sentiment tab)
        self.create_overview_tab()
        self.create_ratings_tab()
        self.create_feedback_tab()

    def create_header(self, parent):
        header_frame = tk.Frame(parent, bg='#ffffff', height=80)
        header_frame.pack(fill=tk.X, padx=20, pady=(20, 0))
        header_frame.pack_propagate(False)
        
        # Back button
        if self.main_callback:
            back_btn = tk.Button(header_frame, text="← Back to Main", 
                                font=("Segoe UI", 12, "bold"), bg="#6b7280", fg="white",
                                relief='flat', bd=0, activebackground="#4b5563",
                                cursor="hand2", command=self.go_back_to_main)
            back_btn.pack(side=tk.LEFT, anchor='nw', pady=10)
        
        # Close button
        close_btn = tk.Button(header_frame, text="✕ Close", 
                             font=("Segoe UI", 12, "bold"), bg="#dc2626", fg="white",
                             relief='flat', bd=0, activebackground="#b91c1c",
                             cursor="hand2", command=self.root.destroy)
        close_btn.pack(side=tk.RIGHT, anchor='ne', pady=10)
        
        # Title section
        title_section = tk.Frame(header_frame, bg='#ffffff')
        title_section.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(20, 20))
        
        # Activity name and basic info
        title_label = tk.Label(title_section, text=f"🎯 {self.activity.name}", 
                              font=("Segoe UI", 24, "bold"), bg="#ffffff", fg="#1e293b")
        title_label.pack(anchor='w')
        
        # Basic info
        info_text = f"📅 {self.activity.day} | ⏰ {self.activity.start}:00-{self.activity.finish}:00 | 📍 {self.activity.location}"
        info_label = tk.Label(title_section, text=info_text, 
                             font=("Segoe UI", 12), bg="#ffffff", fg="#64748b")
        info_label.pack(anchor='w', pady=(5, 0))

    def go_back_to_main(self):
        """Close this window and return to main dashboard"""
        self.root.destroy()
        if self.main_callback:
            self.main_callback()

    def create_overview_tab(self):
        overview_frame = tk.Frame(self.notebook, bg='#ffffff')
        self.notebook.add(overview_frame, text="Overview")
        
        # Create scrollable frame
        canvas = tk.Canvas(overview_frame, bg='#ffffff')
        scrollbar = ttk.Scrollbar(overview_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='#ffffff')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Grid layout
        content_frame = tk.Frame(scrollable_frame, bg='#ffffff')
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        content_frame.grid_columnconfigure(0, weight=1)
        content_frame.grid_columnconfigure(1, weight=1)
        
        # Basic Information
        self.create_info_section(content_frame)
        
        # Participation Information
        self.create_participation_section(content_frame)
        
        # Quick Rating Summary
        self.create_rating_summary_section(content_frame)
        
        # Action buttons
        self.create_action_buttons(content_frame)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def create_info_section(self, parent):
        info_frame = tk.LabelFrame(parent, text="Activity Information", 
                                  font=("Segoe UI", 14, "bold"), bg="#ffffff")
        info_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10), pady=10)
        
        # Description
        if self.activity.description:
            desc_label = tk.Label(info_frame, text="Description:", 
                                 font=("Segoe UI", 12, "bold"), bg="#ffffff")
            desc_label.pack(anchor='w', padx=15, pady=(15, 5))
            
            desc_text = tk.Text(info_frame, height=4, font=("Segoe UI", 11), 
                               bg="#f8fafc", relief='solid', bd=1, wrap=tk.WORD)
            desc_text.pack(fill=tk.X, padx=15, pady=(0, 15))
            desc_text.insert('1.0', self.activity.description)
            desc_text.config(state='disabled')
        
        # Duration and capacity info
        details_frame = tk.Frame(info_frame, bg="#ffffff")
        details_frame.pack(fill=tk.X, padx=15, pady=(0, 15))
        
        if self.activity.duration:
            duration_label = tk.Label(details_frame, text=f"⏱️ Duration: {self.activity.duration} hours", 
                                     font=("Segoe UI", 11), bg="#ffffff")
            duration_label.pack(anchor='w', pady=2)
        
        capacity_text = f"👥 Capacity: "
        if self.activity.maxpart:
            capacity_text += f"{self.activity.maxpart} participants"
        else:
            capacity_text += "Unlimited"
        
        capacity_label = tk.Label(details_frame, text=capacity_text, 
                                 font=("Segoe UI", 11), bg="#ffffff")
        capacity_label.pack(anchor='w', pady=2)

    def create_participation_section(self, parent):
        participation_frame = tk.LabelFrame(parent, text="Participation Status", 
                                           font=("Segoe UI", 14, "bold"), bg="#ffffff")
        participation_frame.grid(row=0, column=1, sticky="nsew", padx=(10, 0), pady=10)
        
        # Current participants info will be loaded dynamically
        self.participation_info_frame = tk.Frame(participation_frame, bg="#ffffff")
        self.participation_info_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)

    def create_rating_summary_section(self, parent):
        rating_frame = tk.LabelFrame(parent, text="Rating Summary", 
                                    font=("Segoe UI", 14, "bold"), bg="#ffffff")
        rating_frame.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=0, pady=10)
        
        # Rating info will be loaded dynamically
        self.rating_summary_frame = tk.Frame(rating_frame, bg="#ffffff")
        self.rating_summary_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)

    def create_action_buttons(self, parent):
        button_frame = tk.Frame(parent, bg="#ffffff")
        button_frame.grid(row=2, column=0, columnspan=2, pady=20)
        
        if self.student:
            # Check if student is already registered
            participants = self.activity.get_participant_list()
            is_registered = any(p[0] == self.student.id for p in participants)
            
            if not is_registered:
                register_btn = tk.Button(button_frame, text="Register for Activity", 
                                        font=("Segoe UI", 12, "bold"), bg="#059669", fg="white",
                                        command=self.register_for_activity)
                register_btn.pack(side=tk.LEFT, padx=10)
            
            # Check if student can leave feedback
            can_feedback, feedback_message = self.activity.can_student_leave_feedback(self.student.id)
            
            if can_feedback:
                feedback_btn = tk.Button(button_frame, text="Leave Feedback", 
                                        font=("Segoe UI", 12, "bold"), bg="#3b82f6", fg="white",
                                        command=self.show_feedback_form)
                feedback_btn.pack(side=tk.LEFT, padx=10)
            else:
                # Show disabled button with reason
                disabled_btn = tk.Button(button_frame, text="Feedback Not Available", 
                                        font=("Segoe UI", 12, "bold"), bg="#9ca3af", fg="white",
                                        state="disabled", command=lambda: messagebox.showinfo("Feedback", feedback_message))
                disabled_btn.pack(side=tk.LEFT, padx=10)
                
                # Add tooltip showing why feedback is disabled
                def show_tooltip(event):
                    messagebox.showinfo("Feedback Status", feedback_message)
                disabled_btn.bind("<Button-3>", show_tooltip)  # Right-click for info
        
        refresh_btn = tk.Button(button_frame, text="Refresh Data", 
                               font=("Segoe UI", 12), bg="#6b7280", fg="white",
                               command=self.load_activity_details)
        refresh_btn.pack(side=tk.LEFT, padx=10)

    def create_ratings_tab(self):
        ratings_frame = tk.Frame(self.notebook, bg='#ffffff')
        self.notebook.add(ratings_frame, text="Ratings & Statistics")
        
        # Will be populated with rating charts and statistics
        self.ratings_content_frame = tk.Frame(ratings_frame, bg='#ffffff')
        self.ratings_content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

    def create_feedback_tab(self):
        feedback_frame = tk.Frame(self.notebook, bg='#ffffff')
        self.notebook.add(feedback_frame, text="Feedback")
        
        # Feedback list
        feedback_list_frame = tk.LabelFrame(feedback_frame, text="Student Feedback", 
                                           font=("Segoe UI", 14, "bold"), bg="#ffffff")
        feedback_list_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Scrollable feedback list
        feedback_canvas = tk.Canvas(feedback_list_frame, bg='#ffffff')
        feedback_scrollbar = ttk.Scrollbar(feedback_list_frame, orient="vertical", command=feedback_canvas.yview)
        
        self.feedback_content_frame = tk.Frame(feedback_canvas, bg='#ffffff')
        self.feedback_content_frame.bind(
            "<Configure>",
            lambda e: feedback_canvas.configure(scrollregion=feedback_canvas.bbox("all"))
        )
        
        feedback_canvas.create_window((0, 0), window=self.feedback_content_frame, anchor="nw")
        feedback_canvas.configure(yscrollcommand=feedback_scrollbar.set)
        
        feedback_canvas.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        feedback_scrollbar.pack(side="right", fill="y", pady=10)

    def load_activity_details(self):
        details = self.activity.get_comprehensive_details()
        if not details:
            return
        
        self.load_participation_info(details['participation'])
        self.load_rating_summary(details['ratings'])
        self.load_detailed_ratings(details['ratings'])
        self.load_feedback_list(details['recent_feedback'])

    def load_participation_info(self, participation_data):
        # Clear existing content
        for widget in self.participation_info_frame.winfo_children():
            widget.destroy()
        
        current = participation_data['current_participants']
        max_participants = self.activity.maxpart
        
        # Current participants count
        count_text = f"👥 Current: {current}"
        if max_participants:
            count_text += f" / {max_participants}"
            percentage = (current / max_participants) * 100
            count_text += f" ({percentage:.1f}%)"
        
        count_label = tk.Label(self.participation_info_frame, text=count_text, 
                              font=("Segoe UI", 12, "bold"), bg="#ffffff")
        count_label.pack(anchor='w', pady=5)
        
        # Status indicator
        if max_participants and current >= max_participants:
            status_text = "🔴 FULL"
            status_color = "#dc2626"
        elif max_participants and current >= max_participants * 0.8:
            status_text = "🟡 ALMOST FULL"
            status_color = "#f59e0b"
        else:
            status_text = "🟢 AVAILABLE"
            status_color = "#059669"
        
        status_label = tk.Label(self.participation_info_frame, text=status_text, 
                               font=("Segoe UI", 11, "bold"), bg="#ffffff", fg=status_color)
        status_label.pack(anchor='w', pady=2)
        
        # Participant list
        if participation_data['participant_list']:
            participants_label = tk.Label(self.participation_info_frame, text="Registered Students:", 
                                         font=("Segoe UI", 10, "bold"), bg="#ffffff")
            participants_label.pack(anchor='w', pady=(10, 5))
            
            # Create scrollable list for many participants
            if len(participation_data['participant_list']) > 5:
                list_frame = tk.Frame(self.participation_info_frame, bg="#ffffff")
                list_frame.pack(fill=tk.BOTH, expand=True)
                
                participant_listbox = tk.Listbox(list_frame, height=5, font=("Segoe UI", 10))
                participant_scrollbar = ttk.Scrollbar(list_frame, orient="vertical")
                
                for student_id, name, surname in participation_data['participant_list']:
                    participant_listbox.insert(tk.END, f"{name} {surname}")
                
                participant_listbox.config(yscrollcommand=participant_scrollbar.set)
                participant_scrollbar.config(command=participant_listbox.yview)
                
                participant_listbox.pack(side="left", fill="both", expand=True)
                participant_scrollbar.pack(side="right", fill="y")
            else:
                for student_id, name, surname in participation_data['participant_list']:
                    student_label = tk.Label(self.participation_info_frame, text=f"• {name} {surname}", 
                                           font=("Segoe UI", 10), bg="#ffffff")
                    student_label.pack(anchor='w', padx=10)

    def load_rating_summary(self, ratings_data):
        # Clear existing content
        for widget in self.rating_summary_frame.winfo_children():
            widget.destroy()
        
        if not ratings_data or ratings_data['total_ratings'] == 0:
            no_ratings_label = tk.Label(self.rating_summary_frame, text="No ratings yet", 
                                       font=("Segoe UI", 12), bg="#ffffff", fg="#6b7280")
            no_ratings_label.pack(anchor='w')
            return
        
        # Create summary info
        summary_frame = tk.Frame(self.rating_summary_frame, bg="#ffffff")
        summary_frame.pack(fill=tk.X)
        
        # Average rating with stars
        avg_rating = ratings_data['average_rating']
        stars = "⭐" * int(round(avg_rating))
        avg_text = f"{stars} {avg_rating:.2f}/5.0"
        
        avg_label = tk.Label(summary_frame, text=avg_text, 
                            font=("Segoe UI", 14, "bold"), bg="#ffffff", fg="#f59e0b")
        avg_label.pack(side=tk.LEFT)
        
        # Median and count
        median_text = f" | Median: {ratings_data['median_rating']:.2f} | {ratings_data['total_ratings']} reviews"
        median_label = tk.Label(summary_frame, text=median_text, 
                               font=("Segoe UI", 12), bg="#ffffff", fg="#6b7280")
        median_label.pack(side=tk.LEFT)

    def load_detailed_ratings(self, ratings_data):
        # Clear existing content
        for widget in self.ratings_content_frame.winfo_children():
            widget.destroy()
        
        if not ratings_data or ratings_data['total_ratings'] == 0:
            no_ratings_label = tk.Label(self.ratings_content_frame, text="No ratings available for detailed analysis", 
                                       font=("Segoe UI", 14), bg="#ffffff", fg="#6b7280")
            no_ratings_label.pack(expand=True)
            return
        
        # Create rating display (chart if matplotlib available, otherwise text)
        if MATPLOTLIB_AVAILABLE:
            self.create_rating_distribution_chart(ratings_data)
        else:
            self.create_rating_distribution_text(ratings_data)

    def create_rating_distribution_chart(self, ratings_data):
        try:
            # Create matplotlib figure
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
            fig.patch.set_facecolor('white')
            
            # Rating distribution bar chart
            ratings = [1, 2, 3, 4, 5]
            counts = [ratings_data['rating_distribution'][i] for i in ratings]
            colors = ['#dc2626', '#f97316', '#eab308', '#22c55e', '#059669']
            
            bars = ax1.bar(ratings, counts, color=colors, alpha=0.8)
            ax1.set_xlabel('Rating (Stars)')
            ax1.set_ylabel('Number of Reviews')
            ax1.set_title('Rating Distribution')
            ax1.set_xticks(ratings)
            ax1.set_ylim(0, max(counts) + 1 if max(counts) > 0 else 1)
            
            # Add value labels on bars
            for bar, count in zip(bars, counts):
                if count > 0:
                    ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1, 
                            str(count), ha='center', va='bottom', fontweight='bold')
            
            # Rating summary pie chart
            non_zero_ratings = [(i, count) for i, count in enumerate(counts, 1) if count > 0]
            if non_zero_ratings:
                # Use text instead of star symbols to avoid font issues
                pie_labels = [f"{rating} Stars" for rating, _ in non_zero_ratings]
                pie_values = [count for _, count in non_zero_ratings]
                pie_colors = [colors[rating-1] for rating, _ in non_zero_ratings]
                
                wedges, texts, autotexts = ax2.pie(pie_values, labels=pie_labels, colors=pie_colors, 
                                                  autopct='%1.1f%%', startangle=90)
                ax2.set_title('Rating Breakdown')
                
                # Make percentage text bold
                for autotext in autotexts:
                    autotext.set_color('white')
                    autotext.set_fontweight('bold')
            else:
                ax2.text(0.5, 0.5, 'No ratings yet', ha='center', va='center', transform=ax2.transAxes)
                ax2.set_title('Rating Breakdown')
            
            plt.tight_layout()
            
            # Embed in tkinter
            canvas = FigureCanvasTkAgg(fig, self.ratings_content_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            
            # Add statistics below the chart
            self.create_rating_statistics_text(ratings_data)
            
        except Exception as e:
            print(f"Error creating chart: {e}")
            # Fallback to text display
            self.create_rating_distribution_text(ratings_data)

    def create_rating_distribution_text(self, ratings_data):
        """Text-based rating distribution display"""
        stats_frame = tk.Frame(self.ratings_content_frame, bg="#ffffff")
        stats_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title
        title_label = tk.Label(stats_frame, text="📊 Rating Distribution", 
                              font=("Segoe UI", 18, "bold"), bg="#ffffff", fg="#1e293b")
        title_label.pack(anchor='w', pady=(0, 20))
        
        # Overall statistics
        overall_frame = tk.LabelFrame(stats_frame, text="Overall Statistics", 
                                     font=("Segoe UI", 14, "bold"), bg="#ffffff")
        overall_frame.pack(fill=tk.X, pady=(0, 20))
        
        overall_content = tk.Frame(overall_frame, bg="#ffffff")
        overall_content.pack(fill=tk.X, padx=15, pady=15)
        
        # Average rating with stars
        avg_rating = ratings_data['average_rating']
        stars = "⭐" * int(round(avg_rating))
        avg_text = f"Average Rating: {stars} {avg_rating:.2f}/5.0"
        
        avg_label = tk.Label(overall_content, text=avg_text, 
                            font=("Segoe UI", 14, "bold"), bg="#ffffff", fg="#f59e0b")
        avg_label.pack(anchor='w', pady=2)
        
        median_label = tk.Label(overall_content, text=f"Median Rating: {ratings_data['median_rating']:.1f}", 
                               font=("Segoe UI", 12), bg="#ffffff", fg="#6b7280")
        median_label.pack(anchor='w', pady=2)
        
        total_label = tk.Label(overall_content, text=f"Total Reviews: {ratings_data['total_ratings']}", 
                              font=("Segoe UI", 12), bg="#ffffff", fg="#6b7280")
        total_label.pack(anchor='w', pady=2)
        
        # Distribution details
        dist_frame = tk.LabelFrame(stats_frame, text="Rating Breakdown", 
                                  font=("Segoe UI", 14, "bold"), bg="#ffffff")
        dist_frame.pack(fill=tk.X, pady=(0, 20))
        
        dist_content = tk.Frame(dist_frame, bg="#ffffff")
        dist_content.pack(fill=tk.X, padx=15, pady=15)
        
        colors = ['#dc2626', '#f97316', '#eab308', '#22c55e', '#059669']
        max_count = max(ratings_data['rating_distribution'].values()) if ratings_data['rating_distribution'] else 1
        
        for rating in [5, 4, 3, 2, 1]:  # Show 5-star first
            count = ratings_data['rating_distribution'][rating]
            percentage = (count / ratings_data['total_ratings']) * 100 if ratings_data['total_ratings'] > 0 else 0
            
            rating_frame = tk.Frame(dist_content, bg="#ffffff")
            rating_frame.pack(fill=tk.X, pady=3)
            
            # Star rating
            star_label = tk.Label(rating_frame, text=f"{rating} ⭐", 
                                 font=("Segoe UI", 12, "bold"), bg="#ffffff", 
                                 fg=colors[rating-1], width=8)
            star_label.pack(side=tk.LEFT)
            
            # Progress bar simulation
            bar_frame = tk.Frame(rating_frame, bg="#e5e7eb", height=20, width=200)
            bar_frame.pack(side=tk.LEFT, padx=(10, 10))
            bar_frame.pack_propagate(False)
            
            if count > 0:
                bar_width = int((count / max_count) * 200)
                bar = tk.Frame(bar_frame, bg=colors[rating-1], height=20, width=bar_width)
                bar.pack(side=tk.LEFT)
            
            # Count and percentage
            count_label = tk.Label(rating_frame, text=f"{count} ({percentage:.1f}%)", 
                                  font=("Segoe UI", 11), bg="#ffffff", fg="#374151")
            count_label.pack(side=tk.LEFT, padx=(10, 0))

    def create_rating_statistics_text(self, ratings_data):
        """Add additional statistics below charts"""
        stats_text_frame = tk.Frame(self.ratings_content_frame, bg="#f8fafc", relief='solid', bd=1)
        stats_text_frame.pack(fill=tk.X, padx=10, pady=10)
        
        stats_content = tk.Frame(stats_text_frame, bg="#f8fafc")
        stats_content.pack(fill=tk.X, padx=15, pady=10)
        
        # Calculate additional statistics
        total = ratings_data['total_ratings']
        dist = ratings_data['rating_distribution']
        
        positive_ratings = dist[4] + dist[5]  # 4 and 5 stars
        negative_ratings = dist[1] + dist[2]  # 1 and 2 stars
        neutral_ratings = dist[3]  # 3 stars
        
        positive_pct = (positive_ratings / total) * 100 if total > 0 else 0
        negative_pct = (negative_ratings / total) * 100 if total > 0 else 0
        neutral_pct = (neutral_ratings / total) * 100 if total > 0 else 0
        
        stats_title = tk.Label(stats_content, text="📈 Quick Statistics", 
                              font=("Segoe UI", 12, "bold"), bg="#f8fafc", fg="#1e293b")
        stats_title.pack(anchor='w', pady=(0, 5))
        
        positive_label = tk.Label(stats_content, text=f"👍 Positive (4-5 ⭐): {positive_ratings} ({positive_pct:.1f}%)", 
                                 font=("Segoe UI", 11), bg="#f8fafc", fg="#059669")
        positive_label.pack(anchor='w', pady=1)
        
        neutral_label = tk.Label(stats_content, text=f"😐 Neutral (3 ⭐): {neutral_ratings} ({neutral_pct:.1f}%)", 
                                font=("Segoe UI", 11), bg="#f8fafc", fg="#f59e0b")
        neutral_label.pack(anchor='w', pady=1)
        
        negative_label = tk.Label(stats_content, text=f"👎 Negative (1-2 ⭐): {negative_ratings} ({negative_pct:.1f}%)", 
                                 font=("Segoe UI", 11), bg="#f8fafc", fg="#dc2626")
        negative_label.pack(anchor='w', pady=1)

    def register_for_activity(self):
        # Implementation for registering student to activity
        from PythonExpenseApp.db_connection import DbConnection
        
        connection = DbConnection.connect()
        if not connection:
            messagebox.showerror("Error", "Could not connect to database")
            return
        
        try:
            cursor = connection.cursor()
            cursor.execute("INSERT INTO student_activities (student_id, activity_id) VALUES (%s, %s)",
                          (self.student.id, self.activity_id))
            connection.commit()
            messagebox.showinfo("Success", "Successfully registered for activity!")
            self.load_activity_details()  # Refresh data
        except Exception as e:
            messagebox.showerror("Error", f"Could not register for activity: {e}")
        finally:
            connection.close()

    def show_feedback_form(self):
        # Validate permission before showing form
        can_feedback, message = self.activity.can_student_leave_feedback(self.student.id)
        if not can_feedback:
            messagebox.showerror("Cannot Leave Feedback", message)
            return
        
        # Create feedback form window
        feedback_window = tk.Toplevel(self.root)
        feedback_window.title("Leave Feedback")
        feedback_window.geometry("500x450")
        feedback_window.configure(bg='#ffffff')
        
        # Center the window
        feedback_window.transient(self.root)
        feedback_window.grab_set()
        
        # Feedback form content
        form_frame = tk.Frame(feedback_window, bg='#ffffff')
        form_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title with participation confirmation
        title_label = tk.Label(form_frame, text=f"Feedback for {self.activity.name}", 
                              font=("Segoe UI", 16, "bold"), bg="#ffffff")
        title_label.pack(anchor='w', pady=(0, 10))
        
        # Participation confirmation
        participation_label = tk.Label(form_frame, text="✅ You participated in this activity", 
                                      font=("Segoe UI", 12), bg="#ffffff", fg="#059669")
        participation_label.pack(anchor='w', pady=(0, 20))
        
        # Rating selection
        rating_label = tk.Label(form_frame, text="Rating:", 
                               font=("Segoe UI", 12, "bold"), bg="#ffffff")
        rating_label.pack(anchor='w', pady=(0, 5))
        
        rating_var = tk.IntVar(value=5)
        rating_frame = tk.Frame(form_frame, bg="#ffffff")
        rating_frame.pack(anchor='w', pady=(0, 15))
        
        for i in range(1, 6):
            star_text = "⭐" * i
            rating_radio = tk.Radiobutton(rating_frame, text=f"{star_text} ({i})", 
                                         variable=rating_var, value=i, 
                                         bg="#ffffff", font=("Segoe UI", 11))
            rating_radio.pack(anchor='w', pady=2)
        
        # Comment
        comment_label = tk.Label(form_frame, text="Comment (optional):", 
                                font=("Segoe UI", 12, "bold"), bg="#ffffff")
        comment_label.pack(anchor='w', pady=(0, 5))
        
        comment_text = tk.Text(form_frame, height=8, font=("Segoe UI", 11), 
                              relief='solid', bd=1)
        comment_text.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        # Guidelines
        guidelines_label = tk.Label(form_frame, 
                                   text="💡 Please share your honest experience to help other students!", 
                                   font=("Segoe UI", 10), bg="#ffffff", fg="#6b7280", 
                                   wraplength=400, justify=tk.LEFT)
        guidelines_label.pack(anchor='w', pady=(0, 15))
        
        # Buttons
        button_frame = tk.Frame(form_frame, bg="#ffffff")
        button_frame.pack(fill=tk.X)
        
        def submit_feedback():
            rating = rating_var.get()
            comment = comment_text.get('1.0', tk.END).strip()
            
            from PythonExpenseApp.feedback import Feedback
            feedback = Feedback(self.student.id, self.activity_id, rating, comment if comment else None)
            success, message = feedback.save_to_database()
            
            if success:
                messagebox.showinfo("Success", "Feedback submitted successfully!")
                feedback_window.destroy()
                self.load_activity_details()  # Refresh data
            else:
                messagebox.showerror("Error", message)
        
        submit_btn = tk.Button(button_frame, text="Submit Feedback", 
                              font=("Segoe UI", 12, "bold"), bg="#059669", fg="white",
                              command=submit_feedback)
        submit_btn.pack(side=tk.RIGHT, padx=(10, 0))
        
        cancel_btn = tk.Button(button_frame, text="Cancel", 
                              font=("Segoe UI", 12), bg="#6b7280", fg="white",
                              command=feedback_window.destroy)
        cancel_btn.pack(side=tk.RIGHT)

    def load_feedback_list(self, feedback_data):
        """Load and display feedback list"""
        # Clear existing content
        for widget in self.feedback_content_frame.winfo_children():
            widget.destroy()
        
        if not feedback_data:
            # No feedback available
            no_feedback_frame = tk.Frame(self.feedback_content_frame, bg='#ffffff')
            no_feedback_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=50)
            
            no_feedback_label = tk.Label(no_feedback_frame, text="📝 No feedback available yet", 
                                        font=("Segoe UI", 16, "bold"), bg="#ffffff", fg="#6b7280")
            no_feedback_label.pack()
            
            help_label = tk.Label(no_feedback_frame, text="Students can leave feedback after participating in the activity", 
                                 font=("Segoe UI", 12), bg="#ffffff", fg="#9ca3af")
            help_label.pack(pady=(10, 0))
            return
        
        # Display feedback entries
        for i, (rating, comment, created_at, name, surname) in enumerate(feedback_data):
            # Create feedback card
            feedback_card = tk.Frame(self.feedback_content_frame, bg='#f8fafc', relief='solid', bd=1)
            feedback_card.pack(fill=tk.X, padx=10, pady=8)
            
            # Card content
            card_content = tk.Frame(feedback_card, bg='#f8fafc')
            card_content.pack(fill=tk.X, padx=15, pady=15)
            
            # Header with rating and student info
            header_frame = tk.Frame(card_content, bg='#f8fafc')
            header_frame.pack(fill=tk.X, pady=(0, 10))
            
            # Rating stars
            stars = "⭐" * rating
            rating_label = tk.Label(header_frame, text=stars, 
                                   font=("Segoe UI", 14, "bold"), bg="#f8fafc", fg="#f59e0b")
            rating_label.pack(side=tk.LEFT)
            
            # Student name
            student_label = tk.Label(header_frame, text=f" by {name} {surname}", 
                                    font=("Segoe UI", 12, "bold"), bg="#f8fafc", fg="#1e293b")
            student_label.pack(side=tk.LEFT)
            
            # Date
            from datetime import datetime
            if isinstance(created_at, str):
                date_str = created_at
            else:
                date_str = created_at.strftime("%Y-%m-%d %H:%M") if created_at else "Unknown date"
            
            date_label = tk.Label(header_frame, text=date_str, 
                                 font=("Segoe UI", 10), bg="#f8fafc", fg="#6b7280")
            date_label.pack(side=tk.RIGHT)
            
            # Verified participant badge
            verified_label = tk.Label(header_frame, text="✅ Verified Participant", 
                                     font=("Segoe UI", 10, "bold"), bg="#f8fafc", fg="#059669")
            verified_label.pack(side=tk.RIGHT, padx=(0, 10))
            
            # Comment (if available)
            if comment and comment.strip():
                comment_frame = tk.Frame(card_content, bg='#ffffff', relief='solid', bd=1)
                comment_frame.pack(fill=tk.X, pady=(0, 5))
                
                comment_text = tk.Text(comment_frame, height=3, font=("Segoe UI", 11), 
                                      bg="#ffffff", fg="#374151", relief='flat', bd=0, 
                                      wrap=tk.WORD, cursor="arrow")
                comment_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=8)
                comment_text.insert('1.0', comment)
                comment_text.config(state='disabled')
            else:
                # No comment placeholder
                no_comment_label = tk.Label(card_content, text="(No written comment provided)", 
                                           font=("Segoe UI", 10, "italic"), bg="#f8fafc", fg="#9ca3af")
                no_comment_label.pack(anchor='w')
        
        # Add summary at the end
        if len(feedback_data) > 0:
            summary_frame = tk.Frame(self.feedback_content_frame, bg='#e0f2fe', relief='solid', bd=1)
            summary_frame.pack(fill=tk.X, padx=10, pady=(20, 10))
            
            summary_content = tk.Frame(summary_frame, bg='#e0f2fe')
            summary_content.pack(fill=tk.X, padx=15, pady=10)
            
            total_participants = self.activity.get_current_participants()
            feedback_count = len(feedback_data)
            completion_rate = (feedback_count / total_participants * 100) if total_participants > 0 else 0
            
            summary_text = f"📊 {feedback_count} feedback entries from {total_participants} participants ({completion_rate:.1f}% completion rate)"
            summary_label = tk.Label(summary_content, text=summary_text, 
                                    font=("Segoe UI", 12, "bold"), bg="#e0f2fe", fg="#0277bd")
            summary_label.pack()
