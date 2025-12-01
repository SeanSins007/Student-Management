Student Management System (Python, OOP, Modular Architecture)

A modular and extensible command-line Student Management System built using Python. This project features a clean file structure, strong input validation, secure password handling, colored CLI messages, and a fully object-oriented service layer.

-📌 Features
-🔐 Authentication

   - Admin login system
   - Password hashing (bcrypt)
   - Password policy enforcement
   - Minimum length
   - Uppercase letters
   - Lowercase letters
   - Numbers
   - Special characters
   - Secure password confirmation prompts

👩‍🎓 Student Management

   1. Admins can:

   2. Add new students

   3. Validate student age

   4. Must be > 18

   5. Must be ≤ 45

   6. Validate email format

   7. View all students

   8. Delete students

   9. Update student records

🎨 Colored Messages (CLI UI)

Uses standardized color-coded messages throughout the project:

       Message Type	   Color	Usage

    1. success()		   Green	Completion / confirmation
    2. error()		      Red	Invalid input, failures
    3. warning()		   Yellow	Caution / borderline input
    4. info()		      Cyan	Neutral informative output
    5. subheading()	   Blue	Input prompts / headers
    6. heading()		   Magenta	Section headers

📁 Project Structure
```
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
```

⚙️ How It Works
1. Authentication Flow

    1. Admin credentials stored in accounts.json

    2. Passwords stored hashed, never plain text

    3. Login compares hashed passwords securely

2. Student Creation Flow

    1. User enters name → stored directly
       
    2. Age prompt validates: numeric input >18 and ≤45
       
    3. Email validated with regex
       
    4. Student saved to students.json
       
    5. Log entry stored automatically

3. Modular Architecture
      
      Every responsibility is separated:

         1. AuthService handles login/register
                   
         2. StudentService manages CRUD
                   
         3. Storage layer manages JSON read/write

         4. Utilities provide reusable helpers

         5. Models define Student/Admin objects

         6. Menu system orchestrates actions

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

   1. Password hashing (bcrypt)

   2. No plaintext passwords stored anywhere

   3. Strict password policy

   4. Input validation on all fields

   5. Logging of admin actions

📌 Future Improvements

   1. Add course management module

   2. Add teacher accounts

   3. Add role-based permissions

   4. Export students to CSV / PDF

   5. Database support (SQLite/PostgreSQL)

📜 License

   This project is free to use and modify.
