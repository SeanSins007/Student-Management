# models/student.py

from utils.msg import subheading

class Student:
    def __init__(self, student_id: str, name: str, age: int, email: str, password: str = None):
        self.student_id = student_id
        self.name = name
        self.age = age
        self.email = email
        self.password = password  # Plain text for now; can hash later

        # Optional validation
        if self.age <= 0:
            raise ValueError("Age must be a positive integer.")

    def to_dict(self) -> dict:
        return {
            "student_id": self.student_id,
            "name": self.name,
            "age": self.age,
            "email": self.email,
            "password": self.password
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            student_id=data["student_id"],
            name=data["name"],
            age=data["age"],
            email=data["email"],
            password=data.get("password")
        )

    def __str__(self):
        print(subheading(f"Student ID: {self.student_id}"))
        print(subheading(f"Name: {self.name}"))
        print(subheading(f"Age: {self.age}"))
        print(subheading(f"Email: {self.email}"))
        return ""  # Prevent default object print

    def __repr__(self):
        return f"Student({self.student_id}, {self.name}, Age: {self.age}, Email: {self.email})"

    def check_password(self, password: str) -> bool:
        """Check password (plain text for now; can hash later)."""
        return self.password == password

    def set_password(self, password: str):
        """Set/update password (hashing can be added later)."""
        if not password:
            raise ValueError("Password cannot be empty.")
        self.password = password
