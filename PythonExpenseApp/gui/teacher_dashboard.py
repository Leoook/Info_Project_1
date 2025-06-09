import tkinter as tk  # Importa la libreria base per la GUI
from tkinter import ttk, messagebox  # Importa widget avanzati e finestre di messaggio di Tkinter
from db_connection import DbConnection  # Importa la classe per la connessione al database
import datetime  # Importa il modulo datetime per gestire date e orari
from collections import defaultdict  # Importa defaultdict per strutture dati avanzate

class TeacherDashboard:  # Definisce la classe principale della dashboard insegnante
    def __init__(self, root, teacher, main_dashboard_callback):  # Costruttore della dashboard
        """
        Initialize the TeacherDashboard window and set up the UI for the teacher's dashboard.
        Args:
            root (tk.Tk): The main Tkinter window instance.
            teacher (object): The teacher object (should have name, surname, role attributes).
            main_dashboard_callback (function): Callback to return to the main dashboard.
        """
        self.root = root  # Salva la finestra principale Tkinter
        self.teacher = teacher  # Salva l'oggetto insegnante (contiene nome, cognome, ruolo)
        self.main_dashboard_callback = main_dashboard_callback  # Callback per tornare alla dashboard principale
        
        self.root.title("Teacher Dashboard - Trip Manager")  # Imposta il titolo della finestra
        self.root.geometry("1400x900")  # Imposta la dimensione della finestra
        self.root.configure(bg='#f8fafc')  # Imposta il colore di sfondo
        
        # Prova a massimizzare la finestra (dipende dal sistema operativo)
        try:
            self.root.state('zoomed')  # Tenta di massimizzare la finestra
        except tk.TclError:
            pass  # Se non funziona, ignora l'errore
        
        self.setup_ui()  # Costruisce e posiziona tutti i widget
        self.load_data()  # Carica tutti i dati dal database

    def setup_ui(self):
        """
        Create and arrange all main UI components: header, tabs, and footer.
        """
        # Main container frame for the dashboard
        main_container = tk.Frame(self.root, bg='#ffffff', relief='solid', bd=1)  # Crea il frame principale bianco con bordo
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)  # Occupa tutto lo spazio disponibile

        # Header section (title, teacher info, quick stats)
        self.create_header(main_container)  # Crea l'header con titolo e info insegnante
        
        # Notebook widget for tabbed interface
        self.notebook = ttk.Notebook(main_container)  # Crea il widget notebook (tab)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)  # Posiziona il notebook
        
        # Create and add all tabs
        self.create_activities_tab()  # Crea il tab panoramica attività
        self.create_participants_tab()  # Crea il tab studenti/iscrizioni
        self.create_schedule_tab()  # Crea il tab orario giornaliero
        self.create_analytics_tab()  # Crea il tab analytics/statistiche
        
        # Footer with navigation and status
        self.create_footer(main_container)  # Crea il footer con pulsante indietro e stato

    def create_header(self, parent):
        """
        Create the header section with the dashboard title, teacher info, and quick stats.
        Args:
            parent (tk.Frame): The parent frame to attach the header to.
        """
        header_frame = tk.Frame(parent, bg='#ffffff', height=100)  # Crea il frame per l'header
        header_frame.pack(fill=tk.X, padx=30, pady=(30, 20))  # Occupa tutta la larghezza, con padding
        header_frame.pack_propagate(False)  # Impedisce il ridimensionamento automatico

        # Title label for the dashboard
        title_label = tk.Label(header_frame, text="Teacher Dashboard",  # Testo del titolo
                              font=("Segoe UI", 32, "bold"), bg="#ffffff", fg="#1e293b")
        title_label.pack(anchor='w')  # Allinea il titolo a sinistra

        # Teacher info label (shows teacher's name)
        teacher_info = f"Teacher: {self.teacher.name} {getattr(self.teacher, 'surname', '')}"  # Stringa con nome insegnante
        info_label = tk.Label(header_frame, text=teacher_info,  # Label con info insegnante
                             font=("Segoe UI", 16), bg="#ffffff", fg="#64748b")
        info_label.pack(anchor='w', pady=(5, 0))  # Allinea a sinistra, con piccolo spazio sopra

        # Quick stats frame (populated later)
        stats_frame = tk.Frame(header_frame, bg="#ffffff")  # Frame per statistiche rapide
        stats_frame.pack(anchor='w', pady=(10, 0))  # Allinea a sinistra, con spazio sopra
        
        self.stats_labels = {}  # Dizionario per riferimenti a label statistiche (se servono)

    def create_activities_tab(self):
        """
        Create the Activities Overview tab, including search/filter and activities treeview.
        """
        # Activities tab
        activities_frame = ttk.Frame(self.notebook)  # Crea il frame per il tab attività
        self.notebook.add(activities_frame, text="📋 Activities Overview")  # Aggiunge il tab al notebook
        
        # Search and filter frame
        search_frame = tk.Frame(activities_frame, bg='#f8fafc')  # Frame per ricerca e filtri
        search_frame.pack(fill=tk.X, padx=10, pady=10)  # Occupa tutta la larghezza
        
        tk.Label(search_frame, text="Search Activities:", font=("Segoe UI", 12, "bold"),
                bg='#f8fafc').pack(side=tk.LEFT, padx=(0, 10))  # Label per ricerca attività
        
        # Variables for search and filter
        self.activity_search_var = tk.StringVar()  # Variabile per il termine di ricerca attività
        self.activity_search_var.trace('w', self.filter_activities)  # Aggiorna filtro quando cambia
        search_entry = tk.Entry(search_frame, textvariable=self.activity_search_var,
                               font=("Segoe UI", 11), width=30)  # Campo di testo ricerca
        search_entry.pack(side=tk.LEFT, padx=(0, 20))  # Posiziona il campo
        
        # Day filter
        tk.Label(search_frame, text="Filter by Day:", font=("Segoe UI", 12, "bold"),
                bg='#f8fafc').pack(side=tk.LEFT, padx=(0, 10))  # Label filtro giorno
        
        self.day_filter_var = tk.StringVar(value="All Days")  # Variabile per filtro giorno
        self.day_filter = ttk.Combobox(search_frame, textvariable=self.day_filter_var,
                                      state="readonly", width=15)  # Combobox filtro giorno
        self.day_filter.pack(side=tk.LEFT)  # Posiziona la combobox
        self.day_filter.bind('<<ComboboxSelected>>', self.filter_activities)  # Aggiorna filtro al cambio
        
        # Activities treeview
        tree_frame = tk.Frame(activities_frame)  # Frame per la treeview attività
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)  # Occupa tutto lo spazio
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(tree_frame, orient="vertical")  # Scrollbar verticale
        h_scrollbar = ttk.Scrollbar(tree_frame, orient="horizontal")  # Scrollbar orizzontale
        
        self.activities_tree = ttk.Treeview(tree_frame, 
                                           columns=("day", "time", "location", "participants", "max_participants", "description"),
                                           show="tree headings",
                                           yscrollcommand=v_scrollbar.set,
                                           xscrollcommand=h_scrollbar.set)  # Treeview con colonne personalizzate
        
        # Configure scrollbars
        v_scrollbar.config(command=self.activities_tree.yview)  # Collega scrollbar verticale
        h_scrollbar.config(command=self.activities_tree.xview)  # Collega scrollbar orizzontale
        
        # Grid layout for treeview and scrollbars
        self.activities_tree.grid(row=0, column=0, sticky="nsew")  # Posiziona la treeview nella griglia
        v_scrollbar.grid(row=0, column=1, sticky="ns")  # Posiziona la scrollbar verticale
        h_scrollbar.grid(row=1, column=0, sticky="ew")  # Posiziona la scrollbar orizzontale
        
        tree_frame.grid_rowconfigure(0, weight=1)  # Permette espansione verticale
        tree_frame.grid_columnconfigure(0, weight=1)  # Permette espansione orizzontale
        
        # Configure columns
        self.activities_tree.heading("#0", text="Activity Name", anchor="w")  # Intestazione colonna nome attività
        self.activities_tree.heading("day", text="Day", anchor="center")  # Intestazione colonna giorno
        self.activities_tree.heading("time", text="Time", anchor="center")  # Intestazione colonna orario
        self.activities_tree.heading("location", text="Location", anchor="w")  # Intestazione colonna luogo
        self.activities_tree.heading("participants", text="Enrolled", anchor="center")  # Intestazione colonna iscritti
        self.activities_tree.heading("max_participants", text="Max", anchor="center")  # Intestazione colonna max iscritti
        self.activities_tree.heading("description", text="Description", anchor="w")  # Intestazione colonna descrizione
        
        # Configure column widths
        self.activities_tree.column("#0", width=200, minwidth=150)  # Larghezza colonna nome
        self.activities_tree.column("day", width=100, minwidth=80)  # Larghezza colonna giorno
        self.activities_tree.column("time", width=120, minwidth=100)  # Larghezza colonna orario
        self.activities_tree.column("location", width=150, minwidth=120)  # Larghezza colonna luogo
        self.activities_tree.column("participants", width=80, minwidth=60)  # Larghezza colonna iscritti
        self.activities_tree.column("max_participants", width=60, minwidth=50)  # Larghezza colonna max iscritti
        self.activities_tree.column("description", width=300, minwidth=200)  # Larghezza colonna descrizione
        
        # Bind double-click to show participants
        self.activities_tree.bind("<Double-1>", self.show_activity_participants)  # Doppio click per mostrare partecipanti

    def create_participants_tab(self):
        """
        Create the Students & Enrollment tab, including search/filter and students treeview.
        """
        # Participants tab
        participants_frame = ttk.Frame(self.notebook)  # Crea il frame per il tab studenti
        self.notebook.add(participants_frame, text="👥 Students & Enrollment")  # Aggiunge il tab al notebook
        
        # Search frame
        search_frame = tk.Frame(participants_frame, bg='#f8fafc')  # Frame per ricerca e filtri
        search_frame.pack(fill=tk.X, padx=10, pady=10)  # Occupa tutta la larghezza
        
        tk.Label(search_frame, text="Search Students:", font=("Segoe UI", 12, "bold"),
                bg='#f8fafc').pack(side=tk.LEFT, padx=(0, 10))  # Label per ricerca studenti
        
        # Variables for search and filter
        self.student_search_var = tk.StringVar()  # Variabile per il termine di ricerca studenti
        self.student_search_var.trace('w', self.filter_students)  # Aggiorna filtro quando cambia
        search_entry = tk.Entry(search_frame, textvariable=self.student_search_var,
                               font=("Segoe UI", 11), width=30)  # Campo di testo ricerca
        search_entry.pack(side=tk.LEFT, padx=(0, 20))  # Posiziona il campo
        
        # Class filter
        tk.Label(search_frame, text="Filter by Class:", font=("Segoe UI", 12, "bold"),
                bg='#f8fafc').pack(side=tk.LEFT, padx=(0, 10))  # Label filtro classe
        
        self.class_filter_var = tk.StringVar(value="All Classes")  # Variabile per filtro classe
        self.class_filter = ttk.Combobox(search_frame, textvariable=self.class_filter_var,
                                        state="readonly", width=15)  # Combobox filtro classe
        self.class_filter.pack(side=tk.LEFT)  # Posiziona la combobox
        self.class_filter.bind('<<ComboboxSelected>>', self.filter_students)  # Aggiorna filtro al cambio
        
        # Students treeview
        tree_frame = tk.Frame(participants_frame)  # Frame per la treeview studenti
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)  # Occupa tutto lo spazio
        
        v_scrollbar = ttk.Scrollbar(tree_frame, orient="vertical")  # Scrollbar verticale
        h_scrollbar = ttk.Scrollbar(tree_frame, orient="horizontal")  # Scrollbar orizzontale
        
        self.students_tree = ttk.Treeview(tree_frame,
                                         columns=("class", "email", "age", "activities_count", "special_needs"),
                                         show="tree headings",
                                         yscrollcommand=v_scrollbar.set,
                                         xscrollcommand=h_scrollbar.set)  # Treeview con colonne personalizzate
        
        v_scrollbar.config(command=self.students_tree.yview)  # Collega scrollbar verticale
        h_scrollbar.config(command=self.students_tree.xview)  # Collega scrollbar orizzontale
        
        self.students_tree.grid(row=0, column=0, sticky="nsew")  # Posiziona la treeview nella griglia
        v_scrollbar.grid(row=0, column=1, sticky="ns")  # Posiziona la scrollbar verticale
        h_scrollbar.grid(row=1, column=0, sticky="ew")  # Posiziona la scrollbar orizzontale
        
        tree_frame.grid_rowconfigure(0, weight=1)  # Permette espansione verticale
        tree_frame.grid_columnconfigure(0, weight=1)  # Permette espansione orizzontale
        
        # Configure columns
        self.students_tree.heading("#0", text="Student Name", anchor="w")  # Intestazione colonna nome studente
        self.students_tree.heading("class", text="Class", anchor="center")  # Intestazione colonna classe
        self.students_tree.heading("email", text="Email", anchor="w")  # Intestazione colonna email
        self.students_tree.heading("age", text="Age", anchor="center")  # Intestazione colonna età
        self.students_tree.heading("activities_count", text="Activities", anchor="center")  # Intestazione colonna attività
        self.students_tree.heading("special_needs", text="Special Needs", anchor="w")  # Intestazione colonna bisogni speciali
        
        # Configure column widths
        self.students_tree.column("#0", width=200, minwidth=150)  # Larghezza colonna nome
        self.students_tree.column("class", width=80, minwidth=60)  # Larghezza colonna classe
        self.students_tree.column("email", width=200, minwidth=150)  # Larghezza colonna email
        self.students_tree.column("age", width=60, minwidth=50)  # Larghezza colonna età
        self.students_tree.column("activities_count", width=80, minwidth=60)  # Larghezza colonna attività
        self.students_tree.column("special_needs", width=300, minwidth=200)  # Larghezza colonna bisogni speciali
        
        # Bind double-click to show student activities
        self.students_tree.bind("<Double-1>", self.show_student_activities)  # Doppio click per mostrare attività studente

    def create_schedule_tab(self):
        """
        Create the Daily Schedule tab, including date selection and schedule display.
        """
        # Daily schedule tab
        schedule_frame = ttk.Frame(self.notebook)  # Crea il frame per il tab orario
        self.notebook.add(schedule_frame, text="📅 Daily Schedule")  # Aggiunge il tab al notebook
        
        # Date selection frame
        date_frame = tk.Frame(schedule_frame, bg='#f8fafc')  # Frame per selezione data
        date_frame.pack(fill=tk.X, padx=10, pady=10)  # Occupa tutta la larghezza
        
        tk.Label(date_frame, text="Select Date:", font=("Segoe UI", 12, "bold"),
                bg='#f8fafc').pack(side=tk.LEFT, padx=(0, 10))  # Label per selezione data
        
        # Variable for selected date
        self.selected_date_var = tk.StringVar()  # Variabile per la data selezionata
        self.date_combo = ttk.Combobox(date_frame, textvariable=self.selected_date_var,
                                      state="readonly", width=20)  # Combobox per selezione data
        self.date_combo.pack(side=tk.LEFT, padx=(0, 20))  # Posiziona la combobox
        self.date_combo.bind('<<ComboboxSelected>>', self.load_daily_schedule)  # Aggiorna orario al cambio
        
        # Today button
        today_btn = tk.Button(date_frame, text="Today", font=("Segoe UI", 10, "bold"),
                             bg="#3b82f6", fg="white", relief='flat',
                             command=self.select_today)  # Pulsante per selezionare oggi
        today_btn.pack(side=tk.LEFT, padx=(0, 10))  # Posiziona il pulsante
        
        # Schedule display frame
        self.schedule_display_frame = tk.Frame(schedule_frame, bg='#ffffff')  # Frame per mostrare l'orario
        self.schedule_display_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)  # Occupa tutto lo spazio

    def create_analytics_tab(self):
        """
        Create the Analytics tab and its widgets.
        """
        # Analytics tab
        analytics_frame = ttk.Frame(self.notebook)  # Crea il frame per il tab analytics
        self.notebook.add(analytics_frame, text="📊 Analytics")  # Aggiunge il tab al notebook
        
        # Create analytics widgets
        self.create_analytics_widgets(analytics_frame)  # Crea i widget delle statistiche

    def create_analytics_widgets(self, parent):
        """
        Create widgets for analytics: trip statistics and most popular activities.
        Args:
            parent (tk.Frame): The parent frame to attach analytics widgets to.
        """
        # Statistics frame
        stats_frame = tk.LabelFrame(parent, text="Trip Statistics", font=("Segoe UI", 14, "bold"),
                                   bg='#ffffff', fg='#1e293b', relief='solid', bd=2)  # Frame per statistiche viaggio
        stats_frame.pack(fill=tk.X, padx=10, pady=10)  # Occupa tutta la larghezza
        
        # Create grid for statistics
        stats_grid = tk.Frame(stats_frame, bg='#ffffff')  # Frame per griglia statistiche
        stats_grid.pack(fill=tk.X, padx=20, pady=20)  # Occupa tutta la larghezza
        
        self.stats_widgets = {}  # Dizionario per riferimenti a widget statistiche
        
        # Popular activities frame
        popular_frame = tk.LabelFrame(parent, text="Most Popular Activities", 
                                     font=("Segoe UI", 14, "bold"),
                                     bg='#ffffff', fg='#1e293b', relief='solid', bd=2)  # Frame per attività popolari
        popular_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)  # Occupa tutto lo spazio
        
        # Popular activities listbox
        popular_container = tk.Frame(popular_frame, bg='#ffffff')  # Frame per la lista attività popolari
        popular_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)  # Occupa tutto lo spazio
        
        scrollbar = tk.Scrollbar(popular_container)  # Scrollbar verticale
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)  # Posiziona la scrollbar
        
        self.popular_activities_list = tk.Listbox(popular_container, 
                                                 font=("Segoe UI", 11),
                                                 bg='#ffffff', fg='#374151',
                                                 yscrollcommand=scrollbar.set)  # Listbox attività popolari
        self.popular_activities_list.pack(fill=tk.BOTH, expand=True)  # Occupa tutto lo spazio
        scrollbar.config(command=self.popular_activities_list.yview)  # Collega la scrollbar

    def create_footer(self, parent):
        """
        Create the footer section with navigation and status label.
        Args:
            parent (tk.Frame): The parent frame to attach the footer to.
        """
        footer_frame = tk.Frame(parent, bg='#e5e7eb', height=60)  # Frame per il footer
        footer_frame.pack(fill=tk.X, side=tk.BOTTOM)  # Occupa tutta la larghezza in basso
        footer_frame.pack_propagate(False)  # Impedisce il ridimensionamento automatico
        
        # Back button to return to main dashboard
        back_btn = tk.Button(footer_frame, text="← Back to Main Dashboard",
                            font=("Segoe UI", 12, "bold"), bg="#6b7280", fg="white",
                            relief='flat', bd=0, activebackground="#4b5563",
                            cursor="hand2", command=self.go_back)  # Pulsante per tornare alla dashboard principale
        back_btn.pack(side=tk.LEFT, padx=20, pady=15)  # Posiziona il pulsante a sinistra
        
        # Status label for messages
        self.status_label = tk.Label(footer_frame, text="Ready",
                                    font=("Segoe UI", 10), bg="#e5e7eb", fg="#64748b")  # Label di stato
        self.status_label.pack(side=tk.RIGHT, padx=20, pady=15)  # Posiziona la label a destra

    def load_data(self):
        """
        Load all activities, students, unique days, and classes from the database.
        Populates the UI with the loaded data and sets up filters and analytics.
        """
        self.update_status("Loading data...")  # Mostra stato di caricamento
        
        connection = DbConnection.connect()  # Connessione al database
        if not connection:
            messagebox.showerror("Database Error", "Could not connect to database")  # Mostra errore se la connessione fallisce
            return
        
        try:
            cursor = connection.cursor()  # Crea un cursore per le query
            # Load all activities with participant counts
            cursor.execute("""
                SELECT a.id, a.name, a.day, a.start_time, a.finish_time, 
                       a.location, a.max_participants, a.description,
                       (SELECT COUNT(*) FROM student_activities sa WHERE sa.activity_id = a.id) as participant_count
                FROM activities a
                ORDER BY a.day, a.start_time
            """)  # Query per tutte le attività con conteggio partecipanti
            self.activities_data = cursor.fetchall()  # Lista di tuple con dati attività
            
            # Load all students with activity counts
            cursor.execute("""
                SELECT s.id, s.name, s.surname, s.class, s.email, s.age, 
                       s.special_needs, 
                       (SELECT COUNT(*) FROM student_activities sa WHERE sa.student_id = s.id) as activity_count
                FROM students s
                WHERE s.role = 'student'
                ORDER BY s.class, s.surname, s.name
            """)  # Query per tutti gli studenti con conteggio attività
            self.students_data = cursor.fetchall()  # Lista di tuple con dati studenti
            
            # Load unique days and classes for filters
            cursor.execute("SELECT DISTINCT day FROM activities ORDER BY day")  # Giorni unici per filtro
            self.unique_days = [row[0] for row in cursor.fetchall()]  # Lista di giorni unici
            
            cursor.execute("SELECT DISTINCT class FROM students WHERE role = 'student' ORDER BY class")  # Classi uniche per filtro
            self.unique_classes = [row[0] for row in cursor.fetchall()]  # Lista di classi uniche
            
            connection.close()  # Chiude la connessione
            
            # Populate UI with loaded data
            self.populate_activities()  # Popola la treeview attività
            self.populate_students()  # Popola la treeview studenti
            self.setup_filters()  # Imposta i valori dei filtri
            self.load_analytics()  # Carica i dati analytics
            self.setup_schedule_dates()  # Imposta le date disponibili per l'orario
            self.update_quick_stats()  # Aggiorna le statistiche rapide
            
            self.update_status("Data loaded successfully")  # Mostra stato di successo
            
        except Exception as e:
            connection.close()  # Chiude la connessione in caso di errore
            messagebox.showerror("Error", f"Error loading data: {str(e)}")  # Mostra errore
            self.update_status("Error loading data")  # Aggiorna stato

    def populate_activities(self):
        """
        Populate the activities treeview with activity data.
        """
        # Clear existing items
        for item in self.activities_tree.get_children():  # Cicla su tutti gli elementi attuali della treeview
            self.activities_tree.delete(item)  # Elimina ogni elemento dalla treeview
        for activity in self.activities_data:  # Cicla su tutte le attività caricate dal database
            activity_id, name, day, start_time, finish_time, location, max_participants, description, participant_count = activity  # Estrae i dati dell'attività
            start_hour = start_time // 60  # Calcola l'ora di inizio
            start_min = start_time % 60  # Calcola i minuti di inizio
            finish_hour = finish_time // 60  # Calcola l'ora di fine
            finish_min = finish_time % 60  # Calcola i minuti di fine
            time_str = f"{start_hour:02d}:{start_min:02d} - {finish_hour:02d}:{finish_min:02d}"  # Crea la stringa orario
            max_str = str(max_participants) if max_participants else "∞"  # Mostra il massimo partecipanti o infinito
            day_str = day.strftime("%Y-%m-%d") if hasattr(day, 'strftime') else str(day)  # Formatta la data
            self.activities_tree.insert("", "end", text=name,  # Inserisce la riga nella treeview
                                       values=(day_str, time_str, location, 
                                              participant_count, max_str, description or ""))

    def populate_students(self):
        """
        Populate the students treeview with student data.
        """
        # Clear existing items
        for item in self.students_tree.get_children():  # Cicla su tutti gli elementi attuali della treeview
            self.students_tree.delete(item)  # Elimina ogni elemento dalla treeview
        for student in self.students_data:  # Cicla su tutti gli studenti caricati dal database
            student_id, name, surname, class_name, email, age, special_needs, activity_count = student  # Estrae i dati dello studente
            full_name = f"{name} {surname}"  # Crea la stringa nome completo
            age_str = str(age) if age else "N/A"  # Mostra l'età o N/A
            special_needs_str = special_needs or "None"  # Mostra bisogni speciali o None
            self.students_tree.insert("", "end", text=full_name,  # Inserisce la riga nella treeview
                                     values=(class_name, email, age_str, 
                                            activity_count, special_needs_str))

    def setup_filters(self):
        """
        Setup the values for day and class filter comboboxes based on loaded data.
        """
        # Day filter
        day_values = ["All Days"] + [day.strftime("%Y-%m-%d") for day in self.unique_days]  # Crea la lista dei giorni per il filtro
        self.day_filter['values'] = day_values  # Imposta i valori della combobox dei giorni
        
        # Class filter  
        class_values = ["All Classes"] + self.unique_classes  # Crea la lista delle classi per il filtro
        self.class_filter['values'] = class_values  # Imposta i valori della combobox delle classi

    def setup_schedule_dates(self):
        """
        Setup the date selection combobox for the schedule tab and set default date.
        """
        date_values = [day.strftime("%Y-%m-%d") for day in self.unique_days]  # Crea la lista delle date disponibili
        self.date_combo['values'] = date_values  # Imposta i valori della combobox delle date
        
        # Set today as default if available
        today = datetime.date.today().strftime("%Y-%m-%d")  # Ottiene la data di oggi
        if today in date_values:  # Se oggi è tra le date disponibili
            self.selected_date_var.set(today)  # Seleziona oggi
            self.load_daily_schedule()  # Carica l'orario di oggi
        elif date_values:  # Se ci sono date disponibili ma non oggi
            self.selected_date_var.set(date_values[0])  # Seleziona la prima data
            self.load_daily_schedule()  # Carica l'orario della prima data

    def filter_activities(self, *args):
        """
        Filter the activities treeview based on the search term and selected day filter.
        Args:
            *args: Required for Tkinter trace compatibility.
        """
        search_term = self.activity_search_var.get().lower()  # Ottiene il termine di ricerca
        day_filter = self.day_filter_var.get()  # Ottiene il filtro giorno selezionato
        
        # Clear existing items
        for item in self.activities_tree.get_children():  # Elimina tutti gli elementi attuali
            self.activities_tree.delete(item)
            
        for activity in self.activities_data:  # Cicla su tutte le attività
            activity_id, name, day, start_time, finish_time, location, max_participants, description, participant_count = activity  # Estrae i dati
            
            # Check search term
            if search_term and search_term not in name.lower() and search_term not in location.lower():  # Se il termine non è nel nome o luogo
                continue  # Salta questa attività
                
            # Check day filter
            day_str = day.strftime("%Y-%m-%d") if day else "N/A"  # Formatta la data
            if day_filter != "All Days" and day_filter != day_str:  # Se il filtro giorno non corrisponde
                continue  # Salta questa attività
                
            # Add item
            start_hour = start_time // 60  # Calcola ora di inizio
            start_min = start_time % 60  # Calcola minuti di inizio
            finish_hour = finish_time // 60  # Calcola l'ora di fine
            finish_min = finish_time % 60  # Calcola minuti di fine
            time_str = f"{start_hour:02d}:{start_min:02d} - {finish_hour:02d}:{finish_min:02d}"  # Crea la stringa orario
            
            max_str = str(max_participants) if max_participants else "∞"  # Mostra max partecipanti o infinito
            
            self.activities_tree.insert("", "end", text=name,  # Inserisce la riga filtrata
                                       values=(day_str, time_str, location,
                                              participant_count, max_str, description or ""))

    def filter_students(self, *args):
        """
        Filter the students treeview based on the search term and selected class filter.
        Args:
            *args: Required for Tkinter trace compatibility.
        """
        search_term = self.student_search_var.get().lower()  # Ottiene il termine di ricerca
        class_filter = self.class_filter_var.get()  # Ottiene il filtro classe selezionato
        
        # Clear existing items
        for item in self.students_tree.get_children():  # Elimina tutti gli elementi attuali
            self.students_tree.delete(item)
            
        for student in self.students_data:  # Cicla su tutti gli studenti
            student_id, name, surname, class_name, email, age, special_needs, activity_count = student  # Estrae i dati
            
            full_name = f"{name} {surname}"  # Crea la stringa nome completo
            
            # Check search term
            if search_term and (search_term not in full_name.lower() and 
                               search_term not in email.lower()):  # Se il termine non è nel nome o email
                continue  # Salta questo studente
                
            # Check class filter
            if class_filter != "All Classes" and class_filter != class_name:  # Se il filtro classe non corrisponde
                continue  # Salta questo studente
                
            # Add item
            age_str = str(age) if age else "N/A"  # Mostra età o N/A
            special_needs_str = special_needs or "None"  # Mostra bisogni speciali o None
            
            self.students_tree.insert("", "end", text=full_name,  # Inserisce la riga filtrata
                                     values=(class_name, email, age_str,
                                            activity_count, special_needs_str))

    def show_activity_participants(self, event):
        """
        Show a popup window listing all participants for the selected activity.
        Args:
            event: The Tkinter event object (from double-click).
        """
        selection = self.activities_tree.selection()  # Ottiene la selezione nella treeview
        if not selection:  # Se non c'è selezione
            return  # Esce dalla funzione
            
        item = selection[0]  # Ottiene il primo elemento selezionato
        activity_name = self.activities_tree.item(item, "text")  # Ottiene il nome dell'attività
        
        # Find activity in data
        activity_data = None  # Inizializza la variabile
        for activity in self.activities_data:  # Cerca l'attività nei dati
            if activity[1] == activity_name:  # name is at index 1
                activity_data = activity
                break
                
        if not activity_data:  # Se non trova l'attività
            return  # Esce dalla funzione
            
        # Get participants from database
        connection = DbConnection.connect()  # Connessione al database
        if not connection:
            return  # Esce se la connessione fallisce
            
        try:
            cursor = connection.cursor()  # Crea un cursore
            cursor.execute("""
                SELECT s.name, s.surname, s.class, s.email
                FROM students s
                JOIN student_activities sa ON s.id = sa.student_id
                WHERE sa.activity_id = %s
                ORDER BY s.class, s.surname, s.name
            """, (activity_data[0],))  # activity_id is at index 0
            
            participants = cursor.fetchall()  # Ottiene la lista dei partecipanti
            connection.close()  # Chiude la connessione
            
            # Show participants window
            self.show_participants_window(activity_name, participants)  # Mostra la finestra popup con i partecipanti
            
        except Exception as e:
            connection.close()  # Chiude la connessione in caso di errore
            messagebox.showerror("Error", f"Error loading participants: {str(e)}")  # Mostra errore

    def show_student_activities(self, event):
        """
        Show a popup window listing all activities for the selected student.
        Args:
            event: The Tkinter event object (from double-click).
        """
        selection = self.students_tree.selection()  # Ottiene la selezione nella treeview
        if not selection:  # Se non c'è selezione
            return  # Esce dalla funzione
            
        item = selection[0]  # Ottiene il primo elemento selezionato
        student_name = self.students_tree.item(item, "text")  # Ottiene il nome dello studente
        
        # Find student in data
        student_data = None  # Inizializza la variabile
        for student in self.students_data:  # Cerca lo studente nei dati
            full_name = f"{student[1]} {student[2]}"  # name and surname
            if full_name == student_name:
                student_data = student
                break
                
        if not student_data:  # Se non trova lo studente
            return  # Esce dalla funzione
            
        # Get activities from database
        connection = DbConnection.connect()  # Connessione al database
        if not connection:
            return  # Esce se la connessione fallisce
            
        try:
            cursor = connection.cursor()  # Crea un cursore
            cursor.execute("""
                SELECT a.name, a.day, a.start_time, a.finish_time, a.location
                FROM activities a
                JOIN student_activities sa ON a.id = sa.activity_id
                WHERE sa.student_id = %s
                ORDER BY a.day, a.start_time
            """, (student_data[0],))  # student_id is at index 0
            
            activities = cursor.fetchall()  # Ottiene la lista delle attività
            connection.close()  # Chiude la connessione
            
            # Show activities window
            self.show_student_activities_window(student_name, activities)  # Mostra la finestra popup con le attività
            
        except Exception as e:
            connection.close()  # Chiude la connessione in caso di errore
            messagebox.showerror("Error", f"Error loading student activities: {str(e)}")  # Mostra errore

    def show_participants_window(self, activity_name, participants):
        """
        Create and display a popup window showing participants for a given activity.
        Args:
            activity_name (str): The name of the activity.
            participants (list): List of tuples with participant info.
        """
        popup = tk.Toplevel(self.root) # Create a new popup window
        popup.title(f"Participants - {activity_name}") # Set the title of the popup
        popup.geometry("600x400") # Set the size of the popup window
        popup.configure(bg='#ffffff') # Set the background color of the popup
        
        # Header
        header_label = tk.Label(popup, text=f"Participants in: {activity_name}", # Set the header label
                               font=("Segoe UI", 16, "bold"), bg='#ffffff', fg='#1e293b') # Set the font and colors
        header_label.pack(pady=20) # Add padding around the header label
        
        # Participants list
        frame = tk.Frame(popup, bg='#ffffff') # Create a frame for the participants list
        frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20) # Add padding around the frame
        
        scrollbar = tk.Scrollbar(frame) # Create a scrollbar for the participants list
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y) # Add the scrollbar to the right side of the frame
        
        participants_list = tk.Listbox(frame, font=("Segoe UI", 11), # Create a listbox for participants
                                      yscrollcommand=scrollbar.set) # Set the font and scrollbar
        participants_list.pack(fill=tk.BOTH, expand=True) # Add the listbox to the frame
        scrollbar.config(command=participants_list.yview) # Link the scrollbar to the listbox
        
        if participants: # If there are participants, populate the listbox
            for name, surname, class_name, email in participants: # Loop through each participant
                participants_list.insert(tk.END, f"{name} {surname} ({class_name}) - {email}") # Format the participant info
        else:
            participants_list.insert(tk.END, "No participants enrolled") # If no participants, show a message
            
        # Close button
        close_btn = tk.Button(popup, text="Close", font=("Segoe UI", 12), # Create a close button
                             bg='#6b7280', fg='white', command=popup.destroy) # Set the button text and colors
        close_btn.pack(pady=20) # Add padding around the close button

    def show_student_activities_window(self, student_name, activities): # Show a popup window with student activities
        """
        Create and display a popup window showing activities for a given student.
        Args:
            student_name (str): The name of the student.
            activities (list): List of tuples with activity info.
        """
        popup = tk.Toplevel(self.root) # Create a new popup window
        popup.title(f"Activities - {student_name}") # Set the title of the popup
        popup.geometry("700x400") # Set the size of the popup window
        popup.configure(bg='#ffffff') # Set the background color of the popup
        
        # Header
        header_label = tk.Label(popup, text=f"Activities for: {student_name}", # Set the header label
                               font=("Segoe UI", 16, "bold"), bg='#ffffff', fg='#1e293b') # Set the font and colors
        header_label.pack(pady=20) # Add padding around the header label
        
        # Activities list
        frame = tk.Frame(popup, bg='#ffffff') # Create a frame for the activities list
        frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20) # Add padding around the frame
        
        scrollbar = tk.Scrollbar(frame) # Create a scrollbar for the activities list
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y) # Add the scrollbar to the right side of the frame
        
        activities_list = tk.Listbox(frame, font=("Segoe UI", 11), # Create a listbox for activities
                                    yscrollcommand=scrollbar.set) # Set the font and scrollbar
        activities_list.pack(fill=tk.BOTH, expand=True) # Add the listbox to the frame
        scrollbar.config(command=activities_list.yview) # Link the scrollbar to the listbox
        
        if activities: # If there are activities, populate the listbox
            for name, day, start_time, finish_time, location in activities: # Loop through each activity
                start_hour = start_time // 60 # Calculate start hour
                start_min = start_time % 60 # Calculate start minutes
                finish_hour = finish_time // 60 # Calculate finish hour
                finish_min = finish_time % 60 # Calculate finish minutes
                time_str = f"{start_hour:02d}:{start_min:02d} - {finish_hour:02d}:{finish_min:02d}" # Format the time string
                day_str = day.strftime("%Y-%m-%d") # Format the day string
                
                activities_list.insert(tk.END, f"{name} | {day_str} {time_str} | {location}") # Format the activity info
        else:
            activities_list.insert(tk.END, "No activities enrolled") # If no activities, show a message
            
        # Close button
        close_btn = tk.Button(popup, text="Close", font=("Segoe UI", 12), # Create a close button
                             bg='#6b7280', fg='white', command=popup.destroy) # Set the button text and colors
        close_btn.pack(pady=20) # Add padding around the close button

    def load_daily_schedule(self, event=None): # Load the schedule for the selected date in the schedule tab.
        """
        Load and display the schedule for the selected date in the schedule tab. 
        Args:
            event: Optional Tkinter event object (from combobox selection).
        """
        selected_date = self.selected_date_var.get() # Get the selected date from the combobox
        if not selected_date: # If no date is selected
            return # Exit the function
            
        # Clear existing schedule
        for widget in self.schedule_display_frame.winfo_children(): # Clear all widgets in the schedule display frame
            widget.destroy() # Destroy each widget to refresh the display
            
        # Get activities for selected date
        connection = DbConnection.connect() # Connect to the database
        if not connection: # If connection fails
            return # Exit the function
            
        try:
            cursor = connection.cursor() # Create a cursor for executing queries
            cursor.execute("""
                SELECT a.name, a.start_time, a.finish_time, a.location, a.description,
                       COUNT(sa.student_id) as participant_count, a.max_participants
                FROM activities a
                LEFT JOIN student_activities sa ON a.id = sa.activity_id
                WHERE a.day = %s
                GROUP BY a.id
                ORDER BY a.start_time
            """, (selected_date,)) # Query to get activities for the selected date
            
            daily_activities = cursor.fetchall() # Fetch all activities for the selected date
            connection.close() # Close the database connection
            
            if not daily_activities: # If no activities found for the selected date
                no_activities_label = tk.Label(self.schedule_display_frame, # Create a label for no activities
                                              text="No activities scheduled for this date",  # Message text
                                              font=("Segoe UI", 16), bg='#ffffff', fg='#64748b') # Set font and colors
                no_activities_label.pack(expand=True) # Add the label to the schedule display frame
                return
                
            # Create schedule display
            canvas = tk.Canvas(self.schedule_display_frame, bg='#ffffff') # Create a canvas for the schedule display
            scrollbar = ttk.Scrollbar(self.schedule_display_frame, orient="vertical", command=canvas.yview) # Create a vertical scrollbar
            scrollable_frame = ttk.Frame(canvas) # Create a frame to hold the scrollable content
            
            scrollable_frame.bind( # Bind the frame to the canvas for scrolling
                "<Configure>", # Configure event to update scroll region
                lambda e: canvas.configure(scrollregion=canvas.bbox("all")) # Update scroll region to encompass the scrollable frame
            )
            
            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw") # Create a window in the canvas to hold the scrollable frame
            canvas.configure(yscrollcommand=scrollbar.set) # Set the scrollbar to control the canvas vertical scrolling
            
            # Add activities to schedule
            for i, activity in enumerate(daily_activities): # Loop through each activity for the selected date
                name, start_time, finish_time, location, description, participant_count, max_participants = activity # Unpack activity data
                
                # Create activity card
                card_frame = tk.Frame(scrollable_frame, bg='#f8fafc', relief='solid', bd=1) # Create a frame for the activity card
                card_frame.pack(fill=tk.X, padx=10, pady=5) # Add padding around the card frame
                
                # Time and title
                start_hour = start_time // 60 # Calculate start hour
                start_min = start_time % 60 # Calculate start minutes
                finish_hour = finish_time // 60 # Calculate finish hour
                finish_min = finish_time % 60 # Calculate finish minutes
                time_str = f"{start_hour:02d}:{start_min:02d} - {finish_hour:02d}:{finish_min:02d}" # Format the time string
                
                header_frame = tk.Frame(card_frame, bg='#f8fafc') # Create a frame for the header of the activity card
                header_frame.pack(fill=tk.X, padx=15, pady=10) # Add padding around the header frame
                
                time_label = tk.Label(header_frame, text=time_str, # Format the time label
                                     font=("Segoe UI", 14, "bold"), bg='#f8fafc', fg='#3b82f6') # Set font and colors for the time label
                time_label.pack(side=tk.LEFT) # Add the time label to the left side of the header frame
                
                title_label = tk.Label(header_frame, text=name, # Create a label for the activity title
                                      font=("Segoe UI", 16, "bold"), bg='#f8fafc', fg='#1e293b') # Set font and colors for the title label
                title_label.pack(side=tk.LEFT, padx=(20, 0)) # Add padding to the left of the title label
                
                # Participants count
                max_str = str(max_participants) if max_participants else "∞" # Show max participants or infinity
                participants_label = tk.Label(header_frame, text=f"👥 {participant_count}/{max_str}",  #Create a label for participants count
                                             font=("Segoe UI", 12), bg='#f8fafc', fg='#059669') # Set font and colors for the participants label
                participants_label.pack(side=tk.RIGHT) # Add the participants label to the right side of the header frame
                
                # Location and description
                details_frame = tk.Frame(card_frame, bg='#f8fafc') # Create a frame for the details of the activity card
                details_frame.pack(fill=tk.X, padx=15, pady=(0, 10)) # Add padding around the details frame
                
                location_label = tk.Label(details_frame, text=f"📍 {location}", #Create a label for the location
                                         font=("Segoe UI", 12), bg='#f8fafc', fg='#64748b') # Set font and colors for the location label
                location_label.pack(anchor='w') # Add the location label to the left side of the details frame
                
                if description:
                    desc_label = tk.Label(details_frame, text=f"ℹ️ {description}", # Create a label for the description
                                         font=("Segoe UI", 11), bg='#f8fafc', fg='#64748b',    # Set font and colors for the description label
                                         wraplength=600, justify='left') # Set wrap length and justification for the description label
                    desc_label.pack(anchor='w', pady=(5, 0)) # Add the description label to the left side of the details frame
            
            canvas.pack(side="left", fill="both", expand=True) # Add the canvas to the schedule display frame
            scrollbar.pack(side="right", fill="y") # Add the scrollbar to the right side of the schedule display frame
            
        except Exception as e: # Handle any exceptions that occur while loading the schedule
            connection.close() # Close the database connection if it was opened
            error_label = tk.Label(self.schedule_display_frame, # Create a label to show the error message
                                  text=f"Error loading schedule: {str(e)}", # Set the error message text
                                  font=("Segoe UI", 12), bg='#ffffff', fg='#dc2626') # Set font and colors for the error label
            error_label.pack(expand=True) # Add the error label to the schedule display frame

    def select_today(self): # Set the schedule date selection to today and load today's schedule.
        """
        Set the schedule date selection to today and load today's schedule.
        """
        today = datetime.date.today().strftime("%Y-%m-%d") # Get today's date in YYYY-MM-DD format
        if today in self.date_combo['values']: # If today is in the available dates
            self.selected_date_var.set(today) # Set the selected date to today
            self.load_daily_schedule() # Load the schedule for today

    def load_analytics(self): # Load analytics data (e.g., most popular activities) from the database and update the analytics tab.
        """
        Load analytics data (e.g., most popular activities) from the database and update the analytics tab.
        """
        connection = DbConnection.connect() # Connect to the database
        if not connection: # If connection fails
            return # Exit the function
            
        try:
            cursor = connection.cursor() # Create a cursor for executing queries
            
            # Get popular activities
            cursor.execute("""
                SELECT a.name, COUNT(sa.student_id) as participant_count
                FROM activities a
                LEFT JOIN student_activities sa ON a.id = sa.activity_id
                GROUP BY a.id
                ORDER BY participant_count DESC, a.name
                LIMIT 10
            """)
            
            popular_activities = cursor.fetchall() # Fetch the top 10 most popular activities
            
            # Clear and populate popular activities list
            self.popular_activities_list.delete(0, tk.END) # Clear existing items in the listbox
            for i, (name, count) in enumerate(popular_activities, 1): # Loop through the popular activities
                self.popular_activities_list.insert(tk.END, f"{i}. {name} ({count} participants)") # Format the activity name and participant count
                
            connection.close() # Close the database connection
            
        except Exception as e: # Handle any exceptions that occur while loading analytics
            connection.close() # Close the connection in case of error
            self.popular_activities_list.delete(0, tk.END) # Clear existing items in the listbox
            self.popular_activities_list.insert(tk.END, f"Error loading analytics: {str(e)}") # Show error message in the listbox

    def update_quick_stats(self): # Update the quick statistics in the header (total activities, students, enrollments).
        """""
        Update the quick statistics in the header (total activities, students, enrollments). 
        """
        total_activities = len(self.activities_data)  # Conta il numero totale di attività caricate
        total_students = len(self.students_data)  # Conta il numero totale di studenti caricati
        total_enrollments = sum(activity[8] for activity in self.activities_data)  # Somma il numero totale di iscrizioni (participant_count)

        # Trova il frame delle statistiche nella tab Analytics
        analytics_tab = self.notebook.tabs()[-1]  # Prende l'ultimo tab, che dovrebbe essere quello Analytics
        analytics_frame = self.notebook.nametowidget(analytics_tab)  # Ottiene il frame del tab Analytics
        stats_frame = analytics_frame.winfo_children()[0]  # Il primo widget figlio è il frame "Trip Statistics"

        # Rimuove tutte le vecchie label di statistiche dal frame
        for child in stats_frame.winfo_children():
            child.destroy()  # Elimina ogni widget figlio (vecchie statistiche)

        # Crea il testo delle statistiche aggiornate
        stats_text = f"📋 {total_activities} Activities  |  👥 {total_students} Students  |  ✅ {total_enrollments} Total Enrollments"

        # Crea una nuova label con le statistiche aggiornate
        stats_label = tk.Label(
            stats_frame,
            text=stats_text,
            font=("Segoe UI", 16, "bold"),
            bg="#ffffff",
            fg="#059669",
            pady=20
        )
        stats_label.pack(fill=tk.X, padx=20, pady=20)  # Posiziona la label con padding

    def update_status(self, message):
        """
        Update the status message in the footer.
        Args:
            message (str): The status message to display.
        """
        if hasattr(self, 'status_label'):  # Controlla se esiste la label di stato
            self.status_label.config(text=message)  # Aggiorna il testo della label di stato
            self.root.update_idletasks()  # Forza l'aggiornamento della GUI

    def go_back(self):
        """
        Destroy the dashboard window and return to the main dashboard via callback.
        """
        self.root.destroy()  # Chiude la finestra della dashboard insegnante
        self.main_dashboard_callback()  # Chiama la funzione di callback per tornare alla dashboard principale

if __name__ == "__main__":  # Esegue questo blocco solo se il file è eseguito direttamente (non importato)
    # Test the teacher dashboard
    class MockTeacher:  # Definisce una classe fittizia per simulare un insegnante
        def __init__(self):  # Costruttore della classe MockTeacher
            self.name = "Dr. Smith"  # Imposta il nome dell'insegnante fittizio
            self.surname = "Johnson"  # Imposta il cognome dell'insegnante fittizio
            self.role = "teacher"  # Imposta il ruolo dell'insegnante fittizio
    
    def mock_callback():  # Definisce una funzione di callback fittizia
        print("Back to main dashboard")  # Stampa un messaggio quando si torna alla dashboard principale
    
    root = tk.Tk()  # Crea la finestra principale Tkinter
    teacher = MockTeacher()  # Crea un oggetto insegnante fittizio
    app = TeacherDashboard(root, teacher, mock_callback)  # Crea la dashboard insegnante con i parametri di test
    root.mainloop()  # Avvia il ciclo principale della GUI (mostra la finestra e gestisce gli eventi)