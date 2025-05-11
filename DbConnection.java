import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;

public class DbConnection {
    private static final String URL = "jdbc:mysql://localhost:3306/test";
    private static final String USER = "root";
    private static final String PASSWORD = "";
    private static Connection connection = null;

    // Establish a connection to the database
    public static Connection connect() {
        if (connection == null) {
            try {
                connection = DriverManager.getConnection(URL, USER, PASSWORD);
                System.out.println("Database connection established.");
            } catch (SQLException e) {
                System.err.println("Failed to connect to the database: " + e.getMessage());
            }
        }
        return connection;
    }

    // Close the database connection
    public static void disconnect() {
        if (connection != null) {
            try {
                connection.close();
                connection = null;
                System.out.println("Database connection closed.");
            } catch (SQLException e) {
                System.err.println("Failed to close the database connection: " + e.getMessage());
            }
        }
    }
}
