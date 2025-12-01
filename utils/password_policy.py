# utils/password_policy.py

import re
from typing import Tuple, Optional
from utils.password_input import input_password
from utils.msg import (
    error, 
    success, 
    info, 
    warning, 
    heading, 
    subheading
)

# Default policy
DEFAULT_MIN_LENGTH = 8
SPECIAL_CHARS = r"!@#\$%\^&\*\(\)\-_=+\[\]\{\};:,.<>\\/\?\|"

def validate_password(password: str, min_length: int = DEFAULT_MIN_LENGTH) -> Tuple[bool, Optional[str]]:
    """Validate password against policy and return (ok, message)."""
    if not password:
        return False, "Password cannot be empty."
    if len(password) < min_length:
        return False, f"Password must be at least {min_length} characters long."
    if not re.search(r"[a-z]", password):
        return False, "Password must include at least one lowercase letter."
    if not re.search(r"[A-Z]", password):
        return False, "Password must include at least one uppercase letter."
    if not re.search(r"\d", password):
        return False, "Password must include at least one digit."
    if not re.search(f"[{SPECIAL_CHARS}]", password):
        return False, "Password must include at least one special character (e.g. !@#$%)."
    common = {"password", "12345678", "qwerty", "letmein", "admin123"}
    if password.lower() in common:
        return False, "Password is too common. Choose a stronger password."
    return True, None

def prompt_password_with_policy(prompt: str = "Enter Password: ",
                                confirm_prompt: str = "Confirm Password: ",
                                min_length: int = DEFAULT_MIN_LENGTH,
                                allow_override: bool = True) -> Optional[str]:
    """
    Prompt user for a password (masked), validate against policy, and confirm.
    Allows override if password is weak. Returns password or None if cancelled.
    """
    heading("=== Password Entry ===")
    while True:
        pwd = input_password(prompt)
        if pwd == "":
            info("Password entry cancelled.")
            return None

        ok, msg = validate_password(pwd, min_length=min_length)
        if not ok:
            warning("Password does not meet the policy requirements.")
            if msg:
                print(subheading(msg))

            if allow_override:
                ans = input("Do you want to keep this password anyway? (y/n): ").strip().lower()
                if ans == "y":
                    confirm = input_password(confirm_prompt)
                    if confirm == "":
                        info("Password confirmation cancelled.")
                        return None
                    if confirm != pwd:
                        error("Passwords do not match. Restarting...")
                        continue
                    success("Weak password accepted by user override.")
                    return pwd
                else:
                    info("Please enter a new password.")
                    continue
            else:
                error("Please choose a stronger password.")
                continue

        # If password passed policy, ask for confirmation
        confirm = input_password(confirm_prompt)
        if confirm == "":
            info("Password confirmation cancelled.")
            return None
        if confirm != pwd:
            error("Passwords do not match. Try again or press Enter to cancel.")
            continue

        success("Password set successfully.")
        return pwd
