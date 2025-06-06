import tkinter as tk  # Importa la libreria tkinter per creare interfacce grafiche
from tkinter import messagebox  # Per popup di errore o informazione
import mysql.connector  # Per la connessione al database MySQL

from PythonExpenseApp.db_connection import DbConnection  # Gestione connessione al database
from PythonExpenseApp.gui.homepage_frame import HomepageFrame  # Per tornare alla homepage (non serve più se usi back_frame)
from PythonExpenseApp.feedback import Feedback  # Classe Feedback (non usata direttamente qui)
from PythonExpenseApp.statistics import Statistics  # Importa la classe Statistics
from PythonExpenseApp.gui.statistics_frame import StatisticsFrame  # Importa il nuovo frame delle statistiche (crealo se non esiste)

class ActivityFrame(tk.Frame):  # Definisce il frame per la gestione delle attività
    def __init__(self, master, switch_callback, back_frame):  # Costruttore: riceve il frame genitore, la funzione di cambio frame e il frame di ritorno
        super().__init__(master)  # Inizializza il frame base di tkinter
        self.switch_callback = switch_callback  # Salva la callback per cambiare schermata
        self.back_frame = back_frame  # Salva il frame di ritorno per la freccia

        # Freccia indietro in alto a sinistra
        back_btn = tk.Button(
            self, # Bottone per tornare al frame precedente
            text="←",
            font=("Arial", 16, "bold"),
            command=lambda: self.switch_callback(self.back_frame),  # Torna al frame precedente
            width=3
        )
        back_btn.grid(row=0, column=0, padx=6, pady=6, sticky="w", columnspan=2)  # Posiziona la freccia

        # Recupera le attività dal database
        self.activities = []  # Lista delle attività da mostrare
        self.activity_ids = []  # Lista degli id delle attività
        connection = DbConnection.connect()  # Connessione al database
        if connection:
            try:
                sql = "SELECT id, name, max_participants FROM activities"  # Query per recuperare le attività
                statement = connection.cursor()
                statement.execute(sql)
                for (id_, name, maxp) in statement:  # Per ogni attività trovata
                    self.activities.append(f"{name} (max: {maxp})")  # Aggiungi nome e max partecipanti alla lista
                    self.activity_ids.append(id_)  # Salva l'id corrispondente
            except mysql.connector.Error as e:
                messagebox.showerror("Error", f"Error loading activities: {e}")  # Mostra errore se la query fallisce

        # Label e Listbox per la selezione attività
        tk.Label(self, text="Select Activity:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.activity_var = tk.StringVar()
        self.activity_listbox = tk.Listbox(self, listvariable=tk.StringVar(value=self.activities), height=6)
        self.activity_listbox.grid(row=1, column=1, padx=5, pady=5)

        # Campo Nome
        tk.Label(self, text="Name:").grid(row=2, column=0, padx=5, pady=5, sticky="e") # Etichetta per il campo Nome
        self.name_var = tk.StringVar() # Variabile associata al campo Nome
        self.name_entry = tk.Entry(self, textvariable=self.name_var) # Campo di input per il nome dello studente
        self.name_entry.grid(row=2, column=1, padx=5, pady=5) # Posiziona il campo di input per il nome     
        
        # Campo Cognome
        tk.Label(self, text="Surname:").grid(row=3, column=0, padx=5, pady=5, sticky="e")
        self.surname_var = tk.StringVar()
        self.surname_entry = tk.Entry(self, textvariable=self.surname_var)
        self.surname_entry.grid(row=3, column=1, padx=5, pady=5)

        # Campo Classe
        tk.Label(self, text="Class:").grid(row=4, column=0, padx=5, pady=5, sticky="e")
        self.class_var = tk.StringVar()
        self.class_entry = tk.Entry(self, textvariable=self.class_var)
        self.class_entry.grid(row=4, column=1, padx=5, pady=5)

        # Bottone per iscrivere lo studente all'attività
        tk.Button(self, text="Subscribe", command=self.subscribe_student).grid(row=5, column=0, columnspan=2, pady=10)

        # Bottone "Statistics" a destra della lista attività
        stats_btn = tk.Button(self, text="Statistics", command=self.open_statistics_frame)
        stats_btn.grid(row=1, column=2, rowspan=5, padx=20, pady=5, sticky="ns")

    def open_statistics_frame(self):
        # Passa al frame delle statistiche, puoi passare dati se necessario
        self.switch_callback(StatisticsFrame, ActivityFrame)

    def subscribe_student(self):  # Metodo per iscrivere lo studente all'attività selezionata
        # Controlla che sia stata selezionata un'attività
        selection = self.activity_listbox.curselection() # Recupera l'indice dell'attività selezionata
        if not selection: # Se non è stata selezionata nessuna attività
            messagebox.showerror("Error", "Please select an activity.") # Mostra errore se non è selezionata un'attività
            return
        activity_idx = selection[0] #   Recupera l'indice dell'attività selezionata
        activity_id = self.activity_ids[activity_idx] # Recupera l'id dell'attività selezionata

        # Recupera i dati dello studente
        name = self.name_var.get().strip() # Prende il nome dallo user input e rimuove spazi iniziali e finali
        surname = self.surname_var.get().strip() # Prende il cognome dallo user input e rimuove spazi iniziali e finali
        class_ = self.class_var.get().strip() # Prende la classe dallo user input e rimuove spazi iniziali e finali

        # Controlla che tutti i campi siano compilati
        if not (name and surname and class_): # Se uno dei campi è vuoto
            messagebox.showerror("Error", "Please fill all student fields.") # Mostra errore se uno dei campi è vuoto
            return

        connection = DbConnection.connect() # Connessione al database
        if not connection:
            messagebox.showerror("Error", "Database connection error.") # Mostra errore se la connessione al database fallisce
            return

        try: # Cerca lo studente nel database
            # Cerca lo studente nel database
            sql = "SELECT id FROM students WHERE name = %s AND surname = %s AND class = %s" # Query per trovare lo studente
            statement = connection.cursor() # Crea un cursore per eseguire la query
            statement.execute(sql, (name, surname, class_)) # Esegue la query con i dati dello studente
            student_row = statement.fetchone() # Recupera la prima riga del risultato della query
            if not student_row: # Se lo studente non è stato trovato
                messagebox.showerror("Error", "Student not found.") # Mostra errore se lo studente non è stato trovato
                return
            student_id = student_row[0] # Recupera l'id dello studente trovato

            # Recupera il numero massimo di partecipanti per l'attività
            sql = "SELECT max_participants FROM activities WHERE id = %s" # Query per trovare il numero massimo di partecipanti all'attività
            statement.execute(sql, (activity_id,)) # Esegue la query con l'id dell'attività selezionata
            maxp_row = statement.fetchone() # Recupera la prima riga del risultato della query
            if not maxp_row: #  Se l'attività non è stata trovata
                messagebox.showerror("Error", "Activity not found.") # Mostra errore se l'attività non è stata trovata
                return 
            max_participants = maxp_row[0] # Recupera il numero massimo di partecipanti all'attività

            # Conta i partecipanti attuali
            sql = "SELECT COUNT(*) FROM student_activities WHERE activity_id = %s" # Query per contare i partecipanti all'attività
            statement.execute(sql, (activity_id,)) # Esegue la query con l'id dell'attività selezionata
            count_row = statement.fetchone() # Recupera la prima riga del risultato della query
            current_participants = count_row[0] if count_row else 0 # Recupera il numero di partecipanti attuali all'attività

            # Controlla se l'attività è piena
            if current_participants >= max_participants: # Se il numero di partecipanti attuali è maggiore o uguale al massimo consentito
                messagebox.showerror("Error", "Activity is full.") # Mostra errore se l'attività è piena
                return

            # Iscrive lo studente all'attività
            sql = "INSERT INTO student_activities (student_id, activity_id) VALUES (%s, %s)" # Query per iscrivere lo studente all'attività
            statement.execute(sql, (student_id, activity_id)) # Esegue la query con l'id dello studente e l'id dell'attività selezionata
            connection.commit() # Salva le modifiche nel database
            messagebox.showinfo("Success", "Student subscribed to activity.") # Mostra messaggio di successo
            self.switch_callback(self.back_frame)  # Torna al frame precedente (menù studente)
        except mysql.connector.Error as e: # Gestione degli errori di database
            messagebox.showerror("Error", f"Database error: {e}") # Mostra errore se si verifica un problema con il database

class ExpenseFrame(tk.Frame): # Definisce il frame per la gestione delle spese
    def __init__(self, master, switch_callback, back_frame): # Costruttore: riceve il frame genitore, la funzione di cambio frame e il frame di ritorno
        super().__init__(master) # Inizializza il frame base di tkinter
        self.switch_callback = switch_callback # Funzione per cambiare schermata
        self.back_frame = back_frame # Frame di ritorno per la freccia indietro
        # ... (resto del codice)