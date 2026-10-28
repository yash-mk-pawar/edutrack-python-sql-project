import time
from database_manager import DatabaseManager

def seed_database():
    db = DatabaseManager()
    db.initialize_database()
    print("Connecting to database and seeding dummy data...")
    
    current_time = time.time()
    
    # 1. Insert a Dummy User (if not already exists)
    db.execute_query('''
        INSERT OR IGNORE INTO Users (user_id, full_name, user_name, phone_number, email, address, password, created_at, account_status)
        VALUES (1, 'Admin Trainer', 'admin_trainer', '9876543210', 'trainer@edutrack.com', 'Pune Hadapsar', 'admin123', ?, 'Active')
    ''', (current_time,))
    
    # 2. Insert Dummy Batch Codes
    batches = [
        ('PY-DATA-01', 1, current_time),
        ('JAVA-DEV-02', 1, current_time)
    ]
    for batch_code, user_id, timestamp in batches:
        db.execute_query('''
            INSERT OR IGNORE INTO BatchCodes (batch_code, user_id, created_at)
            VALUES (?, ?, ?)
        ''', (batch_code, user_id, timestamp))
        
    # 3. Insert Dummy Students
    students = [
        ('Yash Pawar', 'ROLL101', 'PY-DATA-01', '9123456789', 'yash@gmail.com', 'Pune', current_time, 1),
        ('Priya Patil', 'ROLL102', 'PY-DATA-01', '9234567890', 'priya@gmail.com', 'Mumbai', current_time, 1),
        ('Amit Verma', 'ROLL201', 'JAVA-DEV-02', '9345678901', 'amit@gmail.com', 'Nagpur', current_time, 1)
    ]
    for name, roll, batch, phone, email, address, adm_time, usr_id in students:
        db.execute_query('''
            INSERT OR IGNORE INTO Students (full_name, roll_number, batch_code, phone_number, email, address, addmission_time, created_by_user_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (name, roll, batch, phone, email, address, adm_time, usr_id))

    # 4. Insert Dummy Mock Test & Ratings for Yash (ROLL101)
    # First get Yash's student_id
    student = db.fetch_one("SELECT student_id FROM Students WHERE roll_number = ?", ('ROLL101',))
    if student:
        student_id = student[0]
        
        # Insert Mock Test record
        db.execute_query('''
            INSERT OR IGNORE INTO MockTests (mock_test_id, student_id, mock_type, mock_number, taken_at, created_by_user_id)
            VALUES (1, ?, 'Technical', 1, ?, 1)
        ''', (student_id, current_time))
        
        # Insert Mock Rating record
        db.execute_query('''
            INSERT OR IGNORE INTO MockRatings (mock_rating_id, mock_test_id, technical_rating, programming_rating, communication_rating, entered_by_user_id, created_at)
            VALUES (1, 1, 'Good', 'Excellent', 'Average', 1, ?)
        ''', (current_time,))

    print("Dummy data seeded successfully!")
    print("\nTest Credentials to Login:")
    print("  Username: admin_trainer")
    print("  Password: admin123")
    print("\nTest Student Roll Numbers for Practice:")
    print("  - ROLL101 (Yash Pawar in PY-DATA-01)")
    print("  - ROLL102 (Priya Patil in PY-DATA-01)")
    print("  - ROLL201 (Amit Verma in JAVA-DEV-02)")

if __name__ == '__main__':
    seed_database()