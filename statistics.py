from PythonExpenseApp.db_connection import DbConnection  # Importa la classe per la connessione al database
import mysql.connector  # Importa il modulo per la connessione a MySQL
import re  # Importa il modulo per le espressioni regolari

class Statistics:
    def __init__(self, activities, feedbacks):
        # activities: dict di Activity -> lista di Student
        # feedbacks: dict di Activity -> lista di stringhe (commenti)
        self.activities = activities  # Dizionario delle attività e relativi partecipanti
        self.feedbacks = feedbacks  # Dizionario delle attività e relativi feedback/commenti

    def get_total_participants(self):
        # Restituisce il numero totale di partecipanti a tutte le attività
        return sum(len(students) for students in self.activities.values())

    def get_most_popular_activity(self):
        # Restituisce l'attività con il maggior numero di partecipanti
        if not self.activities:
            return None
        return max(self.activities, key=lambda act: len(self.activities[act])) # Trova l'attività con il massimo numero di partecipanti

    def highlight_sentimental_words(self, activity, sentimental_words):
        # Prende la lista dei feedback per l'attività richiesta
        feedback_list = self.feedbacks.get(activity, [])
        highlighted = []  # Lista che conterrà i feedback con le parole evidenziate

        # Per ogni feedback nella lista...
        for feedback in feedback_list:
            highlighted_feedback = feedback  # Inizializza la variabile con il testo originale

            # Per ogni parola sentimentale da evidenziare...
            for word in sentimental_words:
                # Crea un pattern che trova la parola esatta (usando i bordi di parola \b) (word boundary)
                pattern = r"\b" + re.escape(word) + r"\b" # Crea un pattern per trovare la parola esatta
                highlighted_feedback = re.sub(pattern, f"*{word}*", highlighted_feedback) #evidenzia la parola

            # Aggiunge il feedback modificato alla lista dei risultati
            highlighted.append(highlighted_feedback)

        # Restituisce la lista dei feedback con le parole evidenziate
        return highlighted  # Restituisce la lista dei feedback con parole evidenziate

    def get_average_participants(self): # Calcola la media dei partecipanti per attività
        # Calcola la media dei partecipanti per attività
        if not self.activities: # Se non ci sono attività, la media è 0
            return 0.0
        return float(self.get_total_participants()) / len(self.activities) # Calcola la media dividendo il totale dei partecipanti per il numero di attività

    def fetch_statistics_from_database(self): # Recupera alcune statistiche direttamente dal database
        connection = DbConnection.connect() # Connessione al database
        if connection: # Se la connessione è riuscita
            try:# Esegue una query per ottenere il numero totale di partecipanti
                sql = "SELECT COUNT(*) AS total_participants FROM student_activities"  # Query per contare i partecipanti totali
                statement = connection.cursor()
                statement.execute(sql)
                result = statement.fetchone()
                if result:
                    print(f"Total Participants: {result[0]}")  # Stampa il totale dei partecipanti
            except mysql.connector.Error as e:
                print(f"Error fetching statistics from database: {e}")  # Gestione errori

    def __str__(self):
        # Rappresentazione testuale dell'oggetto Statistics
        return (f"Statistics [Total Participants={self.get_total_participants()}, "
                f"Most Popular Activity={self.get_most_popular_activity()}, "
                f"Average Participants={self.get_average_participants()}]")