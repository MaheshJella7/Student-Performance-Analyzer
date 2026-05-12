CREATE DATABASE IF NOT EXISTS spa_enhanced_db;

USE spa_enhanced_db;


CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,

    username VARCHAR(50) NOT NULL UNIQUE
        COLLATE utf8mb4_general_ci,

    password_hash CHAR(64) NOT NULL,

    role ENUM('admin', 'faculty', 'student') NOT NULL,

    is_active BOOLEAN DEFAULT TRUE,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE students (
    id INT AUTO_INCREMENT PRIMARY KEY,

    name VARCHAR(100) NOT NULL,

    department VARCHAR(50) NOT NULL,

    marks DECIMAL(5,2)
        CHECK (marks >= 0 AND marks <= 100),

    user_id INT UNIQUE,

    enrolled_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (user_id)
        REFERENCES users(id)
        ON DELETE CASCADE
);


CREATE TABLE audit_log (
    id INT AUTO_INCREMENT PRIMARY KEY,

    user_id INT,

    action VARCHAR(100),

    details TEXT,

    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (user_id)
        REFERENCES users(id)
        ON DELETE SET NULL
);


INSERT INTO users (username, password_hash, role)
VALUES ('admin', SHA2('1234',256), 'admin');


INSERT INTO users (username, password_hash, role)
VALUES ('faculty1', SHA2('1234',256), 'faculty');


INSERT INTO users (username, password_hash, role)
VALUES ('student1', SHA2('1234',256), 'student');


INSERT INTO students (name, department, marks, user_id)
VALUES ('Rahul', 'CSE', 88, 3);


INSERT INTO students (name, department, marks)
VALUES ('Mahesh', 'AIML', 95);

INSERT INTO students (name, department, marks)
VALUES ('Priya', 'CSE', 82);

INSERT INTO students (name, department, marks)
VALUES ('Kiran', 'ECE', 74);

INSERT INTO students (name, department, marks)
VALUES ('Anjali', 'AIML', 91);


CREATE USER IF NOT EXISTS 'spa_admin'@'localhost'
IDENTIFIED BY 'admin123';

GRANT ALL PRIVILEGES
ON spa_enhanced_db.* 
TO 'spa_admin'@'localhost';


CREATE USER IF NOT EXISTS 'spa_faculty'@'localhost'
IDENTIFIED BY 'faculty123';

GRANT SELECT, INSERT, UPDATE
ON spa_enhanced_db.* 
TO 'spa_faculty'@'localhost';


CREATE USER IF NOT EXISTS 'spa_student'@'localhost'
IDENTIFIED BY 'student123';

GRANT SELECT
ON spa_enhanced_db.* 
TO 'spa_student'@'localhost';


CREATE INDEX idx_department
ON students(department);


CREATE VIEW high_performers AS
SELECT name, department, marks
FROM students
WHERE marks > 75;


FLUSH PRIVILEGES;