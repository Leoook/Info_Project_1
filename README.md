# Trip Manager - School Trip Management System

> **A modern Python application for managing school trips, activities, expenses, and analytics with a role-based, intuitive GUI.**

---

## 📋 Table of Contents
- [Project Overview](#project-overview)
- [Features](#features)
- [System Requirements](#system-requirements)
- [Installation & Setup](#installation--setup)
- [Database Setup](#database-setup)
- [Running the Application](#running-the-application)
- [User Guide](#user-guide)
- [Architecture](#architecture)
- [Database Schema](#database-schema)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

---

## 🎯 Project Overview

Trip Manager is a comprehensive, role-based application for school trip management. It provides:
- **Student Dashboard**: For activity enrollment, expense tracking, and feedback.
- **Teacher Dashboard**: For full oversight, analytics, and group/participant management (teachers cannot participate in activities).
- **Modern GUI**: Built with Tkinter, supporting both students and teachers with tailored interfaces.

---

## ✨ Features

### For Students
- **Secure Login**: Authentication with username/password.
- **Activity Subscription**: Browse and enroll in activities (with conflict and capacity checks).
- **Expense Management**: Add, split, and track expenses; see debts and settlements.
- **Feedback System**: Rate and comment on activities you participated in.
- **Personal Dashboard**: View your schedule, activities, and financial summary.

### For Teachers
- **Dedicated Teacher Dashboard**: Access a separate dashboard with:
  - **Activities Overview**: See all activities, participant counts, and details.
  - **Students & Enrollment**: View all students, their classes, and their activity enrollments.
  - **Daily Schedule**: Visualize the full trip schedule and participant lists for each day.
  - **Analytics**: Access statistics on participation, popular activities, feedback, and expenses.
- **No Participation in Activities**: Teachers cannot enroll in activities (enforced at the database level).
- **Group Management**: All group and participant management is now handled exclusively in the Teacher Dashboard.

### Security & Data Integrity
- **Role-Based Access**: Students and teachers see different dashboards and features.
- **Database Constraints**: Teachers cannot be enrolled in activities (enforced by a CHECK constraint in the database schema).
- **Authentication**: Secure login for all users.

---

## 🖥️ System Requirements
- **Python**: 3.10 or newer
- **MySQL Server**: 8.0 or newer
- **OS**: Windows, macOS, or Linux
- **Python Packages**: See `requirements.txt`

---

## 🚀 Installation & Setup

1. **Clone the Repository:**
   ```sh
   git clone <repository-url>
   cd Info_Project_1
   ```
2. **Create Virtual Environment (Recommended):**
   ```sh
   python -m venv trip_manager_env
   # Activate (Windows)
   trip_manager_env\Scripts\activate
   # Activate (macOS/Linux)
   source trip_manager_env/bin/activate
   ```
3. **Install Dependencies:**
   ```sh
   pip install -r requirements.txt
   ```
4. **Set Up the Database:**
   - Install MySQL and create a database/user as described below.
   - Run `database_setup.sql` to create tables and sample data.
   - Update your database credentials in `PythonExpenseApp/db_connection.py` if needed.

---

## 🗄️ Database Setup

1. **Install MySQL** ([Download](https://dev.mysql.com/downloads/))
2. **Create Database and User:**
   ```sql
   CREATE DATABASE trip_manager;
   CREATE USER 'trip_user'@'localhost' IDENTIFIED BY 'secure_password';
   GRANT ALL PRIVILEGES ON trip_manager.* TO 'trip_user'@'localhost';
   FLUSH PRIVILEGES;
   USE trip_manager;
   ```
3. **Import Schema:**
   ```sh
   mysql -u root -p trip_manager < PythonExpenseApp/database_setup.sql
   ```
4. **Configure Connection:**
   Edit `PythonExpenseApp/db_connection.py` with your MySQL credentials.

---

## ▶️ Running the Application

- **From Project Root:**
  ```sh
  python -m PythonExpenseApp.main
  ```
- **Direct Execution:**
  ```sh
  cd PythonExpenseApp
  python main.py
  ```
- **IDE Integration:**
  - Open the project in your IDE and run `main.py`.

---

## 📖 User Guide

### First Time Setup
1. **Start the Application**: Run using one of the methods above.
2. **Database Check**: The app will verify database connectivity on startup.
3. **Login**: Use the default credentials or create new student/teacher accounts.

### Student Workflow
- **Login** → **Dashboard** → **Activities** → **Expenses** → **Feedback**
- Use the dashboard to access all features. Navigation is intuitive and role-based.

### Teacher Workflow
- **Login** → **Teacher Dashboard**
- Access all activities, students, enrollments, schedules, and analytics from a single interface.
- Teachers cannot participate in activities or use the student dashboard.

---

## 🏗️ Architecture

- **PythonExpenseApp/**: Main application package
  - `main.py`: Entry point, handles login and dashboard routing
  - `db_connection.py`: Database connectivity
  - `student.py`, `activity.py`, `expense.py`, `feedback.py`, `statistics.py`: Core logic
  - `gui/`: All GUI modules (student and teacher dashboards, login, etc.)
- **Role-based Routing**: Users are routed to different dashboards based on their role (student/teacher)

---

## 🗃️ Database Schema

- **students**: Stores both students and teachers, with a `role` field.
- **activities**: All trip activities, with schedule and capacity info.
- **student_activities**: Junction table for student enrollments, with a constraint to prevent teacher participation.
- **expenses**: Tracks all trip-related expenses.
- **debts**: Tracks who owes whom and how much.
- **feedback**: Stores feedback and ratings for activities.

**Key Integrity Constraint:**
```sql
CONSTRAINT check_student_role CHECK (
    (SELECT role FROM students WHERE id = student_id) = 'student'
)
```

---

## 🔧 Troubleshooting

### Common Issues
- **Database Connection Errors**: Check MySQL service, credentials, and database existence.
- **Import Errors**: Run from the project root and activate your virtual environment.
- **GUI Display Issues**: Ensure Tkinter is installed (on Linux: `sudo apt-get install python3-tk`).

---

## 🤝 Contributing


