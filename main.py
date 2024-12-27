# File: main.py
import getpass
import time
from colors import Colors
from display import display_menu, print_fancy
from file_handler import FileHandler
from user_manager import UserManager
from qcm_manager import QCMManager

def main():
    data_dir = "qcm_data"
    file_handler = FileHandler(data_dir)
    user_manager = UserManager(file_handler)
    qcm_manager = QCMManager(file_handler)

    while True:
        display_menu()
        choice = input(f"\n{Colors.GREEN}Enter your choice (1-7): {Colors.ENDC}")

        if choice == '1':
            username = input(f"\n{Colors.BLUE}Enter username: {Colors.ENDC}")
            password = getpass.getpass(f"{Colors.BLUE}Enter password: {Colors.ENDC}")
            success, message = user_manager.register(username, password)
            print(message)
            time.sleep(1)

        elif choice == '2':
            username = input(f"\n{Colors.BLUE}Enter username: {Colors.ENDC}")
            password = getpass.getpass(f"{Colors.BLUE}Enter password: {Colors.ENDC}")
            success, message = user_manager.login(username, password)
            print(message)
            time.sleep(1)

        elif choice == '3':
            if not user_manager.get_current_user():
                print(f"{Colors.RED}Please login first!{Colors.ENDC}")
                time.sleep(1)
                continue

            print_fancy("\nAvailable Categories:", Colors.YELLOW)
            for category in qcm_manager.qcms:
                print(f"{Colors.BLUE}- {category}{Colors.ENDC}")
            
            category = input(f"\n{Colors.GREEN}Enter category: {Colors.ENDC}")
            if category in qcm_manager.qcms:
                print_fancy(f"\nAvailable QCMs in {category}:", Colors.YELLOW)
                for title in qcm_manager.qcms[category]:
                    print(f"{Colors.BLUE}- {title}{Colors.ENDC}")
                
                title = input(f"\n{Colors.GREEN}Enter QCM title: {Colors.ENDC}")
                success, message = qcm_manager.take_qcm(user_manager.get_current_user(), category, title)
                if message:
                    print(message)
                input(f"\n{Colors.YELLOW}Press Enter to continue...{Colors.ENDC}")
            else:
                print(f"{Colors.RED}Category not found!{Colors.ENDC}")
                time.sleep(1)

        elif choice == '4':
            if not user_manager.get_current_user():
                print(f"{Colors.RED}Please login first!{Colors.ENDC}")
                time.sleep(1)
                continue

            success, history = qcm_manager.view_history(user_manager.get_current_user())
            if success:
                print_fancy("\n📜 Your QCM History:", Colors.YELLOW, bold=True)
                for entry in history:
                    print(f"\n{Colors.BLUE}Date: {entry['date']}")
                    print(f"QCM: {entry['category']} - {entry['title']}")
                    print(f"Score: {entry['score']:.1f}%")
                    print(f"Correct answers: {entry['correct_answers']}/{entry['total_questions']}")
                    print(f"Time taken: {entry['time_taken']:.1f} seconds{Colors.ENDC}")
            else:
                print(history)
            input(f"\n{Colors.YELLOW}Press Enter to continue")
        elif choice == '5':
            if not user_manager.get_current_user():
                print(f"{Colors.RED}Please login first!{Colors.ENDC}")
                time.sleep(1)
                continue

            print_fancy("\nAvailable Categories:", Colors.YELLOW)
            for category in qcm_manager.qcms:
                print(f"{Colors.BLUE}- {category}{Colors.ENDC}")
            
            category = input(f"\n{Colors.GREEN}Enter category: {Colors.ENDC}")
            if category in qcm_manager.qcms:
                print_fancy(f"\nAvailable QCMs in {category}:", Colors.YELLOW)
                for title in qcm_manager.qcms[category]:
                    print(f"{Colors.BLUE}- {title}{Colors.ENDC}")
                
                title = input(f"\n{Colors.GREEN}Enter QCM title: {Colors.ENDC}")
                success, message = qcm_manager.show_correct_answers(category, title)
                if message:
                    print(message)
            else:
                print(f"{Colors.RED}Category not found!{Colors.ENDC}")
            input(f"\n{Colors.YELLOW}Press Enter to continue...{Colors.ENDC}")

        elif choice == '6':
            qcm_manager.display_leaderboard()
            input(f"\n{Colors.YELLOW}Press Enter to continue...{Colors.ENDC}")

        elif choice == '7':
            print_fancy("\n👋 Thank you for using the QCM Application! Goodbye!", Colors.GREEN, bold=True)
            time.sleep(1)
            break

        else:
            print(f"{Colors.RED}Invalid choice! Please try again.{Colors.ENDC}")
            time.sleep(1)

if __name__ == "__main__":
    main()