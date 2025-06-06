from PythonExpenseApp.db_connection import DbConnection  # Importa la classe per la connessione al database
import mysql.connector  # Importa il modulo per la connessione a MySQL

class Student:
    def __init__(self, name, surname, age, special_needs):
        self.name = name  # Nome dello studente
        self.surname = surname  # Cognome dello studente
        self.age = age  # Età dello studente
        self.special_needs = special_needs  # Esigenze particolari (es. alimentari)
        self.selected_activities = []  # Lista delle attività selezionate dallo studente
        self.total_expenses = 0.0  # Totale delle spese sostenute dallo studente
        self.fee_share = 0.0  # Quota di spesa da dividere
        self.balance = 0.0  # Saldo finale (positivo o negativo)

    def add_activity(self, activity):
        try:
            if activity.is_full():  # Controlla se l'attività è già piena
                print(f"Activity '{activity.name}' is already full.")
                return
        except Exception as e:
            print(f"Error checking activity capacity: {e}")
        self.selected_activities.append(activity)  # Aggiunge l'attività alla lista

    def get_selected_activities(self):
        return self.selected_activities  # Restituisce la lista delle attività selezionate

    def add_expense(self, amount):
        self.total_expenses += amount  # Aggiunge una spesa al totale

    def get_total_expenses(self):
        return self.total_expenses  # Restituisce il totale delle spese

    def set_fee_share(self, fee_share):
        self.fee_share = fee_share  # Imposta la quota di spesa

    def get_fee_share(self):
        return self.fee_share  # Restituisce la quota di spesa

    def set_balance(self, balance):
        self.balance = balance  # Imposta il saldo

    def get_balance(self):
        return self.balance  # Restituisce il saldo

    def __init__(self, id):
        self.id = id  # Costruttore alternativo che imposta solo l'id (usato per caricamento da DB)

    def save_to_database(self): # Salva lo studente nel database MySQL
        connection = DbConnection.connect()  # Ottiene la connessione al database
        if connection: 
            try:
                sql = """INSERT INTO students
                         (name, surname, age, special_needs, total_expenses, fee_share, balance)
                         VALUES (%s, %s, %s, %s, %s, %s, %s)"""  # Query per inserire uno studente
                statement = connection.cursor() # Crea un cursore per eseguire la query
                statement.execute(sql, (self.name, self.surname, self.age, self.special_needs,
                                        self.total_expenses, self.fee_share, self.balance))
                connection.commit() # Salva le modifiche nel database
                print("Student saved to database.")  # Messaggio di conferma
            except mysql.connector.Error as e:
                print(f"Error saving student to database: {e}")  # Gestione errori

    def update_in_database(self): # Aggiorna i dati dello studente nel database MySQL
        connection = DbConnection.connect()  # Ottiene la connessione al database
        if connection:
            try:
                sql = """UPDATE students
                         SET total_expenses = %s, fee_share = %s, balance = %s
                         WHERE name = %s AND surname = %s"""  # Query per aggiornare i dati dello studente
                statement = connection.cursor()
                statement.execute(sql, (self.total_expenses, self.fee_share, self.balance,
                                        self.name, self.surname))
                connection.commit()
                print("Student updated in database.")  # Messaggio di conferma
            except mysql.connector.Error as e:
                print(f"Error updating student in database: {e}")  # Gestione errori

    @staticmethod # Metodo statico per ottenere tutti gli studenti dal database
    def get_all_students(): #   Recupera tutti gli studenti dal database MySQL
        students = []  # Lista di studenti da restituire
        connection = DbConnection.connect()  # Ottiene la connessione al database
        if connection: # Se la connessione è riuscita
            try:
                sql = """SELECT name, surname, age, special_needs, total_expenses,
                                fee_share, balance FROM students"""  # Query per recuperare tutti gli studenti
                statement = connection.cursor() # Crea un cursore per eseguire la query
                statement.execute(sql) # Esegue la query
                for (name, surname, age, special_needs, total_expenses, fee_share, balance) in statement: # Itera sui risultati
                    stu = Student(name, surname, age, special_needs)  # Crea un oggetto Student
                    stu.add_expense(total_expenses)  # Imposta il totale spese
                    stu.set_fee_share(fee_share)  # Imposta la quota spese
                    stu.set_balance(balance)  # Imposta il saldo
                    students.append(stu)  # Aggiunge lo studente alla lista
            except mysql.connector.Error as e: # Gestione errori MySQL
                print(f"Error retrieving students from database: {e}")  # Gestione errori
        return students  # Restituisce la lista di studenti

    def __str__(self):
        # Rappresentazione testuale dell'oggetto Student
        return (f"Student [name={self.name}, surname={self.surname}, age={self.age}, "
                f"specialNeeds={self.special_needs}, selectedActivities={self.selected_activities}, "
                f"totalExpenses={self.total_expenses}, feeShare={self.fee_share}, "
                f"balance={self.balance}]")