import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.util.ArrayList;

public class ExpenseGUI extends JFrame {
    private ArrayList<Expense> expenses;
    private JTextField amountField;
    private JTextField descriptionField;
    private JTextArea expenseListArea;

    public ExpenseGUI() {
        expenses = new ArrayList<>();
        setTitle("Expense Tracker");
        setSize(400, 300);
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setLayout(new BorderLayout());

        JPanel inputPanel = new JPanel();
        amountField = new JTextField(10);
        descriptionField = new JTextField(10);
        JButton addButton = new JButton("Add Expense");

        inputPanel.add(new JLabel("Amount:"));
        inputPanel.add(amountField);
        inputPanel.add(new JLabel("Description:"));
        inputPanel.add(descriptionField);
        inputPanel.add(addButton);

        expenseListArea = new JTextArea();
        expenseListArea.setEditable(false);

        add(inputPanel, BorderLayout.NORTH);
        add(new JScrollPane(expenseListArea), BorderLayout.CENTER);

        addButton.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                addExpense();
            }
        });
    }

    private void addExpense() {
        String amountText = amountField.getText();
        String description = descriptionField.getText();
        if (!amountText.isEmpty() && !description.isEmpty()) {
            double amount = Double.parseDouble(amountText);
            Expense expense = new Expense(amount, description);
            expenses.add(expense);
            updateExpenseList();
            amountField.setText("");
            descriptionField.setText("");
        } else {
            JOptionPane.showMessageDialog(this, "Please enter both amount and description.");
        }
    }

    private void updateExpenseList() {
        StringBuilder listBuilder = new StringBuilder();
        for (Expense expense : expenses) {
            listBuilder.append(expense.toString()).append("\n");
        }
        expenseListArea.setText(listBuilder.toString());
    }

    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> {
            ExpenseGUI gui = new ExpenseGUI();
            gui.setVisible(true);
        });
    }
}