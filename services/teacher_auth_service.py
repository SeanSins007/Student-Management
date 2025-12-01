# services/teacher_auth_service.py

from typing import Optional
from storage.json_storage import JSONStorage
from models.teacher import Teacher
from utils.id_generator import generate_id
from utils.validators import validate_email
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

class TeacherAuthService:
    def __init__(self, storage_file: str = "data/teachers.json"):
        self.storage = JSONStorage(storage_file)
        info("TeacherAuthService initialized.")

    def register(self, name: str, email: str, password: str) -> Optional[Teacher]:
        heading("Registering Teacher")
        if not validate_email(email):
            error("Invalid email format.")
            return None

        teachers = self.storage.load(Teacher)
        if any(t.email.lower() == email.lower() for t in teachers):
            warning("Email already registered.")
            return None

        teacher_id = generate_id("T")
        teacher = Teacher(teacher_id, name, email, hash_password(password))
        self.storage.add(teacher)

        success(f"Teacher registered successfully (ID: {teacher_id})")
        print(subheading(f"Name: {name} | Email: {email}"))
        return teacher

    def login(self, identifier: str, password: str) -> Optional[Teacher]:
        """
        Login using either teacher ID or email.
        `identifier` may be a teacher ID (e.g. 'T123') or an email address.
        """
        heading("Teacher Login")
        teachers = self.storage.load(Teacher)
        hashed_password = hash_password(password)

        for t in teachers:
            if ((hasattr(t, 'teacher_id') and t.teacher_id.lower() == identifier.lower())
                or (hasattr(t, 'email') and t.email.lower() == identifier.lower())) \
                    and t.password == hashed_password:
                success(f"Welcome, {t.name}")
                return t

        error("Invalid teacher id/email or password.")
        return None

    def validated_registration(self) -> Optional[Teacher]:
        heading("=== Teacher Registration ===")

        # Name input
        while True:
            name = input("Enter Teacher Name (or press Enter to cancel): ").strip()
            if not name:
                info("Registration cancelled by user.")
                return None
            break

        # Email input
        while True:
            email = input("Enter Email (must end with @gmail.com) (or press Enter to cancel): ").strip()
            if not email:
                info("Registration cancelled by user.")
                return None

            if not validate_email(email) or not email.lower().endswith("@gmail.com"):
                error("Invalid email. Must be valid and end with @gmail.com.")
                continue

            teachers = self.storage.load(Teacher)
            if any(t.email.lower() == email.lower() for t in teachers):
                warning("Email already registered. Try a different email or press Enter to cancel.")
                continue
            break

        # Password input with policy
        password = prompt_password_with_policy(
            prompt="Enter Password (or press Enter to cancel): ",
            confirm_prompt="Confirm Password (or press Enter to cancel): ",
            min_length=8,
            allow_override=True
        )
        if password is None:
            info("Registration cancelled during password entry.")
            return None

        hashed = hash_password(password)
        return self.register(name, email, hashed)
