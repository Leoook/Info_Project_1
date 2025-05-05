public class Feedback {
    private int id;
    private Student student;
    private Activity activity;
    private int rating; // da 1 a 5
    private String comment;

    // Costruttore
    public Feedback(Student student, Activity activity, int rating, String comment) {
        this.student = student;
        this.activity = activity;
        this.rating = rating;
        this.comment = comment;
    }

    // Getter
    public Student getStudent() { return student; }
    public Activity getActivity() { return activity; }
    public int getRating() { return rating; }
    public String getComment() { return comment; }
}

//(Verifica partecipazione prima di accettare un feedback)
public boolean canGiveFeedback(Student student, Activity activity) {
    return Activity.getParticipants().contains(student);
}


//(REGISTAZIONE DEI FEEDBACK)
public class FeedbackService {
    public void addFeedback(Student student, Activity activity, int rating, String comment) {
        if (!activity.getParticipants().contains(student)) {
            System.out.println("Errore: lo studente non ha partecipato all'attività.");
            return;
        }

        Feedback feedback = new Feedback(student, activity, rating, comment);
        activity.getFeedbacks().add(feedback);
        // (opzionale) student.getFeedbacks().add(feedback);
        
        // Salva anche su database
    }
}


//(esempi di funzioncine per ricavare vari valori dai feedback)
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



//(evidenziare feedback con parole chiave da segnalare)
List<String> flaggedWords = Arrays.asList("noioso", "pericoloso", "non sicuro");

public List<Feedback> getFlaggedFeedbacks(Activity activity) {
    return activity.getFeedbacks().stream()
        .filter(f -> flaggedWords.stream().anyMatch(word -> f.getComment().toLowerCase().contains(word)))
        .collect(Collectors.toList());
}
