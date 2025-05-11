import java.util.ArrayList;
import java.util.List;
import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.SQLException;

public class Group {
    private List<Student> members;
    private String commonActivity;
    private String dietaryNeeds;

    public Group(String commonActivity, String dietaryNeeds) {
        this.members = new ArrayList<>();
        this.commonActivity = commonActivity;
        this.dietaryNeeds = dietaryNeeds;
    }

    public void addMember(Student student) {
        members.add(student);
    }

    public void removeMember(Student student) {
        members.remove(student);
    }

    public List<Student> getMembers() {
        return members;
    }

    public String getCommonActivity() {
        return commonActivity;
    }

    public void setCommonActivity(String commonActivity) {
        this.commonActivity = commonActivity;
    }

    public String getDietaryNeeds() {
        return dietaryNeeds;
    }

    public void setDietaryNeeds(String dietaryNeeds) {
        this.dietaryNeeds = dietaryNeeds;
    }

    public void saveToDatabase() {
        try (Connection connection = DbConnection.connect()) {
            String sql = "INSERT INTO groups (common_activity, dietary_needs) VALUES (?, ?)";
            PreparedStatement statement = connection.prepareStatement(sql);
            statement.setString(1, commonActivity);
            statement.setString(2, dietaryNeeds);
            statement.executeUpdate();
            System.out.println("Group saved to database.");
        } catch (SQLException e) {
            System.err.println("Error saving group to database: " + e.getMessage());
        }
    }
}
