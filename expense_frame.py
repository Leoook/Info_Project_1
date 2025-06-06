import tkinter as tk  # Libreria per creare GUI
from tkinter import messagebox  # Per finestre popup di errore o avviso

from PythonExpenseApp.db_connection import DbConnection  # Gestione connessione al database
from PythonExpenseApp.expense import Expense  # Classe che rappresenta una spesa
from PythonExpenseApp.feedback import Feedback  # Classe per gestire feedback utente (non usata direttamente qui)

class ExpenseFrame(tk.Frame):  # Classe per la schermata di inserimento spese
    def __init__(self, master, switch_callback, back_frame):  # Costruttore con parametri con funzione di cambio schermata
        super().__init__(master)  # Inizializza il frame base di tkinter
        self.switch_callback = switch_callback  # Salva la callback per cambiare frame
        self.back_frame = back_frame

        # Freccia indietro
        back_btn = tk.Button( # Freccia per tornare al frame precedente
            self,
            text="←",
            font=("Arial", 16, "bold"),
            command=lambda: self.switch_callback(self.back_frame), # Torna al frame precedente quando cliccata
            width=3
        )
        back_btn.grid(row=0, column=0, padx=6, pady=6, sticky="w", columnspan=2) # Posiziona la freccia in alto a sinistra

        # Frame per gli input (usa grid anche qui)
        input_frame = tk.Frame(self)
        input_frame.grid(row=1, column=0, columnspan=2, sticky="ew", padx=5, pady=5)

        # Esempio di campi input:
        tk.Label(input_frame, text="Descrizione:").grid(row=0, column=0, padx=5, pady=5, sticky="e") # Etichetta "Descrizione"
        self.desc_entry = tk.Entry(input_frame) # Campo per inserire la descrizione della spesa
        self.desc_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w") # Campo di input per la descrizione

        tk.Label(input_frame, text="Importo:").grid(row=1, column=0, padx=5, pady=5, sticky="e") # Etichetta "Importo"
        self.amount_entry = tk.Entry(input_frame)
        self.amount_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        tk.Label(input_frame, text="Student Name:").grid(row=2, column=0, padx=8, pady=6, sticky="e")  # Etichetta "Student Name"
        self.name_entry = tk.Entry(input_frame)  # Campo per inserire il nome dello studente
        self.name_entry.grid(row=2, column=1, padx=8, pady=6, sticky="w") # Campo di input per il nome dello studente

        tk.Label(input_frame, text="Surname:").grid(row=3, column=0, padx=8, pady=6, sticky="e")  # Etichetta "Surname"
        self.surname_var = tk.StringVar()  # Variabile associata al campo cognome
        self.surname_entry = tk.Entry(input_frame, textvariable=self.surname_var, state="readonly")  # Campo solo lettura
        self.surname_entry.grid(row=3, column=1, padx=8, pady=6, sticky="w")

        """tk.Button(input_frame, text="Search Student", command=self.search_student, width=16).grid(
            row=2, column=2, padx=8, pady=6)  # Bottone per cercare lo studente nel DB
        tk.Button(input_frame, text="Add Expense", command=self.add_expense, width=16).grid(
            row=4, column=0, columnspan=3, pady=(16, 8))  # Bottone per aggiungere la spesa
"""
        # Area testuale per mostrare le spese
        self.expense_list_area = tk.Text(self, state="normal") #Area di testo per visualizzare le spese
        self.expense_list_area.grid(row=2, column=0, columnspan=2, sticky="nsew", padx=5, pady=5) # Area di testo per le spese

        # Permetti alla text area di espandersi
        self.grid_rowconfigure(2, weight=1) # Configura la riga della text area per espandersi
        self.grid_columnconfigure(0, weight=1) #   Configura la colonna della text area per espandersi

def search_student(self):
        name = self.name_entry.get()  # Prende il nome dallo user input
        if not name.strip():  # Se il campo è vuoto
            messagebox.showerror("Error", "Please enter a student name.")  # Mostra messaggio di errore
            return

        connection = DbConnection.connect()  # Connessione al database
        if connection:
            try:
                sql = "SELECT id, surname FROM students WHERE name = %s LIMIT 1"  # Query per trovare lo studente
                cursor = connection.cursor() # Crea un cursore per eseguire la query
                cursor.execute(sql, (name,)) # Esegue la query con il nome inserito
                result = cursor.fetchone() # Recupera il primo risultato della query

                if result:  # Se lo studente è stato trovato
                    student_id, surname = result # Estrae l'ID e il cognome
                    self.student_id_var = student_id  # Salva ID studente
                    self.surname_var.set(surname)  # Visualizza il cognome nel campo readonly
                else:
                    messagebox.showinfo("Not found", "No student found with that name.")  # Studente non trovato
            except Exception as e:
                messagebox.showerror("Error", str(e))  #Mostra eventuali errori durante l'esecuzione della query
                
def add_expense(self):
        amount_text = self.amount_entry.get()  # Ottiene il valore del campo importo
        description = self.desc_entry.get()  # Ottiene la descrizione

        if amount_text and description:  # Verifica che entrambi i campi siano compilati
            try:
                amount = float(amount_text)  # Converte il testo in float
                expense = Expense(amount, description)  # Crea un oggetto Expense
                self.expenses.append(expense)  # Aggiunge alla lista locale
                expense.save_to_database()  # Salva la spesa nel database

                self.update_expense_list()  # Aggiorna l'area di testo con la lista delle spese
                self.amount_entry.delete(0, tk.END)  # Svuota il campo importo
                self.desc_entry.delete(0, tk.END)  # Svuota il campo descrizione
            except ValueError:  # Errore se l’importo non è numerico
                messagebox.showerror("Error", "Amount must be a number.")
        else:
            messagebox.showerror("Error", "Please enter both amount and description.")  # Se uno dei due è vuoto

def update_expense_list(self):
        self.expense_list_area.config(state="normal")  # Rende modificabile la text area
        self.expense_list_area.delete("1.0", tk.END)  # Cancella il contenuto attuale
        for exp in self.expenses:  # Inserisce ogni spesa nella text area
            self.expense_list_area.insert(tk.END, str(exp) + "\n")
        self.expense_list_area.config(state="disabled")  # Rende di nuovo la text area non modificabile

# Importazione ritardata per evitare importazioni circolari
from PythonExpenseApp.gui.homepage_frame import HomepageFrame