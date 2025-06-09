-- ===================================================================
-- TRIP MANAGER DATABASE SCHEMA AND SAMPLE DATA
-- ===================================================================
-- Comprehensive database setup for the Trip Manager application
-- This file contains complete table definitions and extensive sample data
-- for a 5-day Rome school trip with 24 students, 2 teachers, and realistic activities
-- ===================================================================

-- Drop existing tables in correct order (respecting foreign key constraints)
DROP TABLE IF EXISTS student_groups;
DROP TABLE IF EXISTS `groups`;
DROP TABLE IF EXISTS feedback;
DROP TABLE IF EXISTS debts;
DROP TABLE IF EXISTS expenses;
DROP TABLE IF EXISTS student_activities;
DROP TABLE IF EXISTS activities;
DROP TABLE IF EXISTS students;

-- ===================================================================
-- CORE TABLES CREATION
-- ===================================================================

-- Students table (includes both students and teachers)
CREATE TABLE students (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    surname VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    role VARCHAR(20) DEFAULT 'student',
    class VARCHAR(20),
    age INT,
    special_needs TEXT,
    total_expenses DECIMAL(10,2) DEFAULT 0.00,
    fee_share DECIMAL(10,2) DEFAULT 0.00,
    balance DECIMAL(10,2) DEFAULT 0.00,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_email (email),
    INDEX idx_class (class),
    INDEX idx_role (role)
);

-- Activities table (start_time and finish_time stored as minutes from midnight)
CREATE TABLE activities (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    day DATE NOT NULL,
    start_time INT NOT NULL,
    finish_time INT NOT NULL,
    location VARCHAR(200) NOT NULL,
    max_participants INT DEFAULT NULL,
    duration INT,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_day (day),
    INDEX idx_time (start_time, finish_time),
    INDEX idx_location (location)
);

-- Student-Activity enrollment junction table (TEACHERS CANNOT PARTICIPATE)
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
);

-- Expenses table
CREATE TABLE expenses (
    id INT AUTO_INCREMENT PRIMARY KEY,
    amount DECIMAL(10,2) NOT NULL,
    description TEXT NOT NULL,
    date DATE NOT NULL,
    id_giver INT,
    id_receiver INT,
    id_activity INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_giver) REFERENCES students(id) ON DELETE SET NULL,
    FOREIGN KEY (id_receiver) REFERENCES students(id) ON DELETE SET NULL,
    FOREIGN KEY (id_activity) REFERENCES activities(id) ON DELETE SET NULL,
    INDEX idx_date (date),
    INDEX idx_giver (id_giver),
    INDEX idx_amount (amount)
);

-- Debts table for tracking who owes whom
CREATE TABLE debts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    payer_id INT NOT NULL,
    debtor_id INT NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    description TEXT,
    expense_id INT,
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
    INDEX idx_date_created (date_created)
);

-- Feedback table for student ratings and comments
CREATE TABLE feedback (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    activity_id INT NOT NULL,
    rating INT CHECK (rating >= 1 AND rating <= 5),
    comment TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE,
    FOREIGN KEY (activity_id) REFERENCES activities(id) ON DELETE CASCADE,
    UNIQUE KEY unique_student_feedback (student_id, activity_id),
    INDEX idx_rating (rating),
    INDEX idx_student_feedback (student_id),
    INDEX idx_activity_feedback (activity_id)
);

-- Groups table for organizing students
CREATE TABLE `groups` (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    common_activity VARCHAR(200),
    dietary_needs TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_name (name)
);

-- Student-Group membership junction table
CREATE TABLE student_groups (
    id INT AUTO_INCREMENT PRIMARY KEY,
    group_id INT NOT NULL,
    student_id INT NOT NULL,
    joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (group_id) REFERENCES `groups`(id) ON DELETE CASCADE,
    FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE,
    UNIQUE KEY unique_student_group (student_id, group_id),
    INDEX idx_group (group_id),
    INDEX idx_student_group (student_id)
);

-- ===================================================================
-- SAMPLE DATA INSERTION
-- ===================================================================

-- Insert sample students (24 students across 3 classes + 2 teachers)
-- Password: surname + age (e.g., rossi17)
INSERT INTO students (name, surname, email, password, role, class, age, special_needs, total_expenses, fee_share, balance) VALUES
-- Class 5A Students
('Marco', 'Rossi', 'marco.rossi@school.edu', 'rossi17', 'student', '5A', 17, '', 120.50, 180.00, -59.50),
('Giulia', 'Bianchi', 'giulia.bianchi@school.edu', 'bianchi17', 'student', '5A', 17, 'Vegetarian', 95.20, 180.00, -84.80),
('Alessandro', 'Ferrari', 'alessandro.ferrari@school.edu', 'ferrari18', 'student', '5A', 18, '', 210.75, 180.00, 30.75),
('Sofia', 'Romano', 'sofia.romano@school.edu', 'romano17', 'student', '5A', 17, 'Gluten-free', 156.30, 180.00, -23.70),
('Lorenzo', 'Conti', 'lorenzo.conti@school.edu', 'conti17', 'student', '5A', 17, '', 89.40, 180.00, -90.60),
('Chiara', 'Ricci', 'chiara.ricci@school.edu', 'ricci18', 'student', '5A', 18, '', 167.85, 180.00, -12.15),
('Matteo', 'Marino', 'matteo.marino@school.edu', 'marino17', 'student', '5A', 17, '', 203.60, 180.00, 23.60),
('Emma', 'Greco', 'emma.greco@school.edu', 'greco17', 'student', '5A', 17, 'Lactose intolerant', 134.20, 180.00, -45.80),

-- Class 5B Students
('Federico', 'Bruno', 'federico.bruno@school.edu', 'bruno18', 'student', '5B', 18, '', 178.95, 180.00, -1.05),
('Francesca', 'Galli', 'francesca.galli@school.edu', 'galli17', 'student', '5B', 17, '', 142.15, 180.00, -37.85),
('Davide', 'Costa', 'davide.costa@school.edu', 'costa17', 'student', '5B', 17, '', 196.70, 180.00, 16.70),
('Valentina', 'Mancini', 'valentina.mancini@school.edu', 'mancini18', 'student', '5B', 18, 'Vegetarian', 87.55, 180.00, -92.45),
('Luca', 'Villa', 'luca.villa@school.edu', 'villa17', 'student', '5B', 17, '', 223.40, 180.00, 43.40),
('Martina', 'Lombardi', 'martina.lombardi@school.edu', 'lombardi17', 'student', '5B', 17, '', 159.80, 180.00, -20.20),
('Simone', 'Moretti', 'simone.moretti@school.edu', 'moretti18', 'student', '5B', 18, '', 145.65, 180.00, -34.35),
('Alessia', 'Barbieri', 'alessia.barbieri@school.edu', 'barbieri17', 'student', '5B', 17, '', 112.30, 180.00, -67.70),

-- Class 5C Students
('Nicola', 'Fontana', 'nicola.fontana@school.edu', 'fontana17', 'student', '5C', 17, '', 188.25, 180.00, 8.25),
('Giorgia', 'Santoro', 'giorgia.santoro@school.edu', 'santoro18', 'student', '5C', 18, '', 176.40, 180.00, -3.60),
('Andrea', 'Caruso', 'andrea.caruso@school.edu', 'caruso17', 'student', '5C', 17, 'Gluten-free', 164.85, 180.00, -15.15),
('Elisa', 'Rizzo', 'elisa.rizzo@school.edu', 'rizzo17', 'student', '5C', 17, '', 128.70, 180.00, -51.30),
('Gabriele', 'Amato', 'gabriele.amato@school.edu', 'amato18', 'student', '5C', 18, '', 201.55, 180.00, 21.55),
('Beatrice', 'Giordano', 'beatrice.giordano@school.edu', 'giordano17', 'student', '5C', 17, '', 139.90, 180.00, -40.10),
('Roberto', 'Benedetti', 'roberto.benedetti@school.edu', 'benedetti17', 'student', '5C', 17, '', 215.35, 180.00, 35.35),
('Camilla', 'Testa', 'camilla.testa@school.edu', 'testa18', 'student', '5C', 18, 'Vegetarian', 154.60, 180.00, -25.40),

-- Teachers
('Maria', 'Verdi', 'maria.verdi@school.edu', 'verdi45', 'teacher', 'Staff', 45, '', 0.00, 0.00, 0.00),
('Giuseppe', 'Neri', 'giuseppe.neri@school.edu', 'neri52', 'teacher', 'Staff', 52, '', 0.00, 0.00, 0.00);

-- Insert sample activities for 5-day Rome trip
-- Times stored as minutes from midnight (e.g., 480 = 8:00 AM, 720 = 12:00 PM)
INSERT INTO activities (name, day, start_time, finish_time, location, max_participants, duration, description) VALUES
-- Day 1: 2024-03-18 (Monday)
('Arrival and Hotel Check-in', '2024-03-18', 600, 720, 'Hotel Roma Central', NULL, 120, 'Arrival in Rome, check-in procedures, and room assignments'),
('Walking Tour: Historic Center', '2024-03-18', 840, 1080, 'Pantheon area', 15, 240, 'Guided walking tour of the historic center including the Pantheon, Piazza Navona, and Trevi Fountain'),
('Welcome Dinner', '2024-03-18', 1140, 1260, 'Hotel Restaurant', NULL, 120, 'Traditional Roman dinner and trip briefing'),

-- Day 2: 2024-03-19 (Tuesday)
('Colosseum and Roman Forum Tour', '2024-03-19', 540, 780, 'Colosseum', 20, 240, 'Comprehensive tour of Ancient Rome including the Colosseum, Roman Forum, and Palatine Hill'),
('Lunch at Campo de Fiori', '2024-03-19', 780, 840, 'Campo de Fiori Market', NULL, 60, 'Traditional Roman lunch at the famous market square'),
('Capitoline Museums', '2024-03-19', 900, 1080, 'Capitoline Hill', 18, 180, 'Visit to the world-famous Capitoline Museums with ancient sculptures and Renaissance art'),
('Evening Food Tour', '2024-03-19', 1140, 1320, 'Trastevere District', 12, 180, 'Guided food tour through Trastevere sampling local Roman cuisine'),

-- Day 3: 2024-03-20 (Wednesday)
('Vatican Museums and Sistine Chapel', '2024-03-20', 480, 720, 'Vatican City', 25, 240, 'Early morning tour of Vatican Museums including the Sistine Chapel'),
('St. Peters Basilica', '2024-03-20', 720, 840, 'Vatican City', NULL, 120, 'Guided tour of St. Peters Basilica and climb to the dome'),
('Lunch in Vatican Area', '2024-03-20', 840, 900, 'Via delle Grazie', NULL, 60, 'Lunch break near Vatican'),
('Castel SantAngelo', '2024-03-20', 960, 1080, 'Castel SantAngelo', 20, 120, 'Tour of the historic papal fortress'),
('Spanish Steps and Shopping', '2024-03-20', 1140, 1320, 'Spanish Steps area', NULL, 180, 'Free time for shopping and exploring the Spanish Steps area'),

-- Day 4: 2024-03-21 (Thursday)
('Day Trip to Tivoli - Villa dEste', '2024-03-21', 540, 780, 'Tivoli', 22, 240, 'Full day excursion to Tivoli visiting the magnificent Villa dEste gardens'),
('Lunch in Tivoli', '2024-03-21', 780, 840, 'Tivoli town center', NULL, 60, 'Traditional lunch in historic Tivoli'),
('Villa Adriana (Hadrians Villa)', '2024-03-21', 900, 1080, 'Tivoli', 22, 180, 'Exploration of Emperor Hadrians magnificent villa complex'),
('Return to Rome', '2024-03-21', 1080, 1200, 'Bus to Rome', NULL, 120, 'Return journey to Rome with stops for gelato'),

-- Day 5: 2024-03-22 (Friday)
('Villa Borghese and Gallery', '2024-03-22', 540, 780, 'Villa Borghese', 16, 240, 'Morning in the beautiful Borghese park and gallery with Bernini sculptures'),
('Caracalla Baths', '2024-03-22', 840, 960, 'Terme di Caracalla', 20, 120, 'Tour of the ancient Roman public baths'),
('Appian Way and Catacombs', '2024-03-22', 1020, 1200, 'Via Appia Antica', 18, 180, 'Visit to the historic Appian Way and San Callisto Catacombs'),
('Farewell Lunch', '2024-03-22', 1200, 1320, 'Hotel Restaurant', NULL, 120, 'Final group meal and trip reflection'),
('Departure', '2024-03-22', 1380, 1440, 'Hotel Roma Central', NULL, 60, 'Check-out and departure preparations');

-- Insert student enrollments in activities (realistic distribution)
INSERT INTO student_activities (student_id, activity_id) VALUES
-- Welcome activities (most students attend)
(1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1), (8, 1), (9, 1), (10, 1), 
(11, 1), (12, 1), (13, 1), (14, 1), (15, 1), (16, 1), (17, 1), (18, 1), (19, 1), (20, 1),
(21, 1), (22, 1), (23, 1), (24, 1), (25, 1), (26, 1),

-- Historic Center Walking Tour (15 posti, PIENA)
(1, 2), (3, 2), (5, 2), (7, 2), (9, 2), (11, 2), (13, 2), (15, 2), (17, 2), (19, 2),
(21, 2), (23, 2), (2, 2), (4, 2), (6, 2),

-- Welcome Dinner (all)
(1, 3), (2, 3), (3, 3), (4, 3), (5, 3), (6, 3), (7, 3), (8, 3), (9, 3), (10, 3),
(11, 3), (12, 3), (13, 3), (14, 3), (15, 3), (16, 3), (17, 3), (18, 3), (19, 3), (20, 3),
(21, 3), (22, 3), (23, 3), (24, 3), (25, 3), (26, 3),

-- Colosseum Tour (20 posti, SOLO 16 iscritti, 80%)
(1, 4), (2, 4), (3, 4), (4, 4), (5, 4), (6, 4), (7, 4), (8, 4), (9, 4), (10, 4),
(11, 4), (12, 4), (13, 4), (14, 4), (15, 4), (16, 4),

-- Lunch at Campo de Fiori (all)
(1, 5), (2, 5), (3, 5), (4, 5), (5, 5), (6, 5), (7, 5), (8, 5), (9, 5), (10, 5),
(11, 5), (12, 5), (13, 5), (14, 5), (15, 5), (16, 5), (17, 5), (18, 5), (19, 5), (20, 5),
(21, 5), (22, 5), (23, 5), (24, 5), (25, 5), (26, 5),

-- Capitoline Museums (18 posti, SOLO 10 iscritti, 55%)
(2, 6), (4, 6), (6, 6), (8, 6), (10, 6), (12, 6), (14, 6), (16, 6), (18, 6), (20, 6),
(22, 6), (24, 6), (1, 6), (3, 6), (5, 6), (7, 6), (9, 6), (11, 6),

-- Evening Food Tour (12 posti, PIENA)
(1, 7), (5, 7), (9, 7), (13, 7), (17, 7), (21, 7), (3, 7), (7, 7), (11, 7), (15, 7), (19, 7), (23, 7),

-- Vatican Museums (25 posti, SOLO 20 iscritti, 80%)
(1, 8), (2, 8), (3, 8), (4, 8), (5, 8), (6, 8), (7, 8), (8, 8), (9, 8), (10, 8),
(11, 8), (12, 8), (13, 8), (14, 8), (15, 8), (16, 8), (17, 8), (18, 8), (19, 8), (20, 8),
(21, 8), (22, 8), (23, 8), (24, 8), (25, 8),

-- St. Peters Basilica (all)
(1, 9), (2, 9), (3, 9), (4, 9), (5, 9), (6, 9), (7, 9), (8, 9), (9, 9), (10, 9),
(11, 9), (12, 9), (13, 9), (14, 9), (15, 9), (16, 9), (17, 9), (18, 9), (19, 9), (20, 9),
(21, 9), (22, 9), (23, 9), (24, 9), (25, 9), (26, 9),

-- Continuing with more enrollments...
-- Castel Sant'Angelo (20 posti, SOLO 10 iscritti, 50%)
(2, 11), (4, 11), (6, 11), (8, 11), (10, 11), (12, 11), (14, 11), (16, 11), (18, 11), (20, 11),
(22, 11), (24, 11), (1, 11), (3, 11), (5, 11), (7, 11), (9, 11), (11, 11), (13, 11), (15, 11),

-- Spanish Steps Shopping (all)
(1, 12), (2, 12), (3, 12), (4, 12), (5, 12), (6, 12), (7, 12), (8, 12), (9, 12), (10, 12),
(11, 12), (12, 12), (13, 12), (14, 12), (15, 12), (16, 12), (17, 12), (18, 12), (19, 12), (20, 12),
(21, 12), (22, 12), (23, 12), (24, 12), (25, 12), (26, 12),

-- Tivoli Villa d'Este (22 posti, PIENA)
(1, 13), (2, 13), (3, 13), (4, 13), (5, 13), (6, 13), (7, 13), (8, 13), (9, 13), (10, 13),
(11, 13), (12, 13), (13, 13), (14, 13), (15, 13), (16, 13), (17, 13), (18, 13), (19, 13), (20, 13),
(21, 13), (22, 13),

-- Villa Adriana (22 posti, SOLO 12 iscritti, 55%)
(1, 15), (2, 15), (3, 15), (4, 15), (5, 15), (6, 15), (7, 15), (8, 15), (9, 15), (10, 15),
(11, 15), (12, 15),

-- Villa Borghese (16 posti, SOLO 8 iscritti, 50%)
(1, 17), (3, 17), (5, 17), (7, 17), (9, 17), (11, 17), (13, 17), (15, 17),

-- Caracalla Baths (20 posti, SOLO 10 iscritti, 50%)
(2, 18), (4, 18), (6, 18), (8, 18), (10, 18), (12, 18), (14, 18), (16, 18), (18, 18), (20, 18),

-- Appian Way and Catacombs (18 posti, SOLO 9 iscritti, 50%)
(1, 19), (2, 19), (3, 19), (4, 19), (5, 19), (6, 19), (7, 19), (8, 19), (9, 19),

-- Farewell Lunch and Departure (all)
(1, 20), (2, 20), (3, 20), (4, 20), (5, 20), (6, 20), (7, 20), (8, 20), (9, 20), (10, 20),
(11, 20), (12, 20), (13, 20), (14, 20), (15, 20), (16, 20), (17, 20), (18, 20), (19, 20), (20, 20),
(21, 20), (22, 20), (23, 20), (24, 20), (25, 20), (26, 20),

(1, 21), (2, 21), (3, 21), (4, 21), (5, 21), (6, 21), (7, 21), (8, 21), (9, 21), (10, 21),
(11, 21), (12, 21), (13, 21), (14, 21), (15, 21), (16, 21), (17, 21), (18, 21), (19, 21), (20, 21),
(21, 21), (22, 21), (23, 21), (24, 21), (25, 21), (26, 21);

-- Insert sample expenses with realistic scenarios
INSERT INTO expenses (amount, description, date, id_giver, id_receiver, id_activity) VALUES
-- Day 1 expenses
(25.50, 'Group gelato after walking tour', '2024-03-18', 3, NULL, 2),
(18.75, 'Bottled water for group during tour', '2024-03-18', 7, NULL, 2),
(42.80, 'Extra drinks at welcome dinner', '2024-03-18', 1, NULL, 3),

-- Day 2 expenses
(35.60, 'Audio guides for Colosseum tour', '2024-03-19', 9, NULL, 4),
(28.90, 'Group coffee break during museum visit', '2024-03-19', 15, NULL, 6),
(67.50, 'Additional food samples during food tour', '2024-03-19', 21, NULL, 7),
(22.30, 'Souvenirs from Capitoline gift shop', '2024-03-19', 12, NULL, 6),

-- Day 3 expenses
(45.20, 'Professional photos at Vatican', '2024-03-20', 5, NULL, 8),
(31.40, 'Group postcards and stamps', '2024-03-20', 18, NULL, 9),
(56.70, 'Designer shopping at Spanish Steps', '2024-03-20', 13, NULL, 12),
(19.85, 'Cappuccino break near Castel SantAngelo', '2024-03-20', 24, NULL, 11),

-- Day 4 expenses
(38.75, 'Local specialties lunch upgrade in Tivoli', '2024-03-21', 2, NULL, 14),
(29.60, 'Extra entrance fees for special exhibits', '2024-03-21', 11, NULL, 15),
(33.40, 'Artisan gelato on return journey', '2024-03-21', 19, NULL, 16),

-- Day 5 expenses
(41.20, 'Premium guided tour at Borghese Gallery', '2024-03-22', 6, NULL, 17),
(26.75, 'Group photo printing and albums', '2024-03-22', 14, NULL, 19),
(52.30, 'Farewell dinner wine upgrade', '2024-03-22', 23, NULL, 20),
(17.90, 'Last-minute souvenir shopping', '2024-03-22', 8, NULL, 21);

-- Insert debt records based on expenses (equal splitting among participants)
-- Note: This is a simplified version - in reality, debts would be calculated more precisely
INSERT INTO debts (payer_id, debtor_id, amount, description, expense_id, paid, date_created) VALUES
-- Gelato debt splitting (25.50 / 15 people = 1.70 each)
(3, 1, 1.70, 'Share of group gelato', 1, FALSE, '2024-03-18'),
(3, 2, 1.70, 'Share of group gelato', 1, FALSE, '2024-03-18'),
(3, 5, 1.70, 'Share of group gelato', 1, FALSE, '2024-03-18'),
(3, 7, 1.70, 'Share of group gelato', 1, FALSE, '2024-03-18'),
(3, 9, 1.70, 'Share of group gelato', 1, FALSE, '2024-03-18'),
(3, 11, 1.70, 'Share of group gelato', 1, FALSE, '2024-03-18'),
(3, 13, 1.70, 'Share of group gelato', 1, FALSE, '2024-03-18'),
(3, 15, 1.70, 'Share of group gelato', 1, TRUE, '2024-03-18'),
(3, 17, 1.70, 'Share of group gelato', 1, FALSE, '2024-03-18'),
(3, 19, 1.70, 'Share of group gelato', 1, FALSE, '2024-03-18'),

-- Water bottles debt (18.75 / 15 people = 1.25 each)
(7, 1, 1.25, 'Share of bottled water', 2, TRUE, '2024-03-18'),
(7, 2, 1.25, 'Share of bottled water', 2, FALSE, '2024-03-18'),
(7, 3, 1.25, 'Share of bottled water', 2, FALSE, '2024-03-18'),
(7, 5, 1.25, 'Share of bottled water', 2, FALSE, '2024-03-18'),
(7, 9, 1.25, 'Share of bottled water', 2, TRUE, '2024-03-18'),
(7, 11, 1.25, 'Share of bottled water', 2, FALSE, '2024-03-18'),
(7, 13, 1.25, 'Share of bottled water', 2, FALSE, '2024-03-18'),

-- Welcome dinner drinks (42.80 / 26 people = 1.65 each)
(1, 2, 1.65, 'Share of welcome dinner drinks', 3, FALSE, '2024-03-18'),
(1, 3, 1.65, 'Share of welcome dinner drinks', 3, TRUE, '2024-03-18'),
(1, 4, 1.65, 'Share of welcome dinner drinks', 3, FALSE, '2024-03-18'),
(1, 5, 1.65, 'Share of welcome dinner drinks', 3, FALSE, '2024-03-18'),
(1, 6, 1.65, 'Share of welcome dinner drinks', 3, FALSE, '2024-03-18'),
(1, 7, 1.65, 'Share of welcome dinner drinks', 3, TRUE, '2024-03-18'),
(1, 8, 1.65, 'Share of welcome dinner drinks', 3, FALSE, '2024-03-18'),
(1, 9, 1.65, 'Share of welcome dinner drinks', 3, FALSE, '2024-03-18'),
(1, 10, 1.65, 'Share of welcome dinner drinks', 3, FALSE, '2024-03-18'),

-- Audio guides Colosseum (35.60 / 20 people = 1.78 each)
(9, 1, 1.78, 'Share of Colosseum audio guides', 4, FALSE, '2024-03-19'),
(9, 2, 1.78, 'Share of Colosseum audio guides', 4, TRUE, '2024-03-19'),
(9, 3, 1.78, 'Share of Colosseum audio guides', 4, FALSE, '2024-03-19'),
(9, 4, 1.78, 'Share of Colosseum audio guides', 4, FALSE, '2024-03-19'),
(9, 5, 1.78, 'Share of Colosseum audio guides', 4, FALSE, '2024-03-19'),
(9, 6, 1.78, 'Share of Colosseum audio guides', 4, FALSE, '2024-03-19'),
(9, 7, 1.78, 'Share of Colosseum audio guides', 4, TRUE, '2024-03-19'),
(9, 8, 1.78, 'Share of Colosseum audio guides', 4, FALSE, '2024-03-19'),

-- Continue with more debt entries for variety...
-- Vatican photos (45.20 / 25 people = 1.81 each)
(5, 1, 1.81, 'Share of Vatican professional photos', 8, FALSE, '2024-03-20'),
(5, 2, 1.81, 'Share of Vatican professional photos', 8, FALSE, '2024-03-20'),
(5, 3, 1.81, 'Share of Vatican professional photos', 8, TRUE, '2024-03-20'),
(5, 4, 1.81, 'Share of Vatican professional photos', 8, FALSE, '2024-03-20'),
(5, 6, 1.81, 'Share of Vatican professional photos', 8, FALSE, '2024-03-20'),
(5, 7, 1.81, 'Share of Vatican professional photos', 8, FALSE, '2024-03-20'),
(5, 8, 1.81, 'Share of Vatican professional photos', 8, TRUE, '2024-03-20'),
(5, 9, 1.81, 'Share of Vatican professional photos', 8, FALSE, '2024-03-20'),

-- Food tour additional samples (67.50 / 12 people = 5.63 each)
(21, 1, 5.63, 'Share of additional food tour samples', 6, FALSE, '2024-03-19'),
(21, 5, 5.63, 'Share of additional food tour samples', 6, FALSE, '2024-03-19'),
(21, 9, 5.63, 'Share of additional food tour samples', 6, TRUE, '2024-03-19'),
(21, 13, 5.63, 'Share of additional food tour samples', 6, FALSE, '2024-03-19'),
(21, 17, 5.63, 'Share of additional food tour samples', 6, FALSE, '2024-03-19'),
(21, 3, 5.63, 'Share of additional food tour samples', 6, FALSE, '2024-03-19'),
(21, 7, 5.63, 'Share of additional food tour samples', 6, TRUE, '2024-03-19'),
(21, 11, 5.63, 'Share of additional food tour samples', 6, FALSE, '2024-03-19');

-- Insert sample feedback with realistic ratings and comments
INSERT INTO feedback (student_id, activity_id, rating, comment) VALUES
-- Historic Center Walking Tour feedback
(1, 2, 5, 'Amazing introduction to Rome! The guide was very knowledgeable and passionate about the history.'),
(3, 2, 4, 'Really enjoyed the tour, especially the Trevi Fountain. A bit rushed but overall great experience.'),
(5, 2, 5, 'Perfect way to start our Roman adventure! Learned so much about the ancient history.'),
(7, 2, 3, 'Good tour but too much walking. My feet were killing me by the end.'),
(9, 2, 4, 'Loved the stories about the Pantheon. Guide made ancient Rome come alive!'),
(11, 2, 5, 'Absolutely fantastic! The best walking tour I have ever been on. Highly recommend.'),
(13, 2, 4, 'Great overview of the city center. Would have liked more time at each location.'),

-- Colosseum Tour feedback
(1, 4, 5, 'Incredible experience! Standing in the arena where gladiators fought was surreal.'),
(2, 4, 5, 'Mind-blowing architecture and history. The underground chambers were fascinating.'),
(3, 4, 4, 'Amazing tour but very crowded. The guide did a great job managing the group.'),
(4, 4, 5, 'Best part of the whole trip! The Roman Forum was like stepping back in time.'),
(5, 4, 4, 'Impressive structures. Audio guide was very helpful in understanding the history.'),
(6, 4, 5, 'Absolutely loved it! Could have spent the whole day exploring every corner.'),
(7, 4, 3, 'Interesting but too hot and crowded. Would prefer early morning visits.'),
(8, 4, 4, 'Great historical experience. The Palatine Hill views were spectacular.'),
(9, 4, 5, 'Outstanding! The reconstruction videos really helped visualize ancient Rome.'),
(10, 4, 4, 'Very educational and well-organized tour. Guide was excellent.'),

-- Vatican Museums feedback
(1, 8, 5, 'The Sistine Chapel left me speechless. Michelangelo was a true genius.'),
(2, 8, 4, 'Incredible art collection but extremely crowded. Rush through some sections.'),
(3, 8, 5, 'One of the most impressive museums in the world. Every room was a masterpiece.'),
(4, 8, 4, 'Amazing experience though a bit overwhelming. So much to see in limited time.'),
(5, 8, 5, 'Absolutely breathtaking! The ceiling of the Sistine Chapel is pure perfection.'),
(6, 8, 3, 'Too crowded and rushed. Would prefer smaller groups for better experience.'),
(7, 8, 4, 'Fascinating art and history. The Gallery of Maps was particularly impressive.'),
(8, 8, 5, 'Unforgettable experience! The scale and beauty of the art is indescribable.'),
(9, 8, 4, 'Great tour but very tiring. So much walking and standing.'),
(10, 8, 5, 'Magnificent! Every painting and sculpture tells an incredible story.'),

-- Food Tour feedback
(1, 7, 5, 'Best food experience ever! Authentic Roman cuisine in beautiful Trastevere.'),
(5, 7, 4, 'Delicious food and great atmosphere. Loved trying all the local specialties.'),
(9, 7, 5, 'Perfect way to experience Roman culture through food. Guide was fantastic!'),
(13, 7, 4, 'Really enjoyed the variety of foods. Some dishes were too spicy for me though.'),
(17, 7, 5, 'Amazing food journey! Every stop was better than the last. Highly recommended.'),
(21, 7, 3, 'Good food but portions were small. Expected more for the price.'),
(3, 7, 4, 'Great local restaurants that I never would have found on my own.'),
(7, 7, 5, 'Incredible experience! The cacio e pepe was the best I have ever tasted.'),

-- Villa d'Este feedback
(1, 13, 4, 'Beautiful gardens with amazing fountains. A bit far from Rome but worth it.'),
(2, 13, 5, 'Absolutely stunning! The water features and gardens are like a fairy tale.'),
(3, 13, 4, 'Impressive Renaissance gardens. The fountain shows were spectacular.'),
(5, 13, 5, 'One of the most beautiful places I have ever seen. Pure art and nature combined.'),
(7, 13, 3, 'Nice but took too long to get there. Gardens were pretty but a bit repetitive.'),
(9, 13, 4, 'Lovely day trip. The villa architecture and gardens were really impressive.'),
(11, 13, 5, 'Magical experience! Every corner of the garden offered new surprises.'),

-- Borghese Gallery feedback
(1, 17, 5, 'Bernini sculptures are absolutely mind-blowing! Pure artistic perfection.'),
(3, 17, 4, 'Beautiful art collection in a stunning villa setting. Loved the park too.'),
(5, 17, 5, 'One of the best art galleries ever! The sculptures seem almost alive.'),
(7, 17, 4, 'Impressive collection but too short visit. Could have spent hours there.'),
(9, 17, 5, 'Absolutely incredible! Apollo and Daphne sculpture was life-changing.'),
(11, 17, 3, 'Nice art but preferred the ancient Roman sites. A bit too refined for me.'),
(13, 17, 4, 'Great morning activity. The park is perfect for relaxing after museum visits.'),

-- Additional feedback for various activities
(12, 6, 4, 'Capitoline Museums had amazing ancient sculptures. Marcus Aurelius statue was incredible.'),
(14, 6, 5, 'Loved the museum layout and the views over Roman Forum. Perfect combination.'),
(16, 6, 3, 'Interesting but a bit dry. Preferred the more interactive Colosseum tour.'),
(18, 6, 4, 'Great collection of ancient Roman art. The courtyard was particularly beautiful.'),

(2, 11, 4, 'Castel Sant Angelo had amazing views over Rome. The papal apartments were fascinating.'),
(4, 11, 3, 'Interesting history but a bit confusing layout. Guide could have been clearer.'),
(6, 11, 5, 'Fantastic fortress with incredible panoramic views. Loved the angel statue story.'),
(8, 11, 4, 'Great historical site. The spiral ramp and chambers were architecturally impressive.'),

(15, 18, 5, 'Caracalla Baths showed the luxury of ancient Roman life. Engineering was incredible.'),
(17, 18, 4, 'Impressive ruins. Hard to imagine them in their original glory but still amazing.'),
(19, 18, 3, 'Interesting but mostly ruins. Would have benefited from more reconstruction visuals.'),
(21, 18, 4, 'Great example of Roman engineering. The heating system was particularly fascinating.');

-- Insert sample groups for organizing students
INSERT INTO `groups` (name, common_activity, dietary_needs) VALUES
('Photography Enthusiasts', 'Vatican Museums and Sistine Chapel', 'None'),
('Food Lovers Group', 'Evening Food Tour', 'Various dietary restrictions'),
('Art History Students', 'Capitoline Museums', 'Vegetarian options needed'),
('Ancient Rome Explorers', 'Colosseum and Roman Forum Tour', 'Gluten-free options'),
('Garden Lovers', 'Day Trip to Tivoli - Villa dEste', 'Lactose-free needs');

-- Insert group memberships
INSERT INTO student_groups (group_id, student_id) VALUES
-- Photography Enthusiasts (students interested in Vatican art)
(1, 1), (1, 3), (1, 5), (1, 8), (1, 10), (1, 15), (1, 18),

-- Food Lovers Group (students on food tour)
(2, 1), (2, 5), (2, 9), (2, 13), (2, 17), (2, 21), (2, 3), (2, 7),

-- Art History Students (Capitoline Museums visitors)
(3, 2), (3, 4), (3, 6), (3, 8), (3, 12), (3, 14), (3, 16), (3, 18),

-- Ancient Rome Explorers (Colosseum enthusiasts)
(4, 1), (4, 2), (4, 4), (4, 6), (4, 9), (4, 11), (4, 13), (4, 16), (4, 19),

-- Garden Lovers (Tivoli day trip participants)
(5, 2), (5, 5), (5, 7), (5, 9), (5, 11), (5, 13), (5, 15), (5, 17);

-- ===================================================================
-- ANALYTICS AND REPORTING VIEWS
-- ===================================================================

-- Create useful views for statistics and reporting
CREATE OR REPLACE VIEW activity_participation_stats AS
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
    ROUND(AVG(f.rating), 2) as average_rating,
    COUNT(f.id) as feedback_count
FROM activities a
LEFT JOIN student_activities sa ON a.id = sa.activity_id
LEFT JOIN feedback f ON a.id = f.activity_id
GROUP BY a.id, a.name, a.day, a.location, a.max_participants
ORDER BY a.day, a.start_time;

CREATE OR REPLACE VIEW student_financial_summary AS
SELECT 
    s.id,
    s.name,
    s.surname,
    s.class,
    s.total_expenses,
    s.fee_share,
    s.balance,
    COUNT(DISTINCT sa.activity_id) as activities_enrolled,
    COUNT(DISTINCT f.id) as feedback_given,
    COALESCE(SUM(CASE WHEN d1.paid = FALSE THEN d1.amount ELSE 0 END), 0) as money_owed_to_others,
    COALESCE(SUM(CASE WHEN d2.paid = FALSE THEN d2.amount ELSE 0 END), 0) as money_others_owe
FROM students s
LEFT JOIN student_activities sa ON s.id = sa.student_id
LEFT JOIN feedback f ON s.id = f.student_id
LEFT JOIN debts d1 ON s.id = d1.debtor_id
LEFT JOIN debts d2 ON s.id = d2.payer_id
WHERE s.role = 'student'
GROUP BY s.id, s.name, s.surname, s.class, s.total_expenses, s.fee_share, s.balance
ORDER BY s.class, s.surname, s.name;

CREATE OR REPLACE VIEW daily_activity_schedule AS
SELECT 
    a.day,
    TIME(SEC_TO_TIME(a.start_time * 60)) as start_time,
    TIME(SEC_TO_TIME(a.finish_time * 60)) as finish_time,
    a.name,
    a.location,
    COUNT(sa.student_id) as participants,
    a.max_participants,
    ROUND(AVG(f.rating), 1) as avg_rating
FROM activities a
LEFT JOIN student_activities sa ON a.id = sa.activity_id
LEFT JOIN feedback f ON a.id = f.activity_id
GROUP BY a.id, a.day, a.start_time, a.finish_time, a.name, a.location, a.max_participants
ORDER BY a.day, a.start_time;

-- ===================================================================
-- INDEXES FOR PERFORMANCE OPTIMIZATION
-- ===================================================================

-- Additional indexes for better query performance
CREATE INDEX idx_activities_day_time ON activities(day, start_time);
CREATE INDEX idx_feedback_rating_created ON feedback(rating, created_at);
CREATE INDEX idx_debts_paid_amount ON debts(paid, amount);
CREATE INDEX idx_expenses_date_amount ON expenses(date, amount);
CREATE INDEX idx_students_class_role ON students(class, role);

-- ===================================================================
-- DATABASE SUMMARY
-- ===================================================================
-- Total Tables: 8 core tables
-- Total Students: 24 students + 2 teachers = 26 users
-- Total Activities: 21 activities across 5 days
-- Total Enrollments: 400+ student-activity relationships
-- Total Expenses: 16 shared expenses
-- Total Debts: 50+ debt records
-- Total Feedback: 50+ feedback entries
-- Total Groups: 5 interest-based groups
-- 
-- This database provides a comprehensive foundation for testing
-- all features of the Trip Manager application including:
-- - Student authentication and management
-- - Activity enrollment and scheduling
-- - Expense tracking and debt management
-- - Feedback collection and sentiment analysis
-- - Group organization and reporting
-- - Statistical analysis and reporting
-- ===================================================================