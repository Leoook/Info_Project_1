from PythonExpenseApp.db_connection import DbConnection  # Importa la classe per la connessione al database
import mysql.connector  # Importa il modulo per la connessione a MySQL

class DailyProgram:
    def __init__(self, day):
        self.day = day  # Giorno del programma (può essere un oggetto datetime.date o simile)
        self.activities = {}  # Dizionario: chiave = oggetto Activity, valore = lista di Student

    def add_activity(self, activity, participants):
        self.activities[activity] = participants  # Aggiunge un'attività e la lista dei partecipanti al dizionario

    def get_activities(self):
        return self.activities  # Restituisce tutte le attività del giorno

    def get_participants(self, activity):
        return self.activities.get(activity, [])  # Restituisce la lista dei partecipanti per una data attività

    def remove_activity(self, activity):
        if activity in self.activities:
            del self.activities[activity]  # Rimuove un'attività dal programma del giorno

    def save_to_database(self):
        connection = DbConnection.connect()  # Ottiene la connessione al database
        if connection:
            try:
                sql = "INSERT INTO daily_program (day, activity_id) VALUES (%s, %s)"  # Query per salvare il programma giornaliero
                statement = connection.cursor()  # Crea un cursore per eseguire la query
                for activity, _ in self.activities.items():  # Per ogni attività nel programma
                    statement.execute(sql, (self.day, activity.get_id()))  # Salva giorno e id attività nel database
                connection.commit()  # Conferma le modifiche
                print("Daily program saved to database.")  # Messaggio di conferma
            except mysql.connector.Error as e:  # Gestione errori MySQL
                print(f"Error saving daily program to database: {e}")

    def __str__(self):
        return f"DailyProgram [day={self.day}, activities={self.activities}]"  # Rappresentazione testuale dell'oggetto