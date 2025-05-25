# Trip Manager

> **Note:** All variables and functions in the code are commented for clarity.  
> Each class and method includes a description of its purpose and usage.

## Project Overview

This project is a Python application for managing school trips, including:
- Student registration and management
- Activity management and student subscriptions
- Expense tracking and management
- Feedback collection and statistics

**Main files and their roles:**
- `main.py`: Entry point, launches the main menu and GUI windows.
- `student.py`: Defines the Student class and its database logic.
- `activity.py`: Defines the Activity class and its database logic.
- `group.py`: Defines the Group class for student grouping.
- `expense.py`: Defines the Expense class and its database logic.
- `gui/expense_gui.py`: Contains the ExpenseGUI class for the expense management interface.
- `gui/activity_form_gui.py`: Contains the ActivityFormGUI class for activity subscription.
- `db_connection.py`: Handles MySQL database connections.
- `statistics.py`: Provides statistics and analytics on activities and feedback.
- `feedback.py`: Defines the Feedback class and feedback database logic.
- `daily_program.py`: Manages the daily schedule of activities.

## Requirements

- Python 3.10 or newer
- MySQL server
- [mysql-connector-python](https://pypi.org/project/mysql-connector-python/)
- Tkinter (usually included with Python)

## Setup

1. **Clone or download this repository.**

2. **Create and activate a virtual environment (recommended):**
   ```sh
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```sh
   pip install mysql-connector-python
   ```

4. **Set up the database:**
   - Make sure MySQL server is running.
   - Create a database named `project`.
   - Import the provided SQL schema and example data:
     ```sh
     mysql -u root -p project < project_schema.sql
     ```
     (You may need to adjust the username/password.)

5. **Configure database connection:**
   - If your MySQL credentials are different, edit `PythonExpenseApp/db_connection.py` accordingly.

## Running the Application

From the root folder, run:
```sh
python -m PythonExpenseApp.main
```
or, if that doesn't work, try:
```sh
python PythonExpenseApp/main.py
```

## Usage

- On launch, a window will appear to select between the Expense GUI and the Activity Form.
- Use the GUIs to add expenses or subscribe students to activities.

## Notes

- Ensure your database tables match the schema in `project_schema.sql`.
- All code is under the `PythonExpenseApp` package.
- If you encounter import errors, make sure you are running from the project root and your Python path is correct.

Tools:
-Java (with the libraries needed: JDBC, Interface)
-libraries: -all the utils
            -Swing for the interface
            -JDBC for the database connection
-Mysql server (Probably phpmyadmin)

## Class Structure

1. **Student Class**
   - Stores the student's personal data (name, surname, age, special needs).
   - Contains the selected activities.
   - Keeps track of expenses incurred and the fees to be divided.
   - Contains how much the student has to reimburse or receive.

2. **Activity Class**
   - Represents an activity available during the trip.
   - Contains name, description, duration, location, time, maximum number of participants, and students registered.
   - Manages registration and checks availability of places.

3. **Group Class**
   - Represents a group of students.
   - Keeps track of members and training criteria (e.g., common activity, dietary needs).

4. **Daily Program Class/List**
   - Represents the calendar of activities for a single day.
   - Map of days/activities/participants.

5. **Travel Class**
   - Main Coordinator: contains the list of students, activities, groups, and daily program.
   - Manages group assignment logic and program creation.

6. **Expense Class**
   - Represents an expense made during the trip.
   - Stores who paid, the total amount, and the participants who must divide the expense.

7. **ExpenseManager Class**
   - Manages all registered expenses.
   - Calculates how much each student must receive or reimburse.

8. **Feedback Class**
   - Allows a student to leave a rating on an activity (from 1 to 5 stars) and a comment.

9. **FeedbackService Class**
   - Manages feedback registration and provides methods to analyze feedback data (e.g., average ratings, flagged comments).

10. **Statistics Class**
    - Analyzes feedback data to calculate statistics such as average ratings, most appreciated activities, and trends in feedback.
    - Identifies potential issues by highlighting negative feedback or critical comments.
    - Works in conjunction with the Feedback Class to process and summarize feedback data.

11. **UserInterface Class**
    - Manages interaction with the user (menu, input, output).
    - It can be textual or graphical.
    - Divided into sections for students and teachers.

12. **DataManager Class**
    - Deals with saving and loading data from files or databases.
    - Manages exports of trip summaries.

### Main relationships

- Student objects participate in many Activities.
- Students are grouped into Groups.
- Trip manages all coordination between Student, Activity, Group, Expense, DailyProgram, and Feedback.
- Feedback is linked to Activities.
- ExpenseManager and Statistics work on the Expense and Feedback collections.

### Ideas

- Login page (with passwords and usernames)
- Online website (maybe hosted on a VPS?)
