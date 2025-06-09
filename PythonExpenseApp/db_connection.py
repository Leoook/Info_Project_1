import mysql.connector # Importing mysql.connector for MySQL database connection
from mysql.connector import pooling # Importing pooling for connection pooling - a way to manage multiple connections efficiently
import threading # Importing threading for thread-safe operations - necessary for multi-threaded applications 
import logging # Importing logging for logging database operations - a way to track events that happen during execution

class DbConnection:
    # Class-level variable for the MySQL connection pool (shared by all instances)
    _connection_pool = None
    # Lock for thread-safe pool initialization
    _lock = threading.Lock()
    
    # Database configuration dictionary for connection parameters
    _config = {
        'host': 'localhost',                # Database server host
        'user': 'root',                     # Database user
        'password': 'ccgZ86+d$L:i*Ez',                     # Database password
        'database': 'trip_manager',              # Database name
        'charset': 'utf8mb4',               # Character set for Unicode support
        'collation': 'utf8mb4_unicode_ci',  # Collation for Unicode
        'autocommit': False,                # Disable autocommit for transactions
        'raise_on_warnings': True           # Raise exceptions on warnings
    }
    
    # Configuration for the MySQL connection pool
    _pool_config = {
        'pool_name': 'trip_manager_pool',   # Name of the connection pool
        'pool_size': 10,                    # Maximum number of connections in the pool
        'pool_reset_session': True          # Reset session state when connection is returned to pool
    }

    @classmethod
    def initialize_pool(cls): # Initialize the MySQL connection pool.
        """
        Initialize the MySQL connection pool if it hasn't been created yet.
        Uses thread locking to ensure only one pool is created in multi-threaded environments.
        Combines the base config and pool config for pool creation.
        Raises an exception if pool creation fails.
        """
        if cls._connection_pool is None:
            with cls._lock:
                if cls._connection_pool is None:
                    try:
                        # Combine config with pool config for pool creation
                        pool_config = {**cls._config, **cls._pool_config}
                        cls._connection_pool = pooling.MySQLConnectionPool(**pool_config)
                        logging.info("Database connection pool initialized successfully.")
                        print("Database connection pool initialized.")
                    except mysql.connector.Error as e:
                        logging.error(f"Failed to initialize connection pool: {e}")
                        print(f"Failed to initialize connection pool: {e}")
                        raise

    @classmethod
    def connect(cls):
        """
        Get a connection from the connection pool.
        Initializes the pool if it does not exist.
        Returns a MySQLConnection object if successful, or None if connection fails.
        """
        try:
            # Initialize pool if not already done
            if cls._connection_pool is None:
                cls.initialize_pool()
            
            # Get connection from pool
            connection = cls._connection_pool.get_connection()
            
            # Test the connection
            if connection.is_connected():
                return connection
            else:
                logging.warning("Retrieved invalid connection from pool")
                return None
                
        except mysql.connector.Error as e: # Handle MySQL connection errors
            logging.error(f"Failed to get connection from pool: {e}")
            print(f"Failed to connect to database: {e}")
            return None
        except Exception as e:
            logging.error(f"Unexpected error getting database connection: {e}")
            print(f"Unexpected database error: {e}")
            return None

    @classmethod # Execute a SQL query with automatic connection and cursor management.
    def execute_query(cls, query, params=None, fetch_one=False, fetch_all=False): 
        """
        Execute a SQL query with automatic connection and cursor management.
        Handles SELECT, INSERT, UPDATE, and DELETE queries.
        Supports fetching one or all results for SELECT queries.
        Rolls back on error and returns a tuple (success, result or error message).

        Args:
            query (str): SQL query to execute.
            params (tuple): Parameters for the query (default: None).
            fetch_one (bool): Whether to fetch one result (default: False).
            fetch_all (bool): Whether to fetch all results (default: False).

        Returns:
            tuple: (success, result/error_message)
                - success (bool): True if query executed successfully, False otherwise.
                - result: Query result (fetched data, lastrowid, rowcount) or error message.
        """
        connection = None
        cursor = None
        
        try:
            connection = cls.connect()
            if not connection:
                return False, "Could not establish database connection"
            
            cursor = connection.cursor()
            cursor.execute(query, params or ())  # Fixed missing closing parenthesis
            
            # Handle different query types
            if fetch_one:
                result = cursor.fetchone()
                return True, result
            elif fetch_all:
                result = cursor.fetchall()
                return True, result
            else:
                # For INSERT, UPDATE, DELETE queries
                connection.commit()
                return True, cursor.lastrowid if cursor.lastrowid else cursor.rowcount
                
        except mysql.connector.Error as e:
            if connection:
                connection.rollback()
            logging.error(f"Database query error: {e}")
            return False, str(e)
        except Exception as e:
            if connection:
                connection.rollback()
            logging.error(f"Unexpected error executing query: {e}")
            return False, str(e)
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()  # Returns connection to pool

    @classmethod # Execute multiple SQL queries in a single transaction.
    def execute_transaction(cls, queries_with_params):
        """
        Execute multiple SQL queries in a single transaction.
        Rolls back all queries if any query fails.
        Returns a tuple (success, results or error message).

        Args:
            queries_with_params (list): List of (query, params) tuples.

        Returns:
            tuple: (success, result/error_message)
                - success (bool): True if all queries executed successfully, False otherwise.
                - result: List of lastrowid/rowcount for each query, or error message.
        """
        connection = None
        cursor = None
        
        try:
            connection = cls.connect()
            if not connection:
                return False, "Could not establish database connection"
            
            cursor = connection.cursor()
            
            # Execute all queries in transaction
            results = []
            for query, params in queries_with_params:
                cursor.execute(query, params or ())  # Fixed missing closing parenthesis
                results.append(cursor.lastrowid if cursor.lastrowid else cursor.rowcount)
            
            connection.commit()
            return True, results
            
        except mysql.connector.Error as e:
            if connection:
                connection.rollback()
            logging.error(f"Transaction error: {e}")
            return False, str(e)
        except Exception as e:
            if connection:
                connection.rollback()
            logging.error(f"Unexpected transaction error: {e}")
            return False, str(e)
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

    @classmethod # Test database connectivity by executing a simple SELECT statement.
    def test_connection(cls):
        """
        Test database connectivity by executing a simple SELECT statement.
        Returns True and a success message if the connection works, otherwise False and an error message.

        Returns:
            tuple: (success, message)
        """
        try:
            connection = cls.connect()
            if connection and connection.is_connected():
                cursor = connection.cursor()
                cursor.execute("SELECT 1")
                result = cursor.fetchone()
                cursor.close()
                connection.close()
                return True, "Database connection successful"
            else:
                return False, "Could not establish connection"
        except Exception as e:
            return False, f"Connection test failed: {e}"

    @classmethod # Get information about the connected database server.
    def get_database_info(cls):
        """
        Get information about the connected database server.
        Returns a dictionary with server version, connection ID, database name, user, host, and port.

        Returns:
            tuple: (success, info or error message)
        """
        try:
            connection = cls.connect()
            if connection:
                info = {
                    'server_version': connection.get_server_info(), # MySQL server version string
                    'connection_id': connection.connection_id,      # Unique connection ID
                    'database': connection.database,                # Database name
                    'user': connection.user,                        # Connected user
                    'host': connection.server_host,                  # Server host
                    'port': connection.server_port                   # Server port
                }
                connection.close()
                return True, info
            else:
                return False, "Could not connect to database"
        except Exception as e:
            return False, f"Error getting database info: {e}"

    @classmethod # Create necessary tables if they don't exist.
    def create_tables_if_not_exist(cls):
        """Create necessary tables if they don't exist"""
        tables = {            'students': """
                CREATE TABLE IF NOT EXISTS students (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    surname VARCHAR(100) NOT NULL,
                    email VARCHAR(100) UNIQUE NOT NULL,
                    password VARCHAR(255) NOT NULL,
                    role VARCHAR(20) DEFAULT 'student',
                    class VARCHAR(20),
                    age INT,
                    special_needs TEXT,
                    total_expenses DECIMAL(10,2) DEFAULT 0.00,
                    fee_share DECIMAL(10,2) DEFAULT 0.00,
                    balance DECIMAL(10,2) DEFAULT 0.00,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
                )
            """,
            'activities': """
                CREATE TABLE IF NOT EXISTS activities (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(200) NOT NULL,
                    day DATE NOT NULL,
                    start_time INT NOT NULL,
                    finish_time INT NOT NULL,
                    location VARCHAR(200) NOT NULL,
                    max_participants INT DEFAULT NULL,
                    duration INT,
                    description TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """,
            'student_activities': """
                CREATE TABLE IF NOT EXISTS student_activities (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    student_id INT NOT NULL,
                    activity_id INT NOT NULL,
                    registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE,
                    FOREIGN KEY (activity_id) REFERENCES activities(id) ON DELETE CASCADE,
                    UNIQUE KEY unique_student_activity (student_id, activity_id)
                )
            """,
            'expenses': """
                CREATE TABLE IF NOT EXISTS expenses (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    amount DECIMAL(10,2) NOT NULL,
                    description TEXT NOT NULL,
                    date DATE NOT NULL,
                    id_giver INT,
                    id_receiver INT,
                    id_activity INT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (id_giver) REFERENCES students(id) ON DELETE SET NULL,
                    FOREIGN KEY (id_receiver) REFERENCES students(id) ON DELETE SET NULL,
                    FOREIGN KEY (id_activity) REFERENCES activities(id) ON DELETE SET NULL
                )
            """,
            'debts': """
                CREATE TABLE IF NOT EXISTS debts (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    payer_id INT NOT NULL,
                    debtor_id INT NOT NULL,
                    amount DECIMAL(10,2) NOT NULL,
                    description TEXT,
                    expense_id INT,
                    paid BOOLEAN DEFAULT FALSE,
                    date_created DATE NOT NULL,
                    date_paid DATE DEFAULT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                    FOREIGN KEY (payer_id) REFERENCES students(id) ON DELETE CASCADE,
                    FOREIGN KEY (debtor_id) REFERENCES students(id) ON DELETE CASCADE,
                    FOREIGN KEY (expense_id) REFERENCES expenses(id) ON DELETE CASCADE
                )
            """,
            'feedback': """
                CREATE TABLE IF NOT EXISTS feedback (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    student_id INT NOT NULL,
                    activity_id INT NOT NULL,
                    rating INT CHECK (rating >= 1 AND rating <= 5),
                    comment TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE,
                    FOREIGN KEY (activity_id) REFERENCES activities(id) ON DELETE CASCADE,
                    UNIQUE KEY unique_student_feedback (student_id, activity_id)
                )
            """,
            'groups': """
                CREATE TABLE IF NOT EXISTS groups (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    common_activity VARCHAR(200),
                    dietary_needs TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """,
            'student_groups': """
                CREATE TABLE IF NOT EXISTS student_groups (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    group_id INT NOT NULL,
                    student_id INT NOT NULL,
                    joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (group_id) REFERENCES groups(id) ON DELETE CASCADE,
                    FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE,
                    UNIQUE KEY unique_student_group (student_id, group_id)
                )
            """
        }
        
        success_count = 0
        errors = []
        
        for table_name, create_query in tables.items():
            success, result = cls.execute_query(create_query)
            if success:
                success_count += 1
                print(f"Table '{table_name}' ready.")
            else:
                errors.append(f"Failed to create table '{table_name}': {result}")
        
        return success_count == len(tables), errors

    @classmethod # Close the connection pool and clean up resources.
    def disconnect(cls):
        """Close the connection pool"""
        if cls._connection_pool is not None:
            try:
                # Note: mysql.connector pooling doesn't have a direct close_all method
                # The pool will be garbage collected
                cls._connection_pool = None
                logging.info("Database connection pool closed.")
                print("Database connection pool closed.")
            except Exception as e:
                logging.error(f"Failed to close the database connection pool: {e}")
                print(f"Failed to close the database connection pool: {e}")

    @classmethod # Update the database configuration dynamically.
    def update_config(cls, **kwargs):
        """Update database configuration"""
        cls._config.update(kwargs)
        # Reset pool to use new config
        cls._connection_pool = None

# Initialize logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')