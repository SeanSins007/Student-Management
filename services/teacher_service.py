# services/teacher_service.py

from models.teacher import Teacher
from storage.json_storage import JSONStorage
from utils.id_generator import generate_id
from utils.validators import validate_email
from utils.msg import (
    error, 
    success, 
    info, 
    warning, 
    heading, 
    subheading
)

class TeacherService:
    def __init__(self, storage_file="data/teachers.json"):
        self.storage = JSONStorage(storage_file)
        info("TeacherService initialized.")

    def add_teacher(self, name: str, email: str, password: str) -> Teacher | None:
        heading("Adding a new teacher")
        if not validate_email(email):
            error("Invalid email format.")
            return None

        teachers = self.storage.load(Teacher)
        if any(t.email.lower() == email.lower() for t in teachers):
            warning("Email already exists.")
            return None

        teacher_id = generate_id("T")
        teacher = Teacher(teacher_id, name, email, password)
        self.storage.add(teacher)
        success(f"Teacher added successfully: {teacher_id}")
        print(subheading(f"Name: {name} | Email: {email}"))
        return teacher

    def get_all_teachers(self):
        teachers = self.storage.load(Teacher)
        info(f"{len(teachers)} teachers loaded.")
        return teachers

    def find_teacher(self, teacher_id: str) -> Teacher | None:
        for t in self.get_all_teachers():
            if t.teacher_id == teacher_id:
                info(f"Teacher found: {teacher_id}")
                return t
        warning(f"Teacher not found: {teacher_id}")
        return None

    def update_teacher(self, teacher_id: str, name: str = None, email: str = None, password: str = None):
        heading(f"Updating teacher {teacher_id}")
        teacher = self.find_teacher(teacher_id)
        if not teacher:
            error("Teacher not found.")
            return None

        if email:
            if not validate_email(email):
                error("Invalid email format.")
                return None
            if any(t.email.lower() == email.lower() and t.teacher_id != teacher_id for t in self.get_all_teachers()):
                warning("Email already exists for another teacher.")
                return None
            teacher.email = email
            info(f"Email updated to: {email}")

        if name:
            teacher.name = name
            info(f"Name updated to: {name}")

        if password:
            teacher.password = password
            info("Password updated successfully.")

        self.storage.update(teacher, key="teacher_id")
        success(f"Teacher updated successfully: {teacher_id}")
        return teacher

    def delete_teacher(self, teacher_id: str):
        heading(f"Deleting teacher {teacher_id}")
        teacher = self.find_teacher(teacher_id)
        if not teacher:
            error("Teacher not found.")
            return

        self.storage.delete(teacher_id, Teacher, key="teacher_id")
        success(f"Teacher deleted successfully: {teacher_id}")
