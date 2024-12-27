# File: file_handler.py
import json
import os
from colors import Colors

class FileHandler:
    def __init__(self, data_dir: str):
        self.data_dir = data_dir
        os.makedirs(data_dir, exist_ok=True)

    def load_data(self, filename: str, default: any) -> any:
        filepath = os.path.join(self.data_dir, filename)
        try:
            if os.path.exists(filepath):
                with open(filepath, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except json.JSONDecodeError:
            print(f"{Colors.RED}Error reading {filename}. Using default empty data.{Colors.ENDC}")
        except Exception as e:
            print(f"{Colors.RED}Error: {str(e)}{Colors.ENDC}")
        return default

    def save_data(self, filename: str, data: any):
        filepath = os.path.join(self.data_dir, filename)
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"{Colors.RED}Error saving data: {str(e)}{Colors.ENDC}")
