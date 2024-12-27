# File: user_manager.py
from colors import Colors

class UserManager:
    def __init__(self, file_handler):
        self.file_handler = file_handler
        self.users = self.file_handler.load_data('users.json', {})
        self.current_user = None

    def register(self, username: str, password: str) -> tuple[bool, str]:
        if username in self.users:
            return False, f"{Colors.RED}Username already exists!{Colors.ENDC}"
        self.users[username] = password
        self.file_handler.save_data('users.json', self.users)
        return True, f"{Colors.GREEN}Registration successful!{Colors.ENDC}"

    def login(self, username: str, password: str) -> tuple[bool, str]:
        if username in self.users and self.users[username] == password:
            self.current_user = username
            return True, f"{Colors.GREEN}Welcome back, {username}!{Colors.ENDC}"
        return False, f"{Colors.RED}Invalid username or password!{Colors.ENDC}"

    def get_current_user(self) -> str:
        return self.current_user