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

    @Override
    public String toString() {
        return "Student [name=" + name + ", surname=" + surname + ", age=" + age + ", specialNeeds=" + specialNeeds
                + ", selectedActivities=" + selectedActivities + ", totalExpenses=" + totalExpenses + ", feeShare="
                + feeShare + ", balance=" + balance + "]";
    }
}
