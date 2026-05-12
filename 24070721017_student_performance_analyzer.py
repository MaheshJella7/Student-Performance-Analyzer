import mysql.connector
import csv, hashlib, datetime, os, getpass

# Database Connection Function

DB_CONFIG = {
"host": "localhost",
"user": "root",
"password": "enter_your_password",
"database": "spa_enhanced_db"
}


def get_connection():
    return mysql.connector.connect(**DB_CONFIG)


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


current_user = {
    "id": None,
    "username": None,
    "role": None,
    "student_id": None
}

def log_audit(action, details=''):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO audit_log (user_id, action, details) VALUES (%s, %s, %s)",
            (current_user["id"], action, details)
        )
        conn.commit()
        conn.close()
    except:
        pass


# LOGIN

def login():
    username = input("Username: ")
    password = getpass.getpass("Password: ")

    hashed = hash_password(password)

    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute(
            "SELECT * FROM users WHERE username=%s AND password_hash=%s AND is_active=TRUE",
            (username, hashed)
        )

        user = cursor.fetchone()

        if user:
            current_user["id"] = user["id"]
            current_user["username"] = user["username"]
            current_user["role"] = user["role"]

            log_audit("LOGIN_SUCCESS", username)

            print("\nLogin successful")
            return True
        else:
            log_audit("LOGIN_FAILED", username)
            print("Invalid credentials")
            return False

    except Exception as e:
        print("Error: at login() function", e)
        return False
    

# MENUs

def menu_admin():
    while True:
        print("\n--- ADMIN MENU ---")
        print("1. Add Student")
        print("2. View Students")
        print("3. Search by Department")
        print("4. Update Student")
        print("5. Delete Student")
        print("6. Dashboard")
        print("7. Marks Distribution")
        print("8. Top Performers")
        print("9. Department Leaderboard")
        print("10. Add Bonus Marks")
        print("11. Export High Performers")
        print("12. View Audit Log")
        print("13. Create User")
        print("14. List Users")
        print("15. Toggle User Status")
        print("16. Create MySQL Users")
        print("0. Exit")

        choice = input("Enter choice: ")

        if choice == '0':
            print("\nexiting...\n")
            log_audit("LOGOUT", current_user["username"])
            break
        elif choice == '1':
            add_student()
        elif choice == '2':
            view_students()
        elif choice == '3':
            search_by_dept()
        elif choice == '4':
            update_student()
        elif choice == '5':
            delete_student()
        elif choice == '6':
            dashboard()
        elif choice == '7':
            marks_distribution()
        elif choice == '8':
            show_top_performers()
        elif choice == '9':
            dept_leaderboard()
        elif choice == '10':
            add_bonus_marks()
        elif choice == '11':
            export_high_performers()
        elif choice == '12':
            view_audit_log()
        elif choice == '13':
            create_user()
        elif choice == '14':
            list_users()
        elif choice == '15':
            toggle_user()
        elif choice == '16':
            create_mysql_users()
        else:
            print("Invalid choice")

        print("=" * 50)


def menu_faculty():
    while True:
        print("\n--- FACULTY MENU ---")
        print("1. Add Student")
        print("2. View Students")
        print("3. Search by Department")
        print("4. Update Student")
        print("5. Dashboard")
        print("6. Marks Distribution")
        print("7. Top Performers")
        print("8. Department Leaderboard")
        print("9. Add Bonus Marks")
        print("10. Export High Performers")
        print("0. Exit")

        choice = input("Enter choice: ")

        if choice == '0':
            print("\nexiting...\n")
            log_audit("LOGOUT", current_user["username"])
            break
        elif choice == '1':
            add_student()
        elif choice == '2':
            view_students()
        elif choice == '3':
            search_by_dept()
        elif choice == '4':
            update_student()
        elif choice == '5':
            dashboard()
        elif choice == '6':
            marks_distribution()
        elif choice == '7':
            show_top_performers()
        elif choice == '8':
            dept_leaderboard()
        elif choice == '9':
            add_bonus_marks()
        elif choice == '10':
            export_high_performers()
        else:
            print("Invalid choice")

        print("=" * 50)


def menu_student():
    while True:
        print("\n--- STUDENT MENU ---")
        print("1. View Own Record")
        print("2. Department Leaderboard")
        print("0. Exit")

        choice = input("Enter choice: ")

        if choice == '0':
            print("\nexiting...\n")
            log_audit("LOGOUT", current_user["username"])
            break
        elif choice == '1':
            view_own_record()
        elif choice == '2':
            dept_leaderboard()
        else:
            print("Invalid choice")
        
        print("=" * 50)

# FUNCTIONS

def add_student():
    try:
        name = input("Enter name: ")
        dept = input("Enter department: ")
        marks = float(input("Enter marks: "))
        if marks < 0 or marks > 100:
            print("Marks must be between 0 and 100")
            return

        conn = get_connection()
        cursor = conn.cursor()

        query = """
        INSERT INTO students (name, department, marks)
        VALUES (%s, %s, %s)
        """
        cursor.execute(query, (name, dept, marks))

        conn.commit()
        conn.close()

        log_audit("ADD_STUDENT", name)

        print("Student added successfully")

    except Exception as e:
        print("Error: at add_student() function", e)


def view_students():
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT id, name, department, marks FROM students ORDER BY id")
        rows = cursor.fetchall()

        log_audit("VIEW_STUDENTS", "")

        if not rows:
            print("No students found")
            return

        print("==================================================")
        print("------------------ STUDENT LIST ------------------")
        print("==================================================")
        print(f"{'ID':<5} {'Name':<20} {'Dept':<10} {'Marks':<10}")
        print("-" * 50)

        for row in rows:
            print(f"{row[0]:<5} {row[1]:<20} {row[2]:<10} {row[3]:<10}")

        print("==================================================")

        conn.close()

    except Exception as e:
        print("Error: at view_students() function", e)


def search_by_dept():
    try:
        dept = input("Enter department: ")

        conn = get_connection()
        cursor = conn.cursor()

        query = """
        SELECT id, name, department, marks
        FROM students
        WHERE LOWER(department) = LOWER(%s)
        ORDER BY id
        """
        cursor.execute(query, (dept,))
        rows = cursor.fetchall()

        log_audit("SEARCH_DEPT", dept)

        if not rows:
            print("No students found in this department")
            return

        print("\n--- SEARCH RESULTS ---")
        print(f"{'ID':<5} {'Name':<20} {'Dept':<10} {'Marks':<10}")
        print("-" * 50)

        for row in rows:
            print(f"{row[0]:<5} {row[1]:<20} {row[2]:<10} {row[3]:<10}")

        conn.close()

    except Exception as e:
        print("Error: at search_by_dept() function", e)


def update_student():
    try:
        student_id = int(input("Enter student ID: "))

        print("1. Update Marks")
        print("2. Update Department")

        choice = input("Enter choice: ")

        conn = get_connection()
        cursor = conn.cursor()

        if choice == '1':
            new_marks = float(input("Enter new marks: "))

            query = """
            UPDATE students
            SET marks = %s
            WHERE id = %s
            """
            cursor.execute(query, (new_marks, student_id))

            if cursor.rowcount == 0:
                print("Student not found")
                conn.close()
                return

            log_audit("UPDATE_MARKS", f"Student ID: {student_id}")

        elif choice == '2':
            new_dept = input("Enter new department: ")

            query = """
            UPDATE students
            SET department = %s
            WHERE id = %s
            """
            cursor.execute(query, (new_dept, student_id))

            if cursor.rowcount == 0:
                print("Student not found")
                conn.close()
                return

            log_audit("UPDATE_DEPT", f"Student ID: {student_id}")

        else:
            print("Invalid choice")
            return

        conn.commit()
        conn.close()

        print("Student updated successfully")

    except Exception as e:
        print("Error: at update_student() function", e)


def delete_student():
    try:
        student_id = int(input("Enter student ID to delete: "))

        confirm = input("Are you sure? (y/n): ")

        if confirm.lower() != 'y':
            print("Deletion cancelled")
            return

        conn = get_connection()
        cursor = conn.cursor()

        query = "DELETE FROM students WHERE id = %s"
        cursor.execute(query, (student_id,))

        if cursor.rowcount == 0:
                print("Student not found")
                conn.close()
                return

        conn.commit()
        conn.close()

        log_audit("DELETE_STUDENT", f"Student ID: {student_id}")

        print("Student deleted successfully")

    except Exception as e:
        print("Error: at delete_student() function", e)


def dashboard():
    try:
        conn = get_connection()
        cursor = conn.cursor()

        # Main statistics
        query = """
        SELECT 
            COUNT(*),
            AVG(marks),
            MAX(marks),
            MIN(marks)
        FROM students
        """

        cursor.execute(query)
        data = cursor.fetchone()

        # Total departments
        cursor.execute(
            "SELECT COUNT(DISTINCT department) FROM students"
        )
        dept_count = cursor.fetchone()[0]

        # Pass count
        cursor.execute(
            "SELECT COUNT(*) FROM students WHERE marks >= 40"
        )
        pass_count = cursor.fetchone()[0]

        # Fail count
        cursor.execute(
            "SELECT COUNT(*) FROM students WHERE marks < 40"
        )
        fail_count = cursor.fetchone()[0]

        # Topper
        cursor.execute("""
        SELECT name, marks
        FROM students
        ORDER BY marks DESC
        LIMIT 1
        """)
        topper = cursor.fetchone()

        total_students = data[0]

        pass_percentage = (
            (pass_count / total_students) * 100
            if total_students > 0 else 0
        )

        print("\n" + "=" * 45)
        print("        STUDENT DASHBOARD")
        print("=" * 45)

        print(f"Total Students      : {total_students}")
        print(f"Departments         : {dept_count}")

        print(f"Average Marks       : {round(data[1],2)}")
        print(f"Highest Marks       : {data[2]}")
        print(f"Lowest Marks        : {data[3]}")

        print(f"Pass Percentage     : {round(pass_percentage,2)}%")
        print(f"Failing Students    : {fail_count}")

        if topper:
            print(f"Top Performer       : {topper[0]} ({topper[1]})")


        conn.close()

        log_audit("VIEW_DASHBOARD", "")

    except Exception as e:
        print("Error: at dashboard() function", e)


def marks_distribution():
    try:
        conn = get_connection()
        cursor = conn.cursor()

        query = """
        SELECT
            SUM(CASE WHEN marks >= 90 THEN 1 ELSE 0 END) AS A,
            SUM(CASE WHEN marks BETWEEN 75 AND 89 THEN 1 ELSE 0 END) AS B,
            SUM(CASE WHEN marks BETWEEN 60 AND 74 THEN 1 ELSE 0 END) AS C,
            SUM(CASE WHEN marks BETWEEN 40 AND 59 THEN 1 ELSE 0 END) AS D,
            SUM(CASE WHEN marks < 40 THEN 1 ELSE 0 END) AS F
        FROM students
        """

        cursor.execute(query)
        data = cursor.fetchone()

        print("\n--- MARKS DISTRIBUTION ---")
        print("A Grade :", data[0])
        print("B Grade :", data[1])
        print("C Grade :", data[2])
        print("D Grade :", data[3])
        print("F Grade :", data[4])

        conn.close()

        log_audit("MARKS_DISTRIBUTION", "")

    except Exception as e:
        print("Error: at marks_distribution() function", e)


def show_top_performers():
    try:
        conn = get_connection()
        cursor = conn.cursor()

        query = """
        SELECT id, name, department, marks
        FROM students
        ORDER BY marks DESC
        LIMIT 3
        """

        cursor.execute(query)
        rows = cursor.fetchall()

        if not rows:
            print("No student records found")
            return

        print("=" * 45)

        print("\n--- TOP 3 PERFORMERS ---")
        print(f"{'ID':<5} {'Name':<20} {'Dept':<10} {'Marks':<10}")
        print("-" * 50)

        for row in rows:
            print(f"{row[0]:<5} {row[1]:<20} {row[2]:<10} {row[3]:<10}")


        conn.close()

        log_audit("TOP_PERFORMERS", "")

    except Exception as e:
        print("Error: at show_top_performers() function", e)


def dept_leaderboard():
    try:
        conn = get_connection()
        cursor = conn.cursor()

        query = """
        SELECT 
            department,
            AVG(marks) AS avg_marks
        FROM students
        GROUP BY department
        ORDER BY avg_marks DESC
        """

        cursor.execute(query)
        rows = cursor.fetchall()

        if not rows:
            print("No data found")
            return

        print("=" * 45)

        print("\n--- DEPARTMENT LEADERBOARD ---")
        print(f"{'Department':<15} {'Average Marks':<15}")
        print("-" * 35)

        for row in rows:
            print(f"{row[0]:<15} {round(row[1],2):<15}")


        conn.close()

        log_audit("DEPT_LEADERBOARD", "")

    except Exception as e:
        print("Error: at dept_leaderboard() function", e)


def add_bonus_marks():
    try:
        student_id = int(input("Enter student ID: "))
        bonus = float(input("Enter bonus marks: "))

        if bonus < 0:
            print("Invalid bonus")
            return

        conn = get_connection()
        cursor = conn.cursor()

        # Check student exists
        cursor.execute(
            "SELECT name, marks FROM students WHERE id = %s",
            (student_id,)
        )

        row = cursor.fetchone()

        if not row:
            print("Student not found")
            conn.close()
            return

        student_name = row[0]

        query = """
        UPDATE students
        SET marks = LEAST(marks + %s, 100)
        WHERE id = %s
        """

        cursor.execute(query, (bonus, student_id))

        conn.commit()
        conn.close()

        log_audit(
            "ADD_BONUS",
            f"{student_name} +{bonus}"
        )
        current_marks = float(row[1])
        print(f"Current Marks: {current_marks}")
        print(f"New Marks: {min(current_marks + bonus, 100)}")

        print("Bonus marks added successfully")

    except Exception as e:
        print("Error: at add_bonus_marks() function", e)


def export_high_performers():
    try:
        conn = get_connection()
        cursor = conn.cursor()

        query = """
        SELECT id, name, department, marks
        FROM students
        WHERE marks > (SELECT AVG(marks) FROM students)
        """

        cursor.execute(query)
        rows = cursor.fetchall()

        if not rows:
            print("No high performers found")
            return

        filename = "high_performers_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S") + ".csv"

        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)

            writer.writerow(["ID", "Name", "Department", "Marks"])

            for row in rows:
                writer.writerow(row)

        conn.close()

        log_audit("EXPORT_HIGH_PERFORMERS", filename)

        print("CSV exported successfully")
        print("File:", filename)

    except Exception as e:
        print("Error: at export_high_performers() function", e)


def view_audit_log():
    try:
        conn = get_connection()
        cursor = conn.cursor()

        query = """
        SELECT id, user_id, action, details, timestamp
        FROM audit_log
        ORDER BY timestamp DESC
        LIMIT 20
        """

        cursor.execute(query)
        rows = cursor.fetchall()

        if not rows:
            print("No audit logs found")
            return

        print("=" * 45)

        print("\n--- AUDIT LOGS ---")
        print(f"{'ID':<5} {'UserID':<8} {'Action':<25} {'Details':<25} {'Timestamp'}")
        print("-" * 90)

        for row in rows:
            print(f"{row[0]:<5} {str(row[1]):<8} {row[2]:<25} {str(row[3]):<25} {row[4]}")

        
        conn.close()

        log_audit("VIEW_AUDIT_LOG", "")

    except Exception as e:
        print("Error: at view_audit_log() function", e)


def create_user():
    try:
        username = input("Enter username: ")
        password = getpass.getpass("Enter password: ")
        role = input("Enter role (admin/faculty/student): ").lower()
        if role not in ['admin', 'faculty', 'student']:
            print("Invalid role")
            return

        hashed = hash_password(password)

        conn = get_connection()
        cursor = conn.cursor()

        query = """
        INSERT INTO users (username, password_hash, role)
        VALUES (%s, %s, %s)
        """

        cursor.execute(query, (username, hashed, role))

        user_id = cursor.lastrowid

        # If student, also create student record
        if role == 'student':
            name = input("Enter student name: ")
            dept = input("Enter department: ")
            marks = float(input("Enter marks: "))

            student_query = """
            INSERT INTO students (name, department, marks, user_id)
            VALUES (%s, %s, %s, %s)
            """

            cursor.execute(student_query, (name, dept, marks, user_id))

        conn.commit()
        conn.close()

        log_audit("CREATE_USER", username)

        print("User created successfully")

    except Exception as e:
        print("Error: (at create_user() function)", e)


def list_users():
    try:
        conn = get_connection()
        cursor = conn.cursor()

        query = """
        SELECT username, role, is_active, created_at
        FROM users
        ORDER BY id
        """

        cursor.execute(query)
        rows = cursor.fetchall()

        if not rows:
            conn.close()
            print("No users found")
            return

        print("=" * 45)

        print("\n--- USERS LIST ---")
        print(f"{'Username':<20} {'Role':<12} {'Active':<10} {'Created At'}")
        print("-" * 60)

        for row in rows:
            status = "Yes" if row[2] else "No"

            print(f"{row[0]:<20} {row[1]:<12} {status:<10} {row[3]}")

        print("=" * 45)

        conn.close()

        log_audit("LIST_USERS", "")

    except Exception as e:
        print("Error: (at list_users() function)", e)


def toggle_user():
    try:
        username = input("Enter username: ")

        conn = get_connection()
        cursor = conn.cursor()

        # Get current status
        cursor.execute(
            "SELECT is_active FROM users WHERE username = %s",
            (username,)
        )

        row = cursor.fetchone()

        if not row:
            print("User not found")
            return

        current_status = row[0]

        # Toggle status
        new_status = not current_status

        cursor.execute(
            "UPDATE users SET is_active = %s WHERE username = %s",
            (new_status, username)
        )

        conn.commit()
        conn.close()

        log_audit("TOGGLE_USER", username)

        if new_status:
            print("User enabled successfully")
        else:
            print("User disabled successfully")

    except Exception as e:
        print("Error: (at toggle_user() function)", e)


def create_mysql_users():
    try:
        conn = get_connection()
        cursor = conn.cursor()

        # Admin user
        cursor.execute("""
        CREATE USER IF NOT EXISTS 'spa_admin'@'localhost'
        IDENTIFIED BY 'admin123'
        """)

        cursor.execute("""
        GRANT ALL PRIVILEGES
        ON spa_enhanced_db.* 
        TO 'spa_admin'@'localhost'
        """)

        # Faculty user
        cursor.execute("""
        CREATE USER IF NOT EXISTS 'spa_faculty'@'localhost'
        IDENTIFIED BY 'faculty123'
        """)

        cursor.execute("""
        GRANT SELECT, INSERT, UPDATE
        ON spa_enhanced_db.* 
        TO 'spa_faculty'@'localhost'
        """)

        # Student user
        cursor.execute("""
        CREATE USER IF NOT EXISTS 'spa_student'@'localhost'
        IDENTIFIED BY 'student123'
        """)

        cursor.execute("""
        GRANT SELECT
        ON spa_enhanced_db.* 
        TO 'spa_student'@'localhost'
        """)

        cursor.execute("FLUSH PRIVILEGES")

        conn.commit()
        conn.close()

        log_audit("CREATE_MYSQL_USERS", "")

        print("MySQL users created successfully")

    except Exception as e:
        print("Error: (at create_mysql_users() function)", e) 


def view_own_record():
    try:
        conn = get_connection()
        cursor = conn.cursor()

        query = """
        SELECT id, name, department, marks
        FROM students
        WHERE user_id = %s
        """

        cursor.execute(query, (current_user["id"],))
        row = cursor.fetchone()

        if not row:
            print("No student record found")
            return

        print("\n--- YOUR RECORD ---")
        print("ID         :", row[0])
        print("Name       :", row[1])
        print("Department :", row[2])
        print("Marks      :", row[3])

        conn.close()

        log_audit("VIEW_OWN_RECORD", current_user["username"])

    except Exception as e:
        print("Error: at view_own_record() function", e)

# MAIN FUNCTION

def main():
    if not login(): 
        return
    role = current_user['role']

    if role == 'admin':
        print(f"\nWelcome, {current_user['username']} ({current_user['role']})\n")
        menu_admin()
    elif role == 'faculty':
        print(f"\nWelcome, {current_user['username']} ({current_user['role']})\n")
        menu_faculty()
    elif role == 'student':
        print(f"\nWelcome, {current_user['username']} ({current_user['role']})\n")
        menu_student()

if __name__ == '__main__':
    main()
