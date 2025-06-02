import tkinter as tk
from tkinter import ttk, messagebox
from PythonExpenseApp.activity import Activity
from PythonExpenseApp.feedback import Feedback
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

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
        
        # Create tabs
        self.create_overview_tab()
        self.create_ratings_tab()
        self.create_feedback_tab()
        self.create_sentiment_tab()

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
        feedback_list_frame = tk.LabelFrame(feedback_frame, text="Recent Feedback", 
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

    def create_sentiment_tab(self):
        sentiment_frame = tk.Frame(self.notebook, bg='#ffffff')
        self.notebook.add(sentiment_frame, text="Sentiment Analysis")
        
        # Sentiment analysis content
        self.sentiment_content_frame = tk.Frame(sentiment_frame, bg='#ffffff')
        self.sentiment_content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

    def load_activity_details(self):
        details = self.activity.get_comprehensive_details()
        if not details:
            return
        
        self.load_participation_info(details['participation'])
        self.load_rating_summary(details['ratings'])
        self.load_detailed_ratings(details['ratings'])
        self.load_feedback_list(details['recent_feedback'])
        self.load_sentiment_analysis(details['sentiment_words'])

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
        
        # Create rating distribution chart
        self.create_rating_distribution_chart(ratings_data)

    def create_rating_distribution_chart(self, ratings_data):
        # Create matplotlib figure
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
        fig.patch.set_facecolor('white')
        
        # Rating distribution bar chart
        ratings = [1, 2, 3, 4, 5]
        counts = [ratings_data['rating_distribution'][i] for i in ratings]
        colors = ['#dc2626', '#f97316', '#eab308', '#22c55e', '#059669']
        
        bars = ax1.bar(ratings, counts, color=colors, alpha=0.8)
        ax1.set_xlabel('Rating')
        ax1.set_ylabel('Number of Reviews')
        ax1.set_title('Rating Distribution')
        ax1.set_xticks(ratings)
        
        # Add value labels on bars
        for bar, count in zip(bars, counts):
            if count > 0:
                ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1, 
                        str(count), ha='center', va='bottom')
        
        # Rating summary pie chart
        non_zero_ratings = [(i, count) for i, count in enumerate(counts, 1) if count > 0]
        if non_zero_ratings:
            pie_labels = [f"{rating} Stars" for rating, _ in non_zero_ratings]
            pie_values = [count for _, count in non_zero_ratings]
            pie_colors = [colors[rating-1] for rating, _ in non_zero_ratings]
            
            ax2.pie(pie_values, labels=pie_labels, colors=pie_colors, autopct='%1.1f%%', startangle=90)
            ax2.set_title('Rating Breakdown')
        
        plt.tight_layout()
        
        # Embed in tkinter
        canvas = FigureCanvasTkAgg(fig, self.ratings_content_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def load_feedback_list(self, feedback_data):
        # Clear existing content
        for widget in self.feedback_content_frame.winfo_children():
            widget.destroy()
        
        if not feedback_data:
            no_feedback_label = tk.Label(self.feedback_content_frame, text="No feedback yet", 
                                        font=("Segoe UI", 12), bg="#ffffff", fg="#6b7280")
            no_feedback_label.pack(anchor='w', pady=20)
            
            # Show feedback statistics
            feedback_stats = self.activity.get_feedback_statistics()
            if feedback_stats.get('total_participants', 0) > 0:
                stats_text = f"📊 {feedback_stats['total_participants']} participants, "
                stats_text += f"{feedback_stats['feedback_given']} feedback given "
                stats_text += f"({feedback_stats['feedback_percentage']:.1f}%)"
                
                stats_label = tk.Label(self.feedback_content_frame, text=stats_text, 
                                      font=("Segoe UI", 11), bg="#ffffff", fg="#6b7280")
                stats_label.pack(anchor='w', pady=10)
            return
        
        # Show feedback statistics at the top
        feedback_stats = self.activity.get_feedback_statistics()
        if feedback_stats:
            stats_frame = tk.Frame(self.feedback_content_frame, bg="#e0f2fe", relief='solid', bd=1)
            stats_frame.pack(fill=tk.X, padx=10, pady=(10, 20))
            
            stats_text = f"📊 Feedback Summary: {feedback_stats['feedback_given']}/{feedback_stats['total_participants']} "
            stats_text += f"participants ({feedback_stats['feedback_percentage']:.1f}%) have provided feedback"
            
            stats_label = tk.Label(stats_frame, text=stats_text, 
                                  font=("Segoe UI", 12, "bold"), bg="#e0f2fe", fg="#0369a1")
            stats_label.pack(padx=15, pady=10)
        
        for rating, comment, created_at, student_name, student_surname in feedback_data:
            feedback_frame = tk.Frame(self.feedback_content_frame, bg="#f8fafc", 
                                     relief='solid', bd=1)
            feedback_frame.pack(fill=tk.X, padx=10, pady=5)
            
            # Header with rating and student info
            header_frame = tk.Frame(feedback_frame, bg="#f8fafc")
            header_frame.pack(fill=tk.X, padx=15, pady=(10, 5))
            
            stars = "⭐" * rating
            rating_label = tk.Label(header_frame, text=stars, 
                                   font=("Segoe UI", 12), bg="#f8fafc")
            rating_label.pack(side=tk.LEFT)
            
            student_label = tk.Label(header_frame, text=f" by {student_name} {student_surname}", 
                                    font=("Segoe UI", 10, "bold"), bg="#f8fafc", fg="#6b7280")
            student_label.pack(side=tk.LEFT)
            
            # Verified participant badge
            verified_label = tk.Label(header_frame, text="✅ Verified Participant", 
                                     font=("Segoe UI", 9), bg="#f8fafc", fg="#059669")
            verified_label.pack(side=tk.RIGHT)
            
            date_label = tk.Label(header_frame, text=f"{created_at.strftime('%Y-%m-%d')}", 
                                 font=("Segoe UI", 10), bg="#f8fafc", fg="#6b7280")
            date_label.pack(side=tk.RIGHT, padx=(0, 10))
            
            # Comment
            if comment:
                comment_label = tk.Label(feedback_frame, text=comment, 
                                        font=("Segoe UI", 11), bg="#f8fafc", 
                                        wraplength=600, justify=tk.LEFT)
                comment_label.pack(anchor='w', padx=15, pady=(0, 10))

    def load_sentiment_analysis(self, sentiment_data):
        # Clear existing content
        for widget in self.sentiment_content_frame.winfo_children():
            widget.destroy()
        
        if not sentiment_data:
            no_sentiment_label = tk.Label(self.sentiment_content_frame, text="No sentiment data available", 
                                         font=("Segoe UI", 14), bg="#ffffff", fg="#6b7280")
            no_sentiment_label.pack(expand=True)
            return
        
        # Group words by sentiment
        positive_words = [w for w in sentiment_data if w['sentiment'] == 'positive']
        negative_words = [w for w in sentiment_data if w['sentiment'] == 'negative']
        neutral_words = [w for w in sentiment_data if w['sentiment'] == 'neutral']
        
        # Create sentiment sections
        self.create_sentiment_section("Positive Words", positive_words, "#22c55e")
        self.create_sentiment_section("Negative Words", negative_words, "#dc2626")
        self.create_sentiment_section("Neutral Words", neutral_words, "#6b7280")

    def create_sentiment_section(self, title, words, color):
        if not words:
            return
        
        section_frame = tk.LabelFrame(self.sentiment_content_frame, text=title, 
                                     font=("Segoe UI", 14, "bold"), bg="#ffffff", 
                                     fg=color)
        section_frame.pack(fill=tk.X, padx=10, pady=10)
        
        words_frame = tk.Frame(section_frame, bg="#ffffff")
        words_frame.pack(fill=tk.X, padx=15, pady=15)
        
        for i, word_data in enumerate(words[:10]):  # Show top 10 words
            word_frame = tk.Frame(words_frame, bg="#ffffff")
            word_frame.pack(fill=tk.X, pady=2)
            
            word_text = f"{word_data['word']} ({word_data['frequency']})"
            word_label = tk.Label(word_frame, text=word_text, 
                                 font=("Segoe UI", 11), bg="#ffffff")
            word_label.pack(side=tk.LEFT)
            
            # Frequency bar
            bar_frame = tk.Frame(word_frame, bg="#e5e7eb", height=10, width=100)
            bar_frame.pack(side=tk.RIGHT, padx=(10, 0))
            bar_frame.pack_propagate(False)
            
            max_freq = max(w['frequency'] for w in words) if words else 1
            bar_width = int((word_data['frequency'] / max_freq) * 100)
            
            if bar_width > 0:
                bar = tk.Frame(bar_frame, bg=color, height=10, width=bar_width)
                bar.pack(side=tk.LEFT)

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
