import java.util.List;

public class Expense {
 int id,total;
 String description; 
 List payments;

 public Expense(int id, int total, String description, List payments) {

	this.id = id;
	this.total = total;
	this.description = description;
	this.payments = payments;
}

public int getId() {
	return id;
}

public void setId(int id) {
	this.id = id;
}

public int getTotal() {
	return total;
}

public void setTotal(int total) {
	this.total = total;
}

public String getDescription() {
	return description;
}

public void setDescription(String description) {
	this.description = description;
}

public List getPayments() {
	return payments;
}

public void setPayments(List payments) {
	this.payments = payments;
}

@Override
public String toString() {
	return "Expense [id=" + id + ", total=" + total + ", description=" + description + ", payments=" + payments + "]";
}
 
}
