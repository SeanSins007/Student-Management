# models/teacher.py

from utils.msg import subheading

class Teacher:
    def __init__(self, teacher_id: str, name: str, email: str, password: str = None):
        self.teacher_id = teacher_id
        self.name = name
        self.email = email
        self.password = password  # Plain text for now; can hash later

        # Optional email validation
        if not email or "@" not in email:
            raise ValueError("Invalid email address.")

    def to_dict(self) -> dict:
        return {
            "teacher_id": self.teacher_id,
            "name": self.name,
            "email": self.email,
            "password": self.password
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            teacher_id=data["teacher_id"],
            name=data["name"],
            email=data["email"],
            password=data.get("password")
        )

    def __str__(self):
        print(subheading(f"Teacher ID: {self.teacher_id}"))
        print(subheading(f"Name: {self.name}"))
        print(subheading(f"Email: {self.email}"))
        return ""  # Prevent default object print

    def __repr__(self):
        return f"Teacher({self.teacher_id}, {self.name}, {self.email})"

    def check_password(self, password: str) -> bool:
        """Check password (plain text for now; can hash later)."""
        return self.password == password

    def set_password(self, password: str):
        """Set/update password (hashing can be added later)."""
        if not password:
            raise ValueError("Password cannot be empty.")
        self.password = password
