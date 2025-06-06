from tkinter import messagebox, ttk
from PythonExpenseApp.db_connection import DbConnection
from PythonExpenseApp.expense import Expense
import tkinter as tk
import mysql.connector

class ExpenseGUI:
    """
    Enhanced GUI for managing and recording expenses with multiple participants.
    """
    def __init__(self, root, current_student=None, main_callback=None):
        self.root = root
        self.current_student = current_student # This object now has a .role attribute
        self.main_callback = main_callback
        self.root.title("Advanced Expense Tracker")
        self.root.geometry("1400x800")
        self.root.resizable(True, True)
        self.root.configure(bg='#f8fafc')
        
        # Main container
        main_container = tk.Frame(self.root, bg='#ffffff', relief='solid', bd=1)
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Header with back button
        self.create_header(main_container)
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(main_container)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
          # Create tabs
        self.create_add_expense_tab()
        self.create_debt_tracker_tab()
        
        # Group management is now only available in the Teacher Dashboard
        
        # Status bar
        self.status_frame = tk.Frame(main_container, bg='#e5e7eb', height=30)
        self.status_frame.pack(fill=tk.X, side=tk.BOTTOM)
        self.status_frame.pack_propagate(False)
        
        self.status_label = tk.Label(self.status_frame, text="Ready", 
                                    font=("Segoe UI", 10), bg="#e5e7eb", fg="#64748b")
        self.status_label.pack(side=tk.LEFT, padx=10, pady=5)

    def create_header(self, parent):
        """Create header with title and back button"""
        header_frame = tk.Frame(parent, bg='#ffffff', height=80)
        header_frame.pack(fill=tk.X, padx=20, pady=(20, 10))
        header_frame.pack_propagate(False)
        
        # Back button
        if self.main_callback:
            back_btn = tk.Button(header_frame, text="← Back to Main", 
                                font=("Segoe UI", 12, "bold"), bg="#6b7280", fg="white",
                                relief='flat', bd=0, activebackground="#4b5563",
                                cursor="hand2", command=self.go_back_to_main)
            back_btn.pack(side=tk.LEFT, pady=10)
        
        # Title
        title_label = tk.Label(header_frame, text="💰 Advanced Expense Tracker", 
                              font=("Segoe UI", 24, "bold"), bg="#ffffff", fg="#1e293b")
        title_label.pack(side=tk.LEFT, padx=(20, 0), pady=10)
        
        # User info
        if self.current_student:
            user_info = tk.Label(header_frame, 
                                text=f"User: {self.current_student.name} {getattr(self.current_student, 'surname', '')}", 
                                font=("Segoe UI", 12, "bold"), bg="#ffffff", fg="#059669")
            user_info.pack(side=tk.RIGHT, pady=10)

    def go_back_to_main(self):
        """Close this window and return to main dashboard"""
        self.root.destroy()
        if self.main_callback:
            self.main_callback()

    def create_add_expense_tab(self):
        """Create the add expense tab"""
        add_expense_frame = tk.Frame(self.notebook, bg='#ffffff')
        self.notebook.add(add_expense_frame, text="Add Expense")
        
        # Header
        header_frame = tk.Frame(add_expense_frame, bg='#ffffff', height=60)
        header_frame.pack(fill=tk.X, padx=20, pady=(20, 10), side=tk.TOP)
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(header_frame, text="💰 Add New Expense", 
                              font=("Segoe UI", 24, "bold"), bg="#ffffff", fg="#1e293b")
        title_label.pack(anchor='w')
        
        # Create a container for the canvas and scrollbars
        canvas_container = tk.Frame(add_expense_frame, bg='#ffffff')
        canvas_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # Create Canvas
        canvas = tk.Canvas(canvas_container, bg='#ffffff', highlightthickness=0)
        
        # Create Vertical Scrollbar
        v_scrollbar = ttk.Scrollbar(canvas_container, orient="vertical", command=canvas.yview)
        v_scrollbar.pack(side=tk.RIGHT, fill="y")
        
        # Create Horizontal Scrollbar
        h_scrollbar = ttk.Scrollbar(canvas_container, orient="horizontal", command=canvas.xview)
        h_scrollbar.pack(side=tk.BOTTOM, fill="x")
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        canvas.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # This frame will contain the actual content and be placed inside the canvas
        scrollable_inner_frame = tk.Frame(canvas, bg='#ffffff')
        
        canvas.create_window((0, 0), window=scrollable_inner_frame, anchor="nw")
        
        # Update scrollregion when an event Configure occurs
        scrollable_inner_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        # Main content with three columns - now using scrollable_inner_frame
        # The 'content_frame' variable is now 'scrollable_inner_frame'
        
        # Configure grid on the scrollable_inner_frame
        scrollable_inner_frame.grid_columnconfigure(0, weight=1, minsize=400) # Min size for better layout
        scrollable_inner_frame.grid_columnconfigure(1, weight=1, minsize=400)
        scrollable_inner_frame.grid_columnconfigure(2, weight=1, minsize=400)
        scrollable_inner_frame.grid_rowconfigure(0, weight=1) # Allow vertical expansion of sections
        
        # Payer selection section
        self.create_payer_section(scrollable_inner_frame)
        
        # Participants selection section
        self.create_participants_section(scrollable_inner_frame)
        
        # Expense details section
        self.create_expense_details_section(scrollable_inner_frame)

    def create_payer_section(self, parent):
        """Create the payer selection section"""
        payer_frame = tk.LabelFrame(parent, text="Who Paid?", 
                                   font=("Segoe UI", 14, "bold"), bg="#ffffff", 
                                   fg="#1e293b", relief='solid', bd=2)
        payer_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 5), pady=10)
        
        # Search frame
        search_frame = tk.Frame(payer_frame, bg="#ffffff")
        search_frame.pack(fill=tk.X, padx=15, pady=15)
        
        tk.Label(search_frame, text="Search Student:", font=("Segoe UI", 12, "bold"), 
                bg="#ffffff", fg="#374151").pack(anchor='w', pady=(0, 5))
        
        self.payer_search_entry = tk.Entry(search_frame, font=("Segoe UI", 12))
        self.payer_search_entry.pack(fill=tk.X, pady=(0, 10), ipady=6)
        self.payer_search_entry.bind('<KeyRelease>', self.on_payer_search)
        
        # Payer listbox
        payer_list_frame = tk.Frame(payer_frame, bg="#ffffff")
        payer_list_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 15))
        
        payer_scrollbar = tk.Scrollbar(payer_list_frame)
        payer_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.payer_listbox = tk.Listbox(payer_list_frame, font=("Segoe UI", 11), 
                                       yscrollcommand=payer_scrollbar.set,
                                       selectmode=tk.SINGLE)
        self.payer_listbox.pack(fill=tk.BOTH, expand=True)
        payer_scrollbar.config(command=self.payer_listbox.yview)
        
        # Selected payer display
        self.selected_payer_label = tk.Label(payer_frame, text="Selected: None", 
                                            font=("Segoe UI", 11, "bold"), 
                                            bg="#ffffff", fg="#059669")
        self.selected_payer_label.pack(padx=15, pady=(0, 15))
        
        self.selected_payer = None
        self.load_students_for_payer()

    def create_participants_section(self, parent):
        """Create the participants selection section"""
        participants_frame = tk.LabelFrame(parent, text="Who Owes Money?", 
                                          font=("Segoe UI", 14, "bold"), bg="#ffffff", 
                                          fg="#1e293b", relief='solid', bd=2)
        participants_frame.grid(row=0, column=1, sticky="nsew", padx=5, pady=10)
        
        # Search frame
        search_frame = tk.Frame(participants_frame, bg="#ffffff")
        search_frame.pack(fill=tk.X, padx=15, pady=15)
        
        tk.Label(search_frame, text="Search Students:", font=("Segoe UI", 12, "bold"), 
                bg="#ffffff", fg="#374151").pack(anchor='w', pady=(0, 5))
        
        self.participants_search_entry = tk.Entry(search_frame, font=("Segoe UI", 12))
        self.participants_search_entry.pack(fill=tk.X, pady=(0, 10), ipady=6)
        self.participants_search_entry.bind('<KeyRelease>', self.on_participants_search)
        
        # Available students listbox
        available_frame = tk.Frame(participants_frame, bg="#ffffff")
        available_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 10))
        
        tk.Label(available_frame, text="Available Students:", font=("Segoe UI", 10, "bold"), 
                bg="#ffffff", fg="#374151").pack(anchor='w', pady=(0, 5))
        
        available_list_frame = tk.Frame(available_frame, bg="#ffffff")
        available_list_frame.pack(fill=tk.BOTH, expand=True)
        
        available_scrollbar = tk.Scrollbar(available_list_frame)
        available_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.available_listbox = tk.Listbox(available_list_frame, font=("Segoe UI", 10), 
                                           yscrollcommand=available_scrollbar.set,
                                           selectmode=tk.MULTIPLE)
        self.available_listbox.pack(fill=tk.BOTH, expand=True)
        available_scrollbar.config(command=self.available_listbox.yview)
        
        # Buttons frame
        buttons_frame = tk.Frame(participants_frame, bg="#ffffff")
        buttons_frame.pack(fill=tk.X, padx=15, pady=10)
        
        add_btn = tk.Button(buttons_frame, text="Add →", font=("Segoe UI", 10, "bold"),
                           bg="#3b82f6", fg="white", command=self.add_participants)
        add_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        remove_btn = tk.Button(buttons_frame, text="← Remove", font=("Segoe UI", 10, "bold"),
                              bg="#dc2626", fg="white", command=self.remove_participants)
        remove_btn.pack(side=tk.LEFT, padx=5)
        
        clear_btn = tk.Button(buttons_frame, text="Clear All", font=("Segoe UI", 10, "bold"),
                             bg="#6b7280", fg="white", command=self.clear_participants)
        clear_btn.pack(side=tk.LEFT, padx=5)
        
        # Selected participants listbox
        selected_frame = tk.Frame(participants_frame, bg="#ffffff")
        selected_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 15))
        
        tk.Label(selected_frame, text="Selected Participants:", font=("Segoe UI", 10, "bold"), 
                bg="#ffffff", fg="#374151").pack(anchor='w', pady=(0, 5))
        
        selected_list_frame = tk.Frame(selected_frame, bg="#ffffff")
        selected_list_frame.pack(fill=tk.BOTH, expand=True)
        
        selected_scrollbar = tk.Scrollbar(selected_list_frame)
        selected_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.selected_listbox = tk.Listbox(selected_list_frame, font=("Segoe UI", 10), 
                                          yscrollcommand=selected_scrollbar.set,
                                          selectmode=tk.MULTIPLE)
        self.selected_listbox.pack(fill=tk.BOTH, expand=True)
        selected_scrollbar.config(command=self.selected_listbox.yview)
        
        self.selected_participants = []
        self.load_students_for_participants()

    def create_expense_details_section(self, parent):
        """Create the expense details section"""
        details_frame = tk.LabelFrame(parent, text="Expense Details", 
                                     font=("Segoe UI", 14, "bold"), bg="#ffffff", 
                                     fg="#1e293b", relief='solid', bd=2)
        details_frame.grid(row=0, column=2, sticky="nsew", padx=(5, 0), pady=10)
        
        # Form frame
        form_frame = tk.Frame(details_frame, bg="#ffffff")
        form_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Amount field
        tk.Label(form_frame, text="Total Amount (€):", font=("Segoe UI", 12, "bold"), 
                bg="#ffffff", fg="#374151").pack(anchor='w', pady=(0, 5))
        
        self.amount_entry = tk.Entry(form_frame, font=("Segoe UI", 12))
        self.amount_entry.pack(fill=tk.X, pady=(0, 15), ipady=6)
        
        # Description field
        tk.Label(form_frame, text="Description:", font=("Segoe UI", 12, "bold"), 
                bg="#ffffff", fg="#374151").pack(anchor='w', pady=(0, 5))
        
        self.desc_entry = tk.Entry(form_frame, font=("Segoe UI", 12))
        self.desc_entry.pack(fill=tk.X, pady=(0, 15), ipady=6)
        
        # Split method
        tk.Label(form_frame, text="Split Method:", font=("Segoe UI", 12, "bold"), 
                bg="#ffffff", fg="#374151").pack(anchor='w', pady=(0, 5))
        
        self.split_var = tk.StringVar(value="equal")
        split_frame = tk.Frame(form_frame, bg="#ffffff")
        split_frame.pack(fill=tk.X, pady=(0, 15))
        
        tk.Radiobutton(split_frame, text="Equal Split", variable=self.split_var, 
                      value="equal", bg="#ffffff", font=("Segoe UI", 11)).pack(anchor='w')
        tk.Radiobutton(split_frame, text="Custom Split", variable=self.split_var, 
                      value="custom", bg="#ffffff", font=("Segoe UI", 11)).pack(anchor='w')
        
        # Summary
        summary_frame = tk.LabelFrame(form_frame, text="Summary", 
                                     font=("Segoe UI", 11, "bold"), bg="#f8fafc")
        summary_frame.pack(fill=tk.X, pady=15)
        
        self.summary_label = tk.Label(summary_frame, text="Select payer and participants", 
                                     font=("Segoe UI", 10), bg="#f8fafc", fg="#64748b",
                                     justify=tk.LEFT, wraplength=300)
        self.summary_label.pack(padx=10, pady=10)
        
        # Add expense button
        add_btn = tk.Button(form_frame, text="Add Expense", font=("Segoe UI", 14, "bold"), 
                           bg="#059669", fg="#ffffff", relief='flat', bd=0,
                           activebackground="#047857", cursor="hand2", 
                           command=self.add_expense)
        add_btn.pack(fill=tk.X, pady=20, ipady=12)
        
        # Bind events to update summary
        self.payer_listbox.bind('<<ListboxSelect>>', self.update_summary)
        self.amount_entry.bind('<KeyRelease>', self.update_summary)

    def create_debt_tracker_tab(self):
        """Create the debt tracker tab"""
        debt_frame = tk.Frame(self.notebook, bg='#ffffff')
        self.notebook.add(debt_frame, text="Debt Tracker")
        
        # Header
        header_frame = tk.Frame(debt_frame, bg='#ffffff', height=60)
        header_frame.pack(fill=tk.X, padx=20, pady=(20, 10))
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(header_frame, text="📊 Debt Tracker", 
                              font=("Segoe UI", 24, "bold"), bg="#ffffff", fg="#1e293b")
        title_label.pack(anchor='w')
        
        # Content frame
        content_frame = tk.Frame(debt_frame, bg='#ffffff')
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Configure grid
        content_frame.grid_columnconfigure(0, weight=1)
        content_frame.grid_columnconfigure(1, weight=1)
        content_frame.grid_rowconfigure(0, weight=1)
        
        # People who owe you money
        owe_you_frame = tk.LabelFrame(content_frame, text="People Who Owe You Money", 
                                     font=("Segoe UI", 14, "bold"), bg="#ffffff", 
                                     fg="#dc2626", relief='solid', bd=2)
        owe_you_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10), pady=10)
        
        owe_you_list_frame = tk.Frame(owe_you_frame, bg="#ffffff")
        owe_you_list_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        owe_you_scrollbar = tk.Scrollbar(owe_you_list_frame)
        owe_you_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.owe_you_listbox = tk.Listbox(owe_you_list_frame, font=("Segoe UI", 11), 
                                         yscrollcommand=owe_you_scrollbar.set)
        self.owe_you_listbox.pack(fill=tk.BOTH, expand=True)
        owe_you_scrollbar.config(command=self.owe_you_listbox.yview)
        
        # People you owe money to
        you_owe_frame = tk.LabelFrame(content_frame, text="People You Owe Money To", 
                                     font=("Segoe UI", 14, "bold"), bg="#ffffff", 
                                     fg="#059669", relief='solid', bd=2)
        you_owe_frame.grid(row=0, column=1, sticky="nsew", padx=(10, 0), pady=10)
        
        you_owe_list_frame = tk.Frame(you_owe_frame, bg="#ffffff")
        you_owe_list_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        you_owe_scrollbar = tk.Scrollbar(you_owe_list_frame)
        you_owe_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.you_owe_listbox = tk.Listbox(you_owe_list_frame, font=("Segoe UI", 11), 
                                         yscrollcommand=you_owe_scrollbar.set)
        self.you_owe_listbox.pack(fill=tk.BOTH, expand=True)
        you_owe_scrollbar.config(command=self.you_owe_listbox.yview)
        
        # Refresh button
        refresh_btn = tk.Button(debt_frame, text="Refresh Debts", font=("Segoe UI", 12, "bold"),
                               bg="#3b82f6", fg="white", command=self.load_debts)
        refresh_btn.pack(pady=20)
        
        # Load initial debt data
        self.load_debts()

    def load_students_for_payer(self):
        """Load all students for payer selection"""
        connection = DbConnection.connect()
        if connection:
            try:
                cursor = connection.cursor()
                cursor.execute("SELECT id, name, surname FROM students ORDER BY name, surname")
                students = cursor.fetchall()
                
                self.payer_listbox.delete(0, tk.END)
                self.all_students = []
                
                for student_id, name, surname in students:
                    display_text = f"{name} {surname}"
                    self.payer_listbox.insert(tk.END, display_text)
                    self.all_students.append((student_id, name, surname))
                    
                connection.close()
            except Exception as e:
                self.status_label.config(text=f"Error loading students: {e}")

    def load_students_for_participants(self):
        """Load all students for participants selection"""
        connection = DbConnection.connect()
        if connection:
            try:
                cursor = connection.cursor()
                cursor.execute("SELECT id, name, surname FROM students ORDER BY name, surname")
                students = cursor.fetchall()
                
                self.available_listbox.delete(0, tk.END)
                self.all_participants = []
                
                for student_id, name, surname in students:
                    display_text = f"{name} {surname}"
                    self.available_listbox.insert(tk.END, display_text)
                    self.all_participants.append((student_id, name, surname))
                    
                connection.close()
            except Exception as e:
                self.status_label.config(text=f"Error loading students: {e}")

    def on_payer_search(self, event):
        """Handle payer search"""
        search_term = self.payer_search_entry.get().lower()
        self.payer_listbox.delete(0, tk.END)
        
        for i, (student_id, name, surname) in enumerate(self.all_students):
            if search_term in f"{name} {surname}".lower():
                display_text = f"{name} {surname}"
                self.payer_listbox.insert(tk.END, display_text)

    def on_participants_search(self, event):
        """Handle participants search"""
        search_term = self.participants_search_entry.get().lower()
        self.available_listbox.delete(0, tk.END)
        
        for i, (student_id, name, surname) in enumerate(self.all_participants):
            if search_term in f"{name} {surname}".lower():
                display_text = f"{name} {surname}"
                self.available_listbox.insert(tk.END, display_text)

    def add_participants(self):
        """Add selected participants to the selected list"""
        selections = self.available_listbox.curselection()
        for i in selections:
            participant_text = self.available_listbox.get(i)
            # Find the corresponding student data
            for student_id, name, surname in self.all_participants:
                if f"{name} {surname}" == participant_text:
                    if (student_id, name, surname) not in self.selected_participants:
                        self.selected_participants.append((student_id, name, surname))
                        self.selected_listbox.insert(tk.END, participant_text)
                    break
        self.update_summary()

    def remove_participants(self):
        """Remove selected participants from the selected list"""
        selections = self.selected_listbox.curselection()
        for i in reversed(selections):  # Remove from end to avoid index issues
            participant_text = self.selected_listbox.get(i)
            # Find and remove from selected_participants
            for j, (student_id, name, surname) in enumerate(self.selected_participants):
                if f"{name} {surname}" == participant_text:
                    self.selected_participants.pop(j)
                    break
            self.selected_listbox.delete(i)
        self.update_summary()

    def clear_participants(self):
        """Clear all selected participants"""
        self.selected_participants.clear()
        self.selected_listbox.delete(0, tk.END)
        self.update_summary()

    def update_summary(self, event=None):
        """Update the expense summary"""
        # Get selected payer
        payer_selection = self.payer_listbox.curselection()
        if payer_selection:
            payer_text = self.payer_listbox.get(payer_selection[0])
            self.selected_payer_label.config(text=f"Selected: {payer_text}")
            
            # Find payer data
            for student_id, name, surname in self.all_students:
                if f"{name} {surname}" == payer_text:
                    self.selected_payer = (student_id, name, surname)
                    break
        else:
            self.selected_payer = None
            self.selected_payer_label.config(text="Selected: None")
        
        # Update summary
        try:
            amount = float(self.amount_entry.get() or 0)
            num_participants = len(self.selected_participants)
            
            if self.selected_payer and num_participants > 0 and amount > 0:
                per_person = amount / num_participants
                summary_text = f"Payer: {self.selected_payer[1]} {self.selected_payer[2]}\n"
                summary_text += f"Total: €{amount:.2f}\n"
                summary_text += f"Participants: {num_participants}\n"
                summary_text += f"Per person: €{per_person:.2f}"
            else:
                summary_text = "Select payer, participants, and enter amount"
                
            self.summary_label.config(text=summary_text)
        except ValueError:
            self.summary_label.config(text="Enter valid amount")

    def add_expense(self):
        """Add the expense to the database"""
        if not self.selected_payer:
            messagebox.showerror("Error", "Please select who paid for the expense.")
            return
            
        if not self.selected_participants:
            messagebox.showerror("Error", "Please select participants who owe money.")
            return
            
        try:
            amount = float(self.amount_entry.get())
            description = self.desc_entry.get().strip()
            
            if amount <= 0:
                messagebox.showerror("Error", "Amount must be greater than 0.")
                return
                
            if not description:
                messagebox.showerror("Error", "Please enter a description.")
                return
                
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid amount.")
            return
        
        # Calculate split
        per_person = amount / len(self.selected_participants)
        
        # Save to database
        connection = DbConnection.connect()
        if not connection:
            messagebox.showerror("Error", "Could not connect to database.")
            return
            
        try:
            cursor = connection.cursor()
            
            # Insert main expense record
            cursor.execute("""INSERT INTO expenses (amount, description, date, id_giver, id_receiver, id_activity)
                             VALUES (%s, %s, CURDATE(), %s, NULL, NULL)""",
                          (amount, description, self.selected_payer[0]))
            expense_id = cursor.lastrowid
            
            # Insert debt records for each participant
            for participant_id, name, surname in self.selected_participants:
                cursor.execute("""INSERT INTO debts (payer_id, debtor_id, amount, description, expense_id, date_created)
                                 VALUES (%s, %s, %s, %s, %s, CURDATE())""",
                              (self.selected_payer[0], participant_id, per_person, description, expense_id))
            
            connection.commit()
            messagebox.showinfo("Success", f"Expense added successfully!\nEach participant owes €{per_person:.2f}")
            
            # Clear form
            self.amount_entry.delete(0, tk.END)
            self.desc_entry.delete(0, tk.END)
            self.clear_participants()
            self.payer_listbox.selection_clear(0, tk.END)
            self.selected_payer = None
            self.selected_payer_label.config(text="Selected: None")
            self.update_summary()
            
            # Refresh debt tracker
            self.load_debts()
            
        except Exception as e:
            messagebox.showerror("Error", f"Could not save expense: {e}")
        finally:
            connection.close()

    def load_debts(self):
        """Load debt information for the current user"""
        connection = DbConnection.connect()
        if not connection:
            return
        try:
            cursor = connection.cursor()
            
            # Clear existing lists
            self.owe_you_listbox.delete(0, tk.END)
            self.you_owe_listbox.delete(0, tk.END)
            
            # If we have a current student, filter debts for them
            if self.current_student:
                # Get debts where others owe the current student money
                cursor.execute("""SELECT s.name, s.surname, SUM(d.amount), COUNT(d.id)
                                 FROM debts d
                                 JOIN students s ON d.debtor_id = s.id
                                 WHERE d.paid = FALSE AND d.payer_id = %s
                                 GROUP BY d.debtor_id, s.name, s.surname
                                 ORDER BY SUM(d.amount) DESC""", (self.current_student.id,))
                
                total_owed_to_you = 0
                for name, surname, amount, count in cursor.fetchall():
                    self.owe_you_listbox.insert(tk.END, f"{name} {surname}: €{amount:.2f} ({count} expenses)")
                    total_owed_to_you += amount
                    
                if total_owed_to_you > 0:
                    self.owe_you_listbox.insert(tk.END, "")
                    self.owe_you_listbox.insert(tk.END, f"TOTAL OWED TO YOU: €{total_owed_to_you:.2f}")
                
                # Get debts where the current student owes others money
                cursor.execute("""SELECT s.name, s.surname, SUM(d.amount), COUNT(d.id)
                                 FROM debts d
                                 JOIN students s ON d.payer_id = s.id
                                 WHERE d.paid = FALSE AND d.debtor_id = %s
                                 GROUP BY d.payer_id, s.name, s.surname
                                 ORDER BY SUM(d.amount) DESC""", (self.current_student.id,))
                
                total_you_owe = 0
                for name, surname, amount, count in cursor.fetchall():
                    self.you_owe_listbox.insert(tk.END, f"{name} {surname}: €{amount:.2f} ({count} expenses)")
                    total_you_owe += amount
                    
                if total_you_owe > 0:
                    self.you_owe_listbox.insert(tk.END, "")
                    self.you_owe_listbox.insert(tk.END, f"TOTAL YOU OWE: €{total_you_owe:.2f}")
            else:
                # Show all debts if no specific user
                # Get debts where others owe you money
                cursor.execute("""SELECT s.name, s.surname, SUM(d.amount), COUNT(d.id)
                                 FROM debts d
                                 JOIN students s ON d.debtor_id = s.id
                                 WHERE d.paid = FALSE
                                 GROUP BY d.debtor_id, s.name, s.surname
                                 ORDER BY SUM(d.amount) DESC""")
                
                total_owed_to_you = 0
                for name, surname, amount, count in cursor.fetchall():
                    self.owe_you_listbox.insert(tk.END, f"{name} {surname}: €{amount:.2f} ({count} expenses)")
                    total_owed_to_you += amount
                    
                if total_owed_to_you > 0:
                    self.owe_you_listbox.insert(tk.END, "")
                    self.owe_you_listbox.insert(tk.END, f"TOTAL OWED TO YOU: €{total_owed_to_you:.2f}")
                
                # Get debts where you owe others money
                cursor.execute("""SELECT s.name, s.surname, SUM(d.amount), COUNT(d.id)
                                 FROM debts d
                                 JOIN students s ON d.payer_id = s.id
                                 WHERE d.paid = FALSE
                                 GROUP BY d.payer_id, s.name, s.surname
                                 ORDER BY SUM(d.amount) DESC""")
                
                total_you_owe = 0
                for name, surname, amount, count in cursor.fetchall():
                    self.you_owe_listbox.insert(tk.END, f"{name} {surname}: €{amount:.2f} ({count} expenses)")
                    total_you_owe += amount
                    
                if total_you_owe > 0:
                    self.you_owe_listbox.insert(tk.END, "")
                    self.you_owe_listbox.insert(tk.END, f"TOTAL YOU OWE: €{total_you_owe:.2f}")
        except Exception as err:
            self.status_label.config(text=f"Error loading debts: {err}")
        finally:
            connection.close()

# End of ExpenseGUI class
# All group management code has been removed. Teachers use the Teacher Dashboard for these features.