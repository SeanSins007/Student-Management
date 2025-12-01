# services/student_service.py

from typing import Optional, List
from models.student import Student
from storage.json_storage import JSONStorage
from utils.id_generator import generate_id
from utils.validators import validate_email, validate_age
from utils.msg import (
    error, 
    success, 
    info, 
    warning, 
    heading, 
    subheading
)

class StudentService:
    def __init__(self, storage_file: str = "data/students.json"):
        self.storage = JSONStorage(storage_file)
        info("StudentService initialized.")

    def add_student(self, name: str, age: int, email: str) -> Optional[Student]:
        heading("Adding a new student")
        if not validate_age(age, min_age=19):
            warning("Age must be greater than 18.")
            return None
        if not validate_email(email):
            error("Invalid email format.")
            return None

        if any(s.email.lower() == email.lower() for s in self.get_all_students()):
            warning("Email already exists.")
            return None

        student_id = generate_id("S")
        student = Student(student_id, name, age, email)
        self.storage.add(student)
        success(f"Student added successfully: {student_id}")
        print(subheading(f"Name: {name} | Age: {age} | Email: {email}"))
        return student

    def get_all_students(self) -> List[Student]:
        students = self.storage.load(Student)
        info(f"{len(students)} students loaded.")
        return students

    def find_student(self, student_id: str) -> Optional[Student]:
        for student in self.get_all_students():
            if student.student_id == student_id:
                info(f"Student found: {student_id}")
                return student
        warning(f"Student not found: {student_id}")
        return None

    def update_student(
        self,
        student_id: str,
        name: str = None,
        age: int = None,
        email: str = None
    ) -> Optional[Student]:
        heading(f"Updating student {student_id}")
        student = self.find_student(student_id)
        if not student:
            error("Student not found.")
            return None

        if name:
            student.name = name
            info(f"Name updated to: {name}")
        if age is not None:
            if not validate_age(age, min_age=19):
                warning("Invalid age. Must be greater than 18.")
                return None
            student.age = age
            info(f"Age updated to: {age}")
        if email:
            if not validate_email(email):
                error("Invalid email format.")
                return None
            if any(s.email.lower() == email.lower() and s.student_id != student_id for s in self.get_all_students()):
                warning("Email already exists for another student.")
                return None
            student.email = email
            info(f"Email updated to: {email}")

        self.storage.update(student, key="student_id")
        success(f"Student updated successfully: {student_id}")
        return student

    def delete_student(self, student_id: str) -> bool:
        heading(f"Deleting student {student_id}")
        student = self.find_student(student_id)
        if not student:
            error("Student not found.")
            return False
        self.storage.delete(student_id, Student, key="student_id")
        success(f"Student deleted successfully: {student_id}")
        return True
