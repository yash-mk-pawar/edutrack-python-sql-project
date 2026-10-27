import sqlite3
class DatabaseManager:
    
    def __init__(self):
        self.db_name = "edutrack.db"
        
    def connect_database(self):
        connection = sqlite3.connect(self.db_name)
        return connection
    
    def initialize_database(self):
        connection = self.connect_database()
        cursor = connection.cursor()
        
        # User Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Users (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                full_name TEXT NOT NULL,
                user_name TEXT NOT NULL UNIQUE,
                phone_number TEXT NOT NULL UNIQUE,
                email TEXT NOT NULL UNIQUE,
                address TEXT NOT NULL,
                password TEXT NOT NULL,
                created_at real NOT NULL,
                account_status TEXT NOT NULL)''')
        
        # BatchCodes Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS BatchCodes (
                batch_id INTEGER PRIMARY KEY AUTOINCREMENT,
                batch_code TEXT NOT NULL UNIQUE,
                user_id INTEGER NOT NULL,
                created_at real NOT NULL,
                FOREIGN KEY (user_id) REFERENCES Users(user_id))''')
        
        # Students Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Students (
                student_id INTEGER PRIMARY KEY AUTOINCREMENT,
                full_name TEXT NOT NULL,
                roll_number TEXT NOT NULL UNIQUE,
                batch_code TEXT NOT NULL,
                phone_number TEXT NOT NULL,
                email TEXT NOT NULL,
                address TEXT NOT NULL,
                addmission_time real NOT NULL,
                created_by_user_id INTEGER NOT NULL,
                FOREIGN KEY (batch_code) REFERENCES BatchCodes(batch_code),
                FOREIGN KEY (created_by_user_id) REFERENCES Users(user_id))''')
        
        cursor.execute('''
                CREATE TABLE IF NOT EXISTS MockTests (
                    mock_test_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    student_id INTEGER NOT NULL UNIQUE,
                    mock_type TEXT NOT NULL UNIQUE,
                    mock_number INTEGER NOT NULL UNIQUE,
                    taken_at real NOT NULL,
                    created_by_user_id INTEGER NOT NULL)''')
        
        # MockRatings Table
        cursor.execute('''
                CREATE TABLE IF NOT EXISTS MockRatings (
                    mock_rating_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    mock_test_id INTEGER NOT NULL UNIQUE,
                    technical_rating TEXT NOT NULL,
                    programming_rating TEXT NOT NULL,
                    communication_rating TEXT NOT NULL,
                    entered_by_user_id INTEGER NOT NULL,
                    created_at real NOT NULL)''')
        
        cursor.execute('''
                CREATE TABLE IF NOT EXISTS Sessions (
                    session_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    login_timestamp real NOT NULL,
                    logout_timestamp real,
                    session_duration real,
                    session_status TEXT NOT NULL)''')
        
        connection.commit()
        connection.close()
        
        
    def execute_query(self, query, parameters=()):
        connection = self.connect_database()
        cursor = connection.cursor()
        cursor.execute(query, parameters)
        connection.commit()
        connection.close()
        

    def fetch_one(self, query, parameters=()):
        connection = self.connect_database()
        cursor = connection.cursor()
        cursor.execute(query, parameters)
        record = cursor.fetchone()
        connection.close()
        return record

    def fetch_all(self, query, parameters=()):
        connection = self.connect_database()
        cursor = connection.cursor()
        cursor.execute(query, parameters)
        records = cursor.fetchall()
        connection.close()
        return records
    
    def fetch_many(self, query, parameters=(), record_count=5):
        connection = self.connect_database()
        cursor = connection.cursor()
        cursor.execute(query, parameters)
        records = cursor.fetchmany(record_count)
        connection.close()
        return records
    
    def execute_many(self, query, records):
        connection = self.connect_database()
        cursor = connection.cursor()
        cursor.executemany(query, records)
        connection.commit()
        connection.close()
    
    