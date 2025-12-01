# utils/id_generator.py

import random
import string

def generate_id(prefix: str = "ID", length: int = 6, uppercase: bool = True) -> str:
    """
    Generate a unique ID with a prefix and random alphanumeric characters.

    :param prefix: String to prepend to the ID (default "ID")
    :param length: Length of the random part (default 6)
    :param uppercase: Use uppercase letters if True, lowercase if False (default True)
    :return: Generated ID string, e.g., "ID4G7H2J"
    """
    letters = string.ascii_uppercase if uppercase else string.ascii_lowercase
    chars = letters + string.digits
    random_part = ''.join(random.choices(chars, k=length))
    return f"{prefix}{random_part}"
