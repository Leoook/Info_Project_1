# Java Expense Application

This project is a simple Java application that allows users to manage their expenses through a graphical user interface (GUI). It consists of three main components: the main application entry point, the expense model, and the GUI for user interaction.

## Project Structure

```
JavaExpenseApp
├── src
│   ├── Main.java          # Entry point of the application
│   ├── models
│   │   └── Expense.java   # Represents an expense with properties
│   ├── gui
│   │   └── ExpenseGUI.java # GUI for displaying and managing expenses
└── README.md              # Documentation for the project
```

## Setup Instructions

1. **Clone the repository**:
   ```
   git clone <repository-url>
   ```

2. **Navigate to the project directory**:
   ```
   cd JavaExpenseApp
   ```

3. **Compile the Java files**:
   ```
   javac src/*.java src/models/*.java src/gui/*.java
   ```

4. **Run the application**:
   ```
   java src/Main
   ```

## Usage Guidelines

- Upon running the application, the GUI will appear, allowing users to add, view, and manage their expenses.
- Users can input the amount, description, and date of each expense.
- The application will display a list of all recorded expenses.

## Contributing

Feel free to submit issues or pull requests for improvements or bug fixes.