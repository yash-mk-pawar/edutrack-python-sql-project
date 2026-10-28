import time
import re

class StudentManager:
    def __init__(self, database_manager):
        self.database_manager = database_manager

    def display_timestamp(self, timestamp):
        print(f"Date : {time.strftime('%d-%m-%Y', time.localtime(timestamp))}")
        print(f"Weekday : {time.strftime('%A', time.localtime(timestamp))}")
        print(f"Time : {time.strftime('%H:%M:%S %p', time.localtime(timestamp))}")

    def create_batch(self, user_id):
        print('\n---- Create New Batch Code ----')
        batch_code = input("Enter Batch Code (e.g., PY-DATA-01): ").strip().upper()
        
        if not batch_code:
            print("Batch code cannot be empty.")
            return

        # Check if batch code already exists
        existing = self.database_manager.fetch_one(
            "SELECT batch_id FROM BatchCodes WHERE batch_code = ?", (batch_code,)
        )
        if existing:
            print("Batch code already exists.")
            return

        created_at = time.time()
        self.database_manager.execute_query(
            "INSERT INTO BatchCodes (batch_code, user_id, created_at) VALUES (?, ?, ?)",
            (batch_code, user_id, created_at)
        )
        print(f"Batch '{batch_code}' created successfully!")
        self.display_timestamp(created_at)

    def view_all_batches(self):
        print('\n---- Existing Batches ----')
        batches = self.database_manager.fetch_all("SELECT batch_code, created_at FROM BatchCodes")
        if not batches:
            print("No batches found.")
            return
        
        for code, timestamp in batches:
            date_str = time.strftime('%d-%m-%Y', time.localtime(timestamp))
            print(f"- {code} (Created on: {date_str})")

    def register_student(self, user_id):
        print('\n---- Student Admission ----')
        full_name = input("Enter Student Full Name: ").strip()
        roll_number = input("Enter Roll Number: ").strip()
        batch_code = input("Enter Batch Code: ").strip().upper()
        phone_number = input("Enter Phone Number: ").strip()
        email = input("Enter Email: ").strip()
        address = input("Enter Address: ").strip()

        if not all([full_name, roll_number, batch_code, phone_number, email, address]):
            print("All fields are required.")
            return

        if not re.fullmatch(r'\d{10}', phone_number):
            print("Enter a valid 10-digit Phone Number.")
            return

        if not re.fullmatch(r'[^@\s]+@[^@\s]+\.[^@\s]+', email):
            print("Enter a valid Email Address.")
            return

        # Verify batch code exists
        batch = self.database_manager.fetch_one(
            "SELECT batch_id FROM BatchCodes WHERE batch_code = ?", (batch_code,)
        )
        if not batch:
            print("Error: Batch code does not exist. Please create the batch first.")
            return

        # Check if roll number already exists
        existing_student = self.database_manager.fetch_one(
            "SELECT student_id FROM Students WHERE roll_number = ?", (roll_number,)
        )
        if existing_student:
            print("A student with this Roll Number already exists.")
            return

        admission_time = time.time()
        self.database_manager.execute_query('''
            INSERT INTO Students (full_name, roll_number, batch_code, phone_number, email, address, addmission_time, created_by_user_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
            (full_name, roll_number, batch_code, phone_number, email, address, admission_time, user_id)
        )
        print("Student Admission Successful!")
        self.display_timestamp(admission_time)

    def view_students_in_batch(self):
        print('\n---- View Students by Batch ----')
        batch_code = input("Enter Batch Code to view students: ").strip().upper()
        
        students = self.database_manager.fetch_all(
            "SELECT roll_number, full_name, phone_number, email FROM Students WHERE batch_code = ?",
            (batch_code,)
        )
        
        if not students:
            print(f"No students found for batch '{batch_code}'.")
            return

        print(f"\nStudents enrolled in {batch_code}:")
        print("-" * 50)
        for roll, name, phone, email in students:
            print(f"Roll No: {roll} | Name: {name} | Phone: {phone} | Email: {email}")
        print("-" * 50)