# utils/messages.py
from utils.colors import Colors

def success(msg: str):
    print(f"{Colors.GREEN}{msg}{Colors.RESET}")

def error(msg: str):
    print(f"{Colors.RED}{msg}{Colors.RESET}")

def info(msg: str):
    print(f"{Colors.BLUE}{msg}{Colors.RESET}")

def warning(msg: str):
    print(f"{Colors.YELLOW}{msg}{Colors.RESET}")

def heading(msg: str):
    print(f"{Colors.BOLD}{Colors.MAGENTA}{msg}{Colors.RESET}")

def subheading(msg: str):
    return f"{Colors.BOLD}{Colors.CYAN}{msg}{Colors.RESET}"