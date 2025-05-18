import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.SQLException;
import java.util.ArrayList;
import java.util.List;

public class Student {
    private String name;
    private String surname;
    private int age;
    private String specialNeeds;
    private List<Activity> selectedActivities; // Changed to store Activity objects
    private double totalExpenses;
    private double feeShare;
    private double balance; // Positive: to receive, Negative: to reimburse

    public Student(String name, String surname, int age, String specialNeeds) {
        this.name = name;
        this.surname = surname;
        this.age = age;
        this.specialNeeds = specialNeeds;
        this.selectedActivities = new ArrayList<>();
        this.totalExpenses = 0.0;
        this.feeShare = 0.0;
        this.balance = 0.0;
    }

    public void addActivity(Activity activity) { // Updated to accept Activity objects
        try {
            if (activity.isFull()) {
                System.out.println("Activity '" + activity.getName() + "' is already full.");
                return;
            }
        } catch (Exception e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
        }
        selectedActivities.add(activity);
    }

    public List<Activity> getSelectedActivities() { // Updated return type
        return selectedActivities;
    }

    public void addExpense(double amount) {
        totalExpenses += amount;
    }

    public double getTotalExpenses() {
        return totalExpenses;
    }

    public void setFeeShare(double feeShare) {
        this.feeShare = feeShare;
    }

    public double getFeeShare() {
        return feeShare;
    }

    public void setBalance(double balance) {
        this.balance = balance;
    }

    public double getBalance() {
        return balance;
    }

    public Student(int id) {
    this.id = id;
}

    public void saveToDatabase() {
        try (Connection connection = DbConnection.connect()) {
            String sql = "INSERT INTO students (name, surname, age, special_needs, total_expenses, fee_share, balance) VALUES (?, ?, ?, ?, ?, ?, ?)";
            PreparedStatement statement = connection.prepareStatement(sql);
            statement.setString(1, name);
            statement.setString(2, surname);
            statement.setInt(3, age);
            statement.setString(4, specialNeeds);
            statement.setDouble(5, totalExpenses);
            statement.setDouble(6, feeShare);
            statement.setDouble(7, balance);
            statement.executeUpdate();
            System.out.println("Student saved to database.");
        } catch (SQLException e) {
            System.err.println("Error saving student to database: " + e.getMessage());
        }
    }

    @Override
    public String toString() {
        return "Student [name=" + name + ", surname=" + surname + ", age=" + age + ", specialNeeds=" + specialNeeds
                + ", selectedActivities=" + selectedActivities + ", totalExpenses=" + totalExpenses + ", feeShare="
                + feeShare + ", balance=" + balance + "]";
    }
}
