
public class Feedback {
 int id,rating;
Student student;
 Activity activity;
 
 public Feedback(int id, int rating, Student student, Activity activity) {
		super();
		this.id = id;
		this.rating = rating;
		this.student = student;
		this.activity = activity;
	}

public int getId() {
	return id;
}

public void setId(int id) {
	this.id = id;
}

public int getRating() {
	return rating;
}

public void setRating(int rating) {
	this.rating = rating;
}

public Student getStudent() {
	return student;
}

public void setStudent(Student student) {
	this.student = student;
}

public Activity getActivity() {
	return activity;
}

public void setActivity(Activity activity) {
	this.activity = activity;
}

@Override
public String toString() {
	return "Feedback [id=" + id + ", rating=" + rating + ", student=" + student + ", activity=" + activity + "]";
}
 
}
