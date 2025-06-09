from tkinter import messagebox, ttk  # Importa i moduli per messaggi e widget avanzati di Tkinter
from PythonExpenseApp.db_connection import DbConnection  # Importa la classe per la connessione al database
from PythonExpenseApp.expense import Expense  # Importa la classe Expense (gestione spese)
import tkinter as tk  # Importa la libreria base per la GUI
import mysql.connector  # Importa il connettore MySQL

class ExpenseGUI:
    """
    Enhanced GUI for managing and recording expenses with multiple participants.
    """
    def __init__(self, root, current_student=None, main_callback=None):
        self.root = root  # Salva la finestra principale
        self.current_student = current_student # Oggetto studente corrente (ha anche .role)
        self.main_callback = main_callback  # Callback per tornare alla dashboard principale
        self.root.title("Advanced Expense Tracker")  # Imposta il titolo della finestra
        self.root.geometry("1400x800")  # Imposta la dimensione della finestra
        self.root.resizable(True, True)  # Rende la finestra ridimensionabile
        self.root.configure(bg='#f8fafc')  # Imposta il colore di sfondo
        
        # Main container
        main_container = tk.Frame(self.root, bg='#ffffff', relief='solid', bd=1)  # Crea un frame principale con bordo
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)  # Posiziona il frame nella finestra
        
        # Header with back button
        self.create_header(main_container)  # Crea l'header con titolo e pulsante indietro
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(main_container)  # Crea un widget notebook (tab)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)  # Posiziona il notebook
        
        # Create tabs
        self.create_add_expense_tab()  # Crea il tab per aggiungere spese
        self.create_debt_tracker_tab()  # Crea il tab per tracciare i debiti
        
        # Group management is now only available in the Teacher Dashboard
        
        # Status bar
        self.status_frame = tk.Frame(main_container, bg='#e5e7eb', height=30)  # Crea una barra di stato in basso
        self.status_frame.pack(fill=tk.X, side=tk.BOTTOM)  # Posiziona la barra in basso
        self.status_frame.pack_propagate(False)  # Impedisce il ridimensionamento automatico
        
        self.status_label = tk.Label(self.status_frame, text="Ready",  # Label di stato
                                    font=("Segoe UI", 10), bg="#e5e7eb", fg="#64748b")
        self.status_label.pack(side=tk.LEFT, padx=10, pady=5)  # Posiziona la label a sinistra

    def create_header(self, parent):
        """Create header with title and back button"""
        header_frame = tk.Frame(parent, bg='#ffffff', height=80)  # Crea un frame per l'header
        header_frame.pack(fill=tk.X, padx=20, pady=(20, 10))  # Posiziona il frame in alto
        header_frame.pack_propagate(False)  # Impedisce il ridimensionamento automatico
        
        # Back button
        if self.main_callback:  # Se è stata fornita una callback per tornare indietro
            back_btn = tk.Button(header_frame, text="← Back to Main",  # Crea il pulsante "Back"
                                font=("Segoe UI", 12, "bold"), bg="#6b7280", fg="white",
                                relief='flat', bd=0, activebackground="#4b5563",
                                cursor="hand2", command=self.go_back_to_main)
            back_btn.pack(side=tk.LEFT, pady=10)  # Posiziona il pulsante a sinistra
        
        # Title
        title_label = tk.Label(header_frame, text="💰 Advanced Expense Tracker",  # Titolo della finestra
                              font=("Segoe UI", 24, "bold"), bg="#ffffff", fg="#1e293b")
        title_label.pack(side=tk.LEFT, padx=(20, 0), pady=10)  # Posiziona il titolo a sinistra
        
        # User info
        if self.current_student:  # Se è presente uno studente
            user_info = tk.Label(header_frame, 
                                text=f"User: {self.current_student.name} {getattr(self.current_student, 'surname', '')}", 
                                font=("Segoe UI", 12, "bold"), bg="#ffffff", fg="#059669")
            user_info.pack(side=tk.RIGHT, pady=10)  # Posiziona la label a destra

    def go_back_to_main(self):
        """Close this window and return to main dashboard"""
        self.root.destroy()  # Chiude la finestra corrente
        if self.main_callback:  # Se è stata fornita una callback
            self.main_callback()  # Chiama la callback per tornare indietro

    def create_add_expense_tab(self):
        """Create the add expense tab"""
        add_expense_frame = tk.Frame(self.notebook, bg='#ffffff')  # Crea un frame per il tab "Add Expense"
        self.notebook.add(add_expense_frame, text="Add Expense")  # Aggiunge il tab al notebook
        
        # Header
        header_frame = tk.Frame(add_expense_frame, bg='#ffffff', height=60)  # Crea un frame per l'header del tab
        header_frame.pack(fill=tk.X, padx=20, pady=(20, 10), side=tk.TOP)  # Posiziona il frame in alto
        header_frame.pack_propagate(False)  # Impedisce il ridimensionamento automatico
        
        title_label = tk.Label(header_frame, text="💰 Add New Expense",  # Titolo del tab
                              font=("Segoe UI", 24, "bold"), bg="#ffffff", fg="#1e293b")
        title_label.pack(anchor='w')  # Allinea il titolo a sinistra
        
        # Create a container for the canvas and scrollbars
        canvas_container = tk.Frame(add_expense_frame, bg='#ffffff')  # Crea un frame per il canvas e le scrollbar
        canvas_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)  # Posiziona il frame
        
        # Create Canvas
        canvas = tk.Canvas(canvas_container, bg='#ffffff', highlightthickness=0)  # Crea un canvas per lo scrolling
        
        # Create Vertical Scrollbar
        v_scrollbar = ttk.Scrollbar(canvas_container, orient="vertical", command=canvas.yview)  # Scrollbar verticale
        v_scrollbar.pack(side=tk.RIGHT, fill="y")  # Posiziona la scrollbar a destra
        
        # Create Horizontal Scrollbar
        h_scrollbar = ttk.Scrollbar(canvas_container, orient="horizontal", command=canvas.xview)  # Scrollbar orizzontale
        h_scrollbar.pack(side=tk.BOTTOM, fill="x")  # Posiziona la scrollbar in basso
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)  # Posiziona il canvas
        canvas.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)  # Collega le scrollbar
        
        # This frame will contain the actual content and be placed inside the canvas
        scrollable_inner_frame = tk.Frame(canvas, bg='#ffffff')  # Crea un frame interno scrollabile
        
        canvas.create_window((0, 0), window=scrollable_inner_frame, anchor="nw")  # Inserisce il frame nel canvas
        
        # Update scrollregion when an event Configure occurs
        scrollable_inner_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))  # Aggiorna la regione di scroll

        # Main content with three columns - now using scrollable_inner_frame
        # The 'content_frame' variable is now 'scrollable_inner_frame'
        
        # Configure grid on the scrollable_inner_frame
        scrollable_inner_frame.grid_columnconfigure(0, weight=1, minsize=400) # Prima colonna, larghezza minima 400
        scrollable_inner_frame.grid_columnconfigure(1, weight=1, minsize=400) # Seconda colonna
        scrollable_inner_frame.grid_columnconfigure(2, weight=1, minsize=400) # Terza colonna
        scrollable_inner_frame.grid_rowconfigure(0, weight=1) # Permette l'espansione verticale delle sezioni
        
        # Payer selection section
        self.create_payer_section(scrollable_inner_frame)  # Crea la sezione per selezionare chi ha pagato
        
        # Participants selection section
        self.create_participants_section(scrollable_inner_frame)  # Crea la sezione per selezionare chi deve pagare
        
        # Expense details section
        self.create_expense_details_section(scrollable_inner_frame)  # Crea la sezione per i dettagli della spesa

    def create_payer_section(self, parent):
        """Create the payer selection section"""
        payer_frame = tk.LabelFrame(parent, text="Who Paid?",  # Crea un frame con bordo e titolo
                                   font=("Segoe UI", 14, "bold"), bg="#ffffff", 
                                   fg="#1e293b", relief='solid', bd=2)
        payer_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 5), pady=10)  # Posiziona il frame nella griglia
        
        # Search frame
        search_frame = tk.Frame(payer_frame, bg="#ffffff")  # Crea un frame per la ricerca
        search_frame.pack(fill=tk.X, padx=15, pady=15)  # Posiziona il frame
        
        tk.Label(search_frame, text="Search Student:", font=("Segoe UI", 12, "bold"),  # Label per la ricerca
                bg="#ffffff", fg="#374151").pack(anchor='w', pady=(0, 5))
        
        self.payer_search_entry = tk.Entry(search_frame, font=("Segoe UI", 12))  # Campo di testo per la ricerca
        self.payer_search_entry.pack(fill=tk.X, pady=(0, 10), ipady=6)  # Posiziona il campo
        self.payer_search_entry.bind('<KeyRelease>', self.on_payer_search)  # Collega la ricerca al rilascio di un tasto
        
        # Payer listbox
        payer_list_frame = tk.Frame(payer_frame, bg="#ffffff")  # Crea un frame per la lista dei pagatori
        payer_list_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 15))  # Posiziona il frame
        
        payer_scrollbar = tk.Scrollbar(payer_list_frame)  # Crea una scrollbar verticale
        payer_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)  # Posiziona la scrollbar
        
        self.payer_listbox = tk.Listbox(payer_list_frame, font=("Segoe UI", 11),  # Crea la listbox dei pagatori
                                       yscrollcommand=payer_scrollbar.set,
                                       selectmode=tk.SINGLE)
        self.payer_listbox.pack(fill=tk.BOTH, expand=True)  # Posiziona la listbox
        payer_scrollbar.config(command=self.payer_listbox.yview)  # Collega la scrollbar
        
        # Selected payer display
        self.selected_payer_label = tk.Label(payer_frame, text="Selected: None",  # Label per il pagatore selezionato
                                            font=("Segoe UI", 11, "bold"), 
                                            bg="#ffffff", fg="#059669")
        self.selected_payer_label.pack(padx=15, pady=(0, 15))  # Posiziona la label
        
        self.selected_payer = None  # Inizializza il pagatore selezionato a None
        self.load_students_for_payer()  # Carica la lista degli studenti per la selezione del pagatore

    def create_participants_section(self, parent):
        """Create the participants selection section"""
        participants_frame = tk.LabelFrame(parent, text="Who Owes Money?",  # Crea un frame con bordo e titolo
                                          font=("Segoe UI", 14, "bold"), bg="#ffffff", 
                                          fg="#1e293b", relief='solid', bd=2)
        participants_frame.grid(row=0, column=1, sticky="nsew", padx=5, pady=10)  # Posiziona il frame nella griglia
        
        # Search frame
        search_frame = tk.Frame(participants_frame, bg="#ffffff")  # Crea un frame per la ricerca
        search_frame.pack(fill=tk.X, padx=15, pady=15)  # Posiziona il frame
        
        tk.Label(search_frame, text="Search Students:", font=("Segoe UI", 12, "bold"),  # Label per la ricerca
                bg="#ffffff", fg="#374151").pack(anchor='w', pady=(0, 5))
        
        self.participants_search_entry = tk.Entry(search_frame, font=("Segoe UI", 12))  # Campo di testo per la ricerca
        self.participants_search_entry.pack(fill=tk.X, pady=(0, 10), ipady=6)  # Posiziona il campo
        self.participants_search_entry.bind('<KeyRelease>', self.on_participants_search)  # Collega la ricerca al rilascio di un tasto
        
        # Available students listbox
        available_frame = tk.Frame(participants_frame, bg="#ffffff")  # Crea un frame per la lista degli studenti disponibili
        available_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 10))  # Posiziona il frame
        
        tk.Label(available_frame, text="Available Students:", font=("Segoe UI", 10, "bold"),  # Label sopra la lista
                bg="#ffffff", fg="#374151").pack(anchor='w', pady=(0, 5))
        
        available_list_frame = tk.Frame(available_frame, bg="#ffffff")  # Frame per la listbox e scrollbar
        available_list_frame.pack(fill=tk.BOTH, expand=True)  # Posiziona il frame
        
        available_scrollbar = tk.Scrollbar(available_list_frame)  # Scrollbar verticale
        available_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)  # Posiziona la scrollbar
        
        self.available_listbox = tk.Listbox(available_list_frame, font=("Segoe UI", 10),  # Listbox degli studenti disponibili
                                           yscrollcommand=available_scrollbar.set,
                                           selectmode=tk.MULTIPLE)
        self.available_listbox.pack(fill=tk.BOTH, expand=True)  # Posiziona la listbox
        available_scrollbar.config(command=self.available_listbox.yview)  # Collega la scrollbar
        
        # Buttons frame
        buttons_frame = tk.Frame(participants_frame, bg="#ffffff")  # Crea un frame per i pulsanti
        buttons_frame.pack(fill=tk.X, padx=15, pady=10)  # Posiziona il frame
        
        add_btn = tk.Button(buttons_frame, text="Add →", font=("Segoe UI", 10, "bold"),
                           bg="#3b82f6", fg="white", command=self.add_participants)
        add_btn.pack(side=tk.LEFT, padx=(0, 5))  # Pulsante per aggiungere partecipanti
        
        remove_btn = tk.Button(buttons_frame, text="← Remove", font=("Segoe UI", 10, "bold"),
                              bg="#dc2626", fg="white", command=self.remove_participants)
        remove_btn.pack(side=tk.LEFT, padx=5)  # Pulsante per rimuovere partecipanti
        
        clear_btn = tk.Button(buttons_frame, text="Clear All", font=("Segoe UI", 10, "bold"),
                             bg="#6b7280", fg="white", command=self.clear_participants)
        clear_btn.pack(side=tk.LEFT, padx=5)  # Pulsante per cancellare tutti i partecipanti
        
        # Selected participants listbox
        selected_frame = tk.Frame(participants_frame, bg="#ffffff")  # Crea un frame per la lista dei partecipanti selezionati
        selected_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 15))  # Posiziona il frame
        
        tk.Label(selected_frame, text="Selected Participants:", font=("Segoe UI", 10, "bold"),  # Label sopra la lista
                bg="#ffffff", fg="#374151").pack(anchor='w', pady=(0, 5))
        
        selected_list_frame = tk.Frame(selected_frame, bg="#ffffff")  # Frame per la listbox e scrollbar
        selected_list_frame.pack(fill=tk.BOTH, expand=True)  # Posiziona il frame
        
        selected_scrollbar = tk.Scrollbar(selected_list_frame)  # Scrollbar verticale
        selected_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)  # Posiziona la scrollbar
        
        self.selected_listbox = tk.Listbox(selected_list_frame, font=("Segoe UI", 10),  # Listbox dei partecipanti selezionati
                                          yscrollcommand=selected_scrollbar.set,
                                          selectmode=tk.MULTIPLE)
        self.selected_listbox.pack(fill=tk.BOTH, expand=True)  # Posiziona la listbox
        selected_scrollbar.config(command=self.selected_listbox.yview)  # Collega la scrollbar
        
        self.selected_participants = []  # Inizializza la lista dei partecipanti selezionati
        self.load_students_for_participants()  # Carica la lista degli studenti per la selezione dei partecipanti

    def create_expense_details_section(self, parent):
        """Create the expense details section"""
        details_frame = tk.LabelFrame(parent, text="Expense Details",  # Crea un frame con bordo e titolo
                                     font=("Segoe UI", 14, "bold"), bg="#ffffff", 
                                     fg="#1e293b", relief='solid', bd=2)
        details_frame.grid(row=0, column=2, sticky="nsew", padx=(5, 0), pady=10)  # Posiziona il frame nella griglia
        
        # Form frame
        form_frame = tk.Frame(details_frame, bg="#ffffff")  # Crea un frame per il modulo di inserimento spesa
        form_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)  # Posiziona il frame
        
        # Amount field
        tk.Label(form_frame, text="Total Amount (€):", font=("Segoe UI", 12, "bold"),  # Label per l'importo totale
                bg="#ffffff", fg="#374151").pack(anchor='w', pady=(0, 5))
        
        self.amount_entry = tk.Entry(form_frame, font=("Segoe UI", 12))  # Campo di testo per l'importo
        self.amount_entry.pack(fill=tk.X, pady=(0, 15), ipady=6)  # Posiziona il campo
        
        # Description field
        tk.Label(form_frame, text="Description:", font=("Segoe UI", 12, "bold"),  # Label per la descrizione
                bg="#ffffff", fg="#374151").pack(anchor='w', pady=(0, 5))
        
        self.desc_entry = tk.Entry(form_frame, font=("Segoe UI", 12))  # Campo di testo per la descrizione
        self.desc_entry.pack(fill=tk.X, pady=(0, 15), ipady=6)  # Posiziona il campo
        
        # Split method
        tk.Label(form_frame, text="Split Method:", font=("Segoe UI", 12, "bold"),  # Label per il metodo di suddivisione
                bg="#ffffff", fg="#374151").pack(anchor='w', pady=(0, 5))
        
        self.split_var = tk.StringVar(value="equal")  # Variabile per il metodo di suddivisione (default: uguale)
        split_frame = tk.Frame(form_frame, bg="#ffffff")  # Crea un frame per i pulsanti di suddivisione
        split_frame.pack(fill=tk.X, pady=(0, 15))  # Posiziona il frame
        
        tk.Radiobutton(split_frame, text="Equal Split", variable=self.split_var,  # Pulsante per suddivisione uguale
                      value="equal", bg="#ffffff", font=("Segoe UI", 11)).pack(anchor='w')
        tk.Radiobutton(split_frame, text="Custom Split", variable=self.split_var,  # Pulsante per suddivisione personalizzata
                      value="custom", bg="#ffffff", font=("Segoe UI", 11)).pack(anchor='w')
        
        # Summary
        summary_frame = tk.LabelFrame(form_frame, text="Summary",  # Crea un frame per il riepilogo
                                     font=("Segoe UI", 11, "bold"), bg="#f8fafc")
        summary_frame.pack(fill=tk.X, pady=15)  # Posiziona il frame
        
        self.summary_label = tk.Label(summary_frame, text="Select payer and participants",  # Label per il riepilogo
                                     font=("Segoe UI", 10), bg="#f8fafc", fg="#64748b",
                                     justify=tk.LEFT, wraplength=300)
        self.summary_label.pack(padx=10, pady=10)  # Posiziona la label
        
        # Add expense button
        add_btn = tk.Button(form_frame, text="Add Expense", font=("Segoe UI", 14, "bold"),  # Pulsante per aggiungere la spesa
                           bg="#059669", fg="#ffffff", relief='flat', bd=0,
                           activebackground="#047857", cursor="hand2", 
                           command=self.add_expense)
        add_btn.pack(fill=tk.X, pady=20, ipady=12)  # Posiziona il pulsante
        
        # Bind events to update summary
        self.payer_listbox.bind('<<ListboxSelect>>', self.update_summary)  # Aggiorna il riepilogo alla selezione del pagatore
        self.amount_entry.bind('<KeyRelease>', self.update_summary)  # Aggiorna il riepilogo al rilascio di un tasto

    def create_debt_tracker_tab(self):
        """Create the debt tracker tab"""
        debt_frame = tk.Frame(self.notebook, bg='#ffffff')  # Crea un frame per il tab "Debt Tracker"
        self.notebook.add(debt_frame, text="Debt Tracker")  # Aggiunge il tab al notebook
        
        # Header
        header_frame = tk.Frame(debt_frame, bg='#ffffff', height=60)  # Crea un frame per l'header del tab
        header_frame.pack(fill=tk.X, padx=20, pady=(20, 10))  # Posiziona il frame in alto
        header_frame.pack_propagate(False)  # Impedisce il ridimensionamento automatico
        
        title_label = tk.Label(header_frame, text="📊 Debt Tracker",  # Titolo del tab
                              font=("Segoe UI", 24, "bold"), bg="#ffffff", fg="#1e293b")
        title_label.pack(anchor='w')  # Allinea il titolo a sinistra
        
        # Content frame
        content_frame = tk.Frame(debt_frame, bg='#ffffff')  # Crea un frame per il contenuto del tab
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)  # Posiziona il frame
        
        # Configure grid
        content_frame.grid_columnconfigure(0, weight=1)  # Prima colonna espandibile
        content_frame.grid_columnconfigure(1, weight=1)  # Seconda colonna espandibile
        content_frame.grid_rowconfigure(0, weight=1)  # Prima riga espandibile
        
        # People who owe you money
        owe_you_frame = tk.LabelFrame(content_frame, text="People Who Owe You Money",  # Crea un frame con bordo e titolo
                                     font=("Segoe UI", 14, "bold"), bg="#ffffff", 
                                     fg="#dc2626", relief='solid', bd=2)
        owe_you_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10), pady=10)  # Posiziona il frame nella griglia
        
        owe_you_list_frame = tk.Frame(owe_you_frame, bg="#ffffff")  # Crea un frame per la lista di chi deve soldi
        owe_you_list_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)  # Posiziona il frame
        
        owe_you_scrollbar = tk.Scrollbar(owe_you_list_frame)  # Crea una scrollbar verticale
        owe_you_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)  # Posiziona la scrollbar
        
        self.owe_you_listbox = tk.Listbox(owe_you_list_frame, font=("Segoe UI", 11),  # Crea la listbox di chi deve soldi
                                         yscrollcommand=owe_you_scrollbar.set)
        self.owe_you_listbox.pack(fill=tk.BOTH, expand=True)  # Posiziona la listbox
        owe_you_scrollbar.config(command=self.owe_you_listbox.yview)  # Collega la scrollbar
        
        # People you owe money to
        you_owe_frame = tk.LabelFrame(content_frame, text="People You Owe Money To",  # Crea un frame con bordo e titolo
                                     font=("Segoe UI", 14, "bold"), bg="#ffffff", 
                                     fg="#059669", relief='solid', bd=2)
        you_owe_frame.grid(row=0, column=1, sticky="nsew", padx=(10, 0), pady=10)  # Posiziona il frame nella griglia
        
        you_owe_list_frame = tk.Frame(you_owe_frame, bg="#ffffff")  # Crea un frame per la lista di chi deve essere pagato
        you_owe_list_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)  # Posiziona il frame
        
        you_owe_scrollbar = tk.Scrollbar(you_owe_list_frame)  # Crea una scrollbar verticale
        you_owe_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)  # Posiziona la scrollbar
        
        self.you_owe_listbox = tk.Listbox(you_owe_list_frame, font=("Segoe UI", 11),  # Crea la listbox di chi deve essere pagato
                                         yscrollcommand=you_owe_scrollbar.set)
        self.you_owe_listbox.pack(fill=tk.BOTH, expand=True)  # Posiziona la listbox
        you_owe_scrollbar.config(command=self.you_owe_listbox.yview)  # Collega la scrollbar
        
        # Refresh button
        refresh_btn = tk.Button(debt_frame, text="Refresh Debts", font=("Segoe UI", 12, "bold"),  # Crea il pulsante per aggiornare i debiti
                               bg="#3b82f6", fg="white", command=self.load_debts)
        refresh_btn.pack(pady=20)  # Posiziona il pulsante con padding verticale
        
        # Load initial debt data
        self.load_debts()  # Carica i dati dei debiti all'avvio del tab

    def load_students_for_payer(self):
        """Load all students for payer selection"""
        connection = DbConnection.connect()  # Stabilisce la connessione al database
        if connection:
            try:
                cursor = connection.cursor()  # Crea un cursore per eseguire le query
                cursor.execute("SELECT id, name, surname FROM students ORDER BY name, surname")  # Seleziona tutti gli studenti
                students = cursor.fetchall()  # Recupera tutti i risultati
                
                self.payer_listbox.delete(0, tk.END)  # Pulisce la listbox dei pagatori
                self.all_students = []  # Inizializza la lista di tutti gli studenti
                
                for student_id, name, surname in students:  # Cicla su ogni studente
                    display_text = f"{name} {surname}"  # Testo da visualizzare nella listbox
                    self.payer_listbox.insert(tk.END, display_text)  # Aggiunge lo studente alla listbox
                    self.all_students.append((student_id, name, surname))  # Aggiunge lo studente alla lista completa
                    
                connection.close()  # Chiude la connessione al database
            except Exception as e:
                self.status_label.config(text=f"Error loading students: {e}")  # Mostra un messaggio di errore

    def load_students_for_participants(self):
        """Load all students for participants selection"""
        connection = DbConnection.connect()  # Stabilisce la connessione al database
        if connection:
            try:
                cursor = connection.cursor()  # Crea un cursore per eseguire le query
                cursor.execute("SELECT id, name, surname FROM students ORDER BY name, surname")  # Seleziona tutti gli studenti
                students = cursor.fetchall()  # Recupera tutti i risultati
                
                self.available_listbox.delete(0, tk.END)  # Pulisce la listbox degli studenti disponibili
                self.all_participants = []  # Inizializza la lista di tutti i partecipanti
                
                for student_id, name, surname in students:  # Cicla su ogni studente
                    display_text = f"{name} {surname}"  # Testo da visualizzare nella listbox
                    self.available_listbox.insert(tk.END, display_text)  # Aggiunge lo studente alla listbox
                    self.all_participants.append((student_id, name, surname))  # Aggiunge lo studente alla lista completa
                    
                connection.close()  # Chiude la connessione al database
            except Exception as e:
                self.status_label.config(text=f"Error loading students: {e}")  # Mostra un messaggio di errore

    def on_payer_search(self, event):
        """Handle payer search"""
        search_term = self.payer_search_entry.get().lower()  # Ottiene il termine di ricerca dalla entry
        self.payer_listbox.delete(0, tk.END)  # Pulisce la listbox dei pagatori
        
        for i, (student_id, name, surname) in enumerate(self.all_students):  # Cicla su tutti gli studenti
            if search_term in f"{name} {surname}".lower():  # Se il termine di ricerca è nel nome o cognome
                display_text = f"{name} {surname}"  # Testo da visualizzare nella listbox
                self.payer_listbox.insert(tk.END, display_text)  # Aggiunge lo studente alla listbox

    def on_participants_search(self, event):
        """Handle participants search"""
        search_term = self.participants_search_entry.get().lower()  # Ottiene il termine di ricerca dalla entry
        self.available_listbox.delete(0, tk.END)  # Pulisce la listbox degli studenti disponibili
        
        for i, (student_id, name, surname) in enumerate(self.all_participants):  # Cicla su tutti i partecipanti
            if search_term in f"{name} {surname}".lower():  # Se il termine di ricerca è nel nome o cognome
                display_text = f"{name} {surname}"  # Testo da visualizzare nella listbox
                self.available_listbox.insert(tk.END, display_text)  # Aggiunge lo studente alla listbox

    def add_participants(self):
        """Add selected participants to the selected list"""
        selections = self.available_listbox.curselection()  # Ottiene gli indici selezionati nella listbox
        for i in selections:  # Cicla sugli indici selezionati
            participant_text = self.available_listbox.get(i)  # Ottiene il testo dell'elemento selezionato
            # Find the corresponding student data
            for student_id, name, surname in self.all_participants:  # Cerca lo studente corrispondente
                if f"{name} {surname}" == participant_text:  # Se il testo corrisponde
                    if (student_id, name, surname) not in self.selected_participants:  # Se non è già selezionato
                        self.selected_participants.append((student_id, name, surname))  # Aggiunge il partecipante alla lista
                        self.selected_listbox.insert(tk.END, participant_text)  # Aggiunge il partecipante alla listbox
                    break
        self.update_summary()  # Aggiorna il riepilogo

    def remove_participants(self):
        """Remove selected participants from the selected list"""
        selections = self.selected_listbox.curselection()  # Ottiene gli indici selezionati nella listbox dei partecipanti selezionati
        for i in reversed(selections):  # Cicla sugli indici selezionati (al contrario per evitare problemi di indice)
            participant_text = self.selected_listbox.get(i)  # Ottiene il testo dell'elemento selezionato
            # Find and remove from selected_participants
            for j, (student_id, name, surname) in enumerate(self.selected_participants):  # Cerca il partecipante corrispondente
                if f"{name} {surname}" == participant_text:  # Se il testo corrisponde
                    self.selected_participants.pop(j)  # Rimuove il partecipante dalla lista
                    break
            self.selected_listbox.delete(i)  # Rimuove l'elemento dalla listbox
        self.update_summary()  # Aggiorna il riepilogo

    def clear_participants(self):
        """Clear all selected participants"""
        self.selected_participants.clear()  # Pulisce la lista dei partecipanti selezionati
        self.selected_listbox.delete(0, tk.END)  # Pulisce la listbox
        self.update_summary()  # Aggiorna il riepilogo

    def update_summary(self, event=None):
        """Update the expense summary"""
        # Get selected payer
        payer_selection = self.payer_listbox.curselection()  # Ottiene il pagatore selezionato
        if payer_selection:
            payer_text = self.payer_listbox.get(payer_selection[0])  # Ottiene il testo del pagatore
            self.selected_payer_label.config(text=f"Selected: {payer_text}")  # Aggiorna la label del pagatore selezionato
            
            # Find payer data
            for student_id, name, surname in self.all_students:  # Cerca i dati del pagatore
                if f"{name} {surname}" == payer_text:  # Se il testo corrisponde
                    self.selected_payer = (student_id, name, surname)
                    break
        else:
            self.selected_payer = None  # Nessun pagatore selezionato
            self.selected_payer_label.config(text="Selected: None")  # Aggiorna la label

        # Update summary
        try:
            amount = float(self.amount_entry.get() or 0)  # Ottiene l'importo inserito
            num_participants = len(self.selected_participants)  # Ottiene il numero di partecipanti
            
            if self.selected_payer and num_participants > 0 and amount > 0:  # Se pagatore e partecipanti sono selezionati e l'importo è valido
                per_person = amount / num_participants  # Calcola l'importo per persona
                summary_text = f"Payer: {self.selected_payer[1]} {self.selected_payer[2]}\n"  # Riepilogo del pagatore
                summary_text += f"Total: €{amount:.2f}\n"  # Riepilogo dell'importo totale
                summary_text += f"Participants: {num_participants}\n"  # Riepilogo del numero di partecipanti
                summary_text += f"Per person: €{per_person:.2f}"  # Riepilogo dell'importo per persona
            else:
                summary_text = "Select payer, participants, and enter amount"  # Messaggio di avviso
                
            self.summary_label.config(text=summary_text)  # Aggiorna il testo del riepilogo
        except ValueError:
            self.summary_label.config(text="Enter valid amount")  # Messaggio di errore per importo non valido

    def add_expense(self):
        """Add the expense to the database"""
        if not self.selected_payer:  # Controlla se è stato selezionato un pagatore
            messagebox.showerror("Error", "Please select who paid for the expense.")  # Messaggio di errore
            return
            
        if not self.selected_participants:  # Controlla se sono stati selezionati dei partecipanti
            messagebox.showerror("Error", "Please select participants who owe money.")  # Messaggio di errore
            return
            
        try:
            amount = float(self.amount_entry.get())  # Ottiene l'importo inserito
            description = self.desc_entry.get().strip()  # Ottiene la descrizione inserita
            
            if amount <= 0:  # Controlla se l'importo è maggiore di 0
                messagebox.showerror("Error", "Amount must be greater than 0.")  # Messaggio di errore
                return
                
            if not description:  # Controlla se è stata inserita una descrizione
                messagebox.showerror("Error", "Please enter a description.")  # Messaggio di errore
                return
                
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid amount.")  # Messaggio di errore per importo non valido
            return
        
        # Calculate split
        per_person = amount / len(self.selected_participants)  # Calcola l'importo da pagare da ciascun partecipante
        
        # Save to database
        connection = DbConnection.connect()  # Stabilisce la connessione al database
        if not connection:
            messagebox.showerror("Error", "Could not connect to database.")  # Messaggio di errore
            return
            
        try:
            cursor = connection.cursor()  # Crea un cursore per eseguire le query
            
            # Insert main expense record
            cursor.execute("""INSERT INTO expenses (amount, description, date, id_giver, id_receiver, id_activity)
                             VALUES (%s, %s, CURDATE(), %s, NULL, NULL)""",
                          (amount, description, self.selected_payer[0]))  # Inserisce la spesa nel database
            expense_id = cursor.lastrowid  # Ottiene l'ID dell'ultima spesa inserita
            
            # Insert debt records for each participant
            for participant_id, name, surname in self.selected_participants:  # Cicla su ogni partecipante
                cursor.execute("""INSERT INTO debts (payer_id, debtor_id, amount, description, expense_id, date_created)
                                 VALUES (%s, %s, %s, %s, %s, CURDATE())""",
                              (self.selected_payer[0], participant_id, per_person, description, expense_id))  # Inserisce i debiti nel database
            
            connection.commit()  # Conferma le modifiche nel database
            messagebox.showinfo("Success", f"Expense added successfully!\nEach participant owes €{per_person:.2f}")  # Messaggio di successo
            
            # Clear form
            self.amount_entry.delete(0, tk.END)  # Pulisce il campo dell'importo
            self.desc_entry.delete(0, tk.END)  # Pulisce il campo della descrizione
            self.clear_participants()  # Pulisce la lista dei partecipanti selezionati
            self.payer_listbox.selection_clear(0, tk.END)  # Deseleziona il pagatore
            self.selected_payer = None  # Nessun pagatore selezionato
            self.selected_payer_label.config(text="Selected: None")  # Aggiorna la label
            
            # Refresh debt tracker
            self.load_debts()  # Aggiorna la visualizzazione dei debiti
            
        except Exception as e:
            messagebox.showerror("Error", f"Could not save expense: {e}")  # Mostra un messaggio di errore
        finally:
            connection.close()  # Chiude la connessione al database

    def load_debts(self):
        """Load debt information for the current user"""
        connection = DbConnection.connect()  # Stabilisce la connessione al database
        if not connection:
            return  # Esce se la connessione fallisce
        try:
            cursor = connection.cursor()  # Crea un cursore per eseguire le query
            
            # Clear existing lists
            self.owe_you_listbox.delete(0, tk.END)  # Pulisce la listbox di chi ti deve soldi
            self.you_owe_listbox.delete(0, tk.END)  # Pulisce la listbox di chi devi pagare
            
            # If we have a current student, filter debts for them
            if self.current_student:
                # Get debts where others owe the current student money
                cursor.execute("""SELECT s.name, s.surname, SUM(d.amount), COUNT(d.id)
                                 FROM debts d
                                 JOIN students s ON d.debtor_id = s.id
                                 WHERE d.paid = FALSE AND d.payer_id = %s
                                 GROUP BY d.debtor_id, s.name, s.surname
                                 ORDER BY SUM(d.amount) DESC""", (self.current_student.id,))
                
                total_owed_to_you = 0  # Inizializza il totale che ti devono
                for name, surname, amount, count in cursor.fetchall():  # Cicla su ogni persona che ti deve soldi
                    self.owe_you_listbox.insert(tk.END, f"{name} {surname}: €{amount:.2f} ({count} expenses)")  # Mostra la riga
                    total_owed_to_you += amount  # Aggiorna il totale
                    
                if total_owed_to_you > 0:  # Se qualcuno ti deve soldi
                    self.owe_you_listbox.insert(tk.END, "")  # Riga vuota
                    self.owe_you_listbox.insert(tk.END, f"TOTAL OWED TO YOU: €{total_owed_to_you:.2f}")  # Mostra il totale
                
                # Get debts where the current student owes others money
                cursor.execute("""SELECT s.name, s.surname, SUM(d.amount), COUNT(d.id)
                                 FROM debts d
                                 JOIN students s ON d.payer_id = s.id
                                 WHERE d.paid = FALSE AND d.debtor_id = %s
                                 GROUP BY d.payer_id, s.name, s.surname
                                 ORDER BY SUM(d.amount) DESC""", (self.current_student.id,))
                
                total_you_owe = 0  # Inizializza il totale che devi agli altri
                for name, surname, amount, count in cursor.fetchall():  # Cicla su ogni persona a cui devi soldi
                    self.you_owe_listbox.insert(tk.END, f"{name} {surname}: €{amount:.2f} ({count} expenses)")  # Mostra la riga
                    total_you_owe += amount  # Aggiorna il totale
                    
                if total_you_owe > 0:  # Se devi soldi a qualcuno
                    self.you_owe_listbox.insert(tk.END, "")  # Riga vuota
                    self.you_owe_listbox.insert(tk.END, f"TOTAL YOU OWE: €{total_you_owe:.2f}")  # Mostra il totale
            else:
                # Show all debts if no specific user
                # Get debts where others owe you money
                cursor.execute("""SELECT s.name, s.surname, SUM(d.amount), COUNT(d.id)
                                 FROM debts d
                                 JOIN students s ON d.debtor_id = s.id
                                 WHERE d.paid = FALSE
                                 GROUP BY d.debtor_id, s.name, s.surname
                                 ORDER BY SUM(d.amount) DESC""")
                
                total_owed_to_you = 0  # Inizializza il totale che ti devono
                for name, surname, amount, count in cursor.fetchall():  # Cicla su ogni persona che ti deve soldi
                    self.owe_you_listbox.insert(tk.END, f"{name} {surname}: €{amount:.2f} ({count} expenses)")  # Mostra la riga
                    total_owed_to_you += amount  # Aggiorna il totale
                    
                if total_owed_to_you > 0:  # Se qualcuno ti deve soldi
                    self.owe_you_listbox.insert(tk.END, "")  # Riga vuota
                    self.owe_you_listbox.insert(tk.END, f"TOTAL OWED TO YOU: €{total_owed_to_you:.2f}")  # Mostra il totale
                
                # Get debts where you owe others money
                cursor.execute("""SELECT s.name, s.surname, SUM(d.amount), COUNT(d.id)
                                 FROM debts d
                                 JOIN students s ON d.payer_id = s.id
                                 WHERE d.paid = FALSE
                                 GROUP BY d.payer_id, s.name, s.surname
                                 ORDER BY SUM(d.amount) DESC""")
                
                total_you_owe = 0  # Inizializza il totale che devi agli altri
                for name, surname, amount, count in cursor.fetchall():  # Cicla su ogni persona a cui devi soldi
                    self.you_owe_listbox.insert(tk.END, f"{name} {surname}: €{amount:.2f} ({count} expenses)")  # Mostra la riga
                    total_you_owe += amount  # Aggiorna il totale
                    
                if total_you_owe > 0:  # Se devi soldi a qualcuno
                    self.you_owe_listbox.insert(tk.END, "")  # Riga vuota
                    self.you_owe_listbox.insert(tk.END, f"TOTAL YOU OWE: €{total_you_owe:.2f}")  # Mostra il totale
        except Exception as err:
            self.status_label.config(text=f"Error loading debts: {err}")  # Mostra un messaggio di errore nella barra di stato
        finally:
            connection.close()  # Chiude la connessione al database in ogni caso (sia successo che errore)

# End of ExpenseGUI class
# All group management code has been removed. Teachers use the Teacher Dashboard for these features.