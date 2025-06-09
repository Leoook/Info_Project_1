import sys  # Importa il modulo sys per gestire il path e l'uscita dal programma
import os  # Importa il modulo os per operazioni sul filesystem

# _main_file_directory: The directory where this main.py file is located.
_main_file_directory = os.path.dirname(os.path.abspath(__file__))  # Ottiene la directory dove si trova main.py

# _project_root_directory: The root directory of the project, one level above main.py.
_project_root_directory = os.path.dirname(_main_file_directory)  # Ottiene la directory principale del progetto (un livello sopra)

# Ensure the project root directory is in sys.path for module imports.
if _project_root_directory not in sys.path:  # Controlla se la root del progetto è già nel sys.path
    sys.path.insert(0, _project_root_directory)  # Se non c'è, la aggiunge per permettere gli import dei moduli

import tkinter as tk  # Importa la libreria Tkinter per la GUI
from tkinter import messagebox  # Importa il modulo messagebox per mostrare messaggi popup
from gui.expense_gui import ExpenseGUI  # Importa la GUI delle spese
from gui.activity_form_gui import ActivityFormGUI  # Importa la GUI per iscrizione attività
from gui.login_gui import LoginGUI  # Importa la GUI di login
from gui.dashboard_gui import DashboardGUI  # Importa la dashboard per studenti
from gui.teacher_dashboard import TeacherDashboard  # Importa la dashboard per insegnanti
from db_connection import DbConnection  # Importa la classe per la connessione al database

# Global variable to store the currently logged-in student object.
# This variable is updated after a successful login and is used throughout the session.
logged_in_student = None  # Variabile globale che contiene l'utente loggato

def show_main_dashboard():
    """
    Displays the main dashboard window.
    If a student is already logged in, it calls on_login_success to show the appropriate dashboard.
    Otherwise, it launches the login window.
    """
    global logged_in_student  # Usa la variabile globale
    if logged_in_student:  # Se c'è già uno studente loggato
        on_login_success(logged_in_student)  # Mostra la dashboard appropriata
    else:
        # If no logged in student, show login window.
        root = tk.Tk()  # Crea la finestra principale Tkinter
        login = LoginGUI(root, on_login_success)  # Crea la finestra di login e passa la callback
        root.mainloop()  # Avvia il ciclo principale della GUI

def show_expense_gui():
    """
    Launches the Expense GUI window for the logged-in student.
    This window allows the student to manage and view their expenses.
    """
    root = tk.Tk()  # Crea una nuova finestra Tkinter
    app = ExpenseGUI(root, logged_in_student, show_main_dashboard)  # Avvia la GUI delle spese
    root.mainloop()  # Avvia il ciclo principale della GUI

def show_activity_form():
    """
    Launches the Activity Subscription GUI window for the logged-in student.
    This window allows the student to subscribe to or manage activities.
    """
    global logged_in_student  # Usa la variabile globale
    root = tk.Tk()  # Crea una nuova finestra Tkinter
    app = ActivityFormGUI(root, logged_in_student, show_main_dashboard)  # Avvia la GUI delle attività
    root.mainloop()  # Avvia il ciclo principale della GUI

def on_login_success(student):
    """
    Callback function called after a successful login.
    Sets the global logged_in_student variable and launches the appropriate dashboard
    based on the user's role (student or teacher).

    :param student: Student object - The student who has logged in.
    """
    global logged_in_student  # Usa la variabile globale
    logged_in_student = student  # Aggiorna la variabile con l'utente loggato

    # Check if user is a teacher and redirect to teacher dashboard
    if hasattr(student, 'role') and student.role == 'teacher':  # Se l'utente è un insegnante
        # Launch the teacher dashboard GUI for users with the 'teacher' role.
        root = tk.Tk()  # Crea una nuova finestra Tkinter
        teacher_dashboard = TeacherDashboard(root, student, show_main_dashboard)  # Avvia la dashboard insegnante
        root.mainloop()  # Avvia il ciclo principale della GUI
    else:
        # Launch the regular student dashboard GUI for students.
        root = tk.Tk()  # Crea una nuova finestra Tkinter
        # Pass the callbacks for showing other GUIs (expenses, activities).
        dashboard = DashboardGUI(root, student, show_expense_gui, show_activity_form)  # Avvia la dashboard studente
        root.mainloop()  # Avvia il ciclo principale della GUI

# Main entry point for the application
if __name__ == "__main__":  # Esegue questo blocco solo se il file è eseguito direttamente (non importato)
    # Check database connection before starting the GUI.
    # If the connection fails, show an error message and exit.
    connection = DbConnection.connect()  # Tenta di connettersi al database
    if not connection:  # Se la connessione fallisce
        temp_root = tk.Tk()  # Crea una finestra Tkinter temporanea
        temp_root.withdraw()  # Nasconde la finestra
        messagebox.showerror(
            "Database Error",
            "Could not connect to the database. Please check your connection settings.",
            parent=temp_root
        )  # Mostra un messaggio di errore
        temp_root.destroy()  # Distrugge la finestra temporanea
        sys.exit(1)  # Esce dal programma con errore
    # Show login window first.
    root = tk.Tk()  # Crea la finestra principale Tkinter
    login = LoginGUI(root, on_login_success)  # Avvia la finestra di login
    root.mainloop()  # Avvia il ciclo principale della GUI

# No changes needed in this file based on the current request,
# as the student object passed around will implicitly carry the role.
# The logic for handling the role is within the individual GUI classes.