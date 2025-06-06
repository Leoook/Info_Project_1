from PythonExpenseApp.db_connection import DbConnection  # Importa la classe per la connessione al database
import mysql.connector  # Importa il modulo per la connessione a MySQL
from datetime import datetime  # Importa la classe datetime per gestire le date

class Expense:
    def __init__(self, amount, description, date_=None, giver_id=None, receiver_id=None, activity_id=None):
        self.amount = amount  # Importo della spesa
        self.description = description  # Descrizione della spesa
        self.date = date_ if date_ else datetime.now().strftime("%Y-%m-%d")  # Data della spesa (oggi se non specificata)
        self.giver_id = giver_id  # ID di chi ha pagato
        self.receiver_id = receiver_id  # ID di chi deve rimborsare (opzionale)
        self.activity_id = activity_id  # ID dell'attività associata (opzionale)

    def get_amount(self):
        return self.amount  # Restituisce l'importo

    def set_amount(self, amount):
        self.amount = amount  # Imposta l'importo

    def get_description(self):
        return self.description  # Restituisce la descrizione

    def set_description(self, description):
        self.description = description  # Imposta la descrizione

    def get_date(self):
        return self.date  # Restituisce la data

    def set_date(self, date_):
        self.date = date_  # Imposta la data

    def save_to_database(self):
        connection = DbConnection.connect()  # Ottiene la connessione al database
        if connection:
            try:
                # Query SQL per inserire una nuova spesa (adatta i nomi delle colonne se necessario)
                sql = """INSERT INTO expenses (amount, description, date, id_giver, id_receiver, id_activity)
                         VALUES (%s, %s, %s, %s, %s, %s)"""
                statement = connection.cursor()  # Crea un cursore per eseguire la query
                statement.execute(sql, (self.amount, self.description, self.date,
                                        self.giver_id, self.receiver_id, self.activity_id))  # Esegue la query con i dati della spesa
                connection.commit()  # Salva le modifiche nel database
                print("Expense saved to database.")  # Messaggio di conferma
            except mysql.connector.Error as e:
                print(f"Error saving expense to database: {e}")  # Messaggio di errore in caso di problemi

    def __str__(self):
        # Rappresentazione testuale dell'oggetto Expense
        return f"Expense(amount={self.amount}, description={self.description}, date={self.date})"