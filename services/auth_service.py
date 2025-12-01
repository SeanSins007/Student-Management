import os
import json
from utils.password_input import input_password
# from utils.password_policy import validate_password
from utils.password_policy import prompt_password_with_policy
from utils.password_hash import hash_password
from utils.msg import (
    error, 
    success, 
    info, 
    warning, 
    heading, 
    subheading
    )


class AuthService:
    def __init__(self, data_dir: str):
        self.admin_file = os.path.join(data_dir, "admin.json")

        # Ensure admin file exists
        if not os.path.exists(self.admin_file):
            os.makedirs(os.path.dirname(self.admin_file), exist_ok=True)
            with open(self.admin_file, "w") as f:
                json.dump([], f)

        # Load admins
        self.admins = self._load_admins()

        # If no admin exists, create one
        if not self.admins:
            warning("⚠ No admin found!")
            info("Let's create a new admin account.")
            self.create_admin()

    # -----------------------------------------------------
    # Load Admins
    # -----------------------------------------------------
    def _load_admins(self):
        try:
            with open(self.admin_file, "r") as f:
                return json.load(f)
        except:
            return []

    # -----------------------------------------------------
    # Save Admins
    # -----------------------------------------------------
    def _save_admins(self):
        with open(self.admin_file, "w") as f:
            json.dump(self.admins, f, indent=4)

    # -----------------------------------------------------
    # Password Obfuscation (not full hash)
    # -----------------------------------------------------
    def _obfuscate(self, password: str) -> str:
        return "".join(chr(ord(c) + 2) for c in password)

    def _deobfuscate(self, stored: str) -> str:
        return "".join(chr(ord(c) - 2) for c in stored)

    # -----------------------------------------------------
    # Create Admin
    # -----------------------------------------------------
    def create_admin(self):
        heading("=== Create Admin ===")
        username = input(subheading("Enter admin username: ")).strip()

        pwd = prompt_password_with_policy(
            prompt=subheading("Enter admin password (or press Enter to cancel): "),
            confirm_prompt=subheading("Confirm admin password (or press Enter to cancel): "),
            min_length=8,
            allow_override=True
        )
        if pwd is None:
            info("Admin creation cancelled.")
            return None

        hashed = hash_password(pwd)
        # store hashed in admin record (persist using internal admin list)
        new_admin = {"username": username, "password": hashed}
        self.admins.append(new_admin)
        self._save_admins()

        success("Admin account created successfully!")

    # -----------------------------------------------------
    # Login
    # -----------------------------------------------------
    def login(self) -> bool:
        heading("=== Admin Login ===")
        username = input(subheading("Username: ")).strip()
        password = input_password(subheading("Password: "))

        hashed_input = hash_password(password)
        for admin in self.admins:
            if admin.get("username") == username and admin.get("password") == hashed_input:
                success("Login successful!")
                return True

        error("Invalid credentials.")
        return False
