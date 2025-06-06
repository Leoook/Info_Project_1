import sqlite3  # Importa il modulo per la connessione a SQLite

class Feedback:
    _id_counter = 1  # Variabile di classe per assegnare un id incrementale ai feedback creati in memoria

    def __init__(self, student, activity, rating, comment):
        self.id = Feedback._id_counter  # Assegna un id unico al feedback
        Feedback._id_counter += 1  # Incrementa il contatore per il prossimo feedback
        self.student = student  # Oggetto Student associato al feedback
        self.activity = activity  # Oggetto Activity associato al feedback
        self.rating = rating  # Valutazione (es: da 1 a 5)
        self.comment = comment  # Commento opzionale

    def get_id(self):
        return self.id  # Restituisce l'id del feedback

    def get_student(self):
        return self.student  # Restituisce lo studente che ha lasciato il feedback

    def get_activity(self):
        return self.activity  # Restituisce l'attività a cui si riferisce il feedback

    def get_rating(self):
        return self.rating  # Restituisce la valutazione

    def get_comment(self):
        return self.comment  # Restituisce il commento

def save_to_database(student, activity, rating, comment):
    conn = sqlite3.connect('your_database.db')  # Connessione al database SQLite (aggiorna il percorso se necessario)
    sql = "INSERT INTO feedback (student_id, activity_id, rating, comment) VALUES (?, ?, ?, ?)"  # Query SQL per inserire un feedback
    
    try:
        with conn:  # Gestisce automaticamente il commit e la chiusura della connessione
            stmt = conn.cursor()  # Crea un cursore
            stmt.execute(sql, (student.id, activity.id, rating, comment))  # Esegue la query con i dati forniti
            print("Feedback salvato nel database.")  # Messaggio di conferma
    except sqlite3.Error as e:
        print("Errore durante il salvataggio del feedback:", e)  # Messaggio di errore in caso di problemi

    # Nota: la connessione viene chiusa automaticamente dal context manager "with"

    def __str__(self):
        # Rappresentazione testuale dell'oggetto Feedback
        return f"Feedback(id={self.id}, rating={self.rating}, comment='{self.comment}')"

