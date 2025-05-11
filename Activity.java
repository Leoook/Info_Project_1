import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.SQLException;
import java.util.List;

public class Activity {
	int id,maxpart,start,finish,duration;
	String name,location;
	List partecipants;
	List Activityfeedback;
	
	public Activity(int id, String name, int maxpart, String location, int duration, int start, int finish, List partecipants, List feedback) {
		this.id = id;
		this.name = name;
		this.maxpart = maxpart;
		this.location = location;
		this.duration = duration;
		this.start = start;
		this.finish = finish;
		this.partecipants = partecipants;
		this.Activityfeedback = feedback;
	}
	public int getId() {
		return id;
	}

	public void setId(int id) {
		this.id = id;
	}

	public String getName() {
		return name;
	}

	public void setName(String name) {
		this.name = name;
	}

	public int getMaxpart() {
		return maxpart;
	}

	public void setMaxpart(int maxpart) {
		this.maxpart = maxpart;
	}

	public String getLocation() {
		return location;
	}

	public void setLocation(String location) {
		this.location = location;
	}

	public int getDuration() {
		return duration;
	}

	public void setDuration(int duration) {
		this.duration = duration;
	}

	public int getStart() {
		return start;
	}

	public void setStart(int start) {
		this.start = start;
	}

	public int getFinish() {
		return finish;
	}

	public void setFinish(int finish) {
		this.finish = finish;
	}

	public List getPartecipants() {
		return partecipants;
	}

	public void setPartecipants(List partecipants) {
		this.partecipants = partecipants;
	}

	public List getActivityFeedback() {
		return Activityfeedback;
	}

	public void setActivityFeedback(List Activityfeedback) {
		this.Activityfeedback = Activityfeedback;
	}

	public boolean isFull() {
	    return partecipants.size() >= maxpart;
	}

	public void saveToDatabase() {
	    try (Connection connection = DbConnection.connect()) {
	        String sql = "INSERT INTO activities (name, max_participants, location, duration, start_time, finish_time) VALUES (?, ?, ?, ?, ?, ?)";
	        PreparedStatement statement = connection.prepareStatement(sql);
	        statement.setString(1, name);
	        statement.setInt(2, maxpart);
	        statement.setString(3, location);
	        statement.setInt(4, duration);
	        statement.setInt(5, start);
	        statement.setInt(6, finish);
	        statement.executeUpdate();
	        System.out.println("Activity saved to database.");
	    } catch (SQLException e) {
	        System.err.println("Error saving activity to database: " + e.getMessage());
	    }
	}
  
	@Override
	public String toString() {
		return "Activity [id=" + id + ", name=" + name + ", maxpart=" + maxpart + ", location=" + location
				+ ", duratiion=" + duration + ", start=" + start + ", finish=" + finish + ", partecipants="
				+ partecipants + ", feedback=" + Activityfeedback + "]";
	}
	
	
}
