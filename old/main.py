from PythonExpenseApp.gui.main_app import MainApp  # Importa la classe principale dell'applicazione GUI

if __name__ == "__main__":  # Controlla se il file è eseguito come programma principale
    app = MainApp()         # Crea un'istanza della finestra principale dell'applicazione
    app.mainloop()          # Avvia il ciclo principale di Tkinter (mostra la GUI e gestisce gli eventi)