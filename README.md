Student Management System (Python, OOP, Modular Architecture)

A modular and extensible command-line Student Management System built using Python.
This project features a clean file structure, strong input validation, secure password handling, colored CLI messages, and a fully object-oriented service layer.

📌 Features
🔐 Authentication

Admin login system

Password hashing (bcrypt)

Password policy enforcement

Minimum length

Uppercase letters

Lowercase letters

Numbers

Special characters

Secure password confirmation prompts

👩‍🎓 Student Management

Admins can:

Add new students

Validate student age

Must be > 18

Must be ≤ 45

Validate email format

View all students

Delete students

Update student records

🎨 Colored Messages (CLI UI)

Uses standardized color-coded messages throughout the project:

Message Type	Color	Usage
success()	Green	Completion / confirmation
error()	Red	Invalid input, failures
warning()	Yellow	Caution / borderline input
info()	Cyan	Neutral informative output
subheading()	Blue	Input prompts / headers
heading()	Magenta	Section headers
📁 Project Structure
project_root/
│
├── main.py
├── menu.py
├── auth.py
├── admin.py
├── student_service.py
├── storage.py
│
├── models/
│   ├── admin.py
│   └── student.py
│
├── utils/
│   ├── msg.py
│   ├── password_input.py
│   ├── password_policy.py
│   ├── password_hash.py
│   ├── validators.py
│   └── log.py
│
└── data/
    ├── accounts.json
    └── students.json

⚙️ How It Works
1. Authentication Flow

Admin credentials stored in accounts.json

Passwords stored hashed, never plain text

Login compares hashed passwords securely

2. Student Creation Flow

User enters name → stored directly

Age prompt validates:

numeric input

18

≤45

Email validated with regex

Student saved to students.json

Log entry stored automatically

3. Modular Architecture

Every responsibility is separated:

AuthService handles login/register

StudentService manages CRUD

Storage layer manages JSON read/write

Utilities provide reusable helpers

Models define Student/Admin objects

Menu system orchestrates actions

This ensures the project is:
✔ Maintainable
✔ Scalable
✔ Easy to extend (e.g., courses, teachers, fees, attendance)

🚀 Getting Started
1. Install Dependencies
pip install bcrypt

2. Run the Application
python main.py

3. Default Admin Setup

If no admin exists:

System will prompt you to create one

Password must meet policy requirements

🛡 Security Highlights

Password hashing (bcrypt)

No plaintext passwords stored anywhere

Strict password policy

Input validation on all fields

Logging of admin actions

📌 Future Improvements

Add course management module

Add teacher accounts

Add role-based permissions

Export students to CSV / PDF

Database support (SQLite/PostgreSQL)

📜 License

This project is free to use.