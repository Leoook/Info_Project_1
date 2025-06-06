import mysql.connector  # Importa il modulo per la connessione a MySQL

class DbConnection:
    _connection = None  # Variabile di classe per mantenere la connessione aperta (singleton)

    @staticmethod
    def connect():
        # Metodo statico per ottenere la connessione al database
        if DbConnection._connection is None:  # Se non esiste già una connessione
            try:
                DbConnection._connection = mysql.connector.connect(
                    host="localhost",        # Indirizzo del server MySQL
                    user="root",             # Nome utente del database
                    password="ccgZ86+d$L:i*Ez",  # Password del database
                    database="project"       # Nome del database da usare
                )
                print("Database connection established.")  # Messaggio di conferma
            except mysql.connector.Error as e:
                print(f"Failed to connect to database: {e}")  # Messaggio di errore in caso di problemi
                DbConnection._connection = None  # Imposta la connessione a None in caso di errore
        return DbConnection._connection  # Restituisce la connessione (nuova o già esistente)

    @staticmethod
    def disconnect():
        # Metodo statico per chiudere la connessione al database
        if DbConnection._connection is not None:  # Se esiste una connessione aperta
            try:
                DbConnection._connection.close()  # Chiude la connessione
                DbConnection._connection = None   # Reset della variabile di classe
                print("Database connection closed.")  # Messaggio di conferma
            except mysql.connector.Error as e:
                print(f"Failed to close the database connection: {e}")  # Messaggio di errore in caso di problemi