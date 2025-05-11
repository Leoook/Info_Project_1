import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.SQLException;
import java.text.SimpleDateFormat;
import java.util.Date;

public class Expense {
    private double amount;
    private String description;
    private String date;

    public Expense(double amount, String description, String date) {
        this.amount = amount;
        this.description = description;
        this.date = date;
    }

    public Expense(double amount, String description) {
        this(amount, description, new SimpleDateFormat("yyyy-MM-dd").format(new Date()));
    }

    public double getAmount() {
        return amount;
    }

    public void setAmount(double amount) {
        this.amount = amount;
    }

    public String getDescription() {
        return description;
    }

    public void setDescription(String description) {
        this.description = description;
    }

    public String getDate() {
        return date;
    }

    public void setDate(String date) {
        this.date = date;
    }

    public void saveToDatabase() {
        try (Connection connection = DbConnection.connect()) {
            String sql = "INSERT INTO expenses (amount, description, date) VALUES (?, ?, ?)";
            PreparedStatement statement = connection.prepareStatement(sql);
            statement.setDouble(1, amount);
            statement.setString(2, description);
            statement.setString(3, date);
            statement.executeUpdate();
            System.out.println("Expense saved to database.");
        } catch (SQLException e) {
            System.err.println("Error saving expense to database: " + e.getMessage());
        }
    }
}