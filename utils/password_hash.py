import hashlib

def hash_password(password: str) -> str:
    """Return hashed version of the password using SHA-256."""
    return hashlib.sha256(password.encode()).hexdigest()
