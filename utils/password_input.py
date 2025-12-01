# utils/password_input.py

import sys

def input_password(prompt="Password: "):
    """
    Prompt user for password input, masking the characters with '*'.
    Works on Windows using msvcrt; falls back to getpass on other systems.
    """
    try:
        import msvcrt
        print(prompt, end="", flush=True)
        password = ""
        while True:
            ch = msvcrt.getch()
            
            # ENTER key
            if ch in {b'\r', b'\n'}:
                print()
                break
            
            # BACKSPACE key
            if ch == b'\x08':
                if len(password) > 0:
                    password = password[:-1]
                    sys.stdout.write("\b \b")
                    sys.stdout.flush()
                continue
            
            # Ignore special keys
            if ch in {b'\x00', b'\xe0'}:
                msvcrt.getch()  # skip next byte
                continue
            
            # Normal character
            try:
                char = ch.decode("utf-8")
            except UnicodeDecodeError:
                continue

            password += char
            sys.stdout.write("*")
            sys.stdout.flush()

        return password

    except ImportError:
        # fallback for non-Windows systems
        import getpass
        return getpass.getpass(prompt)
