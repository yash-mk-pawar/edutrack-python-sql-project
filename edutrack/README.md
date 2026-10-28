# EduTrack - Institute & Student Performance Tracking System

EduTrack is a robust, modular console-based application built in Python and SQLite designed for training institutes (such as QSpiders Hadapsar) to manage user authentication, session tracking, batch codes, student admissions, and mock test performance ratings.

---

## 📂 Project Architecture

EduTrack is structured using a clean modular design pattern to separate concerns across different functional files:

1. **`database_manager.py`**: Handles all SQLite database connection pooling, table schema initialization, and raw query executions.
2. **`authentication_manager.py`**: Manages secure user registration, OTP verification with expiry, and interactive randomized CAPTCHA verification.
3. **`login_manager.py`**: Handles user login authentication, account security lockouts after consecutive failed attempts, and active session duration logging.
4. **`student_manager.py`**: Manages institute batch code creation and student admission rosters with validation checks.
5. **`mock_manager.py`**: Records student mock tests and evaluates performance ratings across technical, programming, and communication criteria.
6. **`seed_data.py`**: A utility script to quickly pre-populate the database with test accounts, batches, students, and mock reports.
7. **`main.py`**: The core application entry point featuring a command-line interface (CLI) menu loop to route user actions.

---

## 🗄️ Database Schema

The SQLite database (`edutrack.db`) consists of the following interconnected tables:
* **`Users`**: Stores administrator and trainer credentials (`user_id`, `full_name`, `user_name`, `phone_number`, `email`, `address`, `password`, `created_at`, `account_status`).
* **`Sessions`**: Tracks active user logins, login/logout timestamps, and total session durations (`session_id`, `user_id`, `login_timestamp`, `logout_timestamp`, `session_duration`, `session_status`).
* **`BatchCodes`**: Stores unique training batches created by users (`batch_id`, `batch_code`, `user_id`, `created_at`).
* **`Students`**: Stores student profiles mapped to specific batches (`student_id`, `full_name`, `roll_number`, `batch_code`, `phone_number`, `email`, `address`, `addmission_time`, `created_by_user_id`).
* **`MockTests`**: Records mock examination instances for students (`mock_test_id`, `student_id`, `mock_type`, `mock_number`, `taken_at`, `created_by_user_id`).
* **`MockRatings`**: Stores performance evaluations tied to mock tests (`mock_rating_id`, `mock_test_id`, `technical_rating`, `programming_rating`, `communication_rating`, `entered_by_user_id`, `created_at`).

---

## 🚀 Getting Started & Installation

### Prerequisites
* Python 3.x installed on your machine.

### Setup Instructions
1. Clone or download all project files into a single directory:
   - `database_manager.py`
   - `authentication_manager.py`
   - `login_manager.py`
   - `student_manager.py`
   - `mock_manager.py`
   - `seed_data.py`
   - `main.py`

2. *(Optional)* Seed the database with practice dummy data:
   ```bash
   python seed_data.py
   ```
   * **Test Credentials:** 
     * Username: `admin_trainer`
     * Password: `admin123`
   * **Test Student Roll Numbers:** `ROLL101`, `ROLL102`, `ROLL201`

3. Run the application:
   ```bash
   python main.py
   ```

---

## 💡 Usage Guide

* **Registration**: New users can register by providing their full name, a valid 4-20 character username, 10-digit phone number, email address, and passing the simulated OTP and CAPTCHA challenge.
* **Login**: Log in using your credentials followed by CAPTCHA verification. The system protects against brute-force attacks by locking accounts for 60 seconds after 3 failed attempts.
* **Dashboard Features**:
  * Create and browse unique batch codes.
  * Register new student admissions with roll number uniqueness checks.
  * Record and track mock test scores and qualitative skill ratings.
  * Securely logout to close active session tracking.