import tkinter as tk
from tkinter import messagebox
from PythonExpenseApp.db_connection import DbConnection
from PythonExpenseApp.student import Student


class LoginGUI:
    def __init__(self, root, on_login_success):
        self.root = root
        self.root.title("Trip Manager - Login")
        self.root.geometry("650x750")  # Increased from 500x450 to 600x550
        self.root.resizable(True, True)
        self.root.configure(bg='#f8fafc')
        self.on_login_success = on_login_success
        
        # Center the window
        self.root.eval('tk::PlaceWindow . center')
        
        self.create_widgets()

    def create_widgets(self):
        # Main container
        main_container = tk.Frame(self.root, bg='#ffffff', relief='solid', bd=1)
        main_container.pack(fill=tk.BOTH, expand=True, padx=50, pady=50)
        
        # Header
        header_frame = tk.Frame(main_container, bg='#ffffff', height=80)
        header_frame.pack(fill=tk.X, padx=40, pady=(40, 20))
        header_frame.pack_propagate(False)
        
        # Exit button
        exit_btn = tk.Button(header_frame, text="✕ Exit", 
                            font=("Segoe UI", 12, "bold"), bg="#dc2626", fg="white",
                            relief='flat', bd=0, activebackground="#b91c1c",
                            cursor="hand2", command=self.root.quit)
        exit_btn.pack(side=tk.RIGHT, anchor='ne', pady=10)
        
        title_label = tk.Label(header_frame, text="🎓 Trip Manager", 
                              font=("Segoe UI", 32, "bold"), bg="#ffffff", fg="#1e293b")
        title_label.pack(anchor='w')
        
        subtitle_label = tk.Label(header_frame, text="Student Login Portal", 
                                 font=("Segoe UI", 16), bg="#ffffff", fg="#64748b")
        subtitle_label.pack(anchor='w', pady=(5, 0))
        
        # Form section
        form_frame = tk.Frame(main_container, bg='#ffffff')
        form_frame.pack(fill=tk.BOTH, expand=True, padx=50, pady=30)  # Increased padding
        
        # Username field
        tk.Label(form_frame, text="Username", font=("Segoe UI", 14, "bold"), 
                bg="#ffffff", fg="#374151").pack(anchor='w', pady=(15, 8))  # Increased spacing
        
        self.username_entry = tk.Entry(form_frame, font=("Segoe UI", 16), bg="#ffffff", 
                                      fg="#1f2937", relief='solid', bd=1)
        self.username_entry.pack(fill=tk.X, pady=(0, 20), ipady=10)  # Increased spacing and padding
        
        # Password field
        tk.Label(form_frame, text="Password", font=("Segoe UI", 14, "bold"), 
                bg="#ffffff", fg="#374151").pack(anchor='w', pady=(0, 8))
        
        self.password_entry = tk.Entry(form_frame, font=("Segoe UI", 16), bg="#ffffff", 
                                      fg="#1f2937", relief='solid', bd=1, show="*")
        self.password_entry.pack(fill=tk.X, pady=(0, 25), ipady=10)  # Increased spacing and padding
        
        # Login button
        login_btn = tk.Button(form_frame, text="Sign In", font=("Segoe UI", 16, "bold"), 
                             bg="#3b82f6", fg="#ffffff", relief='flat', bd=0,
                             activebackground="#2563eb", activeforeground="#ffffff", 
                             cursor="hand2", command=self.login)
        login_btn.pack(fill=tk.X, pady=15, ipady=15)  # Increased button padding
        
        # Feedback area
        self.feedback_label = tk.Label(form_frame, text="", font=("Segoe UI", 14), 
                                      bg="#ffffff", fg="#dc2626")
        self.feedback_label.pack(pady=(15, 0))
        
        # Bind Enter key to login
        self.root.bind('<Return>', lambda e: self.login())
        
        # Focus on username field
        self.username_entry.focus()

    def login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        
        if not username or not password:
            self.feedback_label.config(text="Please enter both username and password.")
            return
            
        connection = DbConnection.connect()
        if connection:
            try:
                cursor = connection.cursor()
                sql = "SELECT id, name, surname, class, age, special_needs FROM students WHERE username=%s AND password=%s"
                cursor.execute(sql, (username, password))
                result = cursor.fetchone()
                
                if result:
                    student = Student(result[1], result[2], result[4], result[5])
                    student.id = result[0]
                    student.class_ = result[3]
                    connection.close()
                    self.root.destroy()
                    self.on_login_success(student)
                else:
                    self.feedback_label.config(text="Invalid username or password.")
                    # Clear password field for security
                    self.password_entry.delete(0, tk.END)
                connection.close()
            except Exception as e:
                self.feedback_label.config(text=f"Database error: {e}")
                connection.close()
        else:
            self.feedback_label.config(text="Could not connect to the database.")
