import javax.swing.*;
import java.awt.*;
import models.Expense;
import gui.ExpenseGUI;

public class Main {
    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> {
            ExpenseGUI expenseGUI = new ExpenseGUI();
            expenseGUI.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
            expenseGUI.setVisible(true);
        });
    }
}