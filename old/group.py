from PythonExpenseApp.db_connection import DbConnection  # Importa la classe per la connessione al database
import mysql.connector  # Importa il modulo per la connessione a MySQL

class Group:
    def __init__(self, common_activity, dietary_needs):
        self.members = []  # Lista dei membri del gruppo (Student)
        self.common_activity = common_activity  # Attività comune del gruppo
        self.dietary_needs = dietary_needs  # Esigenze alimentari comuni del gruppo

    def add_member(self, student):
        self.members.append(student)  # Aggiunge uno studente al gruppo

    def remove_member(self, student):
        if student in self.members:
            self.members.remove(student)  # Rimuove uno studente dal gruppo se presente

    def get_members(self):
        return self.members  # Restituisce la lista dei membri

    def get_common_activity(self):
        return self.common_activity  # Restituisce l'attività comune

    def set_common_activity(self, common_activity):
        self.common_activity = common_activity  # Imposta l'attività comune

    def get_dietary_needs(self):
        return self.dietary_needs  # Restituisce le esigenze alimentari

    def set_dietary_needs(self, dietary_needs):
        self.dietary_needs = dietary_needs  # Imposta le esigenze alimentari

    def save_to_database(self):
        connection = DbConnection.connect()  # Ottiene la connessione al database
        if connection:
            try:
                sql = "INSERT INTO groups (common_activity, dietary_needs) VALUES (%s, %s)"  # Query per salvare il gruppo
                statement = connection.cursor()  # Crea un cursore per eseguire la query
                statement.execute(sql, (self.common_activity, self.dietary_needs))  # Esegue la query con i dati del gruppo
                connection.commit()  # Salva le modifiche nel database
                print("Group saved to database.")  # Messaggio di conferma
            except mysql.connector.Error as e:
                print(f"Error saving group to database: {e}")  # Messaggio di errore in caso di problemi

    def __str__(self):
        # Rappresentazione testuale dell'oggetto Group
        return (f"Group [commonActivity={self.common_activity}, "
                f"dietaryNeeds={self.dietary_needs}, members={self.members}]")