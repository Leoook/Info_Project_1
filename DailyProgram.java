import java.util.Date;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.SQLException;

public class DailyProgram {
    private Date day; // Represents the specific day
    private Map<Activity, List<Student>> activities; // Maps activities to their participants

    public DailyProgram(Date day) {
        this.day = day;
        this.activities = new HashMap<>();
    }

    // Getter and Setter for the day
    public Date getDay() {
        return day;
    }

    public void setDay(Date day) {
        this.day = day;
    }

    // Add an activity with participants
    public void addActivity(Activity activity, List<Student> participants) {
        activities.put(activity, participants);
    }

    // Get all activities
    public Map<Activity, List<Student>> getActivities() {
        return activities;
    }

    // Get participants for a specific activity
    public List<Student> getParticipants(Activity activity) {
        return activities.get(activity);
    }

    // Remove an activity
    public void removeActivity(Activity activity) {
        activities.remove(activity);
    }

    public void saveToDatabase() {
        try (Connection connection = DbConnection.connect()) {
            String sql = "INSERT INTO daily_program (day, activity_id) VALUES (?, ?)";
            for (Map.Entry<Activity, List<Student>> entry : activities.entrySet()) {
                PreparedStatement statement = connection.prepareStatement(sql);
                statement.setDate(1, new java.sql.Date(day.getTime()));
                statement.setInt(2, entry.getKey().getId());
                statement.executeUpdate();
            }
            System.out.println("Daily program saved to database.");
        } catch (SQLException e) {
            System.err.println("Error saving daily program to database: " + e.getMessage());
        }
    }

    @Override
    public String toString() {
        return "DailyProgram [day=" + day + ", activities=" + activities + "]";
    }
}