import tkinter as tk  # Importa la libreria base per la GUI
from tkinter import messagebox  # Importa le finestre di messaggio standard di Tkinter
from PIL import Image, ImageTk, ImageDraw, ImageFilter  # Importa PIL per la gestione delle immagini (non usato qui)
from db_connection import DbConnection  # Importa la classe per la connessione al database
from gui.expense_gui import ExpenseGUI  # Importa la GUI delle spese
from gui.activity_form_gui import ActivityFormGUI  # Importa la GUI per le attività
from gui.teacher_dashboard import TeacherDashboard  # Importa la dashboard insegnante
import datetime  # Importa il modulo datetime per gestire date e orari
import sys  # Importa sys per l'uscita dal programma

class DashboardGUI:  # Definisce la classe principale della dashboard
    def __init__(self, root, student, expense_callback, activity_callback):  # Costruttore della dashboard
        self.root = root  # Salva la finestra principale
        self.student = student  # Oggetto studente (contiene anche il ruolo)
        self.expense_callback = expense_callback  # Callback per aprire la GUI delle spese
        self.activity_callback = activity_callback  # Callback per aprire la GUI delle attività
        self.logged_in_student = student # Riferimento allo studente loggato

        self.root.title("Trip Manager Dashboard")  # Imposta il titolo della finestra
        self.root.geometry("1200x800")  # Imposta la dimensione della finestra
        self.root.resizable(True, True)  # Rende la finestra ridimensionabile
        self.root.configure(bg='#f8fafc')  # Imposta il colore di sfondo

        # Prova a massimizzare la finestra su Windows
        try:
            self.root.state('zoomed')  # Tenta di massimizzare la finestra (funziona su Windows)
        except tk.TclError: # Se 'zoomed' non è disponibile (ad esempio su Linux)
            pass # Non fa nulla, la finestra resta della dimensione impostata

        # Crea il contenitore principale con bordo
        main_container = tk.Frame(self.root, bg='#ffffff', relief='solid', bd=1)  # Frame principale bianco con bordo
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)  # Occupa tutto lo spazio disponibile

        # Header della dashboard
        header_frame = tk.Frame(main_container, bg='#ffffff', height=100)  # Frame per l'intestazione
        header_frame.pack(fill=tk.X, padx=30, pady=(30, 20))  # Occupa tutta la larghezza, con padding
        header_frame.pack_propagate(False)  # Impedisce il ridimensionamento automatico del frame

        # Titolo della dashboard
        title_label = tk.Label(header_frame, text="Trip Manager Dashboard",  # Testo del titolo
                              font=("Segoe UI", 32, "bold"), bg="#ffffff", fg="#1e293b")  # Font grande e grassetto
        title_label.pack(anchor='w')  # Allinea il titolo a sinistra

        # Messaggio di benvenuto con nome e classe
        greeting = f"Welcome, {self.student.name} | Class {getattr(self.student, 'class_', getattr(self.student, 'class', ''))}"  # Crea stringa con nome e classe
        greeting_label = tk.Label(header_frame, text=greeting,  # Label di benvenuto
                                 font=("Segoe UI", 14), bg="#ffffff", fg="#64748b")
        greeting_label.pack(anchor='w', pady=(5, 0))  # Allinea a sinistra, con piccolo spazio sopra

        # Sottotitolo
        subtitle_label = tk.Label(header_frame, text="Manage your expenses and activities efficiently",  # Sottotitolo descrittivo
                                 font=("Segoe UI", 16), bg="#ffffff", fg="#64748b")
        subtitle_label.pack(anchor='w', pady=(5, 0))  # Allinea a sinistra, con piccolo spazio sopra

        # Messaggio di benvenuto con ruolo
        welcome_text = f"Welcome, {self.student.name} {getattr(self.student, 'surname', '')}!"  # Messaggio con nome e cognome
        role_text = f"Role: {getattr(self.student, 'role', 'N/A').capitalize()}"  # Mostra il ruolo (es. Student/Teacher)
        
        welcome_label = tk.Label(header_frame, text=welcome_text,  # Label di benvenuto grande
                                font=("Segoe UI", 20, "bold"), bg="#ffffff", fg="#1e293b")
        welcome_label.pack(pady=(10, 0))  # Spazio sopra

        role_label = tk.Label(header_frame, text=role_text,  # Label con il ruolo
                              font=("Segoe UI", 12), bg="#ffffff", fg="#64748b")
        role_label.pack(pady=(0,10))  # Spazio sotto

        # Content area with grid layout
        content_frame = tk.Frame(main_container, bg='#ffffff')  # Frame per il contenuto centrale
        content_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=20)  # Occupa tutto lo spazio disponibile

        # Configure grid
        content_frame.grid_columnconfigure(0, weight=1)  # Prima colonna espandibile
        content_frame.grid_columnconfigure(1, weight=1)  # Seconda colonna espandibile
        content_frame.grid_rowconfigure(0, weight=1)     # Prima riga espandibile

        # Actions section
        actions_frame = tk.LabelFrame(content_frame, text="Quick Actions",  # Sezione per le azioni rapide
                                     font=("Segoe UI", 18, "bold"), bg="#ffffff",
                                     fg="#1e293b", relief='solid', bd=2)
        actions_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10), pady=10)  # Posiziona nella griglia a sinistra

        self._create_action_buttons(actions_frame)  # Crea i pulsanti delle azioni rapide (spese, attività, admin)

        # Schedule section
        schedule_frame = tk.LabelFrame(content_frame, text="Today's Schedule",  # Sezione per l'orario del giorno
                                      font=("Segoe UI", 18, "bold"), bg="#ffffff",
                                      fg="#1e293b", relief='solid', bd=2)
        schedule_frame.grid(row=0, column=1, sticky="nsew", padx=(10, 0), pady=10)  # Posiziona nella griglia a destra

        self._create_schedule_section(schedule_frame)  # Crea la lista delle attività del giorno

        # Status bar
        status_frame = tk.Frame(self.root, bg='#e5e7eb', height=30)  # Barra di stato in basso
        status_frame.pack(fill=tk.X, side=tk.BOTTOM)  # Occupa tutta la larghezza in basso
        status_frame.pack_propagate(False)  # Impedisce il ridimensionamento automatico

        status_label = tk.Label(status_frame, text="Trip Manager © 2025 - Ready",  # Testo della barra di stato
                               font=("Segoe UI", 10), bg="#e5e7eb", fg="#64748b")
        status_label.pack(side=tk.LEFT, padx=10, pady=5)  # Allinea a sinistra con padding

    def _create_action_button(self, parent, text, icon, description, command, bg_color="#3b82f6"):
        btn_frame = tk.Frame(parent, bg="#ffffff", relief='solid', bd=1)  # Crea un frame per il pulsante
        btn_frame.pack(fill=tk.X, padx=20, pady=15)

        # Contenuto del pulsante
        btn_content = tk.Frame(btn_frame, bg="#ffffff")
        btn_content.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)

        # Icona e testo
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

        # Pulsante vero e proprio
        action_btn = tk.Button(btn_content, text="Open →", font=("Segoe UI", 12, "bold"),
                              bg=bg_color, fg="white", relief='flat', bd=0,
                              activebackground="#2563eb", cursor="hand2",
                              command=command)
        action_btn.pack(side=tk.RIGHT, padx=(15, 0), pady=10)

        # Effetti hover
        def on_enter(e):
            btn_frame.config(relief='solid', bd=2)
        def on_leave(e):
            btn_frame.config(relief='solid', bd=1)

        btn_frame.bind("<Enter>", on_enter)
        btn_frame.bind("<Leave>", on_leave)

    def _create_action_buttons(self, actions_frame):
        # Pulsante per la gestione delle spese
        self._create_action_button(actions_frame, "Expense Tracker", "💰",
                                "Track and manage all trip expenses",
                                lambda: [self.root.destroy(), self.expense_callback()], "#3b82f6")

        # Pulsante per la gestione delle attività
        self._create_action_button(actions_frame, "Activity Manager", "🎯",
                                "Subscribe to activities and manage schedule",
                                lambda: [self.root.destroy(), self.activity_callback()], "#059669")

        # Se lo studente è un insegnante, mostra il pulsante admin
        if hasattr(self.student, 'role') and self.student.role == 'teacher':
            admin_button = tk.Button(actions_frame, text="Teacher Admin Panel",
                                     font=("Segoe UI", 14, "bold"), bg="#8b5cf6", fg="white",
                                     relief='flat', bd=0, activebackground="#7c3aed",
                                     cursor="hand2", command=self.open_teacher_admin_panel,
                                     width=20, height=2)
            admin_button.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

    def _create_schedule_section(self, schedule_frame):
        # Contenitore per la lista orario
        schedule_container = tk.Frame(schedule_frame, bg="#ffffff")
        schedule_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Scrollbar per la lista orario
        schedule_scrollbar = tk.Scrollbar(schedule_container)
        schedule_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        schedule_list = tk.Listbox(schedule_container, font=("Segoe UI", 12), bg="#ffffff",
                                  fg="#374151", relief='solid', bd=1,
                                  yscrollcommand=schedule_scrollbar.set,
                                  selectbackground="#dbeafe", selectforeground="#1e40af")
        schedule_list.pack(fill=tk.BOTH, expand=True)
        schedule_scrollbar.config(command=schedule_list.yview)

        # Carica le attività del giorno corrente
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

    def open_expense_gui(self):
        # Metodo per aprire la GUI delle spese
        self.root.destroy()  # Chiude la dashboard
        self.expense_callback() # Chiama la callback per aprire ExpenseGUI

    def open_activity_form(self):
        # Metodo per aprire la GUI delle attività
        self.root.destroy()  # Chiude la dashboard
        self.activity_callback() # Chiama la callback per aprire ActivityFormGUI

    def open_teacher_admin_panel(self):
        """Apre la dashboard insegnante"""
        self.root.destroy()  # Chiude la dashboard corrente
        
        # Crea una nuova finestra per la dashboard insegnante
        teacher_root = tk.Tk()
        teacher_dashboard = TeacherDashboard(teacher_root, self.student, self.show_main_dashboard)
        teacher_root.mainloop()
        
    def show_main_dashboard(self):
        """Callback per riaprire la dashboard principale"""
        # Crea una nuova finestra e dashboard
        new_root = tk.Tk()
        dashboard = DashboardGUI(new_root, self.student, self.expense_callback, self.activity_callback)
        new_root.mainloop()

if __name__ == '__main__':
    # Permette di testare la DashboardGUI direttamente
    # Serve uno studente di test e funzioni di callback
    class MockStudent:
        def __init__(self, name, class_):
            self.name = name
            self.class_ = class_

    def mock_show_expense():
        print("Show expense GUI (mock)")

    def mock_show_activity():
        print("Show activity form GUI (mock)")

    # Esempio:
    # Controlla la connessione al database prima di avviare la GUI
    connection = DbConnection.connect()
    if not connection:
        root = tk.Tk()
        root.withdraw()  # Nasconde la finestra principale
        messagebox.showerror("Database Error", "Could not connect to the database. Please check your connection settings.")
        sys.exit(1) # Esce dal programma

    test_student = MockStudent("Test User", "6A")
    test_student.role = "teacher"  # Per testare le funzioni da insegnante
    main_root = tk.Tk()
    app = DashboardGUI(main_root, test_student, mock_show_expense, mock_show_activity)
    main_root.mainloop()