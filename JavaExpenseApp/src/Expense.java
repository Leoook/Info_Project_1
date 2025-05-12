import java.util.List;

public class Expense {
 int E_id, total;
 String description; 
 List payments;
 int ID_giver;
 int ID_receiver;
 int ID_activity;

 public Expense(int E_id, int total, String description, List payments, int ID_giver, int ID_receiver, int ID_activity) {

	this.E_id = E_id;
	this.total = total;
	this.description = description;
	this.payments = payments;
	this.ID_giver = ID_giver;
	this.ID_receiver = ID_receiver;	
	this.ID_activity = ID_activity;
 }


public int getE_Id() {
	return E_id;
}

public void setE_Id(int E_id) {
	this.E_id = E_id;
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
public int getID_giver() {
	return ID_giver;
}
public void setID_giver(int ID_giver) {
	this.ID_giver = ID_giver;
}
public int getID_receiver() {
	return ID_receiver;
}
public void setID_receiver(int ID_receiver) {
	this.ID_receiver = ID_receiver;
}
public int getID_activity() {
	return ID_activity;
}
public void setID_activity(int ID_activity) {
	this.ID_activity = ID_activity;
}

 
}
