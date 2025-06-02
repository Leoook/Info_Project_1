-- Trip Manager Database Schema
-- MySQL Database Setup

-- Create database if it doesn't exist
CREATE DATABASE IF NOT EXISTS project;
USE project;

-- Set character set for better Unicode support
SET NAMES utf8mb4;
SET CHARACTER SET utf8mb4;

-- Drop tables in correct order (foreign keys first)
DROP TABLE IF EXISTS group_members;
DROP TABLE IF EXISTS groups;
DROP TABLE IF EXISTS feedback;
DROP TABLE IF EXISTS debts;
DROP TABLE IF EXISTS student_activities;
DROP TABLE IF EXISTS expenses;
DROP TABLE IF EXISTS activities;
DROP TABLE IF EXISTS students;

-- =====================================================
-- STUDENTS TABLE
-- =====================================================
CREATE TABLE students (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    surname VARCHAR(100) NOT NULL,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    class VARCHAR(20),
    age INT,
    special_needs TEXT,
    total_expenses DECIMAL(10,2) DEFAULT 0.00,
    fee_share DECIMAL(10,2) DEFAULT 0.00,
    balance DECIMAL(10,2) DEFAULT 0.00,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    INDEX idx_username (username),
    INDEX idx_class (class),
    INDEX idx_name_surname (surname, name)
) ENGINE=InnoDB CHARACTER SET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =====================================================
-- ACTIVITIES TABLE
-- =====================================================
CREATE TABLE activities (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    day DATE NOT NULL,
    start_time INT NOT NULL COMMENT 'Hour in 24h format (0-23)',
    finish_time INT NOT NULL COMMENT 'Hour in 24h format (0-23)',
    location VARCHAR(200) NOT NULL,
    max_participants INT DEFAULT NULL COMMENT 'NULL means unlimited',
    duration INT COMMENT 'Duration in hours',
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    INDEX idx_day (day),
    INDEX idx_time (day, start_time),
    INDEX idx_location (location),
    
    CONSTRAINT chk_time_valid CHECK (start_time >= 0 AND start_time <= 23 AND finish_time >= 0 AND finish_time <= 23),
    CONSTRAINT chk_time_order CHECK (finish_time > start_time OR (finish_time < start_time AND finish_time < 6))
) ENGINE=InnoDB CHARACTER SET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =====================================================
-- STUDENT_ACTIVITIES TABLE (Many-to-Many relationship)
-- =====================================================
CREATE TABLE student_activities (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    activity_id INT NOT NULL,
    registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE,
    FOREIGN KEY (activity_id) REFERENCES activities(id) ON DELETE CASCADE,
    
    UNIQUE KEY unique_student_activity (student_id, activity_id),
    INDEX idx_student (student_id),
    INDEX idx_activity (activity_id)
) ENGINE=InnoDB CHARACTER SET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =====================================================
-- EXPENSES TABLE
-- =====================================================
CREATE TABLE expenses (
    id INT AUTO_INCREMENT PRIMARY KEY,
    amount DECIMAL(10,2) NOT NULL,
    description TEXT NOT NULL,
    date DATE NOT NULL,
    id_giver INT COMMENT 'Student who paid the expense',
    id_receiver INT COMMENT 'Student who received (optional)',
    id_activity INT COMMENT 'Related activity (optional)',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (id_giver) REFERENCES students(id) ON DELETE SET NULL,
    FOREIGN KEY (id_receiver) REFERENCES students(id) ON DELETE SET NULL,
    FOREIGN KEY (id_activity) REFERENCES activities(id) ON DELETE SET NULL,
    
    INDEX idx_date (date),
    INDEX idx_giver (id_giver),
    INDEX idx_amount (amount),
    
    CONSTRAINT chk_amount_positive CHECK (amount > 0)
) ENGINE=InnoDB CHARACTER SET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =====================================================
-- DEBTS TABLE (Tracks who owes money to whom)
-- =====================================================
CREATE TABLE debts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    payer_id INT NOT NULL COMMENT 'Student who paid initially',
    debtor_id INT NOT NULL COMMENT 'Student who owes money',
    amount DECIMAL(10,2) NOT NULL,
    description TEXT,
    expense_id INT COMMENT 'Related expense',
    paid BOOLEAN DEFAULT FALSE,
    date_created DATE NOT NULL,
    date_paid DATE DEFAULT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (payer_id) REFERENCES students(id) ON DELETE CASCADE,
    FOREIGN KEY (debtor_id) REFERENCES students(id) ON DELETE CASCADE,
    FOREIGN KEY (expense_id) REFERENCES expenses(id) ON DELETE CASCADE,
    
    INDEX idx_payer (payer_id),
    INDEX idx_debtor (debtor_id),
    INDEX idx_paid (paid),
    INDEX idx_date_created (date_created),
    
    CONSTRAINT chk_debt_amount_positive CHECK (amount > 0),
    CONSTRAINT chk_different_payer_debtor CHECK (payer_id != debtor_id)
) ENGINE=InnoDB CHARACTER SET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =====================================================
-- FEEDBACK TABLE
-- =====================================================
CREATE TABLE feedback (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    activity_id INT NOT NULL,
    rating INT NOT NULL,
    comment TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE,
    FOREIGN KEY (activity_id) REFERENCES activities(id) ON DELETE CASCADE,
    
    INDEX idx_student (student_id),
    INDEX idx_activity (activity_id),
    INDEX idx_rating (rating),
    
    CONSTRAINT chk_rating_range CHECK (rating >= 1 AND rating <= 5),
    UNIQUE KEY unique_student_activity_feedback (student_id, activity_id)
) ENGINE=InnoDB CHARACTER SET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =====================================================
-- GROUPS TABLE (For organizing students)
-- =====================================================
CREATE TABLE groups (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    common_activity VARCHAR(200),
    dietary_needs TEXT,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    INDEX idx_name (name),
    INDEX idx_common_activity (common_activity)
) ENGINE=InnoDB CHARACTER SET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =====================================================
-- GROUP_MEMBERS TABLE (Many-to-Many for Groups and Students)
-- =====================================================
CREATE TABLE group_members (
    id INT AUTO_INCREMENT PRIMARY KEY,
    group_id INT NOT NULL,
    student_id INT NOT NULL,
    joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    role VARCHAR(50) DEFAULT 'member',
    
    FOREIGN KEY (group_id) REFERENCES groups(id) ON DELETE CASCADE,
    FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE,
    
    UNIQUE KEY unique_group_member (group_id, student_id),
    INDEX idx_group (group_id),
    INDEX idx_student_member (student_id)
) ENGINE=InnoDB CHARACTER SET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =====================================================
-- ACTIVITY RATINGS TABLE (for detailed rating breakdown)
-- =====================================================
CREATE TABLE IF NOT EXISTS activity_ratings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    activity_id INT NOT NULL,
    average_rating DECIMAL(3,2) DEFAULT 0.00,
    median_rating DECIMAL(3,2) DEFAULT 0.00,
    total_ratings INT DEFAULT 0,
    rating_1_count INT DEFAULT 0,
    rating_2_count INT DEFAULT 0,
    rating_3_count INT DEFAULT 0,
    rating_4_count INT DEFAULT 0,
    rating_5_count INT DEFAULT 0,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (activity_id) REFERENCES activities(id) ON DELETE CASCADE,
    UNIQUE KEY unique_activity_rating (activity_id),
    INDEX idx_average_rating (average_rating),
    INDEX idx_median_rating (median_rating)
) ENGINE=InnoDB CHARACTER SET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =====================================================
-- SENTIMENT WORDS TABLE (for tracking common sentiment words)
-- =====================================================
CREATE TABLE IF NOT EXISTS sentiment_words (
    id INT AUTO_INCREMENT PRIMARY KEY,
    activity_id INT NOT NULL,
    word VARCHAR(100) NOT NULL,
    frequency INT DEFAULT 1,
    sentiment_type ENUM('positive', 'negative', 'neutral') DEFAULT 'neutral',
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (activity_id) REFERENCES activities(id) ON DELETE CASCADE,
    INDEX idx_activity_word (activity_id, word),
    INDEX idx_frequency (frequency),
    INDEX idx_sentiment (sentiment_type)
) ENGINE=InnoDB CHARACTER SET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =====================================================
-- SAMPLE DATA INSERTION
-- =====================================================

-- Insert sample students
INSERT INTO students (name, surname, username, password, class, age, special_needs) VALUES
('Mario', 'Rossi', 'mario.rossi', 'rossi18', '5A', 18, ''),
('Giulia', 'Bianchi', 'giulia.bianchi', 'bianchi17', '5A', 17, 'Vegetarian'),
('Luca', 'Verdi', 'luca.verdi', 'verdi18', '5B', 18, ''),
('Sara', 'Neri', 'sara.neri', 'neri17', '5B', 17, 'Lactose intolerant'),
('Andrea', 'Ferrari', 'andrea.ferrari', 'ferrari19', '5A', 19, ''),
('Chiara', 'Romano', 'chiara.romano', 'romano17', '5C', 17, ''),
('Marco', 'Ricci', 'marco.ricci', 'ricci18', '5C', 18, 'Gluten free'),
('Elena', 'Marino', 'elena.marino', 'marino17', '5A', 17, ''),
('Francesco', 'Greco', 'francesco.greco', 'greco18', '5B', 18, ''),
('Anna', 'Bruno', 'anna.bruno', 'bruno17', '5C', 17, 'Vegan');

-- Insert sample activities
INSERT INTO activities (name, day, start_time, finish_time, location, max_participants, duration, description) VALUES
('City Walking Tour', '2025-03-15', 9, 12, 'Historic Center', 25, 3, 'Guided tour of the historic city center'),
('Museum Visit', '2025-03-15', 14, 17, 'National Museum', 20, 3, 'Educational visit to the national museum'),
('Beach Activities', '2025-03-16', 10, 16, 'Seaside Beach', 30, 6, 'Beach games and water sports'),
('Cooking Class', '2025-03-16', 18, 21, 'Local Restaurant', 15, 3, 'Traditional cooking workshop'),
('Mountain Hiking', '2025-03-17', 8, 15, 'Mountain Trail', 20, 7, 'Hiking expedition in the mountains'),
('Art Workshop', '2025-03-17', 16, 19, 'Art Studio', 12, 3, 'Creative art and painting session'),
('Cultural Show', '2025-03-18', 20, 22, 'City Theater', 50, 2, 'Traditional music and dance performance'),
('Shopping Tour', '2025-03-19', 10, 13, 'Shopping District', NULL, 3, 'Free shopping time in the main district'),
('Boat Trip', '2025-03-19', 15, 18, 'Harbor Marina', 25, 3, 'Scenic boat tour around the coast'),
('Farewell Dinner', '2025-03-20', 19, 22, 'Grand Hotel', NULL, 3, 'Final dinner and celebration');

-- Insert sample student activity registrations
INSERT INTO student_activities (student_id, activity_id) VALUES
(1, 1), (1, 3), (1, 5), (1, 7), (1, 10),
(2, 1), (2, 2), (2, 4), (2, 6), (2, 10),
(3, 1), (3, 3), (3, 5), (3, 8), (3, 9),
(4, 2), (4, 4), (4, 6), (4, 7), (4, 10),
(5, 1), (5, 3), (5, 5), (5, 8), (5, 9),
(6, 2), (6, 4), (6, 6), (6, 7), (6, 10),
(7, 1), (7, 2), (7, 4), (7, 6), (7, 10),
(8, 1), (8, 3), (8, 6), (8, 9), (8, 10),
(9, 3), (9, 5), (9, 8), (9, 9), (9, 10),
(10, 2), (10, 4), (10, 6), (10, 7), (10, 10);

-- Insert sample expenses
INSERT INTO expenses (amount, description, date, id_giver, id_activity) VALUES
(150.00, 'Bus transportation to museum', '2025-03-15', 1, 2),
(200.00, 'Beach equipment rental', '2025-03-16', 3, 3),
(80.00, 'Cooking class ingredients', '2025-03-16', 2, 4),
(120.00, 'Mountain hiking guide', '2025-03-17', 5, 5),
(50.00, 'Art supplies for workshop', '2025-03-17', 6, 6),
(300.00, 'Boat trip charter', '2025-03-19', 9, 9),
(25.00, 'Emergency first aid kit', '2025-03-15', 7, NULL),
(60.00, 'Group lunch at beach', '2025-03-16', 4, 3);

-- Insert sample debts
INSERT INTO debts (payer_id, debtor_id, amount, description, expense_id, date_created) VALUES
(1, 2, 30.00, 'Share of bus transportation', 1, '2025-03-15'),
(1, 4, 30.00, 'Share of bus transportation', 1, '2025-03-15'),
(1, 7, 30.00, 'Share of bus transportation', 1, '2025-03-15'),
(1, 10, 30.00, 'Share of bus transportation', 1, '2025-03-15'),
(3, 1, 40.00, 'Share of beach equipment', 2, '2025-03-16'),
(3, 5, 40.00, 'Share of beach equipment', 2, '2025-03-16'),
(3, 8, 40.00, 'Share of beach equipment', 2, '2025-03-16'),
(3, 9, 40.00, 'Share of beach equipment', 2, '2025-03-16'),
(2, 4, 20.00, 'Share of cooking ingredients', 3, '2025-03-16'),
(2, 6, 20.00, 'Share of cooking ingredients', 3, '2025-03-16'),
(2, 7, 20.00, 'Share of cooking ingredients', 3, '2025-03-16'),
(2, 10, 20.00, 'Share of cooking ingredients', 3, '2025-03-16');

-- Insert sample feedback
INSERT INTO feedback (student_id, activity_id, rating, comment) VALUES
(1, 1, 5, 'Excellent walking tour! Very informative guide.'),
(2, 2, 4, 'Museum was interesting but a bit crowded.'),
(3, 3, 5, 'Amazing beach day! Perfect weather and fun activities.'),
(4, 4, 5, 'Loved the cooking class! Learned so much about local cuisine.'),
(5, 5, 4, 'Challenging hike but beautiful views at the top.'),
(6, 6, 5, 'Very creative workshop, enjoyed expressing myself through art.'),
(1, 3, 4, 'Beach was great, would have preferred more water sports.'),
(2, 4, 5, 'Cooking class was the highlight of my trip!'),
(7, 2, 3, 'Museum was okay, some exhibits were outdated.'),
(8, 6, 5, 'Art workshop was fantastic, great instructor!');

-- Insert sample groups
INSERT INTO groups (name, common_activity, dietary_needs, description) VALUES
('Beach Lovers', 'Beach Activities', 'No specific needs', 'Students who love beach and water activities'),
('Culture Enthusiasts', 'Museum Visit', 'Various', 'Students interested in cultural experiences'),
('Adventure Seekers', 'Mountain Hiking', 'High energy meals', 'Students who enjoy outdoor adventures'),
('Food Explorers', 'Cooking Class', 'Various dietary restrictions', 'Students interested in culinary experiences');

-- Insert sample group members
INSERT INTO group_members (group_id, student_id, role) VALUES
(1, 1, 'leader'), (1, 3, 'member'), (1, 5, 'member'), (1, 8, 'member'), (1, 9, 'member'),
(2, 2, 'leader'), (2, 4, 'member'), (2, 6, 'member'), (2, 7, 'member'), (2, 10, 'member'),
(3, 5, 'leader'), (3, 1, 'member'), (3, 3, 'member'), (3, 9, 'member'),
(4, 2, 'leader'), (4, 4, 'member'), (4, 6, 'member'), (4, 7, 'member'), (4, 10, 'member');

-- =====================================================
-- USEFUL VIEWS FOR REPORTING
-- =====================================================

-- View for activity participation summary
CREATE VIEW activity_participation_summary AS
SELECT 
    a.id,
    a.name,
    a.day,
    a.location,
    a.max_participants,
    COUNT(sa.student_id) as current_participants,
    CASE 
        WHEN a.max_participants IS NULL THEN 'Unlimited'
        WHEN COUNT(sa.student_id) >= a.max_participants THEN 'Full'
        ELSE 'Available'
    END as status,
    ROUND(AVG(f.rating), 2) as avg_rating,
    COUNT(f.id) as feedback_count
FROM activities a
LEFT JOIN student_activities sa ON a.id = sa.activity_id
LEFT JOIN feedback f ON a.id = f.activity_id
GROUP BY a.id, a.name, a.day, a.location, a.max_participants;

-- View for student debt summary
CREATE VIEW student_debt_summary AS
SELECT 
    s.id,
    s.name,
    s.surname,
    COALESCE(owed_to.amount, 0) as money_owed_to_student,
    COALESCE(owes.amount, 0) as money_student_owes,
    (COALESCE(owed_to.amount, 0) - COALESCE(owes.amount, 0)) as net_balance
FROM students s
LEFT JOIN (
    SELECT payer_id, SUM(amount) as amount
    FROM debts 
    WHERE paid = FALSE 
    GROUP BY payer_id
) owed_to ON s.id = owed_to.payer_id
LEFT JOIN (
    SELECT debtor_id, SUM(amount) as amount
    FROM debts 
    WHERE paid = FALSE 
    GROUP BY debtor_id
) owes ON s.id = owes.debtor_id;

-- View for expense summary
CREATE VIEW expense_summary AS
SELECT 
    e.id,
    e.description,
    e.amount,
    e.date,
    giver.name as payer_name,
    giver.surname as payer_surname,
    a.name as activity_name,
    COUNT(d.id) as debt_count,
    SUM(CASE WHEN d.paid = FALSE THEN d.amount ELSE 0 END) as outstanding_amount
FROM expenses e
LEFT JOIN students giver ON e.id_giver = giver.id
LEFT JOIN activities a ON e.id_activity = a.id
LEFT JOIN debts d ON e.id = d.expense_id
GROUP BY e.id, e.description, e.amount, e.date, giver.name, giver.surname, a.name;

-- =====================================================
-- TRIGGERS FOR DATA INTEGRITY
-- =====================================================

DELIMITER //

-- Trigger to update student total expenses when an expense is added
CREATE TRIGGER update_student_expenses_after_insert
AFTER INSERT ON expenses
FOR EACH ROW
BEGIN
    IF NEW.id_giver IS NOT NULL THEN
        UPDATE students 
        SET total_expenses = total_expenses + NEW.amount 
        WHERE id = NEW.id_giver;
    END IF;
END //

-- Trigger to prevent registering for activities with time conflicts
CREATE TRIGGER check_activity_time_conflict
BEFORE INSERT ON student_activities
FOR EACH ROW
BEGIN
    DECLARE conflict_count INT DEFAULT 0;
    
    SELECT COUNT(*) INTO conflict_count
    FROM student_activities sa
    JOIN activities a1 ON sa.activity_id = a1.id
    JOIN activities a2 ON NEW.activity_id = a2.id
    WHERE sa.student_id = NEW.student_id
      AND a1.day = a2.day
      AND NOT (a1.finish_time <= a2.start_time OR a1.start_time >= a2.finish_time);
    
    IF conflict_count > 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Time conflict: Student already has an activity at this time';
    END IF;
END //

-- Trigger to validate feedback participation before insert
CREATE TRIGGER validate_feedback_participation_before_insert
BEFORE INSERT ON feedback
FOR EACH ROW
BEGIN
    DECLARE participation_count INT DEFAULT 0;
    
    -- Check if student participated in the activity
    SELECT COUNT(*) INTO participation_count
    FROM student_activities 
    WHERE student_id = NEW.student_id AND activity_id = NEW.activity_id;
    
    IF participation_count = 0 THEN
        SIGNAL SQLSTATE '45000' 
        SET MESSAGE_TEXT = 'Cannot leave feedback: Student must participate in activity first';
    END IF;
END //

-- Trigger to validate feedback participation before update
CREATE TRIGGER validate_feedback_participation_before_update
BEFORE UPDATE ON feedback
FOR EACH ROW
BEGIN
    DECLARE participation_count INT DEFAULT 0;
    
    -- Check if student participated in the activity (only if activity_id is being changed)
    IF NEW.activity_id != OLD.activity_id THEN
        SELECT COUNT(*) INTO participation_count
        FROM student_activities 
        WHERE student_id = NEW.student_id AND activity_id = NEW.activity_id;
        
        IF participation_count = 0 THEN
            SIGNAL SQLSTATE '45000' 
            SET MESSAGE_TEXT = 'Cannot update feedback: Student must participate in activity first';
        END IF;
    END IF;
END //

DELIMITER ;

-- =====================================================
-- INDEXES FOR PERFORMANCE
-- =====================================================

-- Additional indexes for better query performance
CREATE INDEX idx_debts_payer_unpaid ON debts(payer_id, paid);
CREATE INDEX idx_debts_debtor_unpaid ON debts(debtor_id, paid);
CREATE INDEX idx_expenses_date_giver ON expenses(date, id_giver);
CREATE INDEX idx_activities_day_time ON activities(day, start_time, finish_time);
CREATE INDEX idx_feedback_activity_rating ON feedback(activity_id, rating);

-- =====================================================
-- FINAL SETUP
-- =====================================================

-- Show table status
SELECT 
    TABLE_NAME as 'Table',
    TABLE_ROWS as 'Rows',
    ROUND(((DATA_LENGTH + INDEX_LENGTH) / 1024 / 1024), 2) as 'Size (MB)'
FROM information_schema.TABLES 
WHERE TABLE_SCHEMA = 'project'
ORDER BY TABLE_NAME;

-- Display success message
SELECT 'Database setup completed successfully!' as Status;

-- =====================================================
-- TRIGGERS FOR AUTOMATIC RATING UPDATES
-- =====================================================

DELIMITER //

-- Trigger to update activity ratings when feedback is added
CREATE TRIGGER update_activity_ratings_after_feedback_insert
AFTER INSERT ON feedback
FOR EACH ROW
BEGIN
    CALL UpdateActivityRatings(NEW.activity_id);
END //

-- Trigger to update activity ratings when feedback is updated
CREATE TRIGGER update_activity_ratings_after_feedback_update
AFTER UPDATE ON feedback
FOR EACH ROW
BEGIN
    CALL UpdateActivityRatings(NEW.activity_id);
END //

-- Trigger to update activity ratings when feedback is deleted
CREATE TRIGGER update_activity_ratings_after_feedback_delete
AFTER DELETE ON feedback
FOR EACH ROW
BEGIN
    CALL UpdateActivityRatings(OLD.activity_id);
END //

DELIMITER ;

-- =====================================================
-- STORED PROCEDURES FOR RATING CALCULATIONS
-- =====================================================

DELIMITER //

-- Procedure to calculate and update activity ratings
CREATE PROCEDURE UpdateActivityRatings(IN p_activity_id INT)
BEGIN
    DECLARE v_avg_rating DECIMAL(3,2) DEFAULT 0.00;
    DECLARE v_median_rating DECIMAL(3,2) DEFAULT 0.00;
    DECLARE v_total_ratings INT DEFAULT 0;
    DECLARE v_rating_1 INT DEFAULT 0;
    DECLARE v_rating_2 INT DEFAULT 0;
    DECLARE v_rating_3 INT DEFAULT 0;
    DECLARE v_rating_4 INT DEFAULT 0;
    DECLARE v_rating_5 INT DEFAULT 0;
    
    -- Calculate rating statistics
    SELECT 
        COALESCE(AVG(rating), 0),
        COUNT(*),
        SUM(CASE WHEN rating = 1 THEN 1 ELSE 0 END),
        SUM(CASE WHEN rating = 2 THEN 1 ELSE 0 END),
        SUM(CASE WHEN rating = 3 THEN 1 ELSE 0 END),
        SUM(CASE WHEN rating = 4 THEN 1 ELSE 0 END),
        SUM(CASE WHEN rating = 5 THEN 1 ELSE 0 END)
    INTO v_avg_rating, v_total_ratings, v_rating_1, v_rating_2, v_rating_3, v_rating_4, v_rating_5
    FROM feedback 
    WHERE activity_id = p_activity_id;
    
    -- Calculate median rating
    SELECT AVG(rating) INTO v_median_rating
    FROM (
        SELECT rating, ROW_NUMBER() OVER (ORDER BY rating) as row_num,
               COUNT(*) OVER () as total_count
        FROM feedback 
        WHERE activity_id = p_activity_id
    ) ranked
    WHERE row_num IN (FLOOR((total_count + 1) / 2), CEIL((total_count + 1) / 2));
    
    -- Insert or update activity ratings
    INSERT INTO activity_ratings (
        activity_id, average_rating, median_rating, total_ratings,
        rating_1_count, rating_2_count, rating_3_count, rating_4_count, rating_5_count
    ) VALUES (
        p_activity_id, v_avg_rating, COALESCE(v_median_rating, 0), v_total_ratings,
        v_rating_1, v_rating_2, v_rating_3, v_rating_4, v_rating_5
    )
    ON DUPLICATE KEY UPDATE
        average_rating = v_avg_rating,
        median_rating = COALESCE(v_median_rating, 0),
        total_ratings = v_total_ratings,
        rating_1_count = v_rating_1,
        rating_2_count = v_rating_2,
        rating_3_count = v_rating_3,
        rating_4_count = v_rating_4,
        rating_5_count = v_rating_5;
END //

-- Procedure to extract and update sentiment words from feedback
CREATE PROCEDURE UpdateSentimentWords(IN p_activity_id INT)
BEGIN
    DECLARE done INT DEFAULT FALSE;
    DECLARE v_comment TEXT;
    DECLARE word_cursor CURSOR FOR 
        SELECT comment FROM feedback WHERE activity_id = p_activity_id AND comment IS NOT NULL;
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;
    
    -- Clear existing sentiment words for this activity
    DELETE FROM sentiment_words WHERE activity_id = p_activity_id;
    
    OPEN word_cursor;
    read_loop: LOOP
        FETCH word_cursor INTO v_comment;
        IF done THEN
            LEAVE read_loop;
        END IF;
        
        -- Process comment (simplified word extraction)
        -- In a real implementation, you'd use more sophisticated text processing
        CALL ProcessCommentWords(p_activity_id, v_comment);
    END LOOP;
    
    CLOSE word_cursor;
END //

-- Simplified word processing procedure
CREATE PROCEDURE ProcessCommentWords(IN p_activity_id INT, IN p_comment TEXT)
BEGIN
    -- This is a simplified version. In production, you'd use more sophisticated text processing
    DECLARE v_word VARCHAR(100);
    DECLARE v_pos INT DEFAULT 1;
    DECLARE v_next_pos INT;
    DECLARE v_clean_comment TEXT;
    
    -- Clean comment (remove punctuation, convert to lowercase)
    SET v_clean_comment = LOWER(REPLACE(REPLACE(REPLACE(REPLACE(p_comment, '.', ' '), ',', ' '), '!', ' '), '?', ' '));
    
    -- Simple word extraction (split by spaces)
    WHILE v_pos <= LENGTH(v_clean_comment) DO
        SET v_next_pos = LOCATE(' ', v_clean_comment, v_pos);
        IF v_next_pos = 0 THEN
            SET v_next_pos = LENGTH(v_clean_comment) + 1;
        END IF;
        
        SET v_word = TRIM(SUBSTRING(v_clean_comment, v_pos, v_next_pos - v_pos));
        
        IF LENGTH(v_word) > 2 AND v_word NOT IN ('the', 'and', 'but', 'for', 'are', 'was', 'were', 'been', 'have', 'has', 'had', 'this', 'that', 'with', 'from') THEN
            INSERT INTO sentiment_words (activity_id, word, frequency, sentiment_type)
            VALUES (p_activity_id, v_word, 1, DetermineSentiment(v_word))
            ON DUPLICATE KEY UPDATE 
                frequency = frequency + 1;
        END IF;
        
        SET v_pos = v_next_pos + 1;
    END WHILE;
END //

-- Function to determine basic sentiment (simplified)
CREATE FUNCTION DetermineSentiment(word VARCHAR(100)) 
RETURNS ENUM('positive', 'negative', 'neutral')
READS SQL DATA
DETERMINISTIC
BEGIN
    -- Simplified sentiment analysis
    IF word IN ('excellent', 'amazing', 'fantastic', 'wonderful', 'great', 'awesome', 'perfect', 'beautiful', 'loved', 'enjoyable', 'fun', 'interesting', 'good', 'nice', 'pleasant', 'exciting') THEN
        RETURN 'positive';
    ELSEIF word IN ('terrible', 'awful', 'horrible', 'bad', 'worst', 'disappointing', 'boring', 'difficult', 'hard', 'challenging', 'poor', 'weak', 'unpleasant') THEN
        RETURN 'negative';
    ELSE
        RETURN 'neutral';
    END IF;
END //

DELIMITER ;

-- =====================================================
-- ENHANCED SENTIMENT ANALYSIS PROCEDURES
-- =====================================================

DELIMITER //

-- Enhanced procedure to process feedback and extract sentiment words
CREATE OR REPLACE PROCEDURE ProcessFeedbackSentiment(IN p_activity_id INT)
BEGIN
    DECLARE done INT DEFAULT FALSE;
    DECLARE v_comment TEXT;
    DECLARE v_word VARCHAR(100);
    DECLARE v_word_pos INT DEFAULT 1;
    DECLARE v_word_end INT;
    DECLARE v_clean_comment TEXT;
    DECLARE v_sentiment VARCHAR(20);
    
    DECLARE comment_cursor CURSOR FOR 
        SELECT comment FROM feedback 
        WHERE activity_id = p_activity_id AND comment IS NOT NULL AND TRIM(comment) != '';
    
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;
    
    -- Clear existing sentiment words for this activity
    DELETE FROM sentiment_words WHERE activity_id = p_activity_id;
    
    OPEN comment_cursor;
    
    process_comments: LOOP
        FETCH comment_cursor INTO v_comment;
        IF done THEN
            LEAVE process_comments;
        END IF;
        
        -- Clean the comment: lowercase, remove punctuation, normalize spaces
        SET v_clean_comment = LOWER(v_comment);
        SET v_clean_comment = REPLACE(v_clean_comment, '.', ' ');
        SET v_clean_comment = REPLACE(v_clean_comment, ',', ' ');
        SET v_clean_comment = REPLACE(v_clean_comment, '!', ' ');
        SET v_clean_comment = REPLACE(v_clean_comment, '?', ' ');
        SET v_clean_comment = REPLACE(v_clean_comment, ';', ' ');
        SET v_clean_comment = REPLACE(v_clean_comment, ':', ' ');
        SET v_clean_comment = REPLACE(v_clean_comment, '(', ' ');
        SET v_clean_comment = REPLACE(v_clean_comment, ')', ' ');
        SET v_clean_comment = REPLACE(v_clean_comment, '"', ' ');
        SET v_clean_comment = REPLACE(v_clean_comment, "'", ' ');
        SET v_clean_comment = REPLACE(v_clean_comment, '-', ' ');
        SET v_clean_comment = REPLACE(v_clean_comment, '_', ' ');
        
        -- Normalize multiple spaces to single space
        WHILE LOCATE('  ', v_clean_comment) > 0 DO
            SET v_clean_comment = REPLACE(v_clean_comment, '  ', ' ');
        END WHILE;
        
        SET v_clean_comment = TRIM(v_clean_comment);
        
        -- Extract words from the cleaned comment
        SET v_word_pos = 1;
        
        extract_words: WHILE v_word_pos <= LENGTH(v_clean_comment) DO
            SET v_word_end = LOCATE(' ', v_clean_comment, v_word_pos);
            
            IF v_word_end = 0 THEN
                SET v_word_end = LENGTH(v_clean_comment) + 1;
            END IF;
            
            SET v_word = TRIM(SUBSTRING(v_clean_comment, v_word_pos, v_word_end - v_word_pos));
            
            -- Process word if it's meaningful (length > 2 and not a stop word)
            IF LENGTH(v_word) > 2 AND v_word NOT IN (
                'the', 'and', 'but', 'for', 'are', 'was', 'were', 'been', 'have', 'has', 'had',
                'this', 'that', 'with', 'from', 'they', 'them', 'their', 'there', 'where',
                'when', 'what', 'who', 'how', 'why', 'which', 'will', 'would', 'could',
                'should', 'may', 'might', 'must', 'can', 'did', 'does', 'not', 'very',
                'too', 'also', 'just', 'only', 'even', 'much', 'more', 'most', 'than',
                'then', 'now', 'here', 'into', 'onto', 'upon', 'about', 'above', 'below',
                'under', 'over', 'through', 'during', 'before', 'after', 'while', 'since',
                'until', 'although', 'though', 'because', 'unless', 'whether', 'however',
                'therefore', 'thus', 'hence', 'moreover', 'furthermore', 'nevertheless',
                'nonetheless', 'otherwise', 'meanwhile', 'indeed', 'certainly', 'surely',
                'perhaps', 'maybe', 'probably', 'possibly', 'actually', 'really', 'truly',
                'definitely', 'absolutely', 'quite', 'rather', 'fairly', 'pretty',
                'somewhat', 'slightly', 'extremely'
            ) THEN
                -- Determine sentiment
                SET v_sentiment = GetWordSentiment(v_word);
                
                -- Insert or update word frequency
                INSERT INTO sentiment_words (activity_id, word, frequency, sentiment_type)
                VALUES (p_activity_id, v_word, 1, v_sentiment)
                ON DUPLICATE KEY UPDATE frequency = frequency + 1;
            END IF;
            
            SET v_word_pos = v_word_end + 1;
        END WHILE extract_words;
        
    END LOOP process_comments;
    
    CLOSE comment_cursor;
END //

-- Enhanced function to determine word sentiment
CREATE OR REPLACE FUNCTION GetWordSentiment(word VARCHAR(100)) 
RETURNS ENUM('positive', 'negative', 'neutral')
READS SQL DATA
DETERMINISTIC
BEGIN
    DECLARE word_lower VARCHAR(100);
    SET word_lower = LOWER(word);
    
    -- Positive words
    IF word_lower IN (
        'excellent', 'amazing', 'fantastic', 'wonderful', 'great', 'awesome', 'perfect',
        'beautiful', 'loved', 'enjoyable', 'fun', 'interesting', 'good', 'nice', 'pleasant',
        'exciting', 'brilliant', 'outstanding', 'superb', 'magnificent', 'marvelous',
        'incredible', 'spectacular', 'delightful', 'charming', 'lovely', 'attractive',
        'impressive', 'remarkable', 'exceptional', 'extraordinary', 'fabulous', 'gorgeous',
        'splendid', 'terrific', 'thrilling', 'stunning', 'breathtaking', 'captivating',
        'enchanting', 'fascinating', 'engaging', 'absorbing', 'entertaining', 'amusing',
        'hilarious', 'joyful', 'cheerful', 'happy', 'glad', 'pleased', 'satisfied',
        'content', 'comfortable', 'relaxed', 'peaceful', 'calm', 'serene', 'tranquil',
        'refreshing', 'energizing', 'invigorating', 'inspiring', 'motivating', 'uplifting',
        'encouraging', 'supportive', 'helpful', 'useful', 'valuable', 'worthwhile',
        'beneficial', 'rewarding', 'fulfilling', 'satisfying', 'successful', 'productive',
        'effective', 'efficient', 'smooth', 'easy', 'simple', 'clear', 'organized',
        'creative', 'innovative', 'unique', 'special', 'memorable', 'unforgettable'
    ) THEN
        RETURN 'positive';
    
    -- Negative words
    ELSEIF word_lower IN (
        'terrible', 'awful', 'horrible', 'bad', 'worst', 'disappointing', 'boring',
        'difficult', 'hard', 'challenging', 'poor', 'weak', 'unpleasant', 'disgusting',
        'revolting', 'repulsive', 'offensive', 'annoying', 'irritating', 'frustrating',
        'confusing', 'complicated', 'messy', 'disorganized', 'chaotic', 'stressful',
        'overwhelming', 'exhausting', 'tiring', 'draining', 'depressing', 'sad',
        'unhappy', 'miserable', 'upset', 'angry', 'furious', 'outraged', 'disgusted',
        'shocked', 'surprised', 'disappointed', 'failed', 'unsuccessful', 'ineffective',
        'useless', 'worthless', 'pointless', 'meaningless', 'empty', 'hollow', 'shallow',
        'superficial', 'fake', 'artificial', 'forced', 'uncomfortable', 'awkward',
        'embarrassing', 'humiliating', 'shameful', 'regrettable', 'unfortunate',
        'unlucky', 'hopeless', 'impossible', 'unrealistic', 'unreasonable', 'unfair',
        'unjust', 'wrong', 'incorrect', 'false', 'misleading', 'deceptive', 'dishonest'
    ) THEN
        RETURN 'negative';
    
    -- Neutral words
    ELSEIF word_lower IN (
        'okay', 'alright', 'fine', 'normal', 'average', 'typical', 'usual', 'standard',
        'regular', 'ordinary', 'common', 'general', 'basic', 'simple', 'plain',
        'moderate', 'medium', 'middle', 'central', 'balanced', 'neutral', 'stable',
        'steady', 'consistent', 'reliable', 'predictable', 'expected', 'appropriate',
        'suitable', 'adequate', 'sufficient', 'acceptable', 'reasonable', 'logical',
        'practical', 'realistic', 'possible', 'feasible', 'manageable', 'achievable',
        'accessible', 'available', 'present', 'existing', 'current', 'recent',
        'modern', 'contemporary', 'traditional', 'classic', 'conventional', 'formal'
    ) THEN
        RETURN 'neutral';
    
    -- Default to neutral for unknown words
    ELSE
        RETURN 'neutral';
    END IF;
END //

DELIMITER ;

-- =====================================================
-- VIEWS FOR SENTIMENT ANALYSIS
-- =====================================================

-- View for activity sentiment summary
CREATE OR REPLACE VIEW activity_sentiment_summary AS
SELECT 
    a.id as activity_id,
    a.name as activity_name,
    COALESCE(pos.word_count, 0) as positive_word_count,
    COALESCE(pos.frequency_sum, 0) as positive_frequency,
    COALESCE(neg.word_count, 0) as negative_word_count,
    COALESCE(neg.frequency_sum, 0) as negative_frequency,
    COALESCE(neu.word_count, 0) as neutral_word_count,
    COALESCE(neu.frequency_sum, 0) as neutral_frequency,
    COALESCE(total.total_words, 0) as total_sentiment_words,
    CASE 
        WHEN COALESCE(total.total_words, 0) > 0 THEN
            ROUND((COALESCE(pos.frequency_sum, 0) - COALESCE(neg.frequency_sum, 0)) / total.total_words * 100, 2)
        ELSE 0
    END as sentiment_score
FROM activities a
LEFT JOIN (
    SELECT activity_id, COUNT(*) as word_count, SUM(frequency) as frequency_sum
    FROM sentiment_words 
    WHERE sentiment_type = 'positive'
    GROUP BY activity_id
) pos ON a.id = pos.activity_id
LEFT JOIN (
    SELECT activity_id, COUNT(*) as word_count, SUM(frequency) as frequency_sum
    FROM sentiment_words 
    WHERE sentiment_type = 'negative'
    GROUP BY activity_id
) neg ON a.id = neg.activity_id
LEFT JOIN (
    SELECT activity_id, COUNT(*) as word_count, SUM(frequency) as frequency_sum
    FROM sentiment_words 
    WHERE sentiment_type = 'neutral'
    GROUP BY activity_id
) neu ON a.id = neu.activity_id
LEFT JOIN (
    SELECT activity_id, COUNT(*) as total_words
    FROM sentiment_words
    GROUP BY activity_id
) total ON a.id = total.activity_id;

-- Initialize sentiment analysis for existing feedback
DELIMITER //
CREATE OR REPLACE PROCEDURE InitializeAllSentimentAnalysis()
BEGIN
    DECLARE done INT DEFAULT FALSE;
    DECLARE v_activity_id INT;
    DECLARE activity_cursor CURSOR FOR 
        SELECT DISTINCT activity_id FROM feedback WHERE comment IS NOT NULL AND TRIM(comment) != '';
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;
    
    OPEN activity_cursor;
    sentiment_loop: LOOP
        FETCH activity_cursor INTO v_activity_id;
        IF done THEN
            LEAVE sentiment_loop;
        END IF;
        
        CALL ProcessFeedbackSentiment(v_activity_id);
    END LOOP;
    
    CLOSE activity_cursor;
END //
DELIMITER ;

-- Run initialization
CALL InitializeAllSentimentAnalysis();
