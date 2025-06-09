import tkinter as tk  # Importa la libreria base per la GUI
from tkinter import messagebox  # Importa le finestre di messaggio standard di Tkinter
from PIL import Image, ImageTk, ImageDraw, ImageFilter  # Importa PIL per la gestione delle immagini (non usato qui)
from PythonExpenseApp.db_connection import DbConnection  # Importa la classe per la connessione al database
import mysql.connector  # Importa il connettore MySQL (potrebbe non essere necessario se usi solo DbConnection)

class ActivityFormGUI:
    """
    GUI per iscrivere uno studente a un'attività.
    La variabile 'self' si riferisce all'istanza corrente di ActivityFormGUI.
    Serve per accedere a variabili e metodi dell'istanza.
    Ad esempio, self.activities si riferisce alla lista delle attività per questa finestra.
    """
    def __init__(self, root, student, main_callback=None):
        """
        Inizializza la finestra GUI per l'iscrizione alle attività e i suoi widget.
        - Carica tutte le attività dal database e le mostra in una listbox.
        - Fornisce un pulsante per iscrivere lo studente all'attività selezionata.
        """
        self.root = root  # Salva la finestra principale
        self.student = student  # Salva l'oggetto studente
        self.main_callback = main_callback  # Callback per tornare alla dashboard principale
        self.root.title("Activity Subscription")  # Imposta il titolo della finestra
        self.root.geometry("1000x700")  # Imposta la dimensione della finestra
        self.root.resizable(True, True)  # Rende la finestra ridimensionabile
        self.root.configure(bg='#f8fafc')  # Imposta il colore di sfondo
        
        # Main container
        main_container = tk.Frame(self.root, bg='#ffffff', relief='solid', bd=1)  # Crea un frame principale con bordo
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)  # Posiziona il frame nella finestra
        
        # Header section with back button
        header_frame = tk.Frame(main_container, bg='#ffffff', height=100)  # Crea un frame per l'header
        header_frame.pack(fill=tk.X, padx=30, pady=(20, 10))  # Posiziona il frame in alto
        header_frame.pack_propagate(False)  # Impedisce il ridimensionamento automatico
        
        # Back button
        if self.main_callback:  # Se è stata fornita una callback per tornare indietro
            back_btn = tk.Button(header_frame, text="← Back to Main",  # Crea il pulsante "Back"
                                font=("Segoe UI", 12, "bold"), bg="#6b7280", fg="white",
                                relief='flat', bd=0, activebackground="#4b5563",
                                cursor="hand2", command=self.go_back_to_main)  # Collega il comando
            back_btn.pack(side=tk.LEFT, anchor='nw', pady=10)  # Posiziona il pulsante a sinistra
        
        # Title section
        title_section = tk.Frame(header_frame, bg='#ffffff')  # Crea un frame per il titolo
        title_section.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(20, 0))  # Posiziona il frame
        
        title_label = tk.Label(title_section, text="🎯 Activity Manager",  # Crea una label con il titolo
                              font=("Segoe UI", 28, "bold"), bg="#ffffff", fg="#1e293b")
        title_label.pack(anchor='w')  # Posiziona la label a sinistra
        
        subtitle_label = tk.Label(title_section, text="Subscribe to activities and manage your schedule",  # Sottotitolo
                                 font=("Segoe UI", 14), bg="#ffffff", fg="#64748b")
        subtitle_label.pack(anchor='w', pady=(5, 0))  # Posiziona la label sotto il titolo
        
        # Student info on the right
        student_info = tk.Label(header_frame, text=f"Student: {student.name} {getattr(student, 'surname', '')}",  # Info studente
                               font=("Segoe UI", 12, "bold"), bg="#ffffff", fg="#059669")
        student_info.pack(side=tk.RIGHT, anchor='ne', pady=10)  # Posiziona la label a destra
        
        # Content area
        content_frame = tk.Frame(main_container, bg='#ffffff')  # Crea un frame per il contenuto
        content_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=20)  # Posiziona il frame
        
        # Configure grid
        content_frame.grid_columnconfigure(0, weight=2)  # Prima colonna più larga
        content_frame.grid_columnconfigure(1, weight=1)  # Seconda colonna
        content_frame.grid_rowconfigure(0, weight=1)  # Riga espandibile
        
        # Activities section
        activities_section = tk.LabelFrame(content_frame, text="Available Activities",  # Crea un frame con bordo e titolo
                                          font=("Segoe UI", 16, "bold"), bg="#ffffff", 
                                          fg="#1e293b", relief='solid', bd=2)
        activities_section.grid(row=0, column=0, sticky="nsew", padx=(0, 10), pady=10)  # Posiziona il frame
        
        # Activities list container
        list_container = tk.Frame(activities_section, bg="#ffffff")  # Crea un frame per la lista
        list_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)  # Posiziona il frame
        
        # Scrollbar
        activities_scrollbar = tk.Scrollbar(list_container)  # Crea una scrollbar verticale
        activities_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)  # Posiziona la scrollbar
        
        self.activity_listbox = tk.Listbox(list_container, font=("Segoe UI", 11), bg="#ffffff",  # Crea la listbox delle attività
                                          fg="#374151", relief='solid', bd=1,
                                          yscrollcommand=activities_scrollbar.set,
                                          selectbackground="#dbeafe", selectforeground="#1e40af")
        self.activity_listbox.pack(fill=tk.BOTH, expand=True)  # Posiziona la listbox
        activities_scrollbar.config(command=self.activity_listbox.yview)  # Collega la scrollbar
        
        # Action section
        action_section = tk.LabelFrame(content_frame, text="Actions",  # Crea un frame per le azioni
                                      font=("Segoe UI", 16, "bold"), bg="#ffffff", 
                                      fg="#1e293b", relief='solid', bd=2)
        action_section.grid(row=0, column=1, sticky="nsew", padx=(10, 0), pady=10)  # Posiziona il frame
        
        # Action buttons frame
        button_frame = tk.Frame(action_section, bg="#ffffff")  # Crea un frame per i pulsanti
        button_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)  # Posiziona il frame
        
        # Subscribe button
        subscribe_btn = tk.Button(button_frame, text="Subscribe to Activity",  # Pulsante iscrizione
                                 font=("Segoe UI", 12, "bold"), bg="#3b82f6", fg="#ffffff", 
                                 relief='flat', bd=0, activebackground="#2563eb", 
                                 activeforeground="#ffffff", cursor="hand2", 
                                 command=self.subscribe_to_activity)
        subscribe_btn.pack(fill=tk.X, pady=10, ipady=12)  # Posiziona il pulsante
        
        # View subscriptions button
        view_btn = tk.Button(button_frame, text="View My Activities",  # Pulsante visualizza iscrizioni
                            font=("Segoe UI", 12, "bold"), bg="#059669", fg="#ffffff", 
                            relief='flat', bd=0, activebackground="#047857", 
                            activeforeground="#ffffff", cursor="hand2", 
                            command=self.view_subscriptions)
        view_btn.pack(fill=tk.X, pady=10, ipady=12)  # Posiziona il pulsante
        
        # Refresh button
        refresh_btn = tk.Button(button_frame, text="Refresh Activities",  # Pulsante aggiorna attività
                               font=("Segoe UI", 11), bg="#6b7280", fg="#ffffff", 
                               relief='flat', bd=0, activebackground="#4b5563", 
                               activeforeground="#ffffff", cursor="hand2", 
                               command=self.load_activities)
        refresh_btn.pack(fill=tk.X, pady=10, ipady=8)  # Posiziona il pulsante
        
        # View details button
        details_btn = tk.Button(button_frame, text="View Details",  # Pulsante dettagli attività
                               font=("Segoe UI", 12, "bold"), bg="#8b5cf6", fg="#ffffff", 
                               relief='flat', bd=0, activebackground="#7c3aed", 
                               activeforeground="#ffffff", cursor="hand2", 
                               command=self.view_activity_details)
        details_btn.pack(fill=tk.X, pady=10, ipady=12)  # Posiziona il pulsante
        
        # Feedback area
        feedback_frame = tk.Frame(main_container, bg='#ffffff', height=40)  # Frame per messaggi di feedback
        feedback_frame.pack(fill=tk.X, padx=30, pady=(0, 20))  # Posiziona il frame
        feedback_frame.pack_propagate(False)  # Impedisce il ridimensionamento automatico
        
        self.feedback_label = tk.Label(feedback_frame, text="", font=("Segoe UI", 12),  # Label per messaggi di feedback
                                      bg="#ffffff", fg="#dc2626")
        self.feedback_label.pack(anchor='center', pady=10)  # Posiziona la label
        
        # Initialize data
        self.activities = []  # Lista delle attività caricate
        self.activity_ids = []  # Lista degli ID delle attività
        self.activity_days = []  # Lista di tuple (giorno, inizio, fine)
        self.load_activities()  # Carica le attività dal database

    def load_activities(self):
        """Carica tutte le attività disponibili dal database"""
        self.activity_listbox.delete(0, tk.END)  # Svuota la listbox
        self.activities = []  # Svuota la lista delle attività
        self.activity_ids = []  # Svuota la lista degli ID
        self.activity_days = []  # Svuota la lista dei giorni
        
        connection = DbConnection.connect()  # Ottiene la connessione al database
        if connection:  # Se la connessione è riuscita
            try:
                cursor = connection.cursor()  # Ottiene il cursore
                cursor.execute("""SELECT id, name, day, start_time, finish_time, location, 
                                max_participants FROM activities ORDER BY day, start_time""")  # Query attività
                activities = cursor.fetchall()  # Ottiene tutte le attività
                
                for activity in activities:  # Cicla su ogni attività
                    id, name, day, start, finish, location, max_part = activity  # Estrae i dati
                    
                    # Ottieni il numero attuale di iscritti
                    cursor.execute("SELECT COUNT(*) FROM student_activities WHERE activity_id=%s", (id,))
                    current_count = cursor.fetchone()[0]
                    
                    # Formatta il testo da mostrare
                    if max_part is not None:
                        status = f"({current_count}/{max_part})"  # Mostra iscritti/max
                        full = current_count >= max_part  # True se pieno
                    else:
                        status = f"({current_count})"  # Solo iscritti
                        full = False
                    start_str = normalize_time(start)  # Formatta orario inizio
                    finish_str = normalize_time(finish)  # Formatta orario fine
                    display_text = f"📅 {day} | ⏰ {start_str}-{finish_str}"  # Riga giorno/orario
                    display_text += f"\n🎯 {name} @ {location} {status}"  # Riga nome/luogo
                    display_text += f"\n{'🔴 FULL' if full else '🟢 Available'}"  # Stato
                    
                    self.activity_listbox.insert(tk.END, display_text)  # Inserisce il testo nella listbox
                    self.activity_listbox.insert(tk.END, "")  # Riga vuota come separatore
                    
                    self.activities.append(activity)  # Salva l'attività
                    self.activity_ids.append(id)  # Salva l'ID
                    self.activity_days.append((day, start, finish))  # Salva giorno e orari
                    
                connection.close()  # Chiude la connessione
            except Exception as e:
                self.feedback_label.config(text=f"Error loading activities: {e}", fg="#dc2626")  # Mostra errore
        else:
            self.feedback_label.config(text="Could not connect to database", fg="#dc2626")  # Errore connessione

    def view_subscriptions(self):
        """Mostra le iscrizioni correnti dello studente"""
        connection = DbConnection.connect()  # Ottiene la connessione al database
        if connection:
            try:
                cursor = connection.cursor()  # Ottiene il cursore
                cursor.execute("""SELECT a.name, a.day, a.start_time, a.finish_time, a.location
                                FROM student_activities sa 
                                JOIN activities a ON sa.activity_id = a.id 
                                WHERE sa.student_id = %s 
                                ORDER BY a.day, a.start_time""", (self.student.id,))  # Query iscrizioni
                subscriptions = cursor.fetchall()  # Ottiene tutte le iscrizioni
                
                if subscriptions:  # Se ci sono iscrizioni
                    msg = "Your Current Activities:\n\n"  # Testo iniziale
                    for name, day, start, finish, location in subscriptions:  # Cicla sulle iscrizioni
                        start_str = normalize_time(start)  # Formatta orario inizio
                        finish_str = normalize_time(finish)  # Formatta orario fine
                        msg += f"📅 {day} | ⏰ {start_str}-{finish_str}\n"  # Riga giorno/orario
                        msg += f"🎯 {name} @ {location}\n\n"  # Riga nome/luogo
                    messagebox.showinfo("My Activities", msg)  # Mostra le iscrizioni
                else:
                    messagebox.showinfo("My Activities", "You are not subscribed to any activities yet.")  # Nessuna iscrizione
                    
                connection.close()  # Chiude la connessione
            except Exception as e:
                messagebox.showerror("Error", f"Could not load subscriptions: {e}")  # Mostra errore

    def subscribe_to_activity(self):
        """Iscrive lo studente all'attività selezionata"""
        selection = self.activity_listbox.curselection()  # Ottiene la selezione nella listbox
        if not selection:  # Se nulla è selezionato
            messagebox.showerror("Error", "Please select an activity.")  # Mostra errore
            return
            
        # Ottieni l'indice reale dell'attività (considerando i separatori)
        selected_index = selection[0]  # Indice selezionato
        activity_index = selected_index // 2  # Ogni altro elemento è un separatore
        
        if activity_index >= len(self.activity_ids):  # Se l'indice non è valido
            messagebox.showerror("Error", "Invalid selection.")  # Mostra errore
            return
            
        activity_id = self.activity_ids[activity_index]  # Ottieni l'ID dell'attività
        day, start_time, finish_time = self.activity_days[activity_index]  # Ottieni giorno e orari
        
        connection = DbConnection.connect()  # Ottieni la connessione al database
        if not connection:
            messagebox.showerror("Database Error", "Could not connect to the database.")  # Mostra errore
            return

        try:
            cursor = connection.cursor()  # Ottieni il cursore
            
            # Controlla conflitti di orario
            cursor.execute("""SELECT a.name, a.start_time, a.finish_time FROM student_activities sa
                            JOIN activities a ON sa.activity_id = a.id
                            WHERE sa.student_id=%s AND a.day=%s""", (self.student.id, day))
            
            for row in cursor.fetchall():  # Cicla sulle attività già iscritte nello stesso giorno
                existing_start, existing_finish = row[1], row[2]
                if not (finish_time <= existing_start or start_time >= existing_finish):  # Se c'è sovrapposizione
                    messagebox.showerror("Time Conflict", 
                                       f"You are already subscribed to '{row[0]}' at this time.")  # Mostra errore
                    return
            
            # Controlla se già iscritto
            cursor.execute("SELECT id FROM student_activities WHERE student_id=%s AND activity_id=%s", 
                          (self.student.id, activity_id))
            if cursor.fetchone():
                messagebox.showinfo("Already Subscribed", "You are already subscribed to this activity.")  # Già iscritto
                return
            
            # Controlla se l'attività è piena
            cursor.execute("SELECT COUNT(*) FROM student_activities WHERE activity_id=%s", (activity_id,))
            count = cursor.fetchone()[0]
            cursor.execute("SELECT max_participants FROM activities WHERE id=%s", (activity_id,))
            max_part = cursor.fetchone()[0]
            
            # Controlla se piena
            if max_part is not None and count >= max_part:
                messagebox.showerror("Full", "This activity is already full.")  # Mostra errore
                return
            
            # Iscrivi lo studente
            cursor.execute("INSERT INTO student_activities (student_id, activity_id) VALUES (%s, %s)", 
                          (self.student.id, activity_id))
            connection.commit()  # Conferma la transazione
            
            self.feedback_label.config(text="Successfully subscribed to activity!", fg="#059669")  # Messaggio feedback
            messagebox.showinfo("Success", "You have been subscribed to the activity.")  # Mostra successo
            
            # Aggiorna la lista per mostrare i nuovi conteggi
            self.load_activities()
            
        except Exception as e:
            messagebox.showerror("Error", f"Could not subscribe: {e}")  # Mostra errore
        finally:
            connection.close()  # Chiude la connessione

    def view_activity_details(self):  # Metodo che mostra i dettagli dell'attività selezionata
        """Mostra i dettagli dell'attività selezionata"""
        selection = self.activity_listbox.curselection()  # Ottiene la selezione nella listbox
        if not selection:  # Se nulla è selezionato
            messagebox.showerror("Error", "Please select an activity to view details.")  # Mostra errore
            return  # Esce dal metodo
            
        # Ottieni l'indice reale dell'attività (considerando i separatori)
        selected_index = selection[0]  # Indice selezionato nella listbox
        activity_index = selected_index // 2  # Ogni altro elemento è un separatore, quindi si divide per 2
        
        if activity_index >= len(self.activity_ids):  # Se l'indice non è valido
            messagebox.showerror("Error", "Invalid selection.")  # Mostra errore
            return  # Esce dal metodo
            
        activity_id = self.activity_ids[activity_index]  # Ottieni l'ID dell'attività selezionata
        
        # Crea una nuova finestra per i dettagli
        details_window = tk.Toplevel(self.root)  # Nuova finestra figlia
        from PythonExpenseApp.gui.activity_details_gui import ActivityDetailsGUI  # Importa la GUI dettagli
        ActivityDetailsGUI(details_window, activity_id, self.student)  # Mostra i dettagli dell'attività nella nuova finestra

    def go_back_to_main(self):  # Metodo per tornare alla dashboard principale
        """Chiude questa finestra e torna alla dashboard principale"""
        self.root.destroy()  # Chiude la finestra corrente
        if self.main_callback:  # Se è stata fornita una callback
            self.main_callback()  # Chiama la callback per tornare indietro

# Funzione di utilità per formattare l'orario (es. 930 -> "09:30")
def format_time(t):
    t = int(t)  # Converte in intero
    return f"{t // 100:02d}:{t % 100:02d}"  # Restituisce la stringa orario formattata

# Funzione di utilità per normalizzare orari con overflow minuti (es. 970 -> "10:10")
def normalize_time(t):
    t = int(t)  # Converte in intero
    hours = t // 100  # Calcola le ore
    minutes = t % 100  # Calcola i minuti
    # Normalizza i minuti in eccesso (es. 970 -> 10:10)
    hours += minutes // 60  # Aggiunge eventuali ore dai minuti in eccesso
    minutes = minutes % 60  # Ricalcola i minuti rimanenti
    return f"{hours:02d}:{minutes:02d}"  # Restituisce la stringa orario normalizzata
