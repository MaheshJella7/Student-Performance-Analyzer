# Student-Performance-Analyzer

## Overview
The Student Performance Analyzer is a role-based database management mini-project developed using Python and MySQL. The system is designed to manage student academic records efficiently while demonstrating core DBMS concepts such as authentication, CRUD operations, role-based access control, SQL analytics, audit logging, views, constraints, and database privileges.

The application supports three different user roles:
- Admin
- Faculty
- Student

Each role has specific permissions and menu access within the system.

---

## Objectives
- Develop a secure and role-based student record management system.
- Implement CRUD operations using MySQL and Python.
- Demonstrate SQL concepts such as aggregate functions, views, constraints, joins, and privileges.
- Provide analytics and reporting features for student performance evaluation.
- Maintain audit logs for monitoring important user activities.

---

## Technologies Used
- Python 3
- MySQL
- mysql-connector-python
- PyInstaller
- VS Code

---

## Features Implemented

### Authentication & Security
- Secure login authentication using SHA-256 password hashing.
- Role-based access control for Admin, Faculty, and Student users.
- User account activation/deactivation support.
- Parameterized SQL queries to prevent SQL injection attacks.

### Student Management
- Add new student records.
- View all student records.
- Search students department-wise.
- Update marks and department details.
- Delete student records with confirmation.

### Analytics & Reporting
- Dashboard displaying:
  - Total students
  - Average marks
  - Highest and lowest marks
  - Pass percentage
  - Top performer
  - Department count
- Marks distribution analysis using SQL CASE statements.
- Department-wise leaderboard using aggregate functions.
- Top 3 performer ranking.
- Bonus marks system with maximum cap using LEAST().

### Export Functionality
- Export high-performing students to CSV files with timestamps.

### Audit Logging
- Logs important activities such as:
  - Login/logout
  - Add/update/delete operations
  - Export operations
  - User management actions

### Database-Level Features
- Foreign key relationships
- CHECK constraints
- SQL VIEW creation
- MySQL GRANT privileges
- Indexed department searches

---

## Database Design

The project uses three main tables:

### 1. users
Stores authentication credentials, user roles, account status, and account creation details.

### 2. students
Stores academic information such as student name, department, and marks.

### 3. audit_log
Stores activity logs for tracking important user operations performed within the system.

---

## Database Relationships

- `users.id → students.user_id`
- `users.id → audit_log.user_id`

These relationships help maintain normalization and reduce redundancy.

---

## Files Included

| File Name | Description |
|---|---|
| `24070721017_student_performance_analyzer.py` | Main Python application |
| `24070721017_setup.sql` | Database setup script |
| `24070721017_queries.txt` | Important SQL queries used |
| `24070721017_report.pdf` | Mini-project report |
| `README.md` | Project documentation |

---

## How to Run the Project

### 1. Clone Repository
```bash
git clone <repository-link>
