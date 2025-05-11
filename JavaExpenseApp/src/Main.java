import javax.swing.JFrame;
import javax.swing.SwingUtilities;




public class Main {
    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> {
            ExpenseGUI expenseGUI = new ExpenseGUI();
            expenseGUI.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
            expenseGUI.setVisible(true);
        });
    }
}