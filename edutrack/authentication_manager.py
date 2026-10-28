import random  
import re
import time

class AuthenticationManager:
    def __init__(self, database_manager):
        self.database_manager = database_manager
        self.failed_attempts = 0
        self.lockout_until = 0

    def display_timestamp(self, timestamp):
        print(f"Date : {time.strftime('%d-%m-%Y', time.localtime(timestamp))}")
        print(f"Weekday : {time.strftime('%A', time.localtime(timestamp))}")
        print(f"Time : {time.strftime('%H:%M:%S %p', time.localtime(timestamp))}")
    
    def verify_otp(self):
        otp = str(random.randint(100000, 999999))
        expiry_time = time.time() + 120  # OTP valid for 2 minutes
        attempts = 0
        print(f"OTP for demonstration : {otp}")
        
        while attempts < 3:
            entered_otp = input("Enter OTP: ")
            
            if time.time() > expiry_time:
                print("OTP expired.")
                return False
            
            if entered_otp == otp:
                print("OTP verified.")
                return True
            
            attempts += 1
            print(f"Incorrect OTP.")
            
        return False
    
    def verify_captcha(self):
        characters = ''
        for i in range(48, 123):
            if 'A' <= chr(i) <= 'Z' or 'a' <= chr(i) <= 'z' or '0' <= chr(i) <= '9':
                characters += chr(i)
        
        captcha = ''
        
        for i in range(6):
            captcha += random.choice(characters)
            
        attempts = 0
        while attempts < 3:
            print(f"Captcha: {captcha}")
            entered_captcha = input("Enter CAPTCHA or Refresh: ")
            
            if entered_captcha == 'Refresh':
                captcha = ''
                for i in range(6):
                    captcha += random.choice(characters)
            
            elif entered_captcha == captcha:
                print("Captcha verified.")
                return True
            
            else:
                attempts += 1
                print("Incorrect Captcha.")
            
    def register_user(self):
        print('\n---- Qspider Hadapsar Registration ----')
        full_name = input("Enter Full Name: ").strip()
        username = input("Enter Username: ").strip()
        phone_number = input("Enter Phone Number: ").strip()
        email = input("Enter Email: ").strip()
        address = input("Enter Address: ").strip()
        password = input("Enter Password: ").strip()
        confirm_password = input("Confirm Password: ").strip()
        
        if full_name == '' or username == '' or phone_number == '' or email == '' or address == '' or password == '':
            print("All fields are required.")
            return
        
        if password != confirm_password:
            print("Passwords doesn't match.")
            return
        
        if re.fullmatch('\w{4,20}',username) is None:
            print("Username must contain 4-20 letters, digits/ or underscores.")
            return
        
        if re.fullmatch('\d{10}', phone_number) is None:
            print("Enter a valid 10-digit Phone Number.")
            return
        
        if re.fullmatch('[^@\s]+@[^@\s]+\.[^@\s]+', email) is None:
            print("Enter a valid Email Address.")
            return 
        
        existing_user = self.database_manager.fetch_one('''SELECT user_id FROM Users WHERE user_name = ? or email = ? or phone_number = ?''', (username, email, phone_number))
        
        if existing_user is not None:
            print("User with this username, email, or phone number already exists.")
            return
        
        if not self.verify_otp():
            print("Registration Cancelled.")
            return
        
        if not self.verify_captcha():
            print("Registration Cancelled.")
            return
        
        current_time = time.time()
        
        self.database_manager.execute_query('''
            INSERT INTO Users (full_name, user_name, phone_number, email, address, password, created_at, account_status) VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
            (full_name, username, phone_number, email, address, password, current_time, 'Active'))
        
        print("Registration Successful.")
        self.display_timestamp(current_time)