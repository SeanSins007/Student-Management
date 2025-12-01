# app.py
from services.auth_service import AuthService
from services.student_auth_service import StudentAuthService
from services.teacher_auth_service import TeacherAuthService
from menus.admin_menu import run_admin_menu
from menus.student_menu import run_student_menu
from menus.teacher_menu import run_teacher_menu
from utils.password_input import input_password
from utils.msg import (
    error, 
    success, 
    info, 
    warning, 
    heading, 
    subheading,
)

def main():
    # Initialize Admin Auth Service
    admin_auth = AuthService("data")
    info("Admin authentication system initialized.")

    while True:
        heading("\n=== Welcome to Student Management System ===")
        print(subheading("1. Admin Login"))
        print(subheading("2. Student Login"))
        print(subheading("3. Student Registration"))
        print(subheading("4. Teacher Login"))
        print(subheading("5. Exit"))

        info("Enter your choice:")
        choice = input(">> ").strip()


        # choice = input(subheading("Enter choice: ")).strip()

        # ---------------- Admin Login ----------------
        if choice == "1":
            heading("Admin Login")
            if admin_auth.login():
                success("Admin logged in successfully.")
                run_admin_menu()
            else:
                error("Admin login failed.")

        # ---------------- Student Login ----------------
        elif choice == "2":
            heading("Student Login")
            auth = StudentAuthService()
            identifier = input(subheading("Email or ID: ")).strip()
            password = input_password(subheading("Password: "))
            student = auth.login(identifier, password)
            if student:
                success(f"Welcome, {student.name}!")
                run_student_menu(student)
            else:
                error("Login failed. Check id/email and password.")

        # ---------------- Student Registration ----------------
        elif choice == "3":
            heading("Student Registration")
            auth = StudentAuthService()
            student = auth.validated_registration()
            if student:
                success(f"Registration successful! Student ID: {student.student_id}")
            else:
                warning("Registration canceled or failed.")

        # ---------------- Teacher Login ----------------
        elif choice == "4":
            heading("Teacher Login")
            teacher_auth = TeacherAuthService()
            identifier = input(subheading("Email or ID: ")).strip()
            password = input_password(subheading("Password: "))
            teacher = teacher_auth.login(identifier, password)
            if teacher:
                success(f"Welcome, {teacher.name}!")
                run_teacher_menu(teacher)
            else:
                error("Login failed. Check id/email and password.")

        elif choice == "5":
            info("Exiting... Goodbye!")
            break

        else:
            error("Invalid choice. Please enter a number from 1 to 5.")

if __name__ == "__main__":
    main()

