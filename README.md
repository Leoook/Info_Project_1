# Trip Manager - Complete Student Trip Management System

> **A comprehensive Python-based application for managing school trips, activities, expenses, and student feedback with an intuitive GUI interface.**

## 📋 Table of Contents
- [Project Overview](#project-overview)
- [Features](#features)
- [System Requirements](#system-requirements)
- [Installation & Setup](#installation--setup)
- [Database Setup](#database-setup)
- [Running the Application](#running-the-application)
- [User Guide](#user-guide)
- [Program Structure](#program-structure)
- [Database Schema](#database-schema)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)

## 🎯 Project Overview

Trip Manager is a comprehensive application designed to streamline the management of school trips. It provides tools for:

- **Student Management**: Registration, authentication, and profile management
- **Activity Management**: Creating, scheduling, and managing trip activities
- **Expense Tracking**: Recording and splitting expenses among participants
- **Feedback System**: Collecting and analyzing student feedback with sentiment analysis
- **Statistics & Analytics**: Comprehensive reporting and data visualization

## ✨ Features

### Core Features
- 🔐 **Secure Login System** - Student authentication with username/password
- 🎯 **Activity Subscription** - Students can browse and subscribe to activities
- 💰 **Expense Management** - Track shared expenses and calculate debt settlements
- 📝 **Feedback Collection** - Rate activities and leave comments (participation required)
- 📊 **Real-time Statistics** - Sentiment analysis and activity popularity metrics
- 🗓️ **Schedule Management** - Daily activity schedules and conflict detection

### Advanced Features
- **Sentiment Analysis** - Automatic analysis of feedback comments
- **Debt Tracking** - Who owes whom and how much
- **Conflict Detection** - Prevents scheduling conflicts for students
- **Participation Validation** - Only participants can leave feedback
- **Real-time Updates** - Live data refresh across all components

## 🖥️ System Requirements

### Software Requirements
- **Python**: 3.8 or newer (3.10+ recommended)
- **MySQL Server**: 8.0 or newer
- **Operating System**: Windows 10/11, macOS 10.14+, or Linux

### Python Dependencies
- `mysql-connector-python`: Database connectivity
- `tkinter`: GUI framework (usually included with Python)
- `PIL (Pillow)`: Image processing for GUI
- `datetime`: Date/time handling (built-in)
- `re`: Regular expressions (built-in)

## 🚀 Installation & Setup

### Step 1: Clone the Repository
```bash
git clone <repository-url>
cd Info_Project_1
```

### Step 2: Create Virtual Environment (Recommended)
```bash
# Create virtual environment
python -m venv trip_manager_env

# Activate virtual environment
# Windows:
trip_manager_env\Scripts\activate
# macOS/Linux:
source trip_manager_env/bin/activate
```

### Step 3: Install Dependencies
```bash
# Install required packages
pip install mysql-connector-python Pillow

# Or use requirements file if available
pip install -r requirements.txt
```

### Step 4: Verify Installation
```bash
python -c "import mysql.connector, tkinter, PIL; print('All dependencies installed successfully!')"
```

## 🗄️ Database Setup

### Step 1: Install MySQL
1. Download and install MySQL Server from [mysql.com](https://dev.mysql.com/downloads/)
2. During installation, remember your root password
3. Start the MySQL service

### Step 2: Create Database
```sql
-- Connect to MySQL as root
mysql -u root -p

-- Create the database
CREATE DATABASE trip_manager;

-- Create a user for the application (optional but recommended)
CREATE USER 'trip_user'@'localhost' IDENTIFIED BY 'secure_password';
GRANT ALL PRIVILEGES ON trip_manager.* TO 'trip_user'@'localhost';
FLUSH PRIVILEGES;

-- Use the database
USE trip_manager;
```

### Step 3: Import Schema
```bash
# Import the database schema
mysql -u root -p trip_manager < database_schema.sql
```

### Step 4: Configure Connection
Edit `PythonExpenseApp/db_connection.py` if needed:
```python
# Update these values to match your MySQL setup
'host': 'localhost',
'database': 'trip_manager',
'user': 'trip_user',  # or 'root'
'password': 'your_password'
```

## ▶️ Running the Application

### Method 1: From Project Root
```bash
# Navigate to project root directory
cd c:\Users\Utente\Documents\scola\Info\progetto\Info_Project_1

# Run the application
python -m PythonExpenseApp.main
```

### Method 2: Direct Execution
```bash
# Navigate to the PythonExpenseApp directory
cd PythonExpenseApp

# Run main.py directly
python main.py
```

### Method 3: IDE Integration
- **PyCharm**: Open the project folder and run `main.py`
- **VS Code**: Open the project folder and run `python -m PythonExpenseApp.main` in terminal
- **IDLE**: Open `main.py` and press F5

## 📖 User Guide

### First Time Setup
1. **Start the Application**: Run using one of the methods above
2. **Database Check**: The app will verify database connectivity on startup
3. **Login**: Use the default credentials or create new student accounts

### Student Workflow
1. **Login**: Enter username and password
2. **Dashboard**: Access main features from the dashboard
3. **Activities**: Browse, subscribe to, and manage activities
4. **Expenses**: Add shared expenses and track debts
5. **Feedback**: Rate activities you've participated in

### Navigation
- **Back to Main**: All windows have a "Back to Main" button
- **Refresh**: Most lists have refresh functionality
- **Search**: Use search boxes to filter students/activities
- **Help**: Tooltips and error messages provide guidance

## 🏗️ Program Structure

### Core Architecture

```
PythonExpenseApp/
├── main.py                 # Application entry point and main dashboard
├── db_connection.py        # Database connectivity and query execution
├── student.py             # Student class and database operations
├── activity.py            # Activity class and management
├── expense.py             # Expense tracking and debt calculation
├── feedback.py            # Feedback system with validation
├── statistics.py          # Analytics and sentiment analysis
├── daily_program.py       # Schedule management
└── gui/                   # User interface components
    ├── login_gui.py       # Login and authentication
    ├── expense_gui.py     # Expense management interface
    ├── activity_form_gui.py # Activity subscription interface
    └── activity_details_gui.py # Detailed activity information
```

### Class Hierarchy and Relationships

#### 1. **Student Class** (`student.py`)
```python
class Student:
    # Core attributes
    - id, name, surname, age, username, class_
    - selected_activities[], total_expenses, fee_share, balance
    
    # Key methods
    + authenticate(username, password)        # Static login method
    + get_participated_activities()           # Activities student joined
    + has_participated_in_activity(id)       # Participation check
    + can_leave_feedback_for_activity(id)    # Feedback eligibility
    + save_to_database() / update_in_database()
```

#### 2. **Activity Class** (`activity.py`)
```python
class Activity:
    # Core attributes
    - id, name, day, start, finish, location
    - maxpart, duration, description
    - participants[], activity_feedback[]
    
    # Key methods
    + get_current_participants()              # Live participant count
    + get_participant_list()                  # List of enrolled students
    + can_student_leave_feedback(student_id)  # Feedback validation
    + get_feedback_statistics()               # Participation vs feedback
    + get_sentiment_words() / get_sentiment_summary()
```

#### 3. **Expense Class** (`expense.py`)
```python
class Expense:
    # Core attributes
    - id, amount, description, date
    - id_giver, id_receiver, id_activity
    
    # Key methods
    + calculate_split(participants)           # Equal/custom splitting
    + create_debt_records()                   # Generate debt entries
    + save_to_database()
```

#### 4. **Feedback Class** (`feedback.py`)
```python
class Feedback:
    # Core attributes
    - id, student_id, activity_id
    - rating (1-5), comment, created_at
    
    # Key methods
    + can_student_leave_feedback(s_id, a_id) # Static validation
    + validate_before_save()                  # Participation check
    + save_to_database()                      # With validation
    + get_feedback_sentiment_analysis(a_id)  # Analytics
```

#### 5. **Statistics Class** (`statistics.py`)
```python
class Statistics:
    # Analytics capabilities
    + fetch_statistics_from_database()       # Comprehensive stats
    + extract_and_analyze_sentiment_words()  # NLP processing
    + get_sentiment_words_for_activity()     # Word frequency
    + get_activity_sentiment_summary()       # Positive/negative/neutral
```

### GUI Architecture

#### 1. **Main Dashboard** (`main.py`)
- **Purpose**: Central navigation hub
- **Features**: Quick actions, today's schedule, user info
- **Navigation**: Launches Expense GUI and Activity GUI

#### 2. **Login System** (`gui/login_gui.py`)
- **Purpose**: Secure authentication
- **Features**: Username/password validation, error handling
- **Security**: Password verification against database

#### 3. **Expense Management** (`gui/expense_gui.py`)
- **Purpose**: Comprehensive expense tracking
- **Features**: 
  - Multi-participant expense creation
  - Debt tracking and visualization
  - Search and filter capabilities
  - Real-time debt calculations

#### 4. **Activity Management** (`gui/activity_form_gui.py`)
- **Purpose**: Activity browsing and subscription
- **Features**:
  - Activity list with availability status
  - Subscription management
  - Schedule conflict detection
  - Activity details integration

#### 5. **Activity Details** (`gui/activity_details_gui.py`)
- **Purpose**: Comprehensive activity information
- **Features**:
  - Participant lists and statistics
  - Feedback collection (with validation)
  - Sentiment analysis visualization
  - Rating distributions

### Database Integration

#### Connection Management (`db_connection.py`)
```python
class DbConnection:
    + connect()                               # Establish connection
    + execute_query(query, params, fetch_*)   # Safe query execution
    + close_connection()                      # Resource cleanup
```

#### Key Database Operations
- **Parameterized Queries**: Prevents SQL injection
- **Transaction Support**: Ensures data consistency
- **Error Handling**: Comprehensive exception management
- **Connection Pooling**: Efficient resource usage

### Data Flow and Relationships

```
User Login → Student Authentication → Main Dashboard
    ↓
Dashboard → [Expense GUI | Activity GUI]
    ↓
Expense GUI → Student Selection → Expense Creation → Debt Calculation
Activity GUI → Activity List → Subscription → Feedback (if participated)
    ↓
All Operations → Database Updates → Statistics Refresh → UI Updates
```

### Security and Validation

#### Input Validation
- **SQL Injection Prevention**: Parameterized queries only
- **Data Type Validation**: Amount, rating, date validation
- **Business Logic Validation**: Participation requirements for feedback

#### Business Rules
1. **Activity Subscription**: 
   - No time conflicts allowed
   - Capacity limits enforced
   - No duplicate subscriptions

2. **Feedback System**:
   - Only participants can leave feedback
   - One feedback per student per activity
   - Rating must be 1-5 stars

3. **Expense Management**:
   - Positive amounts only
   - Valid participant selection required
   - Equal split calculations

### Advanced Features

#### Sentiment Analysis Pipeline
1. **Text Processing**: Extract meaningful words from comments
2. **Sentiment Classification**: Positive/negative/neutral categorization
3. **Frequency Analysis**: Most common sentiment words
4. **Statistical Aggregation**: Overall sentiment scores per activity

#### Real-time Updates
- **Live Participant Counts**: Activity capacity tracking
- **Dynamic Debt Calculations**: Real-time debt updates
- **Automatic Statistics**: Sentiment analysis triggers

## 🗃️ Database Schema

### Core Tables
- `students`: User accounts and profiles
- `activities`: Trip activities and schedules
- `student_activities`: Enrollment relationships
- `expenses`: Financial transactions
- `debts`: Individual debt records
- `feedback`: Student ratings and comments

### Analytics Tables
- `activity_ratings`: Aggregated rating statistics
- `sentiment_words`: Processed sentiment analysis data

## 🔧 Troubleshooting

### Common Issues

#### Database Connection Errors
```
Error: Can't connect to MySQL server
Solution: 
1. Verify MySQL service is running
2. Check credentials in db_connection.py
3. Ensure database 'trip_manager' exists
```

#### Import Errors
```
Error: ModuleNotFoundError: No module named 'PythonExpenseApp'
Solution: 
1. Run from project root directory
2. Use: python -m PythonExpenseApp.main
3. Check virtual environment activation
```

#### GUI Display Issues
```
Error: tkinter module not found
Solution: 
1. Reinstall Python with tkinter
2. On Linux: sudo apt-get install python3-tk
3. On macOS: Use Python from python.org
```

### Performance Optimization
- **Database Indexing**: Ensure proper indexes on foreign keys
- **Connection Pooling**: Reuse database connections
- **Lazy Loading**: Load data only when needed

## 🤝 Contributing

### Development Setup
1. Fork the repository
2. Create feature branch: `git checkout -b feature-name`
3. Make changes and test thoroughly
4. Submit pull request with detailed description

### Code Style
- Follow PEP 8 for Python code
- Use descriptive variable and method names
- Add docstrings to all classes and methods
- Include error handling for all database operations

### Testing
- Test all GUI components thoroughly
- Verify database operations work correctly
- Check edge cases and error conditions
- Test with different user scenarios

---

**For additional support or questions, please refer to the code comments or create an issue in the repository.**
