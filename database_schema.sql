-- ===================================================================
-- TRIP MANAGER DATABASE SCHEMA
-- ===================================================================
-- This file contains the complete database schema for the Trip Manager application.
-- The database stores information about students, activities, expenses, feedback, and analytics.
-- 
-- MAIN ENTITIES:
-- 1. students - User accounts and personal information
-- 2. activities - Trip activities with scheduling and capacity
-- 3. student_activities - Many-to-many relationship for activity enrollment
-- 4. expenses - Financial transactions between students
-- 5. debts - Individual debt records from expense splitting
-- 6. feedback - Student ratings and comments for activities
-- 7. sentiment_words - Analytics data for sentiment analysis
-- ===================================================================

-- Drop existing database if it exists (for clean installation)
DROP DATABASE IF EXISTS trip_manager;

-- Create the main database with UTF-8 support for international characters
CREATE DATABASE trip_manager 
CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;

-- Use the newly created database
USE trip_manager;

-- ===================================================================
-- STUDENTS TABLE - Central user management
-- ===================================================================
-- Purpose: Store all student information including login credentials and financial data
-- This is the central user table that connects to all other entities
CREATE TABLE students (
    -- Primary key: Unique identifier for each student
    id INT AUTO_INCREMENT PRIMARY KEY,
    
    -- Personal Information Fields
    name VARCHAR(100) NOT NULL COMMENT 'Student first name - required for identification',
    surname VARCHAR(100) NOT NULL COMMENT 'Student last name/family name - required for identification',
    age INT NOT NULL COMMENT 'Student age in years - used for age-appropriate activities',
    class VARCHAR(20) COMMENT 'Student class/grade designation - for organizing groups',
    special_needs TEXT COMMENT 'Any special dietary or accessibility requirements - important for trip planning',
    
    -- Authentication Credentials - Security Layer
    username VARCHAR(50) UNIQUE NOT NULL COMMENT 'Unique login username - must be unique across all students',
    password VARCHAR(255) NOT NULL COMMENT 'Login password - should be hashed in production for security',
    
    -- Financial Tracking Fields - Money Management
    total_expenses DECIMAL(10,2) DEFAULT 0.00 COMMENT 'Total amount student has spent - running total of all expenses',
    fee_share DECIMAL(10,2) DEFAULT 0.00 COMMENT 'Students share of overall trip fees - calculated portion of total costs',
    balance DECIMAL(10,2) DEFAULT 0.00 COMMENT 'Current balance (positive = owed money, negative = owes money)',
    
    -- Audit Fields - System tracking
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT 'When the student account was created - for record keeping',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT 'Last update time - automatic tracking'
) COMMENT 'Central table storing all student information, authentication data, and financial status';

-- ===================================================================
-- ACTIVITIES TABLE - Trip event management
-- ===================================================================
-- Purpose: Store all trip activities with scheduling and capacity information
-- Each activity represents a specific event during the trip with time/location constraints
CREATE TABLE activities (
    -- Primary key: Unique identifier for each activity
    id INT AUTO_INCREMENT PRIMARY KEY,
    
    -- Activity Identification and Description
    name VARCHAR(200) NOT NULL COMMENT 'Activity name/title - what students see when browsing',
    description TEXT COMMENT 'Detailed description of what the activity involves - helps students make informed choices',
    location VARCHAR(200) NOT NULL COMMENT 'Where the activity takes place - physical address or venue name',
    
    -- Scheduling Information - Time management
    day DATE NOT NULL COMMENT 'Date when the activity occurs - used for schedule conflict detection',
    start_time INT NOT NULL COMMENT 'Starting hour in 24-hour format (e.g., 14 for 2 PM) - simple integer for easy comparison',
    finish_time INT NOT NULL COMMENT 'Ending hour in 24-hour format - must be after start_time',
    duration INT COMMENT 'Activity duration in hours - optional field, can be calculated from start/finish',
    
    -- Capacity Management - Resource constraints
    max_participants INT DEFAULT NULL COMMENT 'Maximum number of participants (NULL = unlimited) - prevents overbooking',
    
    -- System tracking
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT 'When the activity was created - for audit purposes'
) COMMENT 'Table storing all trip activities with scheduling information and capacity constraints';

-- ===================================================================
-- STUDENT_ACTIVITIES TABLE - Enrollment relationship management
-- ===================================================================
-- Purpose: Track which students are enrolled in which activities (many-to-many relationship)
-- This junction table creates the connection between students and activities
CREATE TABLE student_activities (
    -- Primary key: Unique identifier for each enrollment record
    id INT AUTO_INCREMENT PRIMARY KEY,
    
    -- Foreign Key Relationships - Links to main entities
    student_id INT NOT NULL COMMENT 'Reference to students table - which student is enrolled',
    activity_id INT NOT NULL COMMENT 'Reference to activities table - which activity they joined',
    
    -- Enrollment Metadata
    registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT 'When the student registered - for tracking enrollment timing',
    
    -- Referential Integrity Constraints - Data consistency rules
    FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE COMMENT 'If student deleted, remove all their enrollments',
    FOREIGN KEY (activity_id) REFERENCES activities(id) ON DELETE CASCADE COMMENT 'If activity deleted, remove all enrollments',
    
    -- Business Logic Constraints
    UNIQUE KEY unique_student_activity (student_id, activity_id) COMMENT 'Prevent duplicate enrollments - one student per activity max'
) COMMENT 'Junction table managing student enrollment in activities - enables many-to-many relationship';

-- ===================================================================
-- EXPENSES TABLE - Financial transaction records
-- ===================================================================
-- Purpose: Record all financial transactions and shared expenses during the trip
-- Each record represents money spent that may need to be split among multiple people
CREATE TABLE expenses (
    -- Primary key: Unique identifier for each expense transaction
    id INT AUTO_INCREMENT PRIMARY KEY,
    
    -- Transaction Core Information
    amount DECIMAL(10,2) NOT NULL COMMENT 'Total amount spent in currency units - must be positive value',
    description TEXT NOT NULL COMMENT 'What the money was spent on - required for transparency and record keeping',
    date DATE NOT NULL COMMENT 'Date when the expense occurred - for chronological tracking',
    
    -- Participant Information - Who was involved in the transaction
    id_giver INT COMMENT 'Student who paid the money (reference to students table) - the person out of pocket',
    id_receiver INT COMMENT 'Student who received the money (NULL for shared expenses) - for direct transfers',
    id_activity INT COMMENT 'Activity this expense is related to (NULL if not activity-specific) - categorization',
    
    -- System tracking
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT 'When the expense record was created - audit trail',
    
    -- Referential Integrity with graceful handling
    FOREIGN KEY (id_giver) REFERENCES students(id) ON DELETE SET NULL COMMENT 'Preserve financial records even if student account deleted',
    FOREIGN KEY (id_receiver) REFERENCES students(id) ON DELETE SET NULL COMMENT 'Preserve financial records even if student account deleted',
    FOREIGN KEY (id_activity) REFERENCES activities(id) ON DELETE SET NULL COMMENT 'Preserve expense records even if activity deleted'
) COMMENT 'Table recording all expenses and financial transactions during the trip';

-- ===================================================================
-- DEBTS TABLE - Individual debt tracking from expense splitting
-- ===================================================================
-- Purpose: Track individual debt records created when expenses are split among multiple people
-- When a shared expense is recorded, individual debt records are created for each person who owes money
CREATE TABLE debts (
    -- Primary key: Unique identifier for each debt relationship
    id INT AUTO_INCREMENT PRIMARY KEY,
    
    -- Debt Relationship Participants
    payer_id INT NOT NULL COMMENT 'Student who paid and is owed money (creditor) - reference to students table',
    debtor_id INT NOT NULL COMMENT 'Student who owes money (debtor) - reference to students table',
    
    -- Debt Financial Details
    amount DECIMAL(10,2) NOT NULL COMMENT 'Amount owed in currency units - must be positive',
    description TEXT COMMENT 'Description of what this debt is for - usually matches original expense description',
    expense_id INT COMMENT 'Reference to the original expense that created this debt - traceability',
    
    -- Payment Status Tracking - Lifecycle management
    paid BOOLEAN DEFAULT FALSE COMMENT 'Whether this debt has been settled (TRUE = paid, FALSE = outstanding)',
    
    -- Important Date Tracking - Timeline management
    date_created DATE NOT NULL COMMENT 'Date when the debt was created - usually matches expense date',
    date_paid DATE DEFAULT NULL COMMENT 'Date when the debt was settled (NULL if still outstanding)',
    
    -- System Audit Fields
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT 'When the debt record was created in system',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT 'Last update time - tracks payment changes',
    
    -- Referential Integrity Constraints
    FOREIGN KEY (payer_id) REFERENCES students(id) ON DELETE CASCADE COMMENT 'If creditor account deleted, remove debt records',
    FOREIGN KEY (debtor_id) REFERENCES students(id) ON DELETE CASCADE COMMENT 'If debtor account deleted, remove debt records',
    FOREIGN KEY (expense_id) REFERENCES expenses(id) ON DELETE CASCADE COMMENT 'If original expense deleted, remove related debts'
) COMMENT 'Table tracking individual debts between students from shared expenses';

-- ===================================================================
-- FEEDBACK TABLE - Student activity ratings and comments
-- ===================================================================
-- Purpose: Store student feedback and ratings for activities they participated in
-- Only students who actually participated in an activity can leave feedback (enforced by business logic)
CREATE TABLE feedback (
    -- Primary key: Unique identifier for each feedback entry
    id INT AUTO_INCREMENT PRIMARY KEY,
    
    -- Reference Information - Links feedback to student and activity
    student_id INT NOT NULL COMMENT 'Student who left the feedback (reference to students table)',
    activity_id INT NOT NULL COMMENT 'Activity being rated (reference to activities table)',
    
    -- Feedback Content - The actual rating and comments
    rating INT NOT NULL COMMENT 'Numerical rating from 1-5 stars - standardized rating scale',
    comment TEXT COMMENT 'Optional written feedback from the student - qualitative assessment',
    
    -- Timestamp Information
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT 'When the feedback was submitted - for chronological ordering',
    
    -- Referential Integrity Constraints
    FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE COMMENT 'If student deleted, remove their feedback',
    FOREIGN KEY (activity_id) REFERENCES activities(id) ON DELETE CASCADE COMMENT 'If activity deleted, remove all feedback',
    
    -- Business Logic Constraints
    CHECK (rating >= 1 AND rating <= 5) COMMENT 'Ensure rating is within valid 1-5 star range',
    
    -- Prevent Duplicate Feedback
    UNIQUE KEY unique_student_feedback (student_id, activity_id) COMMENT 'Each student can only leave one feedback per activity'
) COMMENT 'Table storing student feedback and ratings for activities they participated in';

-- ===================================================================
-- SENTIMENT_WORDS TABLE - Analytics and text processing
-- ===================================================================
-- Purpose: Store processed sentiment analysis data from feedback comments
-- This table is populated automatically by the sentiment analysis system
CREATE TABLE sentiment_words (
    -- Primary key: Unique identifier for each sentiment word entry
    id INT AUTO_INCREMENT PRIMARY KEY,
    
    -- Reference Information - Links sentiment data to specific activity
    activity_id INT NOT NULL COMMENT 'Activity this sentiment data relates to (reference to activities table)',
    
    -- Sentiment Analysis Results - Natural Language Processing output
    word VARCHAR(100) NOT NULL COMMENT 'The actual word extracted from feedback comments - cleaned and processed',
    frequency INT NOT NULL DEFAULT 1 COMMENT 'How many times this word appeared in feedback for this activity',
    sentiment_type ENUM('positive', 'negative', 'neutral') NOT NULL COMMENT 'Categorization of words emotional sentiment',
    
    -- System Audit Fields
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT 'When this sentiment data was processed by the system',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT 'Last update time - tracks reprocessing',
    
    -- Referential Integrity
    FOREIGN KEY (activity_id) REFERENCES activities(id) ON DELETE CASCADE COMMENT 'If activity deleted, remove sentiment data',
    
    -- Prevent Duplicate Word Entries
    UNIQUE KEY unique_activity_word (activity_id, word) COMMENT 'Each word recorded only once per activity (frequency tracks repeats)'
) COMMENT 'Analytics table storing sentiment analysis results from feedback comments';

-- ===================================================================
-- PERFORMANCE OPTIMIZATION INDEXES
-- ===================================================================
-- These indexes improve query performance for common database operations
-- They speed up lookups, joins, and filtering operations

-- Student Authentication Queries - Login performance
CREATE INDEX idx_student_login ON students(username, password) 
COMMENT 'Speeds up login verification queries';

-- Activity Scheduling Queries - Schedule browsing and conflict detection
CREATE INDEX idx_activity_schedule ON activities(day, start_time) 
COMMENT 'Optimizes schedule queries and conflict detection';

-- Student Activity Lookups - Enrollment checks and participation verification
CREATE INDEX idx_student_activity_lookup ON student_activities(student_id, activity_id) 
COMMENT 'Faster enrollment and participation verification';

-- Expense Queries - Financial reporting and analysis
CREATE INDEX idx_expense_date ON expenses(date) 
COMMENT 'Speeds up date-based expense reporting';
CREATE INDEX idx_expense_participants ON expenses(id_giver, id_receiver) 
COMMENT 'Optimizes participant-based expense queries';

-- Debt Management Queries - Outstanding debt tracking
CREATE INDEX idx_debt_payer ON debts(payer_id, paid) 
COMMENT 'Faster queries for money owed to specific students';
CREATE INDEX idx_debt_debtor ON debts(debtor_id, paid) 
COMMENT 'Faster queries for money owed by specific students';

-- Feedback and Analytics Queries - Rating analysis and sentiment processing
CREATE INDEX idx_feedback_activity ON feedback(activity_id, rating) 
COMMENT 'Optimizes activity rating calculations and analysis';
CREATE INDEX idx_sentiment_lookup ON sentiment_words(activity_id, sentiment_type) 
COMMENT 'Speeds up sentiment analysis queries';

-- ===================================================================
-- SAMPLE DATA FOR TESTING AND DEVELOPMENT
-- ===================================================================
-- Insert realistic test data to verify system functionality

-- Sample Students with Different Profiles
-- Note: In production, passwords should be properly hashed for security
INSERT INTO students (name, surname, username, password, class, age, special_needs) VALUES
('John', 'Doe', 'john.doe', 'password123', '12A', 18, NULL),
('Jane', 'Smith', 'jane.smith', 'password123', '12A', 17, 'Vegetarian diet - no meat products'),
('Mike', 'Johnson', 'mike.j', 'password123', '12B', 18, NULL),
('Sarah', 'Williams', 'sarah.w', 'password123', '12A', 17, 'Gluten-free diet - celiac disease'),
('Alex', 'Brown', 'alex.brown', 'password123', '12B', 18, 'Wheelchair accessible venues required');

-- Sample Activities with Realistic Scheduling
-- These represent different types of activities students might encounter on a trip
INSERT INTO activities (name, description, day, start_time, finish_time, location, max_participants, duration) VALUES
('Museum Visit', 'Guided tour of the National History Museum with interactive exhibits focusing on ancient civilizations', '2024-03-15', 9, 12, 'National History Museum, Downtown', 25, 3),
('City Walking Tour', 'Exploring the historic city center with a local guide, visiting landmarks and learning about local culture', '2024-03-15', 14, 17, 'City Center Historic District', 30, 3),
('Beach Day', 'Relaxing day at the beach with optional water sports including volleyball and swimming', '2024-03-16', 10, 16, 'Sunny Beach Resort', NULL, 6),
('Cultural Workshop', 'Traditional craft workshop learning local pottery and weaving techniques from master artisans', '2024-03-16', 9, 11, 'Cultural Heritage Center', 15, 2),
('Mountain Hiking', 'Guided hike through scenic mountain trails with photography opportunities and nature education', '2024-03-17', 8, 15, 'Mountain Trail Head, Eagle Peak', 20, 7);

-- Sample Activity Enrollments - Creating realistic participation patterns
-- Students enroll in different combinations of activities based on interests
INSERT INTO student_activities (student_id, activity_id) VALUES
(1, 1), (1, 2), (1, 3),  -- John enrolled in first 3 activities (museum, walking tour, beach)
(2, 1), (2, 3), (2, 4),  -- Jane enrolled in activities 1, 3, 4 (museum, beach, workshop)
(3, 2), (3, 3), (3, 5),  -- Mike enrolled in activities 2, 3, 5 (walking tour, beach, hiking)
(4, 1), (4, 4), (4, 5),  -- Sarah enrolled in activities 1, 4, 5 (museum, workshop, hiking)
(5, 2), (5, 3), (5, 4);  -- Alex enrolled in activities 2, 3, 4 (walking tour, beach, workshop)

-- Sample Expenses - Different types of shared costs
-- These represent realistic expenses that might occur during a trip
INSERT INTO expenses (amount, description, date, id_giver, id_receiver, id_activity) VALUES
(45.50, 'Group lunch at museum cafe - shared meal for 5 students', '2024-03-15', 1, NULL, 1),
(30.00, 'Taxi fare back to hotel after walking tour - shared transportation', '2024-03-15', 2, NULL, 2),
(75.20, 'Beach equipment rental - umbrellas, chairs, and sports equipment', '2024-03-16', 3, NULL, 3),
(25.80, 'Materials for workshop - clay, tools, and supplies', '2024-03-16', 4, NULL, 4),
(120.00, 'Emergency medical supplies and first aid kit for hiking', '2024-03-17', 5, NULL, 5);

-- Sample Feedback - Realistic student responses with varying ratings
-- These show different student perspectives and writing styles
INSERT INTO feedback (student_id, activity_id, rating, comment) VALUES
(1, 1, 5, 'Amazing museum with incredible exhibits! The guide was very knowledgeable and made everything interesting. Learned so much about ancient history.'),
(2, 1, 4, 'Really enjoyed the museum visit. Some sections were a bit crowded but overall excellent experience. The interactive displays were fantastic.'),
(1, 2, 4, 'Nice walking tour of the city. Weather was perfect and learned a lot about the local history and architecture. Guide was friendly and informative.'),
(3, 2, 3, 'Tour was okay but felt a bit rushed. Would have liked more time at each location to really appreciate the details and take photos.'),
(2, 3, 5, 'Perfect beach day! Water was warm and the facilities were great. Very relaxing after busy days of sightseeing. Great way to unwind.'),
(3, 3, 5, 'Loved the beach! Great way to unwind after busy days of sightseeing. The water sports were fun and the weather was perfect.'),
(2, 4, 4, 'Workshop was educational and fun. Making pottery was harder than expected but very rewarding. The instructor was patient and helpful.'),
(4, 4, 5, 'Absolutely loved the cultural workshop! Learning traditional techniques was fascinating and the artisans were incredibly skilled. Great hands-on experience.');

-- ===================================================================
-- DATABASE VIEWS FOR COMMON QUERIES
-- ===================================================================
-- Create views to simplify complex queries used frequently by the application

-- Activity Summary View - Combines activity info with participation and ratings
CREATE VIEW activity_summary AS
SELECT 
    a.id,
    a.name,
    a.day,
    a.start_time,
    a.finish_time,
    a.location,
    a.max_participants,
    COUNT(DISTINCT sa.student_id) as current_participants,
    COALESCE(AVG(f.rating), 0) as average_rating,
    COUNT(DISTINCT f.id) as feedback_count
FROM activities a
LEFT JOIN student_activities sa ON a.id = sa.activity_id
LEFT JOIN feedback f ON a.id = f.activity_id
GROUP BY a.id, a.name, a.day, a.start_time, a.finish_time, a.location, a.max_participants;

-- Student Financial Summary View - Aggregates financial data per student
CREATE VIEW student_financial_summary AS
SELECT 
    s.id,
    s.name,
    s.surname,
    s.username,
    COALESCE(SUM(CASE WHEN e.id_giver = s.id THEN e.amount ELSE 0 END), 0) as total_paid,
    COALESCE(SUM(CASE WHEN d.payer_id = s.id AND d.paid = FALSE THEN d.amount ELSE 0 END), 0) as money_owed_to_student,
    COALESCE(SUM(CASE WHEN d.debtor_id = s.id AND d.paid = FALSE THEN d.amount ELSE 0 END), 0) as money_student_owes
FROM students s
LEFT JOIN expenses e ON s.id = e.id_giver
LEFT JOIN debts d ON s.id = d.payer_id OR s.id = d.debtor_id
GROUP BY s.id, s.name, s.surname, s.username;

-- ===================================================================
-- STORED PROCEDURES FOR COMMON OPERATIONS
-- ===================================================================
-- Create stored procedures to encapsulate complex business logic

DELIMITER //

-- Procedure to register a student for an activity with validation
CREATE PROCEDURE RegisterStudentForActivity(
    IN p_student_id INT,
    IN p_activity_id INT,
    OUT p_success BOOLEAN,
    OUT p_message VARCHAR(255)
)
BEGIN
    DECLARE v_current_participants INT DEFAULT 0;
    DECLARE v_max_participants INT DEFAULT NULL;
    DECLARE v_already_registered INT DEFAULT 0;
    
    -- Check if student is already registered
    SELECT COUNT(*) INTO v_already_registered
    FROM student_activities 
    WHERE student_id = p_student_id AND activity_id = p_activity_id;
    
    IF v_already_registered > 0 THEN
        SET p_success = FALSE;
        SET p_message = 'Student is already registered for this activity';
    ELSE
        -- Check activity capacity
        SELECT COUNT(sa.student_id), a.max_participants 
        INTO v_current_participants, v_max_participants
        FROM activities a
        LEFT JOIN student_activities sa ON a.id = sa.activity_id
        WHERE a.id = p_activity_id
        GROUP BY a.id, a.max_participants;
        
        IF v_max_participants IS NOT NULL AND v_current_participants >= v_max_participants THEN
            SET p_success = FALSE;
            SET p_message = 'Activity is at full capacity';
        ELSE
            -- Register the student
            INSERT INTO student_activities (student_id, activity_id) 
            VALUES (p_student_id, p_activity_id);
            
            SET p_success = TRUE;
            SET p_message = 'Student registered successfully';
        END IF;
    END IF;
END //

DELIMITER ;

-- ===================================================================
-- DATABASE SETUP COMPLETE
-- ===================================================================
-- The database is now fully configured and ready for use with the Trip Manager application.
-- 
-- SUMMARY OF WHAT WAS CREATED:
-- 
-- TABLES (7):
-- - students: 5 sample students with authentication and profile data
-- - activities: 5 sample activities across 3 days with various types
-- - student_activities: Enrollment relationships between students and activities
-- - expenses: 5 sample shared expenses representing different cost types
-- - debts: Will be populated by application when expenses are split
-- - feedback: 8 sample feedback entries showing student opinions
-- - sentiment_words: Will be populated by sentiment analysis system
-- 
-- VIEWS (2):
-- - activity_summary: Combines activity data with participation and ratings
-- - student_financial_summary: Aggregates financial data per student
-- 
-- INDEXES (8): Performance optimization for common queries
-- 
-- STORED PROCEDURES (1):
-- - RegisterStudentForActivity: Handles activity registration with validation
-- 
-- DEFAULT LOGIN CREDENTIALS (for testing):
-- Username: john.doe, Password: password123
-- Username: jane.smith, Password: password123
-- Username: mike.j, Password: password123
-- Username: sarah.w, Password: password123
-- Username: alex.brown, Password: password123
-- 
-- NEXT STEPS:
-- 1. Connect the Python application to this database
-- 2. Test all functionality with the sample data
-- 3. Add additional students and activities as needed
-- 4. Update passwords to use proper hashing in production
-- ===================================================================
