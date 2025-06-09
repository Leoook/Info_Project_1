import tkinter as tk  # Importa la libreria base per la creazione di GUI in Python
from tkinter import ttk, messagebox  # Importa widget avanzati (ttk) e finestre di messaggio (messagebox)
from PythonExpenseApp.activity import Activity  # Importa la classe Activity dal tuo progetto
from PythonExpenseApp.feedback import Feedback  # Importa la classe Feedback dal tuo progetto

# Prova a importare matplotlib per i grafici, fallback su testo se non disponibile
try:
    import matplotlib.pyplot as plt  # Importa pyplot per creare grafici
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg  # Permette di integrare grafici matplotlib in Tkinter
    import numpy as np  # Importa numpy per operazioni numeriche
    MATPLOTLIB_AVAILABLE = True  # Flag che indica se matplotlib è disponibile
except ImportError:
    MATPLOTLIB_AVAILABLE = False  # Se matplotlib non è disponibile, imposta il flag a False
    print("Matplotlib not available. Charts will be displayed as text.")  # Messaggio di fallback

class ActivityDetailsGUI:  # Definisce la classe principale per la finestra dei dettagli attività
    def __init__(self, root, activity_id, student=None, main_callback=None):  # Costruttore della classe
        self.root = root  # Salva la finestra principale
        self.activity_id = activity_id  # Salva l'ID dell'attività da mostrare
        self.student = student  # Salva l'oggetto studente (se presente)
        self.main_callback = main_callback  # Salva la callback per tornare alla dashboard principale
        self.activity = Activity.get_activity_by_id(activity_id)  # Carica l'attività dal database tramite ID
        
        if not self.activity:  # Se l'attività non viene trovata
            messagebox.showerror("Error", "Activity not found")  # Mostra un messaggio di errore
            root.destroy() # Chiude la finestra se non trova l'attività
            return  # Esce dal costruttore
            
        self.setup_window()  # Imposta le proprietà della finestra
        self.create_interface()  # Crea la struttura grafica della finestra
        self.load_activity_details()  # Carica e mostra i dati dell'attività

    def setup_window(self):  # Metodo per impostare la finestra principale
        self.root.title(f"Activity Details - {self.activity.name}")  # Imposta il titolo della finestra
        self.root.geometry("1200x800")  # Imposta la dimensione della finestra
        self.root.configure(bg='#f8fafc')  # Imposta il colore di sfondo della finestra
        self.root.resizable(True, True)  # Rende la finestra ridimensionabile

    def create_interface(self):  # Metodo che crea la struttura grafica principale
        main_container = tk.Frame(self.root, bg='#ffffff', relief='solid', bd=1)  # Crea un frame principale con bordo
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)  # Posiziona il frame nella finestra
        
        self.create_header(main_container)  # Crea l'header con titolo e pulsanti
        
        self.notebook = ttk.Notebook(main_container)  # Crea un widget notebook (tab)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)  # Posiziona il notebook
        
        self.create_overview_tab()   # Crea il tab "Overview"
        self.create_ratings_tab()    # Crea il tab "Ratings & Statistics"
        self.create_feedback_tab()   # Crea il tab "Feedback"

    def create_header(self, parent):  # Metodo che crea l'header della finestra
        header_frame = tk.Frame(parent, bg='#ffffff', height=80)  # Crea un frame per l'header
        header_frame.pack(fill=tk.X, padx=20, pady=(20, 0))  # Posiziona il frame in alto
        header_frame.pack_propagate(False)  # Impedisce al frame di ridimensionarsi automaticamente
        
        # Pulsante "Back" per tornare alla dashboard principale
        if self.main_callback:  # Se è stata fornita una callback per tornare indietro
            back_btn = tk.Button(header_frame, text="← Back to Main",  # Crea il pulsante "Back"
                                font=("Segoe UI", 12, "bold"), bg="#6b7280", fg="white",
                                relief='flat', bd=0, activebackground="#4b5563",
                                cursor="hand2", command=self.go_back_to_main)  # Collega il comando
            back_btn.pack(side=tk.LEFT, anchor='nw', pady=10)  # Posiziona il pulsante a sinistra
        
        # Pulsante "Close" per chiudere la finestra
        close_btn = tk.Button(header_frame, text="✕ Close",  # Crea il pulsante "Close"
                             font=("Segoe UI", 12, "bold"), bg="#dc2626", fg="white",
                             relief='flat', bd=0, activebackground="#b91c1c",
                             cursor="hand2", command=self.root.destroy)  # Collega il comando di chiusura
        close_btn.pack(side=tk.RIGHT, anchor='ne', pady=10)  # Posiziona il pulsante a destra
        
        # Sezione titolo
        title_section = tk.Frame(header_frame, bg='#ffffff')  # Crea un frame per il titolo
        title_section.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(20, 20))  # Posiziona il frame
        
        # Nome attività
        title_label = tk.Label(title_section, text=f"🎯 {self.activity.name}",  # Crea una label con il nome dell'attività
                              font=("Segoe UI", 24, "bold"), bg="#ffffff", fg="#1e293b")
        title_label.pack(anchor='w')  # Posiziona la label a sinistra
        
        # Info base (giorno, orario, luogo)
        def format_time(t):  # Funzione interna per formattare l'orario
            t = int(t)  # Converte in intero
            hours = t // 100  # Ore
            minutes = t % 100  # Minuti
            hours += minutes // 60  # Gestisce overflow minuti
            minutes = minutes % 60  # Normalizza minuti
            return f"{hours:02d}:{minutes:02d}"  # Restituisce stringa formattata

        start_str = format_time(self.activity.start)  # Formatta orario di inizio
        finish_str = format_time(self.activity.finish)  # Formatta orario di fine
        info_text = f"📅 {self.activity.day} | ⏰ {start_str}-{finish_str} | 📍 {self.activity.location}"  # Crea testo info
        info_label = tk.Label(title_section, text=info_text,  # Crea una label con le info base
                             font=("Segoe UI", 12), bg="#ffffff", fg="#64748b")
        info_label.pack(anchor='w', pady=(5, 0))  # Posiziona la label sotto il titolo

    def go_back_to_main(self):  # Metodo per tornare alla dashboard principale
        """Chiude questa finestra e torna alla dashboard principale"""
        self.root.destroy()  # Chiude la finestra corrente
        if self.main_callback:  # Se è stata fornita una callback
            self.main_callback()  # Chiama la callback

    def create_overview_tab(self):  # Metodo che crea il tab "Overview"
        overview_frame = tk.Frame(self.notebook, bg='#ffffff')  # Crea un frame per il tab
        self.notebook.add(overview_frame, text="Overview")  # Aggiunge il tab al notebook
        
        # Frame scrollabile
        canvas = tk.Canvas(overview_frame, bg='#ffffff')  # Crea un canvas per lo scrolling
        scrollbar = ttk.Scrollbar(overview_frame, orient="vertical", command=canvas.yview)  # Scrollbar verticale
        scrollable_frame = tk.Frame(canvas, bg='#ffffff')  # Frame interno scrollabile
        
        scrollable_frame.bind(
            "<Configure>",  # Quando il frame cambia dimensione
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))  # Aggiorna la regione di scroll
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")  # Inserisce il frame nel canvas
        canvas.configure(yscrollcommand=scrollbar.set)  # Collega la scrollbar
        
        # Layout a griglia
        content_frame = tk.Frame(scrollable_frame, bg='#ffffff')  # Crea un frame per il contenuto
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)  # Posiziona il frame
        
        content_frame.grid_columnconfigure(0, weight=1)  # Prima colonna espandibile
        content_frame.grid_columnconfigure(1, weight=1)  # Seconda colonna espandibile
        
        self.create_info_section(content_frame)           # Crea la sezione info attività
        self.create_participation_section(content_frame)  # Crea la sezione partecipazione
        self.create_rating_summary_section(content_frame) # Crea la sezione riepilogo rating
        self.create_action_buttons(content_frame)         # Crea i pulsanti azione
        
        canvas.pack(side="left", fill="both", expand=True)  # Posiziona il canvas
        scrollbar.pack(side="right", fill="y")  # Posiziona la scrollbar

    def create_info_section(self, parent):  # Metodo che crea la sezione info attività
        info_frame = tk.LabelFrame(parent, text="Activity Information",  # Crea un frame con bordo e titolo
                                  font=("Segoe UI", 14, "bold"), bg="#ffffff")
        info_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10), pady=10)  # Posiziona il frame nella griglia
        
        # Descrizione attività
        if self.activity.description:  # Se esiste una descrizione
            desc_label = tk.Label(info_frame, text="Description:",  # Crea una label "Description:"
                                 font=("Segoe UI", 12, "bold"), bg="#ffffff")
            desc_label.pack(anchor='w', padx=15, pady=(15, 5))  # Posiziona la label
            
            desc_text = tk.Text(info_frame, height=4, font=("Segoe UI", 11),  # Crea un widget testo per la descrizione
                               bg="#f8fafc", relief='solid', bd=1, wrap=tk.WORD)
            desc_text.pack(fill=tk.X, padx=15, pady=(0, 15))  # Posiziona il testo
            desc_text.insert('1.0', self.activity.description)  # Inserisce la descrizione
            desc_text.config(state='disabled')  # Rende il testo non modificabile
        
        # Durata e capacità
        details_frame = tk.Frame(info_frame, bg="#ffffff")  # Crea un frame per dettagli aggiuntivi
        details_frame.pack(fill=tk.X, padx=15, pady=(0, 15))  # Posiziona il frame
        
        # Calcola la durata dagli orari di inizio e fine
        start = int(self.activity.start)  # Orario di inizio (es. 900)
        finish = int(self.activity.finish)  # Orario di fine (es. 1030)
        start_hours = start // 100  # Ore di inizio
        start_minutes = start % 100  # Minuti di inizio
        finish_hours = finish // 100  # Ore di fine
        finish_minutes = finish % 100  # Minuti di fine

        start_total_minutes = start_hours * 60 + start_minutes  # Minuti totali di inizio
        finish_total_minutes = finish_hours * 60 + finish_minutes  # Minuti totali di fine
        duration_minutes = finish_total_minutes - start_total_minutes  # Durata in minuti

        if duration_minutes > 0:  # Se la durata è positiva
            hours = duration_minutes // 60  # Ore intere
            minutes = duration_minutes % 60  # Minuti rimanenti
            if minutes > 0:
                duration_str = f"{hours}:{minutes:02d} h"  # Formatta come "h:mm h"
            else:
                duration_str = f"{hours} h"  # Solo ore
            duration_label = tk.Label(details_frame, text=f"⏱️ Duration: {duration_str}",  # Crea una label durata
                                     font=("Segoe UI", 11), bg="#ffffff")
            duration_label.pack(anchor='w', pady=2)  # Posiziona la label
        
        capacity_text = f"👥 Capacity: "  # Testo base capacità
        if self.activity.maxpart:  # Se c'è un limite di partecipanti
            capacity_text += f"{self.activity.maxpart} participants"  # Aggiungi il numero massimo
        else:
            capacity_text += "Unlimited"  # Altrimenti "Unlimited"
        
        capacity_label = tk.Label(details_frame, text=capacity_text,  # Crea una label capacità
                                 font=("Segoe UI", 11), bg="#ffffff")
        capacity_label.pack(anchor='w', pady=2)  # Posiziona la label

    def create_participation_section(self, parent):  # Metodo che crea la sezione partecipazione
        participation_frame = tk.LabelFrame(parent, text="Participation Status",  # Crea un frame con bordo e titolo
                                           font=("Segoe UI", 14, "bold"), bg="#ffffff")
        participation_frame.grid(row=0, column=1, sticky="nsew", padx=(10, 0), pady=10)  # Posiziona il frame
        
        # Qui verranno caricati dinamicamente i dati di partecipazione
        self.participation_info_frame = tk.Frame(participation_frame, bg="#ffffff")  # Crea un frame per info partecipazione
        self.participation_info_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)  # Posiziona il frame

    def create_rating_summary_section(self, parent):  # Metodo che crea la sezione riepilogo rating
        rating_frame = tk.LabelFrame(parent, text="Rating Summary",  # Crea un frame con bordo e titolo
                                    font=("Segoe UI", 14, "bold"), bg="#ffffff")
        rating_frame.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=0, pady=10)  # Posiziona il frame
        
        # Qui verrà caricato dinamicamente il riepilogo dei rating
        self.rating_summary_frame = tk.Frame(rating_frame, bg="#ffffff")  # Crea un frame per il riepilogo
        self.rating_summary_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)  # Posiziona il frame

    def create_action_buttons(self, parent):  # Metodo che crea i pulsanti azione
        button_frame = tk.Frame(parent, bg="#ffffff")  # Crea un frame per i pulsanti
        button_frame.grid(row=2, column=0, columnspan=2, pady=20)  # Posiziona il frame
        
        if self.student:  # Se è presente uno studente
            # Controlla se lo studente è già iscritto
            participants = self.activity.get_participant_list()  # Ottiene la lista dei partecipanti
            is_registered = any(p[0] == self.student.id for p in participants)  # Verifica se lo studente è già iscritto
            
            if not is_registered:  # Se non è iscritto
                register_btn = tk.Button(button_frame, text="Register for Activity",  # Crea il pulsante di iscrizione
                                        font=("Segoe UI", 12, "bold"), bg="#059669", fg="white",
                                        command=self.register_for_activity)
                register_btn.pack(side=tk.LEFT, padx=10)  # Posiziona il pulsante
            
            # Controlla se può lasciare feedback
            can_feedback, feedback_message = self.activity.can_student_leave_feedback(self.student.id)  # Verifica permesso
            
            if can_feedback:  # Se può lasciare feedback
                feedback_btn = tk.Button(button_frame, text="Leave Feedback",  # Crea il pulsante feedback
                                        font=("Segoe UI", 12, "bold"), bg="#3b82f6", fg="white",
                                        command=self.show_feedback_form)
                feedback_btn.pack(side=tk.LEFT, padx=10)  # Posiziona il pulsante
            else:  # Se non può lasciare feedback
                # Pulsante disabilitato con motivo
                disabled_btn = tk.Button(button_frame, text="Feedback Not Available",  # Crea pulsante disabilitato
                                        font=("Segoe UI", 12, "bold"), bg="#9ca3af", fg="white",
                                        state="disabled", command=lambda: messagebox.showinfo("Feedback", feedback_message))
                disabled_btn.pack(side=tk.LEFT, padx=10)  # Posiziona il pulsante
                
                # Tooltip per spiegazione
                def show_tooltip(event):  # Funzione per mostrare il motivo
                    messagebox.showinfo("Feedback Status", feedback_message)
                disabled_btn.bind("<Button-3>", show_tooltip)  # Tasto destro per info
        
        refresh_btn = tk.Button(button_frame, text="Refresh Data",  # Crea il pulsante di refresh
                               font=("Segoe UI", 12), bg="#6b7280", fg="white",
                               command=self.load_activity_details)
        refresh_btn.pack(side=tk.LEFT, padx=10)  # Posiziona il pulsante

    def create_ratings_tab(self):  # Metodo che crea il tab "Ratings & Statistics"
        ratings_frame = tk.Frame(self.notebook, bg='#ffffff')  # Crea un frame per il tab
        self.notebook.add(ratings_frame, text="Ratings & Statistics")  # Aggiunge il tab
        
        # Sarà popolato con grafici/statistiche
        self.ratings_content_frame = tk.Frame(ratings_frame, bg='#ffffff')  # Crea un frame per i contenuti
        self.ratings_content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)  # Posiziona il frame

    def create_feedback_tab(self):  # Metodo che crea il tab "Feedback"
        feedback_frame = tk.Frame(self.notebook, bg='#ffffff')  # Crea un frame per il tab
        self.notebook.add(feedback_frame, text="Feedback")  # Aggiunge il tab
        
        # Lista feedback
        feedback_list_frame = tk.LabelFrame(feedback_frame, text="Student Feedback",  # Crea un frame con bordo e titolo
                                           font=("Segoe UI", 14, "bold"), bg="#ffffff")
        feedback_list_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)  # Posiziona il frame
        
        # Lista scrollabile feedback
        feedback_canvas = tk.Canvas(feedback_list_frame, bg='#ffffff')  # Crea un canvas per lo scrolling
        feedback_scrollbar = ttk.Scrollbar(feedback_list_frame, orient="vertical", command=feedback_canvas.yview)  # Scrollbar
        
        self.feedback_content_frame = tk.Frame(feedback_canvas, bg='#ffffff')  # Frame interno per i feedback
        self.feedback_content_frame.bind(
            "<Configure>",  # Quando il frame cambia dimensione
            lambda e: feedback_canvas.configure(scrollregion=feedback_canvas.bbox("all"))  # Aggiorna la regione di scroll
        )
        
        feedback_canvas.create_window((0, 0), window=self.feedback_content_frame, anchor="nw")  # Inserisce il frame nel canvas
        feedback_canvas.configure(yscrollcommand=feedback_scrollbar.set)  # Collega la scrollbar
        
        feedback_canvas.pack(side="left", fill="both", expand=True, padx=10, pady=10)  # Posiziona il canvas
        feedback_scrollbar.pack(side="right", fill="y", pady=10)  # Posiziona la scrollbar

    def load_activity_details(self):  # Metodo che carica e aggiorna tutti i dati dell'attività
        details = self.activity.get_comprehensive_details()  # Ottieni tutti i dati dal modello Activity
        if not details:  # Se non ci sono dettagli, esci
            return
        
        self.load_participation_info(details['participation'])  # Aggiorna la sezione partecipazione
        self.load_rating_summary(details['ratings'])            # Aggiorna la sezione rating
        self.load_detailed_ratings(details['ratings'])          # Aggiorna la sezione dettagli rating
        self.load_feedback_list(details['recent_feedback'])     # Aggiorna la sezione feedback

    def load_participation_info(self, participation_data):  # Metodo che aggiorna la sezione partecipazione
        # Pulisci frame
        for widget in self.participation_info_frame.winfo_children():  # Cicla su tutti i widget figli
            widget.destroy()  # Rimuove ogni widget
        
        current = participation_data['current_participants']  # Numero attuale di partecipanti
        max_participants = self.activity.maxpart  # Numero massimo di partecipanti

        count_text = f"👥 Current: {current}"  # Testo base con numero attuale
        if max_participants is not None:  # Se c'è un limite massimo
            count_text += f" / {max_participants}"  # Aggiungi il massimo
            percentage = (current / max_participants) * 100 if max_participants else 0  # Calcola percentuale
            count_text += f" ({percentage:.1f}%)"  # Aggiungi percentuale
        
        count_label = tk.Label(self.participation_info_frame, text=count_text,  # Crea label con conteggio
                              font=("Segoe UI", 12, "bold"), bg="#ffffff")
        count_label.pack(anchor='w', pady=5)  # Posiziona la label
        
        # Stato (FULL, ALMOST FULL, AVAILABLE)
        if max_participants is not None and current >= max_participants:  # Se pieno
            status_text = "🔴 FULL"  # Testo stato pieno
            status_color = "#dc2626"  # Colore rosso
        elif max_participants is not None and current >= max_participants * 0.8:  # Se quasi pieno
            status_text = "🟡 ALMOST FULL"  # Testo quasi pieno
            status_color = "#f59e0b"  # Colore giallo
        else:  # Se disponibile
            status_text = "🟢 AVAILABLE"  # Testo disponibile
            status_color = "#059669"  # Colore verde
        
        status_label = tk.Label(self.participation_info_frame, text=status_text,  # Crea label stato
                               font=("Segoe UI", 11, "bold"), bg="#ffffff", fg=status_color)
        status_label.pack(anchor='w', pady=2)  # Posiziona la label
        
        # Lista partecipanti
        if participation_data['participant_list']:  # Se ci sono partecipanti
            participants_label = tk.Label(self.participation_info_frame, text="Registered Students:",  # Label titolo lista
                                         font=("Segoe UI", 10, "bold"), bg="#ffffff")
            participants_label.pack(anchor='w', pady=(10, 5))  # Posiziona la label
            
            if len(participation_data['participant_list']) > 5:  # Se più di 5 partecipanti
                list_frame = tk.Frame(self.participation_info_frame, bg="#ffffff")  # Crea frame per la lista
                list_frame.pack(fill=tk.BOTH, expand=True)
                
                participant_listbox = tk.Listbox(list_frame, height=5, font=("Segoe UI", 10))  # Crea listbox
                participant_scrollbar = ttk.Scrollbar(list_frame, orient="vertical")  # Scrollbar verticale
                
                for student_id, name, surname in participation_data['participant_list']:  # Cicla sui partecipanti
                    participant_listbox.insert(tk.END, f"{name} {surname}")  # Inserisce nome e cognome
                
                participant_listbox.config(yscrollcommand=participant_scrollbar.set)  # Collega scrollbar
                participant_scrollbar.config(command=participant_listbox.yview)
                
                participant_listbox.pack(side="left", fill="both", expand=True)  # Posiziona listbox
                participant_scrollbar.pack(side="right", fill="y")  # Posiziona scrollbar
            else:  # Se 5 o meno partecipanti
                for student_id, name, surname in participation_data['participant_list']:  # Cicla sui partecipanti
                    student_label = tk.Label(self.participation_info_frame, text=f"• {name} {surname}",  # Crea label nome
                                           font=("Segoe UI", 10), bg="#ffffff")
                    student_label.pack(anchor='w', padx=10)  # Posiziona la label

    def load_rating_summary(self, ratings_data):  # Metodo che aggiorna la sezione riepilogo rating
        # Pulisci frame
        for widget in self.rating_summary_frame.winfo_children():  # Cicla sui widget figli
            widget.destroy()  # Rimuove ogni widget
        
        if not ratings_data or ratings_data['total_ratings'] == 0:  # Se non ci sono rating
            no_ratings_label = tk.Label(self.rating_summary_frame, text="No ratings yet",  # Label "nessun rating"
                                       font=("Segoe UI", 12), bg="#ffffff", fg="#6b7280")
            no_ratings_label.pack(anchor='w')
            return  # Esce dal metodo
        
        # Crea riepilogo
        summary_frame = tk.Frame(self.rating_summary_frame, bg="#ffffff")  # Frame per il riepilogo
        summary_frame.pack(fill=tk.X)
        
        # Valutazione media con stelle
        avg_rating = ratings_data['average_rating']  # Media
        stars = "⭐" * int(round(avg_rating))  # Stelle
        avg_text = f"{stars} {avg_rating:.2f}/5.0"  # Testo media
        
        avg_label = tk.Label(summary_frame, text=avg_text,  # Label media
                            font=("Segoe UI", 14, "bold"), bg="#ffffff", fg="#f59e0b")
        avg_label.pack(side=tk.LEFT)
        
        # Mediana e conteggio
        median_text = f" | Median: {ratings_data['median_rating']:.2f} | {ratings_data['total_ratings']} reviews"  # Testo mediana
        median_label = tk.Label(summary_frame, text=median_text,  # Label mediana
                               font=("Segoe UI", 12), bg="#ffffff", fg="#6b7280")
        median_label.pack(side=tk.LEFT)

    def load_detailed_ratings(self, ratings_data):  # Metodo che aggiorna la sezione dettagli rating
        # Pulisci frame
        for widget in self.ratings_content_frame.winfo_children():  # Cicla sui widget figli
            widget.destroy()  # Rimuove ogni widget
        
        if not ratings_data or ratings_data['total_ratings'] == 0:  # Se non ci sono rating
            no_ratings_label = tk.Label(self.ratings_content_frame, text="No ratings available for detailed analysis",  # Label "nessun rating"
                                       font=("Segoe UI", 14), bg="#ffffff", fg="#6b7280")
            no_ratings_label.pack(expand=True)
            return  # Esce dal metodo
        
        # Crea distribuzione rating (grafico se matplotlib disponibile, altrimenti testo)
        if MATPLOTLIB_AVAILABLE:  # Se matplotlib disponibile
            self.create_rating_distribution_chart(ratings_data)  # Crea grafico
        else:
            self.create_rating_distribution_text(ratings_data)  # Altrimenti mostra testo

    def create_rating_distribution_chart(self, ratings_data):  # Metodo che crea il grafico distribuzione rating
        try:
            # Crea figura matplotlib
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
            fig.patch.set_facecolor('white')
            
            # Grafico a barre distribuzione rating
            ratings = [1, 2, 3, 4, 5]
            counts = [ratings_data['rating_distribution'][i] for i in ratings]
            colors = ['#dc2626', '#f97316', '#eab308', '#22c55e', '#059669']
            
            bars = ax1.bar(ratings, counts, color=colors, alpha=0.8)
            ax1.set_xlabel('Rating (Stars)')
            ax1.set_ylabel('Number of Reviews')
            ax1.set_title('Rating Distribution')
            ax1.set_xticks(ratings)
            ax1.set_ylim(0, max(counts) + 1 if max(counts) > 0 else 1)
            
            # Aggiungi etichette valori sulle barre
            for bar, count in zip(bars, counts):
                if count > 0:
                    ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1, 
                            str(count), ha='center', va='bottom', fontweight='bold')
        """""
            # Grafico a torta riepilogo rating
            non_zero_ratings = [(i, count) for i, count in enumerate(counts, 1) if count > 0]
            if non_zero_ratings:
                # Usa testo invece di simboli stella per evitare problemi di font
                pie_labels = [f"{rating} Stars" for rating, _ in non_zero_ratings]
                pie_values = [count for _, count in non_zero_ratings]
                pie_colors = [colors[rating-1] for rating, _ in non_zero_ratings]
                
                wedges, texts, autotexts = ax2.pie(pie_values, labels=pie_labels, colors=pie_colors, 
                                                  autopct='%1.1f%%', startangle=90)
                ax2.set_title('Rating Breakdown')
                
                # Rendi il testo percentuale in grassetto
                for autotext in autotexts:
                    autotext.set_color('white')
                    autotext.set_fontweight('bold')
            else:
                ax2.text(0.5, 0.5, 'No ratings yet', ha='center', va='center', transform=ax2.transAxes)
                ax2.set_title('Rating Breakdown')
            
            plt.tight_layout()
            
            # Incorpora in tkinter
            canvas = FigureCanvasTkAgg(fig, self.ratings_content_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            
            # Aggiungi statistiche sotto il grafico
            self.create_rating_statistics_text(ratings_data)
            """
            
        except Exception as e:
            print(f"Error creating chart: {e}")
            # Fallback su display testo
            self.create_rating_distribution_text(ratings_data)

    def create_rating_distribution_text(self, ratings_data):  # Metodo che mostra la distribuzione rating come testo
        """Visualizzazione distribuzione rating basata su testo"""
        stats_frame = tk.Frame(self.ratings_content_frame, bg="#ffffff")
        stats_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Titolo
        title_label = tk.Label(stats_frame, text="📊 Rating Distribution", 
                              font=("Segoe UI", 18, "bold"), bg="#ffffff", fg="#1e293b")
        title_label.pack(anchor='w', pady=(0, 20))
        
        # Statistiche generali
        overall_frame = tk.LabelFrame(stats_frame, text="Overall Statistics", 
                                     font=("Segoe UI", 14, "bold"), bg="#ffffff")
        overall_frame.pack(fill=tk.X, pady=(0, 20))
        
        overall_content = tk.Frame(overall_frame, bg="#ffffff")
        overall_content.pack(fill=tk.X, padx=15, pady=15)
        
        # Valutazione media con stelle
        avg_rating = ratings_data['average_rating']
        stars = "⭐" * int(round(avg_rating))
        avg_text = f"Average Rating: {stars} {avg_rating:.2f}/5.0"
        
        avg_label = tk.Label(overall_content, text=avg_text, 
                            font=("Segoe UI", 14, "bold"), bg="#ffffff", fg="#f59e0b")
        avg_label.pack(anchor='w', pady=2)
        
        median_label = tk.Label(overall_content, text=f"Median Rating: {ratings_data['median_rating']:.1f}", 
                               font=("Segoe UI", 12), bg="#ffffff", fg="#6b7280")
        median_label.pack(anchor='w', pady=2)
        
        total_label = tk.Label(overall_content, text=f"Total Reviews: {ratings_data['total_ratings']}", 
                              font=("Segoe UI", 12), bg="#ffffff", fg="#6b7280")
        total_label.pack(anchor='w', pady=2)
        
        # Dettagli distribuzione
        dist_frame = tk.LabelFrame(stats_frame, text="Rating Breakdown", 
                                  font=("Segoe UI", 14, "bold"), bg="#ffffff")
        dist_frame.pack(fill=tk.X, pady=(0, 20))
        
        dist_content = tk.Frame(dist_frame, bg="#ffffff")
        dist_content.pack(fill=tk.X, padx=15, pady=15)
        
        colors = ['#dc2626', '#f97316', '#eab308', '#22c55e', '#059669']
        max_count = max(ratings_data['rating_distribution'].values()) if ratings_data['rating_distribution'] else 1
        
        for rating in [5, 4, 3, 2, 1]:  # Mostra prima il rating da 5 stelle
            count = ratings_data['rating_distribution'][rating]
            percentage = (count / ratings_data['total_ratings']) * 100 if ratings_data['total_ratings'] > 0 else 0
            
            rating_frame = tk.Frame(dist_content, bg="#ffffff")
            rating_frame.pack(fill=tk.X, pady=3)
            
            # Valutazione in stelle
            star_label = tk.Label(rating_frame, text=f"{rating} ⭐", 
                                 font=("Segoe UI", 12, "bold"), bg="#ffffff", 
                                 fg=colors[rating-1], width=8)
            star_label.pack(side=tk.LEFT)
            
            # Simulazione barra di progresso
            bar_frame = tk.Frame(rating_frame, bg="#e5e7eb", height=20, width=200)
            bar_frame.pack(side=tk.LEFT, padx=(10, 10))
            bar_frame.pack_propagate(False)
            
            if count > 0:
                bar_width = int((count / max_count) * 200)
                bar = tk.Frame(bar_frame, bg=colors[rating-1], height=20, width=bar_width)
                bar.pack(side=tk.LEFT)
            
            # Conteggio e percentuale
            count_label = tk.Label(rating_frame, text=f"{count} ({percentage:.1f}%)", 
                                  font=("Segoe UI", 11), bg="#ffffff", fg="#374151")
            count_label.pack(side=tk.LEFT, padx=(10, 0))

    def create_rating_statistics_text(self, ratings_data):  # Metodo che mostra statistiche aggiuntive sotto ai grafici
        """Aggiungi statistiche aggiuntive sotto ai grafici"""
        stats_text_frame = tk.Frame(self.ratings_content_frame, bg="#f8fafc", relief='solid', bd=1)
        stats_text_frame.pack(fill=tk.X, padx=10, pady=10)
        
        stats_content = tk.Frame(stats_text_frame, bg="#f8fafc")
        stats_content.pack(fill=tk.X, padx=15, pady=10)
        
        # Calcola statistiche aggiuntive
        total = ratings_data['total_ratings']
        dist = ratings_data['rating_distribution']
        
        positive_ratings = dist[4] + dist[5]  # 4 e 5 stelle
        negative_ratings = dist[1] + dist[2]  # 1 e 2 stelle
        neutral_ratings = dist[3]  # 3 stelle
        
        positive_pct = (positive_ratings / total) * 100 if total > 0 else 0
        negative_pct = (negative_ratings / total) * 100 if total > 0 else 0
        neutral_pct = (neutral_ratings / total) * 100 if total > 0 else 0
        
        stats_title = tk.Label(stats_content, text="📈 Quick Statistics", 
                              font=("Segoe UI", 12, "bold"), bg="#f8fafc", fg="#1e293b")
        stats_title.pack(anchor='w', pady=(0, 5))
        
        positive_label = tk.Label(stats_content, text=f"👍 Positive (4-5 ⭐): {positive_ratings} ({positive_pct:.1f}%)", 
                                 font=("Segoe UI", 11), bg="#f8fafc", fg="#059669")
        positive_label.pack(anchor='w', pady=1)
        
        neutral_label = tk.Label(stats_content, text=f"😐 Neutral (3 ⭐): {neutral_ratings} ({neutral_pct:.1f}%)", 
                                font=("Segoe UI", 11), bg="#f8fafc", fg="#f59e0b")
        neutral_label.pack(anchor='w', pady=1)
        
        negative_label = tk.Label(stats_content, text=f"👎 Negative (1-2 ⭐): {negative_ratings} ({negative_pct:.1f}%)", 
                                 font=("Segoe UI", 11), bg="#f8fafc", fg="#dc2626")
        negative_label.pack(anchor='w', pady=1)

    def register_for_activity(self):  # Metodo per registrare lo studente all'attività
        # Implementazione per registrare lo studente all'attività
        from PythonExpenseApp.db_connection import DbConnection  # Importa la connessione al DB
        
        connection = DbConnection.connect()  # Ottiene la connessione
        if not connection:  # Se non riesce a connettersi
            messagebox.showerror("Error", "Could not connect to database")  # Mostra errore
            return
        
        try:
            cursor = connection.cursor()  # Ottiene il cursore
            cursor.execute("INSERT INTO student_activities (student_id, activity_id) VALUES (%s, %s)",
                          (self.student.id, self.activity_id))  # Inserisce la registrazione
            connection.commit()  # Conferma la transazione
            messagebox.showinfo("Success", "Successfully registered for activity!")  # Mostra successo
            self.load_activity_details()  # Aggiorna i dati
        except Exception as e:
            messagebox.showerror("Error", f"Could not register for activity: {e}")  # Mostra errore
        finally:
            connection.close()  # Chiude la connessione

    def show_feedback_form(self):  # Metodo che mostra il modulo per lasciare feedback
        # Valida permesso prima di mostrare il modulo
        can_feedback, message = self.activity.can_student_leave_feedback(self.student.id)  # Controlla permesso
        if not can_feedback:  # Se non può lasciare feedback
            messagebox.showerror("Cannot Leave Feedback", message)  # Mostra errore
            return
        
        # Crea finestra modulo feedback
        feedback_window = tk.Toplevel(self.root)  # Nuova finestra
        feedback_window.title("Leave Feedback")  # Titolo
        feedback_window.geometry("800x700")  # Dimensione
        feedback_window.configure(bg='#ffffff')  # Sfondo
        
        # Centra la finestra
        feedback_window.transient(self.root)  # Rende la finestra figlia
        feedback_window.grab_set()  # Blocca l'interazione con la finestra principale
        
        # Contenuto modulo
        form_frame = tk.Frame(feedback_window, bg='#ffffff')  # Frame principale
        form_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Titolo con conferma partecipazione
        title_label = tk.Label(form_frame, text=f"Feedback for {self.activity.name}", 
                              font=("Segoe UI", 16, "bold"), bg="#ffffff")
        title_label.pack(anchor='w', pady=(0, 10))
        
        # Conferma partecipazione
        participation_label = tk.Label(form_frame, text="✅ You participated in this activity", 
                                      font=("Segoe UI", 12), bg="#ffffff", fg="#059669")
        participation_label.pack(anchor='w', pady=(0, 20))
        
        # Selezione rating
        rating_label = tk.Label(form_frame, text="Rating:", 
                               font=("Segoe UI", 12, "bold"), bg="#ffffff")
        rating_label.pack(anchor='w', pady=(0, 5))
        
        rating_var = tk.IntVar(value=5)  # Variabile per il rating
        rating_frame = tk.Frame(form_frame, bg="#ffffff")  # Frame per le stelle
        rating_frame.pack(anchor='w', pady=(0, 15))
        
        for i in range(1, 6):  # Crea 5 radio button per le stelle
            star_text = "⭐" * i
            rating_radio = tk.Radiobutton(rating_frame, text=f"{star_text} ({i})", 
                                         variable=rating_var, value=i, 
                                         bg="#ffffff", font=("Segoe UI", 11))
            rating_radio.pack(anchor='w', pady=2)
        
        # Commento
        comment_label = tk.Label(form_frame, text="Comment (optional):", 
                                font=("Segoe UI", 12, "bold"), bg="#ffffff")
        comment_label.pack(anchor='w', pady=(0, 5))
        
        comment_text = tk.Text(form_frame, height=8, font=("Segoe UI", 11), 
                              relief='solid', bd=1)
        comment_text.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        # Linee guida
        guidelines_label = tk.Label(form_frame, 
                                   text="💡 Please share your honest experience to help other students!", 
                                   font=("Segoe UI", 10), bg="#ffffff", fg="#6b7280", 
                                   wraplength=400, justify=tk.LEFT)
        guidelines_label.pack(anchor='w', pady=(0, 15))
        
        # Pulsanti
        button_frame = tk.Frame(form_frame, bg="#ffffff")
        button_frame.pack(fill=tk.X, side=tk.BOTTOM, pady=(20, 0), anchor='se')  # Ancorato in basso a destra

        def submit_feedback():  # Funzione interna per inviare il feedback
            rating = rating_var.get()  # Ottiene il rating selezionato
            comment = comment_text.get('1.0', tk.END).strip()  # Ottiene il commento
            from PythonExpenseApp.feedback import Feedback  # Importa Feedback
            feedback = Feedback(self.student.id, self.activity_id, rating, comment if comment else None)  # Crea oggetto Feedback
            success, message = feedback.save_to_database()  # Salva nel database
            if success:
                messagebox.showinfo("Success", "Feedback submitted successfully!")  # Mostra successo
                feedback_window.destroy()  # Chiude la finestra feedback
                self.load_activity_details()  # Aggiorna i dati
            else:
                messagebox.showerror("Error", message)  # Mostra errore

        submit_btn = tk.Button(button_frame, text="Invia Feedback", 
                              font=("Segoe UI", 13, "bold"), bg="#059669", fg="white",
                              height=2, width=16, command=submit_feedback)
        submit_btn.pack(side=tk.RIGHT, padx=(10, 0), pady=5)

        cancel_btn = tk.Button(button_frame, text="Annulla", 
                              font=("Segoe UI", 12), bg="#6b7280", fg="white",
                              height=2, width=10, command=feedback_window.destroy)
        cancel_btn.pack(side=tk.RIGHT, padx=(0, 10), pady=5)
        
    def load_feedback_list(self, feedback_data):  # Metodo che mostra la lista dei feedback
        """Carica e mostra la lista dei feedback"""
        # Pulisci frame
        for widget in self.feedback_content_frame.winfo_children():  # Cicla sui widget figli
            widget.destroy()  # Rimuove ogni widget
        
        if not feedback_data:  # Se non ci sono feedback
            # Nessun feedback disponibile
            no_feedback_frame = tk.Frame(self.feedback_content_frame, bg='#ffffff')  # Frame placeholder
            no_feedback_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=50)
            
            no_feedback_label = tk.Label(no_feedback_frame, text="📝 No feedback available yet", 
                                        font=("Segoe UI", 16, "bold"), bg="#ffffff", fg="#6b7280")
            no_feedback_label.pack()
            
            help_label = tk.Label(no_feedback_frame, text="Students can leave feedback after participating in the activity", 
                                 font=("Segoe UI", 12), bg="#ffffff", fg="#9ca3af")
            help_label.pack(pady=(10, 0))
            return  # Esce dal metodo
        
        # Mostra ogni feedback
        for i, (rating, comment, created_at, name, surname) in enumerate(feedback_data):  # Cicla sui feedback
            feedback_card = tk.Frame(self.feedback_content_frame, bg='#f8fafc', relief='solid', bd=1)  # Card feedback
            feedback_card.pack(fill=tk.X, padx=10, pady=8)
            
            card_content = tk.Frame(feedback_card, bg='#f8fafc')
            card_content.pack(fill=tk.X, padx=15, pady=15)
            
            header_frame = tk.Frame(card_content, bg='#f8fafc')
            header_frame.pack(fill=tk.X, pady=(0, 10))
            
            stars = "⭐" * rating  # Stelle in base al voto
            rating_label = tk.Label(header_frame, text=stars, 
                                   font=("Segoe UI", 14, "bold"), bg="#f8fafc", fg="#f59e0b")
            rating_label.pack(side=tk.LEFT)
            
            student_label = tk.Label(header_frame, text=f" by {name} {surname}", 
                                    font=("Segoe UI", 12, "bold"), bg="#f8fafc", fg="#1e293b")
            student_label.pack(side=tk.LEFT)
            
            # Data
            from datetime import datetime
            if isinstance(created_at, str):  # Se la data è una stringa
                date_str = created_at
            else:
                date_str = created_at.strftime("%Y-%m-%d %H:%M") if created_at else "Unknown date"
            
            date_label = tk.Label(header_frame, text=date_str, 
                                 font=("Segoe UI", 10), bg="#f8fafc", fg="#6b7280")
            date_label.pack(side=tk.RIGHT)
            
            verified_label = tk.Label(header_frame, text="✅ Verified Participant", 
                                     font=("Segoe UI", 10, "bold"), bg="#f8fafc", fg="#059669")
            verified_label.pack(side=tk.RIGHT, padx=(0, 10))
            
            # Commento (se disponibile)
            if comment and comment.strip():  # Se c'è un commento
                comment_frame = tk.Frame(card_content, bg='#ffffff', relief='solid', bd=1)
                comment_frame.pack(fill=tk.X, pady=(0, 5))
                
                comment_text = tk.Text(comment_frame, height=3, font=("Segoe UI", 11), 
                                      bg="#ffffff", fg="#374151", relief='flat', bd=0, 
                                      wrap=tk.WORD, cursor="arrow")
                comment_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=8)
                comment_text.insert('1.0', comment)
                comment_text.config(state='disabled')
            else:  # Se non c'è commento
                # Segnaposto per assenza commento
                no_comment_label = tk.Label(card_content, text="(No written comment provided)", 
                                           font=("Segoe UI", 10, "italic"), bg="#f8fafc", fg="#9ca3af")
                no_comment_label.pack(anchor='w')
        
        # Riepilogo feedback alla fine
        if len(feedback_data) > 0:  # Se ci sono feedback
            summary_frame = tk.Frame(self.feedback_content_frame, bg='#e0f2fe', relief='solid', bd=1)  # Frame riepilogo
            summary_frame.pack(fill=tk.X, padx=10, pady=(20, 10))
            
            summary_content = tk.Frame(summary_frame, bg='#e0f2fe')
            summary_content.pack(fill=tk.X, padx=15, pady=10)
            
            total_participants = self.activity.get_current_participants()  # Numero totale partecipanti
            feedback_count = len(feedback_data)  # Numero feedback
            completion_rate = (feedback_count / total_participants * 100) if total_participants > 0 else 0  # Percentuale
            
            summary_text = f"📊 {feedback_count} feedback entries from {total_participants} participants ({completion_rate:.1f}% completion rate)"  # Testo riepilogo
            summary_label = tk.Label(summary_content, text=summary_text, 
                                    font=("Segoe UI", 12, "bold"), bg="#e0f2fe", fg="#0277bd")
            summary_label.pack()

# Funzione di utilità per normalizzare orari (es. 930 -> "09:30")
def normalize_time(t):
    t = int(t)  # Converte in intero
    hours = t // 100  # Ore
    minutes = t % 100  # Minuti
    hours += minutes // 60  # Gestisce overflow minuti
    minutes = minutes % 60  # Normalizza minuti
    return f"{hours:02d}:{minutes:02d}"  # Restituisce stringa formattata
