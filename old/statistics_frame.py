import tkinter as tk

class StatisticsFrame(tk.Frame):
    def __init__(self, master, switch_callback, back_frame):
        super().__init__(master)
        self.switch_callback = switch_callback
        self.back_frame = back_frame

        # Freccia per tornare indietro
        back_btn = tk.Button(
            self,
            text="←",
            font=("Arial", 16, "bold"),
            command=lambda: self.switch_callback(self.back_frame, self.__class__),  # Passa anche il back_frame richiesto
            width=3
        )
        back_btn.grid(row=0, column=0, padx=6, pady=6, sticky="w")

        # Titolo
        title_label = tk.Label(self, text="Statistics", font=("Arial", 18))
        title_label.grid(row=1, column=0, columnspan=2, pady=20)

        # Qui puoi aggiungere la visualizzazione delle statistiche reali
        info_label = tk.Label(self, text="Qui verranno mostrate le statistiche sulle attività.")
        info_label.grid(row=2, column=0, columnspan=2, pady=10)