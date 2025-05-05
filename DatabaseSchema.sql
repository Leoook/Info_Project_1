-- Table for students
CREATE TABLE students (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    surname VARCHAR(255),
    age INT,
    special_needs TEXT,
    total_expenses DECIMAL(10, 2),
    fee_share DECIMAL(10, 2),
    balance DECIMAL(10, 2)
);

-- Table for activities
CREATE TABLE activities (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    max_participants INT,
    location VARCHAR(255),
    duration INT,
    start_time INT,
    finish_time INT
);

-- Table for groups
CREATE TABLE groups (
    id INT AUTO_INCREMENT PRIMARY KEY,
    common_activity VARCHAR(255),
    dietary_needs TEXT
);

-- Table for group members (relationship between groups and students)
CREATE TABLE group_members (
    group_id INT,
    student_id INT,
    PRIMARY KEY (group_id, student_id),
    FOREIGN KEY (group_id) REFERENCES groups(id),
    FOREIGN KEY (student_id) REFERENCES students(id)
);

-- Table for expenses
CREATE TABLE expenses (
    id INT AUTO_INCREMENT PRIMARY KEY,
    total INT,
    description TEXT,
    id_giver INT,
    id_receiver INT,
    id_activity INT,
    FOREIGN KEY (id_giver) REFERENCES students(id),
    FOREIGN KEY (id_receiver) REFERENCES students(id),
    FOREIGN KEY (id_activity) REFERENCES activities(id)
);

-- Table for feedback
CREATE TABLE feedback (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT,
    activity_id INT,
    rating INT CHECK (rating BETWEEN 1 AND 5),
    comment TEXT,
    FOREIGN KEY (student_id) REFERENCES students(id),
    FOREIGN KEY (activity_id) REFERENCES activities(id)
);

-- Table for daily program
CREATE TABLE daily_program (
    id INT AUTO_INCREMENT PRIMARY KEY,
    day DATE,
    activity_id INT,
    FOREIGN KEY (activity_id) REFERENCES activities(id)
);

-- Join table for students and activities (many-to-many relationship)
CREATE TABLE student_activities (
    student_id INT,
    activity_id INT,
    PRIMARY KEY (student_id, activity_id),
    FOREIGN KEY (student_id) REFERENCES students(id),
    FOREIGN KEY (activity_id) REFERENCES activities(id)
);
