# services/enrollment_service.py

from storage.json_storage import JSONStorage
from models.enrollment import Enrollment
from utils.id_generator import generate_id
from utils.msg import (
    error, 
    success, 
    info, 
    warning, 
    heading, 
    # subheading
)

class EnrollmentService:
    def __init__(self, storage_file="data/enrollments.json"):
        self.storage = JSONStorage(storage_file)
        info("EnrollmentService initialized.")  # Informational

    def enroll(self, student_id: str, course_id: str):
        heading("Enroll a student in a course")
        enrollments = self.storage.load(Enrollment)

        # Prevent duplicate enrollment
        for e in enrollments:
            if e.student_id == student_id and e.course_id == course_id:
                warning(f"Student {student_id} is already enrolled in course {course_id}.")
                return None

        enrollment_id = generate_id("E")
        enrollment = Enrollment(enrollment_id, student_id, course_id)
        self.storage.add(enrollment)
        success(f"Enrollment successful: {enrollment_id}")
        info(f"Student {student_id} enrolled in course {course_id}")  # Informational
        return enrollment

    def get_student_enrollments(self, student_id: str):
        enrollments = self.storage.load(Enrollment)
        student_enrollments = [e for e in enrollments if e.student_id == student_id]
        info(f"{len(student_enrollments)} enrollments found for student {student_id}")
        return student_enrollments

    def get_all_enrollments(self):
        enrollments = self.storage.load(Enrollment)
        info(f"{len(enrollments)} total enrollments loaded")
        return enrollments

    def assign_grade(self, enrollment_id: str, grade: str):
        heading(f"Assign grade to enrollment {enrollment_id}")
        enrollments = self.storage.load(Enrollment)
        for e in enrollments:
            if e.enrollment_id == enrollment_id:
                if not grade:
                    warning("No grade provided. Operation cancelled.")
                    return None
                e.grade = grade.upper()
                self.storage.update(e, key="enrollment_id")
                success(f"Grade {grade.upper()} assigned to enrollment {enrollment_id}")
                return e

        error(f"Enrollment not found: {enrollment_id}")
        return None

