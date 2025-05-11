import java.util.Random;
import java.sql.Connection;

public class Main {
    public static void main(String[] args) {
        try (Connection connection = DbConnection.connect()) {
            System.out.println("Database connection initialized.");
            // ...existing code...
        } catch (Exception e) {
            System.err.println("Error initializing database connection: " + e.getMessage());
        }
    }
}
