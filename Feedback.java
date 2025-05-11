import java.util.ArrayList;
import java.util.List;

public class Feedback {
    private static int idCounter = 1; // Static counter for unique IDs
    private int id;
    private Student student;
    private Activity activity;
    private int rating; // da 1 a 5
    private String comment;

    // Costruttore
    public Feedback(Student student, Activity activity, int rating, String comment) {
        this.id = idCounter++;
        this.student = student;
        this.activity = activity;
        this.rating = rating;
        this.comment = comment;
    }

    // Getter
    public int getId() { return id; }
    public Student getStudent() { return student; }
    public Activity getActivity() { return activity; }
    public int getRating() { return rating; }
    public String getComment() { return comment; }
}

class StudentLocal {
    private String name;
    private List<Feedback> feedbacks;

    public StudentLocal(String name) {
        this.name = name;
        this.feedbacks = new ArrayList<>();
    }

    public String getName() { return name; }
    public List<Feedback> getFeedbacks() { return feedbacks; }
}

class ActivityLocal {
    private String name;
    private List<StudentLocal> participants;
    private List<Feedback> feedbacks;

    public ActivityLocal(String name) {
        this.name = name;
        this.participants = new ArrayList<>();
        this.feedbacks = new ArrayList<>();
    }

    public String getName() { return name; }
    public List<StudentLocal> getParticipants() { return participants; }
    public List<Feedback> getFeedbacks() { return feedbacks; }

    public void addParticipant(StudentLocal student) {
        participants.add(student);
    }

    public static boolean isFull() {
        throw new UnsupportedOperationException("Unimplemented method 'isFull'");
    }
}

