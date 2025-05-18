-- Drop tables if they exist (for clean import)
DROP TABLE IF EXISTS feedback;
DROP TABLE IF EXISTS student_activities;
DROP TABLE IF EXISTS expenses;
DROP TABLE IF EXISTS daily_program;
DROP TABLE IF EXISTS groups;
DROP TABLE IF EXISTS students;
DROP TABLE IF EXISTS activities;

-- Students table
CREATE TABLE students (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    surname VARCHAR(50) NOT NULL,
    class VARCHAR(20) NOT NULL,
    age INT,
    special_needs VARCHAR(255),
    total_expenses DECIMAL(10,2) DEFAULT 0,
    fee_share DECIMAL(10,2) DEFAULT 0,
    balance DECIMAL(10,2) DEFAULT 0
);

-- Activities table
CREATE TABLE activities (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    max_participants INT NOT NULL,
    location VARCHAR(100),
    duration INT,
    start_time INT,
    finish_time INT
);

-- Student-Activities join table
CREATE TABLE student_activities (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    activity_id INT NOT NULL,
    FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE,
    FOREIGN KEY (activity_id) REFERENCES activities(id) ON DELETE CASCADE
);

-- Expenses table
CREATE TABLE expenses (
    id INT AUTO_INCREMENT PRIMARY KEY,
    amount DECIMAL(10,2) NOT NULL,
    description VARCHAR(255),
    date DATE,
    id_giver INT,
    id_receiver INT,
    id_activity INT,
    FOREIGN KEY (id_giver) REFERENCES students(id) ON DELETE SET NULL,
    FOREIGN KEY (id_receiver) REFERENCES students(id) ON DELETE SET NULL,
    FOREIGN KEY (id_activity) REFERENCES activities(id) ON DELETE SET NULL
);

-- Groups table
CREATE TABLE groups (
    id INT AUTO_INCREMENT PRIMARY KEY,
    common_activity VARCHAR(100),
    dietary_needs VARCHAR(255)
);

-- Daily Program table
CREATE TABLE daily_program (
    id INT AUTO_INCREMENT PRIMARY KEY,
    day DATE,
    activity_id INT,
    FOREIGN KEY (activity_id) REFERENCES activities(id) ON DELETE CASCADE
);

-- Feedback table
CREATE TABLE feedback (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT,
    activity_id INT,
    rating INT,
    comment VARCHAR(255),
    FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE,
    FOREIGN KEY (activity_id) REFERENCES activities(id) ON DELETE CASCADE
);

-- Example data for students
INSERT INTO students (name, surname, class, age, special_needs, total_expenses, fee_share, balance) VALUES
('Alice', 'Rossi', '3A', 16, '', 50.00, 25.00, 25.00),
('Bob', 'Bianchi', '3B', 17, 'Gluten Free', 30.00, 15.00, 15.00),
('Carla', 'Verdi', '3A', 16, '', 40.00, 20.00, 20.00);

-- Example data for activities
INSERT INTO activities (name, max_participants, location, duration, start_time, finish_time) VALUES
('Basketball', 10, 'Gym', 60, 9, 10),
('Painting', 8, 'Art Room', 90, 11, 12),
('Music', 12, 'Music Hall', 45, 13, 14);

-- Example data for student_activities
INSERT INTO student_activities (student_id, activity_id) VALUES
(1, 1),
(2, 2),
(3, 1),
(1, 3);

-- Example data for expenses
INSERT INTO expenses (amount, description, date, id_giver, id_receiver, id_activity) VALUES
(20.00, 'Basketballs', '2024-06-01', 1, NULL, 1),
(15.00, 'Paints', '2024-06-02', 2, NULL, 2),
(10.00, 'Sheet Music', '2024-06-03', 3, NULL, 3);

-- Example data for groups
INSERT INTO groups (common_activity, dietary_needs) VALUES
('Basketball', ''),
('Painting', 'Gluten Free');

-- Example data for daily_program
INSERT INTO daily_program (day, activity_id) VALUES
('2024-06-10', 1),
('2024-06-10', 2),
('2024-06-11', 3);

-- Example data for feedback
INSERT INTO feedback (student_id, activity_id, rating, comment) VALUES
(1, 1, 5, 'Great activity!'),
(2, 2, 4, 'Fun but tiring.'),
(3, 1, 3, 'Could be better organized.');
