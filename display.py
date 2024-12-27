# File: display.py
import os
import time
from colors import Colors

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_fancy(text: str, color: str = Colors.BLUE, bold: bool = False, delay: float = 0.02):
    text = f"{color}{Colors.BOLD if bold else ''}{text}{Colors.ENDC}"
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()

def display_menu():
    clear_screen()
    print_fancy("🎓 QCM Application 🎓", Colors.YELLOW, bold=True)
    print(f"\n{Colors.BLUE}1.{Colors.ENDC} Register")
    print(f"{Colors.BLUE}2.{Colors.ENDC} Login")
    print(f"{Colors.BLUE}3.{Colors.ENDC} Take QCM")
    print(f"{Colors.BLUE}4.{Colors.ENDC} View History")
    print(f"{Colors.BLUE}5.{Colors.ENDC} Show Correct Answers")
    print(f"{Colors.BLUE}6.{Colors.ENDC} View Leaderboard")
    print(f"{Colors.RED}7.{Colors.ENDC} Exit")

