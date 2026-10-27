import time
import random


class Demonstration:

    '''

    def display_timestamp(self, timestamp):
        print(f"Date : {time.strftime('%d-%m-%Y', time.localtime(timestamp))}")
        print(f"Weekday : {time.strftime('%A', time.localtime(timestamp))}")
        print(f"Time : {time.strftime('%H:%M:%S %p', time.localtime(timestamp))}")
        

    
    '''
    #Checked
    '''
    def verify_otp(self):
        otp = str(random.randint(100000, 999999))
        expiry_time = time.time() + 120  # OTP valid for 2 minutes
        attempts = 0
        print(f"OTP for demonstration : {otp}")
    '''
    #Checked


obj1 = Demonstration()
#obj1.verify_otp()
#obj1.display_timestamp(None, time.time())  
    
