# services/report_service.py

from models.student import Student
from models.course import Course
from models.enrollment import Enrollment
from storage.json_storage import JSONStorage
from utils.msg import (
    # error, 
    # success, 
    info, 
    warning, 
    heading, 
    subheading
)

class ReportService:
    def __init__(self):
        self.student_storage = JSONStorage("data/students.json")
        self.course_storage = JSONStorage("data/courses.json")
        self.enrollment_storage = JSONStorage("data/enrollments.json")
        info("ReportService initialized.")

    def list_students(self):
        students = self.student_storage.load(Student)
        heading("=== All Students ===")
        if not students:
            warning("No students found.")
            return
        for s in students:
            print(subheading(f"{s.student_id}: {s.name} | Age: {s.age} | Email: {s.email}"))

    def list_courses(self):
        courses = self.course_storage.load(Course)
        heading("=== All Courses ===")
        if not courses:
            warning("No courses found.")
            return
        for c in courses:
            print(subheading(f"{c.course_id}: {c.name} | Instructor: {c.instructor_name or 'Unassigned'} | Credits: {c.credits}"))

    def list_enrollments(self):
        enrollments = self.enrollment_storage.load(Enrollment)
        heading("=== All Enrollments ===")
        if not enrollments:
            warning("No enrollments found.")
            return
        for e in enrollments:
            print(subheading(f"{e.enrollment_id}: Student {e.student_id} | Course {e.course_id} | Grade: {e.grade or 'Not graded'}"))

    def student_report(self, student_id: str):
        enrollments = self.enrollment_storage.load(Enrollment)
        courses = self.course_storage.load(Course)
        student_enrollments = [e for e in enrollments if e.student_id == student_id]

        heading(f"=== Report for Student {student_id} ===")
        if not student_enrollments:
            warning("No enrollments found for this student.")
            return

        for e in student_enrollments:
            course = next((c for c in courses if c.course_id == e.course_id), None)
            grade = e.grade if e.grade is not None else "Not graded"
            if course:
                    print(subheading(f"{course.name} ({course.course_id}) - Grade: {grade}"))
            else:
                warning(f"Course not found for enrollment {e.enrollment_id}")
