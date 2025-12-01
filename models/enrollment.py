# models/enrollment.py

from utils.msg import subheading

class Enrollment:
    def __init__(self, enrollment_id: str, student_id: str, course_id: str, grade: str = None):
        self.enrollment_id = enrollment_id
        self.student_id = student_id
        self.course_id = course_id
        self.grade = grade  # Initially None

    def to_dict(self) -> dict:
        return {
            "enrollment_id": self.enrollment_id,
            "student_id": self.student_id,
            "course_id": self.course_id,
            "grade": self.grade
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            enrollment_id=data["enrollment_id"],
            student_id=data["student_id"],
            course_id=data["course_id"],
            grade=data.get("grade")
        )

    def __str__(self):
        print(subheading(f"Enrollment ID: {self.enrollment_id}"))
        print(subheading(f"Student ID: {self.student_id}"))
        print(subheading(f"Course ID: {self.course_id}"))
        print(subheading(f"Grade: {self.grade or 'N/A'}"))
        return ""  # Prevent default object print

    def __repr__(self):
        return f"Enrollment({self.enrollment_id}, Student: {self.student_id}, Course: {self.course_id}, Grade: {self.grade or 'N/A'})"

    def assign_grade(self, grade: str):
        """Assign a grade to this enrollment."""
        if not grade:
            raise ValueError("Grade cannot be empty.")
        self.grade = grade.upper()

    def has_grade(self) -> bool:
        """Return True if a grade is assigned."""
        return self.grade is not None
