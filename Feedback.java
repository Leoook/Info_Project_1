import java.util.List;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.stream.Collectors;
import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.SQLException;

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

class Student {
    private String name;
    private List<Feedback> feedbacks;

    public Student(String name) {
        this.name = name;
        this.feedbacks = new ArrayList<>();
    }

    public String getName() { return name; }
    public List<Feedback> getFeedbacks() { return feedbacks; }
}

class Activity {
    private String name;
    private List<Student> participants;
    private List<Feedback> feedbacks;

    public Activity(String name) {
        this.name = name;
        this.participants = new ArrayList<>();
        this.feedbacks = new ArrayList<>();
    }

    public String getName() { return name; }
    public List<Student> getParticipants() { return participants; }
    public List<Feedback> getFeedbacks() { return feedbacks; }

    public void addParticipant(Student student) {
        participants.add(student);
    }
}

public class FeedbackService {
    // REGISTRAZIONE DEI FEEDBACK
    public void addFeedback(Student student, Activity activity, int rating, String comment) {
        if (!activity.getParticipants().contains(student)) {
            System.out.println("Errore: lo studente non ha partecipato all'attività.");
            return;
        }

        Feedback feedback = new Feedback(student, activity, rating, comment);
        activity.getFeedbacks().add(feedback);
        student.getFeedbacks().add(feedback); // Save feedback in student's list

        // Save feedback to the database
        try (Connection connection = DbConnection.connect()) {
            String sql = "INSERT INTO feedback (student_name, activity_name, rating, comment) VALUES (?, ?, ?, ?)";
            PreparedStatement statement = connection.prepareStatement(sql);
            statement.setString(1, student.getName());
            statement.setString(2, activity.getName());
            statement.setInt(3, rating);
            statement.setString(4, comment);
            statement.executeUpdate();
            System.out.println("Feedback salvato nel database.");
        } catch (SQLException e) {
            System.err.println("Errore durante il salvataggio del feedback nel database: " + e.getMessage());
        }
    }

    // Verifica partecipazione prima di accettare un feedback
    public boolean canGiveFeedback(Student student, Activity activity) {
        return activity.getParticipants().contains(student);
    }

    // Esempi di funzioncine per ricavare vari valori dai feedback
    public double getAverageRating(Activity activity) {
        List<Feedback> feedbacks = activity.getFeedbacks();
        if (feedbacks.isEmpty()) return 0.0;

        double sum = 0;
        for (Feedback f : feedbacks) sum += f.getRating();
        return sum / feedbacks.size();
    }

    public List<Feedback> getNegativeFeedbacks(Activity activity) {
        return activity.getFeedbacks().stream()
            .filter(f -> f.getRating() <= 2)
            .collect(Collectors.toList());
    }

    // Evidenziare feedback con parole chiave da segnalare
    private List<String> flaggedWords = Arrays.asList("noioso", "pericoloso", "non sicuro");

    public List<Feedback> getFlaggedFeedbacks(Activity activity) {
        return activity.getFeedbacks().stream()
            .filter(f -> flaggedWords.stream().anyMatch(word -> f.getComment().toLowerCase().contains(word)))
            .collect(Collectors.toList());
    }
}
