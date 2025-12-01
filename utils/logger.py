# utils/logger.py

import datetime
import os
from threading import Lock

LOG_DIR = "logs"
_lock = Lock()

def _ensure_log_dir():
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)

def _get_log_file():
    """Returns the log file path based on current date."""
    _ensure_log_dir()
    date_str = datetime.datetime.now().strftime("%Y-%m-%d")
    return os.path.join(LOG_DIR, f"log_{date_str}.txt")

def log_action(action: str, console: bool = False):
    """
    Log an action with timestamp to a file.
    
    :param action: Description of the action to log
    :param console: If True, also prints the action to console
    """
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] {action}\n"
    
    with _lock:
        with open(_get_log_file(), "a") as f:
            f.write(log_entry)
    
    if console:
        print(log_entry, end="")

def log_print(action: str):
    """Shortcut to log an action and always print it."""
    log_action(action, console=True)
