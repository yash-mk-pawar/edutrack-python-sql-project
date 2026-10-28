import time
from authentication_manager import AuthenticationManager

class LoginManager:
    def __init__(self, database_manager):
        self.database_manager = database_manager
        # Instantiate AuthenticationManager to reuse features like verify_captcha()
        self.auth_helper = AuthenticationManager(database_manager)
        self.failed_attempts = 0
        self.lockout_until = 0

    def display_timestamp(self, timestamp):
        print(f"Date : {time.strftime('%d-%m-%Y', time.localtime(timestamp))}")
        print(f"Weekday : {time.strftime('%A', time.localtime(timestamp))}")
        print(f"Time : {time.strftime('%H:%M:%S %p', time.localtime(timestamp))}")

    def login_user(self):
        print('\n---- Qspider Hadapsar Login ----')
        
        # Check for temporary lockout
        if time.time() < self.lockout_until:
            remaining_time = int(self.lockout_until - time.time())
            print(f"Too many failed attempts. Try again in {remaining_time} seconds.")
            return None, None
        
        username = input("Enter Username: ").strip()
        password = input("Enter Password: ").strip()
        
        if username == '' or password == '':
            print("Username and Password are required.")
            return None, None
        
        # Query matching the 'user_name' column defined in DatabaseManager
        user = self.database_manager.fetch_one(
            '''SELECT user_id, password, account_status, full_name FROM Users WHERE user_name = ?''', 
            (username,)
        )
        
        if user is None:
            self.handle_failed_login()
            print("Invalid username or password.")
            return None, None
            
        user_id, stored_password, account_status, full_name = user
        
        if account_status != 'Active':
            print(f"Account status is {account_status}. Access denied.")
            return None, None
            
        if password != stored_password:
            self.handle_failed_login()
            print("Invalid username or password.")
            return None, None
        
        # Reusing the secure CAPTCHA check from AuthenticationManager
        if not self.auth_helper.verify_captcha():
            print("Login Cancelled due to Captcha failure.")
            return None, None
            
        # Reset failed login tracking on success
        self.failed_attempts = 0
        self.lockout_until = 0
        
        # Record session in the Sessions table
        login_time = time.time()
        self.database_manager.execute_query(
            '''INSERT INTO Sessions (user_id, login_timestamp, session_status) VALUES (?, ?, ?)''',
            (user_id, login_time, 'Active')
        )
        
        # Fetch the active session ID
        session_record = self.database_manager.fetch_one(
            '''SELECT session_id FROM Sessions WHERE user_id = ? AND session_status = 'Active' ORDER BY login_timestamp DESC LIMIT 1''',
            (user_id,)
        )
        session_id = session_record[0] if session_record else None
        
        print(f"\nLogin Successful! Welcome back, {full_name}.")
        self.display_timestamp(login_time)
        
        return user_id, session_id

    def handle_failed_login(self):
        self.failed_attempts += 1
        if self.failed_attempts >= 3:
            self.lockout_until = time.time() + 60  # Lock out for 60 seconds
            print("❌ Account temporarily locked for 60 seconds due to 3 consecutive failed login attempts.")

    def logout_user(self, session_id):
        if session_id is None:
            print("No active session found.")
            return
            
        logout_time = time.time()
        
        # Fetch login timestamp to calculate total session duration
        session = self.database_manager.fetch_one(
            '''SELECT login_timestamp FROM Sessions WHERE session_id = ?''',
            (session_id,)
        )
        
        if session:
            login_time = session[0]
            session_duration = logout_time - login_time
            
            # Update Session record to closed
            self.database_manager.execute_query(
                '''UPDATE Sessions SET logout_timestamp = ?, session_duration = ?, session_status = ? WHERE session_id = ?''',
                (logout_time, session_duration, 'Closed', session_id)
            )
            print("\nLogged out successfully.")
            self.display_timestamp(logout_time)