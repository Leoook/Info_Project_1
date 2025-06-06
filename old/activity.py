from PythonExpenseApp.db_connection import DbConnection  # Importa la classe per la connessione al database
from PythonExpenseApp.student import Student  # Importa la classe Student
from PythonExpenseApp.feedback import Feedback  # Importa la classe Feedback
import mysql.connector  # Per la connessione a MySQL
import sqlite3  # Per la connessione a SQLite

class Activity:
    def __init__(self, id_, name, maxpart, location, duration, start, finish, participants, feedback):
        self.id = id_  # ID dell'attività
        self.name = name  # Nome dell'attività
        self.maxpart = maxpart  # Numero massimo di partecipanti
        self.location = location  # Luogo dell'attività
        self.duration = duration  # Durata dell'attività
        self.start = start  # Orario di inizio
        self.finish = finish  # Orario di fine
        self.participants = participants  # Lista dei partecipanti (Student)
        self.activity_feedback = feedback  # Lista dei feedback (Feedback)

    def get_id(self):
        return self.id  # Restituisce l'ID dell'attività

    def set_id(self, id_):
        self.id = id_  # Imposta l'ID dell'attività

    def is_full(self):
        return len(self.participants) >= self.maxpart  # Ritorna True se l'attività è piena

    def save_to_database(self):  # Salva l'attività nel database MySQL
        connection = DbConnection.connect()  # Ottiene la connessione al database
        if connection:  # Se la connessione è riuscita
            try:
                sql = """INSERT INTO activities 
                         (name, max_participants, location, duration, start_time, finish_time)
                         VALUES (%s, %s, %s, %s, %s, %s)"""  # Query SQL per inserire una nuova attività
                statement = connection.cursor()  # Crea un cursore per eseguire la query
                statement.execute(sql, (self.name, self.maxpart, self.location, 
                                        self.duration, self.start, self.finish))  # Esegue la query con i dati dell'attività
                connection.commit()  # Salva le modifiche nel database
                print("Activity saved to database.")  # Messaggio di conferma
            except mysql.connector.Error as e:  # Gestione errori MySQL
                print(f"Error saving activity to database: {e}")

    def __str__(self):  # Rappresentazione testuale dell'oggetto Activity
        return (f"Activity [id={self.id}, name={self.name}, maxpart={self.maxpart}, " 
                f"location={self.location}, duration={self.duration}, start={self.start}, "
                f"finish={self.finish}, participants={self.participants}, "
                f"feedback={self.activity_feedback}]") 

    def load_feedback_from_database(self):  # Carica i feedback dal database SQLite
        feedback_list = []  # Lista temporanea per i feedback
        sql = "SELECT * FROM feedback WHERE activity_id = ?"  # Query per selezionare i feedback di questa attività

        try:
            conn = sqlite3.connect('your_database.db')  # Connessione al database SQLite (modifica il percorso se necessario)
            cursor = conn.cursor()  # Crea un cursore
            cursor.execute(sql, (self.id,))  # Esegue la query per questa attività

            rows = cursor.fetchall()  # Ottiene tutte le righe risultanti

            for row in rows:  # Per ogni feedback trovato
                feedback_id = row[0]  # id feedback
                student_id = row[1]   # id studente
                rating = row[2]       # valutazione
                comment = row[3]      # commento

                # Crea oggetti Student e Feedback (modifica secondo la tua implementazione)
                student = Student(student_id)  # Qui dovresti recuperare lo studente dal DB o da una lista
                feedback = Feedback(student, self, rating, comment)  # Crea il feedback
                feedback_list.append(feedback)  # Aggiungi alla lista

            self.activity_feedback = feedback_list  # Salva la lista dei feedback nell'oggetto

        except Exception as e:  # Gestione errori generici
            print("Errore durante il caricamento dei feedback:", e)
        finally:
            if conn:
                conn.close()  # Chiude la connessione al database