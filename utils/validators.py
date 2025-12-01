# utils/validators.py

import re

def validate_email(email: str) -> bool:
    """
    Check if an email is in a valid format.
    Ensures proper characters, a single '@', and a domain with at least 2 characters.
    """
    pattern = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
    return bool(re.fullmatch(pattern, email))

def validate_age(age: int, min_age: int = 10, max_age: int = 100) -> bool:
    """
    Ensure age is within a specified range.
    Default range is 10 to 100.
    """
    if not isinstance(age, int):
        return False
    return min_age <= age <= max_age

def validate_credits(credits: int, min_credits: int = 1, max_credits: int = 10) -> bool:
    """
    Ensure course credits are within a valid range.
    Default range is 1 to 10 credits.
    """
    if not isinstance(credits, int):
        return False
    return min_credits <= credits <= max_credits
