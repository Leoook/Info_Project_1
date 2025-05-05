Tools:
-Java (with the libraries needed: JDBC, Interface)
-libraries: -all the utils
            -Swing for the interface
            -JDBC for the database connection
-Mysql server (Probably phpmyadmin)

1. 
Student Class
Stores the student's personal data (name, surname, age, special needs).
Contains the selected activities.
Keeps track of expenses incurred and the fees to be divided.
Contains how much the student has to reimburse or receive.

2. 
Activity Class
Represents an activity available during the trip.
Contains name, description, duration, location, time, maximum number of participants and students registered.
Manages registration and checks availability of places.

3. 
Group Class
Represents a group of students.
Keeps track of members and training criteria (e.g. common activity, dietary needs).

4. 
Daily Program Class/List
Represents the calendar of activities for a single day.
Map of days/activities/participants.

5. 
Travel Class
Main Coordinator: contains the list of students, activities, groups and daily program.
Manages group assignment logic and program creation.

6. 
Expense Class
Represents an expense made during the trip.
Stores who paid, the total amount and the participants who must divide the expense.

7. 
ExpenseManager Class
Manages all registered expenses.
Calculates how much each student must receive or reimburse.

8. 
Feedback Class
Allows a student to leave a rating on an activity (from 1 to 5 stars) and a comment.

9. 
FeedbackService Class
Manages feedback registration and provides methods to analyze feedback data (e.g., average ratings, flagged comments).

10. 
Statistics Class
Analyzes feedback data to calculate statistics such as average ratings, most appreciated activities, and trends in feedback.
Identifies potential issues by highlighting negative feedback or critical comments.
Works in conjunction with the Feedback Class to process and summarize feedback data.

11. 
UserInterface Class
Manages interaction with the user (menu, input, output).
It can be textual or graphical.
Divided into sections for students and teachers.

12. 
DataManager Class
It deals with saving and loading data from files or databases.
It manages exports of trip summaries.

Main relationships:
- Student objects participate in many Activities.
- Students are grouped into Groups.
- Trip manages all coordination between Student, Activity, Group, Expense, DailyProgram, and Feedback.
- Feedback is linked to Activities.
- ExpenseManager and Statistics work on the Expense and Feedback collections.

Ideas:
- Login page (with passwords and usernames)
- Online website (maybe hosted on a VPS?)

FARE DATABASE
FRAMEWORK PER SENTIMENTAL WORDS