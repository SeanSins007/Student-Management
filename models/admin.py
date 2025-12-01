# models/admin.py
from utils.msg import subheading
from utils.password_input import input_password

class Admin:
    def __init__(self, username: str, password_hash: str):
        self.username = username
        self.password = password_hash

    def to_dict(self):
        return {"username": self.username, "password": self.password}

    @classmethod
    def from_dict(cls, data: dict):
        return cls(data["username"], data["password"])

    @staticmethod
    def prompt_credentials():
        """Prompt username and password from user."""
        # subheading("Username: ")
        # username = input().strip()

        # subheading("Password: ")
        # password = input_password()

        # return username, password
        username, password = Admin.prompt_credentials()
        admin = Admin("admin1", "<hashed_password>")

        if username == admin.username and admin.check_password_hash(password):
            print("Login successful!")
        else:
            print("Login failed!")


    def __str__(self):
        """Return string representation without input prompts."""
        return f"Admin(username={self.username}, password=********)"

    def check_password_hash(self, hashed: str) -> bool:
        return self.password == hashed
