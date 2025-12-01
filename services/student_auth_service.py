# services/student_auth_service.py

from typing import Optional
from storage.json_storage import JSONStorage
from models.student import Student
from utils.id_generator import generate_id
from utils.validators import validate_email, validate_age
from utils.password_hash import hash_password
from utils.password_policy import prompt_password_with_policy
from utils.msg import (
    error, 
    success, 
    info, 
    warning, 
    heading, 
    subheading
)

class StudentAuthService:
    def __init__(self):
        self.storage = JSONStorage("data/students.json")
        info("StudentAuthService initialized.")

    def register(self, name: str, age: int, email: str, password: str) -> Optional[Student]:
        existing_students = self.storage.load(Student)
        for s in existing_students:
            if s.email.lower() == email.lower():
                error("Email already registered.")
                return None

        student_id = generate_id("S")
        student = Student(student_id, name, age, email, hash_password(password))
        self.storage.add(student)
        success(f"Student registered successfully: {student_id}")
        print(subheading(f"Name: {name} | Age: {age} | Email: {email}"))
        return student

    def login(self, identifier: str, password: str) -> Optional[Student]:
        """
        Login using either student ID or email.
        `identifier` may be a student ID (e.g. 'S123') or an email address.
        """
        students = self.storage.load(Student)
        hashed_password = hash_password(password)
        for s in students:
            if ((hasattr(s, 'student_id') and s.student_id.lower() == identifier.lower())
                or (hasattr(s, 'email') and s.email.lower() == identifier.lower())) \
                    and s.password == hashed_password:
                success(f"Login successful: {identifier}")
                return s
        error("Invalid id/email or password.")
        return None

    def validated_registration(self) -> Optional[Student]:
        """
        Interactive registration with validation and cancel option.
        Flow: name -> age -> email -> password (policy + optional override).
        Press Enter at any prompt to cancel and return to the menu.
        Password input is masked and the stored password will be hashed.
        """
        heading("=== Student Registration ===")

        while True:
            name = input(subheading("Enter Name (or press Enter to cancel): ")).strip()
            if not name:
                info("Registration cancelled by user.")
                return None

            # Age
            while True:
                age_input = input(subheading("Enter Age (19-45) (or press Enter to cancel): ")).strip()
                if not age_input:
                    print(info("Registration cancelled by user."))
                    return None
                try:
                    age = int(age_input)
                except ValueError:
                    print(error("Invalid age. Please enter a number."))
                    continue

                if age < 19:
                    print(warning("Age must be greater than 18."))
                    continue
                elif age > 45:
                    print(warning("Age must be less than 45."))
                    continue

                # Age is valid
                break


            # Email
            while True:
                email = input(subheading("Enter Email (must end with @gmail.com) (or press Enter to cancel): ")).strip()
                if not email:
                    info("Registration cancelled by user.")
                    return None
                if not validate_email(email) or not email.lower().endswith("@gmail.com"):
                    error("Invalid email. Must be valid and end with @gmail.com.")
                    continue
                existing_students = self.storage.load(Student)
                if any(s.email.lower() == email.lower() for s in existing_students):
                    warning("Email already registered. Try a different email or press Enter to cancel.")
                    continue
                break

            # Password
            password = prompt_password_with_policy(
                prompt=subheading("Enter Password (or press Enter to cancel): "),
                confirm_prompt="Confirm Password (or press Enter to cancel): ",
                min_length=8,
                allow_override=True
            )
            if password is None:
                info("Registration cancelled during password entry.")
                return None

            # Hash password
            hashed = hash_password(password)

            # All validations passed
            return self.register(name, age, email, hashed)
