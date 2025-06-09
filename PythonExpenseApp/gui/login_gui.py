import tkinter as tk
from tkinter import messagebox
from db_connection import DbConnection
from student import Student  # Assuming Student class can hold role


class LoginGUI:
    def __init__(self, root, on_login_success):
        """
        Initialize the LoginGUI window.
        
        Args:
            root (tk.Tk): The root Tkinter window instance.
            on_login_success (function): Callback function to be called after successful login, receives the current_user object.
        """
        self.root = root  # The main Tkinter window for the login GUI
        self.root.title("Trip Manager - Login")  # Set the window title
        self.root.geometry("650x800")  # Set the window size (width x height)
        self.root.resizable(True, True)  # Allow window resizing in both directions
        self.root.configure(bg='#f8fafc')  # Set the background color of the window
        self.on_login_success = on_login_success  # Callback for successful login
        
        # Center the window on the screen
        self.root.eval('tk::PlaceWindow . center')
        
        self.create_widgets()  # Build and place all widgets in the window

    def create_widgets(self):
        """
        Create and arrange all widgets (labels, entries, buttons) for the login form.
        """
        # Main container frame for the login form
        main_container = tk.Frame(self.root, bg='#ffffff', relief='solid', bd=1)
        main_container.pack(fill=tk.BOTH, expand=True, padx=50, pady=50)
        
        # Header section containing the title and exit button
        header_frame = tk.Frame(main_container, bg='#ffffff', height=100)
        header_frame.pack(fill=tk.X, padx=40, pady=(40, 20))
        header_frame.pack_propagate(False)
        
        # Exit button to close the application
        exit_btn = tk.Button(header_frame, text="✕ Exit", 
                            font=("Segoe UI", 12, "bold"), bg="#dc2626", fg="white",
                            relief='flat', bd=0, activebackground="#b91c1c",
                            cursor="hand2", command=self.root.quit)
        exit_btn.pack(side=tk.RIGHT, anchor='ne', pady=10)
        
        # Main title label for the application
        title_label = tk.Label(header_frame, text="🎓 Trip Manager", 
                              font=("Segoe UI", 32, "bold"), bg="#ffffff", fg="#1e293b")
        title_label.pack(anchor='w')
        
        # Subtitle label for the login portal
        subtitle_label = tk.Label(header_frame, text="Login Portal", 
                                 font=("Segoe UI", 16), bg="#ffffff", fg="#64748b")
        subtitle_label.pack(anchor='w', pady=(5, 0))
        
        # Form section for username and password fields
        form_frame = tk.Frame(main_container, bg='#ffffff')
        form_frame.pack(fill=tk.BOTH, expand=True, padx=50, pady=30)  # Increased padding
        
        # Username label
        tk.Label(form_frame, text="Username", font=("Segoe UI", 14, "bold"), 
                bg="#ffffff", fg="#374151").pack(anchor='w', pady=(15, 8))  # Increased spacing
        
        # Username entry field for user input
        self.username_entry = tk.Entry(form_frame, font=("Segoe UI", 16), bg="#ffffff", 
                                      fg="#1f2937", relief='solid', bd=1)
        self.username_entry.pack(fill=tk.X, pady=(0, 20), ipady=10)  # Increased spacing and padding
        
        # Password label
        tk.Label(form_frame, text="Password", font=("Segoe UI", 14, "bold"), 
                bg="#ffffff", fg="#374151").pack(anchor='w', pady=(0, 8))
        
        # Password entry field for user input (masked)
        self.password_entry = tk.Entry(form_frame, font=("Segoe UI", 16), bg="#ffffff", 
                                      fg="#1f2937", relief='solid', bd=1, show="*")
        self.password_entry.pack(fill=tk.X, pady=(0, 25), ipady=10)  # Increased spacing and padding
        
        # Login button to submit credentials
        login_btn = tk.Button(form_frame, text="Sign In", font=("Segoe UI", 16, "bold"), 
                             bg="#3b82f6", fg="#ffffff", relief='flat', bd=0,
                             activebackground="#2563eb", activeforeground="#ffffff", 
                             cursor="hand2", command=self.login)
        login_btn.pack(fill=tk.X, pady=15, ipady=15)  # Increased button padding
        
        # Feedback label to display error or status messages
        self.feedback_label = tk.Label(form_frame, text="", font=("Segoe UI", 14), 
                                      bg="#ffffff", fg="#dc2626")
        self.feedback_label.pack(pady=(15, 0))
        
        # Bind the Enter key to trigger the login function
        self.root.bind('<Return>', lambda e: self.login())
        # Focus on the username entry field by default
        self.username_entry.focus()

    def login(self):
        """
        Handle the login process: validate input, check credentials against the database,
        provide feedback, and call the success callback if login is successful.
        """
        username = self.username_entry.get().strip()  # Get the entered username (email), remove whitespace
        password = self.password_entry.get().strip()  # Get the entered password, remove whitespace
        
        if not username or not password:
            # Show feedback if either field is empty
            self.feedback_label.config(text="Please enter both username and password.")
            return
            
        connection = DbConnection.connect()  # Establish a connection to the database
        if connection:
            try:
                cursor = connection.cursor()  # Create a cursor for executing SQL queries
                # Use plain text password comparison (for demonstration; not secure for production)
                query = "SELECT id, name, surname, email, password, special_needs, role, class, age FROM students WHERE email = %s"
                cursor.execute(query, (username,))  # Execute the query with the provided username (email)
                result = cursor.fetchone()  # Fetch the first matching record
                connection.close()

                if result:
                    user_id, name, surname, email, stored_password, special_needs, role, class_, age = result
                    if stored_password == password:  # Controlla se la password inserita corrisponde a quella salvata nel database
                        current_user = Student(name, surname, age, special_needs)  # Crea un oggetto Student con i dati dell'utente
                        current_user.class_ = class_  # Assegna la classe all'oggetto Student
                        current_user.id = user_id  # Assegna l'ID all'oggetto Student
                        current_user.email = email  # Assegna l'email all'oggetto Student
                        setattr(current_user, 'role', role)  # Imposta il ruolo (es. student, teacher) nell'oggetto Student

                        # Show a success message and close the login window
                        messagebox.showinfo("Login Successful", f"Welcome {name} {surname} ({role})!", parent=self.root)  # Mostra un messaggio di successo
                        self.root.destroy()  # Chiude la finestra di login
                        if self.on_login_success:  # Se è stata fornita una callback per il login
                            self.on_login_success(current_user)  # Chiama la callback passando l'oggetto utente loggato
                    else:
                        # Show error if password does not match
                        messagebox.showerror("Login Failed", "Invalid username or password.", parent=self.root)  # Mostra errore se la password non corrisponde
                else:
                    # Show error if no user is found with the given username
                    messagebox.showerror("Login Failed", "Invalid username or password.", parent=self.root)  # Mostra errore se l'utente non esiste
            except Exception as e:
                # Show error if a database or query error occurs
                messagebox.showerror("Login Error", f"An error occurred: {e}", parent=self.root)  # Mostra errore se c'è un problema con il database o la query
        else:
            # Show error if the database connection fails
            messagebox.showerror("Database Error", "Could not connect to the database.", parent=self.root)  # Mostra errore se la connessione al database fallisce
