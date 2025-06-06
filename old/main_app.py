import tkinter as tk # Importa la libreria Tkinter per la GUI
# Importa i frame personalizzati dell'app
from PythonExpenseApp.gui.homepage_frame import HomepageFrame  # Schermata principale
from PythonExpenseApp.gui.expense_frame import ExpenseFrame    # Schermata gestione spese
from PythonExpenseApp.gui.activity_frame import ActivityFrame  # Schermata attività 

class MainApp(tk.Tk):  # La classe principale dell'applicazione, eredita da tk.Tk (finestra principale)
    def __init__(self):
        super().__init__()  # Inizializza la finestra Tk
        self.title("Student Management App")  # Imposta il titolo della finestra
        self.geometry("600x400")  # Imposta la dimensione iniziale della finestra
        self.current_frame = None  # Variabile per tenere traccia del frame attivo
        self.switch_frame(HomepageFrame)  # Mostra la schermata iniziale (Homepage)

    def switch_frame(self, frame_class, back_frame=None):  # Metodo per cambiare schermata (frame)
        """Rimuove il frame attuale e mostra quello nuovo"""
        if self.current_frame is not None:  # Se c'è già un frame visibile
            self.current_frame.destroy()  # Lo rimuove dalla finestra
        if back_frame:
            self.current_frame = frame_class(self, self.switch_frame, back_frame)
        else:
            self.current_frame = frame_class(self, self.switch_frame)
        self.current_frame.pack(fill="both", expand=True)  # Mostra il nuovo frame, espandendolo in tutta la finestra