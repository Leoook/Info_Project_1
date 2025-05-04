import java.util.ArrayList;
import java.util.List;

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
}
