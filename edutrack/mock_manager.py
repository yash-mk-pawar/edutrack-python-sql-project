import time

class MockManager:
    def __init__(self, database_manager):
        self.database_manager = database_manager

    def display_timestamp(self, timestamp):
        print(f"Date : {time.strftime('%d-%m-%Y', time.localtime(timestamp))}")
        print(f"Weekday : {time.strftime('%A', time.localtime(timestamp))}")
        print(f"Time : {time.strftime('%H:%M:%S %p', time.localtime(timestamp))}")

    def record_mock_test(self, user_id):
        print('\n---- Record Mock Test & Ratings ----')
        roll_number = input("Enter Student Roll Number: ").strip()
        
        # Verify student exists
        student = self.database_manager.fetch_one(
            "SELECT student_id, full_name FROM Students WHERE roll_number = ?", (roll_number,)
        )
        if not student:
            print("Error: Student with this roll number does not exist.")
            return

        student_id, full_name = student
        print(f"Found Student: {full_name}")

        mock_type = input("Enter Mock Type (e.g., Technical, HR, Coding): ").strip().title()
        try:
            mock_number = int(input("Enter Mock Number (e.g., 1, 2, 3): ").strip())
        except ValueError:
            print("Invalid mock number. Please enter a valid integer.")
            return

        taken_at = time.time()

        try:
            # Insert Mock Test record
            self.database_manager.execute_query(
                '''INSERT INTO MockTests (student_id, mock_type, mock_number, taken_at, created_by_user_id)
                   VALUES (?, ?, ?, ?, ?)''',
                (student_id, mock_type, mock_number, taken_at, user_id)
            )
            
            # Fetch the generated mock_test_id
            mock_test_record = self.database_manager.fetch_one(
                '''SELECT mock_test_id FROM MockTests WHERE student_id = ? AND mock_type = ? AND mock_number = ?''',
                (student_id, mock_type, mock_number)
            )
            
            if not mock_test_record:
                print("Error recording mock test.")
                return
            
            mock_test_id = mock_test_record[0]

            # Enter Ratings
            print("\nEnter Ratings (e.g., Excellent, Good, Average, Needs Improvement)")
            tech_rating = input("Technical Rating: ").strip()
            prog_rating = input("Programming Rating: ").strip()
            comm_rating = input("Communication Rating: ").strip()

            if not all([tech_rating, prog_rating, comm_rating]):
                print("All ratings are required.")
                return

            # Insert Mock Rating record
            self.database_manager.execute_query(
                '''INSERT INTO MockRatings (mock_test_id, technical_rating, programming_rating, communication_rating, entered_by_user_id, created_at)
                   VALUES (?, ?, ?, ?, ?, ?)''',
                (mock_test_id, tech_rating, prog_rating, comm_rating, user_id, time.time())
            )

            print("Mock Test and Ratings Saved Successfully!")
            self.display_timestamp(taken_at)

        except Exception as e:
            print(f"Error: Could not record mock test. (Note: Ensure unique mock types/numbers per student constraints). Details: {e}")

    def view_student_mock_reports(self):
        print('\n---- View Student Mock Performance ----')
        roll_number = input("Enter Student Roll Number: ").strip()

        student = self.database_manager.fetch_one(
            "SELECT student_id, full_name FROM Students WHERE roll_number = ?", (roll_number,)
        )
        if not student:
            print("Error: Student not found.")
            return

        student_id, full_name = student
        
        records = self.database_manager.fetch_all(
            '''SELECT m.mock_type, m.mock_number, m.taken_at, r.technical_rating, r.programming_rating, r.communication_rating
               FROM MockTests m
               JOIN MockRatings r ON m.mock_test_id = r.mock_test_id
               WHERE m.student_id = ?''',
            (student_id,)
        )

        if not records:
            print(f"No mock test records found for {full_name}.")
            return

        print(f"\nMock Performance Report for: {full_name} (Roll: {roll_number})")
        print("-" * 75)
        for m_type, m_num, timestamp, tech, prog, comm in records:
            date_str = time.strftime('%d-%m-%Y', time.localtime(timestamp))
            print(f"Type: {m_type} #{m_num} | Date: {date_str}")
            print(f"  - Technical Rating     : {tech}")
            print(f"  - Programming Rating   : {prog}")
            print(f"  - Communication Rating : {comm}")
            print("-" * 75)