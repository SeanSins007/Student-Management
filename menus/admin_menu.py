# menus/admin_menu.py

from services.student_service import StudentService
from services.course_service import CourseService
from services.report_service import ReportService
from services.teacher_service import TeacherService
from utils.validators import validate_email, validate_age, validate_credits
from utils.password_input import input_password
from utils.password_policy import prompt_password_with_policy

from utils.logger import log_print
from utils.msg import (
    error, 
    success, 
    info, 
    # warning, 
    heading, 
    subheading
    )


def run_admin_menu():
    student_service = StudentService()
    course_service = CourseService()
    report_service = ReportService()
    teacher_service = TeacherService()

    def input_age(prompt=subheading("Enter your age (age must be greater than 18): ")):
        while True:
            age_input = input(prompt).strip()
            if not age_input:
                return None
            try:
                age = int(age_input)
                if age < 19:  # Using your min_age logic
                    print(error("Age must be greater than 18."))
                    continue
                return age
            except ValueError:
                print(error("Invalid number. Please enter digits only."))


    def input_email(prompt=subheading("Enter your email (must end with @gmail.com): ")):
        while True:
            email = input(prompt).strip()
            if not email:
                return None
            if not validate_email(email) or not email.endswith("@gmail.com"):
                print(error("Invalid email. Must be valid and end with @gmail.com."))
                continue
            return email


    def input_credits(prompt=subheading("Enter credits (1-10): ")):
        while True:
            credit_input = input(prompt).strip()
            if not credit_input:
                return None
            try:
                credits = int(credit_input)
                if not validate_credits(credits):
                    error("Credits must be 1-10.")
                    continue
                return credits
            except ValueError:
                error("Invalid number. Please enter digits only.")
    while True:
        heading("\n=== Admin Menu ===")
        print(subheading("1. Add Student"))
        print(subheading("2. Update Student"))
        print(subheading("3. List All Students"))
        print(subheading("4. Delete Student"))
        print(subheading("5. Add Course"))
        print(subheading("6. Update Course"))
        print(subheading("7. Delete Course"))
        print(subheading("8. List All Courses"))
        print(subheading("9. Reports"))
        print(subheading("10. Add Teacher"))
        print(subheading("11. Update Teacher"))
        print(subheading("12. Delete Teacher"))
        print(subheading("13. List Teachers"))
        print(subheading("14. Logout"))

        info("Enter choice: ")
        choice = input().strip()
        # ---------------- Student Operations ----------------
        if choice == "1":
            print(subheading("=== Add New Student ==="))

            # Name
            name = input(subheading("Student Name: ")).strip()
            if not name:
                print(error("Name cannot be empty."))
                continue

            # Age
            age = input_age()  # Prompt is already inside the function
            if age is None:
                print(info("Age input cancelled."))
                continue

            # Email
            email = input_email()
            if email is None:
                print(info("Email input cancelled."))
                continue

            # Password
            password = prompt_password_with_policy(
                prompt=subheading("Enter student password: "),
                confirm_prompt=subheading("Confirm student password: "),
                min_length=8
            )
            if password is None:
                print(info("Password input cancelled."))
                continue


            # Add student
            student_service.add_student(name, age, email)
            print(success(f"Added student: {name} ({email}) successfully!"))

        elif choice == "2":
            identifier = input(subheading("Student ID or Email to update: ")).strip()
            if not identifier:
                print(info("Update cancelled."))
                continue

            # Optional fields
            name = input(subheading("New Name (leave blank to skip): ")).strip() or None
            age = input_age(subheading("New Age (leave blank to skip): "))
            email = input_email(subheading("New Email (leave blank to skip): ")) or None

            # Call update using ID or email
            student_service.update_student(identifier, name, age, email)
            log_print(subheading(f"Updated student: {identifier}"))


        # elif choice == "2":
        #     student_id = input(subheading("Student ID to update: ")).strip()
        #     name = input(subheading("New Name (leave blank to skip): ")).strip() or None
        #     age = input_age(subheading("New Age (leave blank to skip): "))
        #     email = input_email(subheading("New Email (leave blank to skip): ")) or None
        #     student_service.update_student(student_id, name, age, email)
        #     log_print(subheading(f"Updated student: {student_id}"))

        elif choice == "3":
            students = student_service.get_all_students()
            heading("=== All Students ===")
            for s in students:
                print(s)

        elif choice == "4":
            identifier = input(subheading("Student ID or Email to delete: ")).strip()
            if not identifier:
                print(info("Delete cancelled."))
                continue

            student_service.delete_student(identifier)
            log_print(subheading(f"Deleted student: {identifier}"))

        # elif choice == "4":
        #     student_id = input(subheading("Student ID to delete: ")).strip()
        #     student_service.delete_student(student_id)
        #     log_print(subheading(f"Deleted student: {student_id}"))

        # ---------------- Course Operations ----------------
        elif choice == "5":  # Add Course
            name = input(subheading("Course Name: ")).strip()
            teacher_identifier = input(subheading("Assign Teacher (ID or Email, Enter to skip): ")).strip()
            credits = input_credits()
            course_service.add_course(name, teacher_identifier or None, credits)
            log_print(subheading(f"Added course: {name}"))

        elif choice == "6":  # Update Course
            course_id = input(subheading("Course ID to update: ")).strip()
            name = input(subheading("New Name (leave blank to skip): ")).strip() or None
            teacher_identifier = input(subheading("New Teacher ID or Email (type 'UNASSIGN' to remove, leave blank to skip): ")).strip()
            credits = input_credits(subheading("New Credits (leave blank to skip): "))
            if teacher_identifier.upper() == "UNASSIGN":
                teacher_identifier = ""
            elif teacher_identifier == "":
                teacher_identifier = None
            course_service.update_course(course_id, name, teacher_identifier, credits)
            log_print(f"Updated course: {course_id}")

        elif choice == "7":  # Delete Course
            course_id = input(subheading("Course ID to delete: ")).strip()
            course_service.delete_course(course_id)
            log_print(subheading(f"Deleted course: {course_id}"))

        elif choice == "8":  # List Courses
            courses = course_service.get_all_courses()
            heading("=== All Courses ===")
            for c in courses:
                print(c)

        # ---------------- Reports ----------------
        elif choice == "9":
            student_id = input(subheading("Enter Student ID for report: ")).strip()
            report_service.student_report(student_id)

        # ---------------- Teacher Operations ----------------
        elif choice == "10":  # Add Teacher
            name = input(subheading("Teacher Name: ")).strip()
            email = input_email(subheading("Teacher Email: "))
            if email is None:
                continue
            password = input_password(subheading("Teacher Password: "))
            if not password:
                continue
            teacher_service.add_teacher(name, email, password)
            log_print(subheading(f"Added teacher: {name} ({email})"))

        elif choice == "11":  # Update Teacher
            identifier = input(subheading("Teacher ID or Email: ")).strip()
            if not identifier:
                print(info("Update cancelled."))
                continue

            name = input(subheading("New Name (press Enter to skip): ")).strip() or None
            email = input_email(subheading("New Email (press Enter to skip): ")) or None
            password = input_password(subheading("New Password (press Enter to skip): ")).strip() or None

            teacher_service.update_teacher(identifier, name, email, password)
            log_print(subheading(f"Updated teacher: {identifier}"))


        # elif choice == "11":  # Update Teacher
        #     teacher_id = input(subheading("Teacher ID: ")).strip()
        #     name = input(subheading("New Name (press Enter to skip): ")).strip() or None
        #     email = input_email(subheading("New Email (press Enter to skip): ")) or None
        #     password = input_password(subheading("New Password (press Enter to skip): ")).strip() or None
        #     teacher_service.update_teacher(teacher_id, name, email, password)
        #     log_print(subheading(f"Updated teacher: {teacher_id}"))

        # elif choice == "12":  # Delete Teacher
        #     teacher_id = input(subheading("Teacher ID: ")).strip()
        #     teacher_service.delete_teacher(teacher_id)
        #     log_print(subheading(f"Deleted teacher: {teacher_id}"))

        elif choice == "12":  # Delete Teacher
            identifier = input(subheading("Teacher ID or Email to delete: ")).strip()
            if not identifier:
                print(info("Delete cancelled."))
                continue

            teacher_service.delete_teacher(identifier)
            log_print(subheading(f"Deleted teacher: {identifier}"))


        elif choice == "13":  # List Teachers
            teachers = teacher_service.get_all_teachers()
            heading("=== All Teachers ===")
            for t in teachers:
                print(t)

        elif choice == "14":
            info("Logging out...")
            break

        else:
            error("Invalid choice. Please select a valid option.")