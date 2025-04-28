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

	@Override
	public String toString() {
		return "Activity [id=" + id + ", name=" + name + ", maxpart=" + maxpart + ", location=" + location
				+ ", duratiion=" + duration + ", start=" + start + ", finish=" + finish + ", partecipants="
				+ partecipants + ", feedback=" + Activityfeedback + "]";
	}
	
	
}
