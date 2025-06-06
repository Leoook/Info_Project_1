import tkinter as tk  # Importa il modulo tkinter per creare interfacce grafiche
from tkinter import messagebox  # Importa messagebox per mostrare popup informativi o di errore

class HomepageFrame(tk.Frame):  # Definisce la schermata principale, eredita da tk.Frame
    def __init__(self, master, switch_callback):  # Costruttore: riceve il frame genitore e la funzione per cambiare schermata
        super().__init__(master)  # Inizializza il frame base di tkinter
        self.switch_callback = switch_callback  # Salva la callback per il cambio di schermata

        label = tk.Label(self, text="Homepage", font=("Arial", 20))  # Crea un'etichetta con il titolo "Homepage"
        label.pack(pady=20)  # Posiziona l'etichetta al centro, con margine verticale di 20

        teacher_btn = tk.Button(
            self, text="Menù Docente", width=20, height=2,
            command=self.show_teacher_menu)  # Bottone per accedere al menù docente (ancora in costruzione)
        teacher_btn.pack(pady=10)  # Posiziona il bottone con margine verticale

        student_btn = tk.Button(
            self, text="Menù Studente", width=20, height=2,
            command=lambda: self.switch_callback(StudentMenuFrame))  # Bottone per accedere al menù studente
        student_btn.pack(pady=10)  # Posiziona il bottone con margine verticale

    def show_teacher_menu(self):  # Metodo chiamato quando si clicca su "Menù Docente"
        messagebox.showinfo("Menù Docente", "Funzionalità in fase di costruzione.")  # Mostra popup informativo

# Frame per il menù studente
class StudentMenuFrame(tk.Frame):  # Definisce la schermata del menù studente
    def __init__(self, master, switch_callback):  # Costruttore: riceve il frame genitore e la funzione per cambiare schermata
        super().__init__(master)  # Inizializza il frame base di tkinter
        self.switch_callback = switch_callback  # Salva la callback per il cambio di schermata

        # Freccia per tornare alla homepage
        back_btn = tk.Button(
            self,
            text="←",
            font=("Arial", 16, "bold"),
            command=lambda: self.switch_callback(HomepageFrame),  # Torna alla homepage quando cliccata
            width=3
        )
        back_btn.pack(anchor="nw", padx=6, pady=6)  # Posiziona la freccia in alto a sinistra

        label = tk.Label(self, text="Menù Studente", font=("Arial", 18))  # Etichetta per il titolo del menù studente
        label.pack(pady=20)  # Posiziona l'etichetta con margine verticale

        expense_btn = tk.Button(
            self, text="Expense", width=20, height=2,
            command=lambda: self.switch_callback(ExpenseFrame, StudentMenuFrame)  # Passa a ExpenseFrame, con ritorno a StudentMenuFrame
        )
        expense_btn.pack(pady=10)  # Posiziona il bottone con margine verticale

        activity_btn = tk.Button(
            self, text="Activity", width=20, height=2,
            command=lambda: self.switch_callback(ActivityFrame, StudentMenuFrame)  # Passa a ActivityFrame, con ritorno a StudentMenuFrame
        )
        activity_btn.pack(pady=10)  # Posiziona il bottone con margine verticale

# Importazioni ritardate per evitare errori circolari tra moduli
from PythonExpenseApp.gui.expense_frame import ExpenseFrame
from PythonExpenseApp.gui.activity_frame import ActivityFrame