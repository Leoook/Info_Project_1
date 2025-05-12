import java.util.*;
import java.util.regex.Pattern;
import java.util.regex.Matcher;
import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;

public class Statistics {
    private Map<Activity, List<Student>> activities; // Activities and their participants
    private Map<Activity, List<String>> feedbacks; // Activities and their feedbacks

    public Statistics(Map<Activity, List<Student>> activities, Map<Activity, List<String>> feedbacks) {
        this.activities = activities;
        this.feedbacks = feedbacks;
    }

    // Calculate the total number of participants across all activities
    public int getTotalParticipants() {
        return activities.values().stream()
                .mapToInt(List::size)
                .sum();
    }

    // Get the activity with the highest number of participants
    public Activity getMostPopularActivity() {
        return activities.entrySet().stream()
                .max(Comparator.comparingInt(entry -> entry.getValue().size()))
                .map(Map.Entry::getKey)
                .orElse(null);
    }

    // Highlight sentimental words in feedbacks for a specific activity
    public List<String> highlightSentimentalWords(Activity activity, List<String> sentimentalWords) {
        List<String> feedbackList = feedbacks.getOrDefault(activity, new ArrayList<>());
        List<String> highlightedFeedbacks = new ArrayList<>();

        for (String feedback : feedbackList) {
            String highlightedFeedback = feedback;
            for (String word : sentimentalWords) {
                // Highlight sentimental words by wrapping them in asterisks (*)
                highlightedFeedback = highlightedFeedback.replaceAll(
                        "\\b" + Pattern.quote(word) + "\\b", 
                        "*" + word + "*"
                );
            }
            highlightedFeedbacks.add(highlightedFeedback);
        }

        return highlightedFeedbacks;
    }

    // Get average participants per activity
    public double getAverageParticipants() {
        if (activities.isEmpty()) return 0.0;
        return (double) getTotalParticipants() / activities.size();
    }

    public void fetchStatisticsFromDatabase() {
        try (Connection connection = DbConnection.connect()) {
            String sql = "SELECT COUNT(*) AS total_participants FROM student_activities";
            PreparedStatement statement = connection.prepareStatement(sql);
            ResultSet resultSet = statement.executeQuery();
            if (resultSet.next()) {
                System.out.println("Total Participants: " + resultSet.getInt("total_participants"));
            }
        } catch (SQLException e) {
            System.err.println("Error fetching statistics from database: " + e.getMessage());
        }
    }

    @Override
    public String toString() {
        return "Statistics [Total Participants=" + getTotalParticipants() +
                ", Most Popular Activity=" + getMostPopularActivity() +
                ", Average Participants=" + getAverageParticipants() + "]";
    }
}