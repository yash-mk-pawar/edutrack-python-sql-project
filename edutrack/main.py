from database_manager import DatabaseManager
from authentication_manager import AuthenticationManager
from login_manager import LoginManager
from student_manager import StudentManager
from mock_manager import MockManager  # Import the new mock module

def main():
    db = DatabaseManager()
    db.initialize_database()
    
    auth = AuthenticationManager(db)
    login_mgr = LoginManager(db)
    student_mgr = StudentManager(db)
    mock_mgr = MockManager(db)  # Initialize Mock Manager
    
    current_user_id = None
    current_session_id = None
    
    while True:
        print("\n==============================")
        print("      EDUTRACK SYSTEM         ")
        print("==============================")
        
        if current_user_id is None:
            print("[1] Register New User")
            print("[2] Login")
            print("[3] Exit")
            choice = input("Enter your choice: ").strip()
            
            if choice == '1':
                auth.register_user()
            elif choice == '2':
                current_user_id, current_session_id = login_mgr.login_user()
            elif choice == '3':
                print("Exiting EduTrack. Goodbye!")
                break
            else:
                print("Invalid choice.")
        else:
            print(f"\n--- Dashboard (User ID: {current_user_id}) ---")
            print("[1] Create Batch Code")
            print("[2] View All Batches")
            print("[3] Register New Student")
            print("[4] View Students by Batch")
            print("[5] Record Mock Test & Ratings")
            print("[6] View Student Mock Performance")
            print("[7] Logout")
            print("[8] Exit System")
            choice = input("Enter your choice: ").strip()
            
            if choice == '1':
                student_mgr.create_batch(current_user_id)
            elif choice == '2':
                student_mgr.view_all_batches()
            elif choice == '3':
                student_mgr.register_student(current_user_id)
            elif choice == '4':
                student_mgr.view_students_in_batch()
            elif choice == '5':
                mock_mgr.record_mock_test(current_user_id)
            elif choice == '6':
                mock_mgr.view_student_mock_reports()
            elif choice == '7':
                login_mgr.logout_user(current_session_id)
                current_user_id = None
                current_session_id = None
            elif choice == '8':
                if current_session_id:
                    login_mgr.logout_user(current_session_id)
                print("Exiting EduTrack. Goodbye!")
                break
            else:
                print("Invalid choice.")

if __name__ == "__main__":
    main()