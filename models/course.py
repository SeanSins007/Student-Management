# models/course.py


from utils.msg import subheading

class Course:
    def __init__(self, course_id: str, name: str, instructor_id: str = None, instructor_name: str = None, credits: int = 0):
        self.course_id = course_id
        self.name = name
        self.instructor_id = instructor_id
        self.instructor_name = instructor_name
        self.credits = int(credits) if credits is not None else 0
        if self.credits < 0:
            raise ValueError("Credits cannot be negative")

    def to_dict(self) -> dict:
        return {
            "course_id": self.course_id,
            "name": self.name,
            "instructor_id": self.instructor_id,
            "instructor_name": self.instructor_name,
            "credits": self.credits
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            course_id=data["course_id"],
            name=data["name"],
            instructor_id=data.get("instructor_id"),
            instructor_name=data.get("instructor_name"),
            credits=data.get("credits", 0)
        )

    def __str__(self):
        print(subheading(f"Course ID: {self.course_id}"))
        print(subheading(f"Name: {self.name}"))
        print(subheading(f"Instructor: {self.instructor_name or 'Unassigned'}"))
        print(subheading(f"Credits: {self.credits}"))
        return ""  # prevents default object print

    def __repr__(self):
        return f"Course({self.course_id}, {self.name}, Instructor: {self.instructor_name}, Credits: {self.credits})"

    def get_instructor_display(self):
        return self.instructor_name or "Unassigned"

    def assign_teacher(self, teacher_id: str, teacher_name: str):
        self.instructor_id = teacher_id
        self.instructor_name = teacher_name

    def unassign_teacher(self):
        self.instructor_id = None
        self.instructor_name = None
