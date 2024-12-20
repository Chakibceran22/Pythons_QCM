import json
import os
from datetime import datetime
import time
from typing import List, Dict, Any, Union
import getpass

class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_fancy(text: str, color: str = Colors.BLUE, bold: bool = False, delay: float = 0.02):
    text = f"{color}{Colors.BOLD if bold else ''}{text}{Colors.ENDC}"
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()

def handle_question_input(question: dict) -> Union[int, list]:
    """Handle user input for both single and multiple choice questions"""
    if question.get('type') == 'multiple':
        print(f"\n{Colors.YELLOW}This is a multiple choice question. Select multiple answers.{Colors.ENDC}")
        num_answers = len(question['correct'])
        print(f"{Colors.BLUE}(Select {num_answers} answers){Colors.ENDC}")
        answers = []
        while len(answers) < num_answers:
            try:
                remaining = num_answers - len(answers)
                answer = int(input(f"\n{Colors.GREEN}Enter answer #{len(answers)+1} ({remaining} more needed): {Colors.ENDC}"))
                if 1 <= answer <= len(question['options']) and answer not in answers:
                    answers.append(answer)
                elif answer in answers:
                    print(f"{Colors.RED}You've already selected this answer! Try another one.{Colors.ENDC}")
                else:
                    print(f"{Colors.RED}Invalid choice! Please enter a number between 1 and {len(question['options'])}{Colors.ENDC}")
            except ValueError:
                print(f"{Colors.RED}Please enter a number!{Colors.ENDC}")
        return sorted(answers)
    else:
        while True:
            try:
                answer = int(input(f"\n{Colors.GREEN}Your answer (number): {Colors.ENDC}"))
                if 1 <= answer <= len(question['options']):
                    return answer
                print(f"{Colors.RED}Invalid choice! Please enter a number between 1 and {len(question['options'])}{Colors.ENDC}")
            except ValueError:
                print(f"{Colors.RED}Please enter a number!{Colors.ENDC}")

def check_answer(question: dict, user_answer: Union[int, list]) -> bool:
    """Check if the answer is correct for both single and multiple choice questions"""
    if question.get('type') == 'multiple':
        return sorted(user_answer) == sorted(question['correct'])
    else:
        return user_answer == question['correct']

def display_correct_answer(question: dict):
    """Display the correct answer(s) for both types of questions"""
    if question.get('type') == 'multiple':
        print(f"{Colors.GREEN}Correct answers:{Colors.ENDC}")
        for ans in question['correct']:
            print(f"{Colors.GREEN}- {question['options'][ans-1]}{Colors.ENDC}")
    else:
        print(f"{Colors.GREEN}Correct answer: {question['options'][question['correct']-1]}{Colors.ENDC}")

class QCMApp:
    def __init__(self):
        self.data_dir = "qcm_data"
        os.makedirs(self.data_dir, exist_ok=True)
        
        # Load QCMs directly from qcms.json
        self.qcms = self.load_data('qcms.json', {})
        self.users = self.load_data(os.path.join(self.data_dir, 'users.json'), {})
        self.history = self.load_data(os.path.join(self.data_dir, 'history.json'), {})
        self.user_scores = self.load_data(os.path.join(self.data_dir, 'scores.json'), {})
        self.current_user = None

    def load_data(self, filename: str, default: Any) -> Any:
        try:
            if os.path.exists(filename):
                with open(filename, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except json.JSONDecodeError:
            print(f"{Colors.RED}Error reading {filename}. Using default empty data.{Colors.ENDC}")
        except Exception as e:
            print(f"{Colors.RED}Error: {str(e)}{Colors.ENDC}")
        return default

    def save_data(self, filename: str, data: Any):
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"{Colors.RED}Error saving data: {str(e)}{Colors.ENDC}")

    def register(self, username: str, password: str) -> tuple[bool, str]:
        if username in self.users:
            return False, f"{Colors.RED}Username already exists!{Colors.ENDC}"
        self.users[username] = password
        self.history[username] = []
        self.user_scores[username] = {'total_score': 0, 'quizzes_taken': 0}
        self.save_data(os.path.join(self.data_dir, 'users.json'), self.users)
        self.save_data(os.path.join(self.data_dir, 'history.json'), self.history)
        self.save_data(os.path.join(self.data_dir, 'scores.json'), self.user_scores)
        return True, f"{Colors.GREEN}Registration successful!{Colors.ENDC}"

    def login(self, username: str, password: str) -> tuple[bool, str]:
        if username in self.users and self.users[username] == password:
            self.current_user = username
            return True, f"{Colors.GREEN}Welcome back, {username}!{Colors.ENDC}"
        return False, f"{Colors.RED}Invalid username or password!{Colors.ENDC}"

    def take_qcm(self, category: str, title: str) -> tuple[bool, str]:
        if not self.current_user:
            return False, f"{Colors.RED}Please login first!{Colors.ENDC}"
        
        if category not in self.qcms or title not in self.qcms[category]:
            return False, f"{Colors.RED}QCM not found!{Colors.ENDC}"

        questions = self.qcms[category][title]
        score = 0
        user_answers = []
        start_time = time.time()

        clear_screen()
        print_fancy(f"🎯 Starting QCM: {title}", Colors.YELLOW, bold=True)
        print_fancy(f"Category: {category}", Colors.BLUE)
        print_fancy(f"Total questions: {len(questions)}\n", Colors.BLUE)

        for i, q in enumerate(questions, 1):
            print(f"\n{Colors.BOLD}Question {i}/{len(questions)}{Colors.ENDC}")
            print(f"{Colors.YELLOW}{q['question']}{Colors.ENDC}\n")
            
            for j, option in enumerate(q['options'], 1):
                print(f"{Colors.BLUE}{j}. {option}{Colors.ENDC}")
            
            answer = handle_question_input(q)
            user_answers.append(answer)
            
            if check_answer(q, answer):
                score += 1
                print(f"{Colors.GREEN}✓ Correct!{Colors.ENDC}")
            else:
                print(f"{Colors.RED}✗ Incorrect!{Colors.ENDC}")
                print("\nThe correct answer(s):")
                display_correct_answer(q)
            
            time.sleep(1)

        time_taken = time.time() - start_time
        percentage = (score / len(questions)) * 100
        
        self.user_scores[self.current_user]['total_score'] += percentage
        self.user_scores[self.current_user]['quizzes_taken'] += 1
        self.save_data(os.path.join(self.data_dir, 'scores.json'), self.user_scores)

        result = {
            'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'category': category,
            'title': title,
            'score': percentage,
            'time_taken': time_taken,
            'answers': user_answers,
            'total_questions': len(questions),
            'correct_answers': score
        }

        self.history[self.current_user].append(result)
        self.save_data(os.path.join(self.data_dir, 'history.json'), self.history)

        clear_screen()
        print_fancy("🎉 Quiz Completed! 🎉", Colors.YELLOW, bold=True)
        print(f"\n{Colors.GREEN}Score: {percentage:.1f}%{Colors.ENDC}")
        print(f"{Colors.BLUE}Time taken: {time_taken:.1f} seconds{Colors.ENDC}")
        print(f"{Colors.YELLOW}Correct answers: {score}/{len(questions)}{Colors.ENDC}")
        
        self.display_leaderboard()
        return True, ""

    def view_history(self) -> tuple[bool, Any]:
        if not self.current_user:
            return False, f"{Colors.RED}Please login first!{Colors.ENDC}"
        
        user_history = self.history[self.current_user]
        if not user_history:
            return False, f"{Colors.YELLOW}No history found!{Colors.ENDC}"
        
        return True, user_history

    def show_correct_answers(self, category: str, title: str) -> tuple[bool, str]:
        if category not in self.qcms or title not in self.qcms[category]:
            return False, f"{Colors.RED}QCM not found!{Colors.ENDC}"
        
        questions = self.qcms[category][title]
        print_fancy(f"\n📝 Correct answers for {title}:", Colors.YELLOW, bold=True)
        for i, q in enumerate(questions, 1):
            print(f"\n{Colors.BOLD}Question {i}:{Colors.ENDC} {q['question']}")
            display_correct_answer(q)
        return True, ""

    def display_leaderboard(self):
        print_fancy("\n📊 LEADERBOARD 📊", Colors.YELLOW, bold=True)
        sorted_scores = sorted(
            self.user_scores.items(),
            key=lambda x: x[1]['total_score'] / max(x[1]['quizzes_taken'], 1),
            reverse=True
        )
        for i, (user, stats) in enumerate(sorted_scores[:5], 1):
            avg_score = stats['total_score'] / max(stats['quizzes_taken'], 1)
            print(f"{Colors.BLUE}{i}. {user}: {Colors.GREEN}{avg_score:.1f}%{Colors.ENDC}")

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

def main():
    app = QCMApp()

    while True:
        display_menu()
        choice = input(f"\n{Colors.GREEN}Enter your choice (1-7): {Colors.ENDC}")

        if choice == '1':
            username = input(f"\n{Colors.BLUE}Enter username: {Colors.ENDC}")
            password = getpass.getpass(f"{Colors.BLUE}Enter password: {Colors.ENDC}")
            success, message = app.register(username, password)
            print(message)
            time.sleep(1)

        elif choice == '2':
            username = input(f"\n{Colors.BLUE}Enter username: {Colors.ENDC}")
            password = getpass.getpass(f"{Colors.BLUE}Enter password: {Colors.ENDC}")
            success, message = app.login(username, password)
            print(message)
            time.sleep(1)

        elif choice == '3':
            if not app.current_user:
                print(f"{Colors.RED}Please login first!{Colors.ENDC}")
                time.sleep(1)
                continue

            print_fancy("\nAvailable Categories:", Colors.YELLOW)
            for category in app.qcms:
                print(f"{Colors.BLUE}- {category}{Colors.ENDC}")
            
            category = input(f"\n{Colors.GREEN}Enter category: {Colors.ENDC}")
            if category in app.qcms:
                print_fancy(f"\nAvailable QCMs in {category}:", Colors.YELLOW)
                for title in app.qcms[category]:
                    print(f"{Colors.BLUE}- {title}{Colors.ENDC}")
                
                title = input(f"\n{Colors.GREEN}Enter QCM title: {Colors.ENDC}")
                success, message = app.take_qcm(category, title)
                if message:
                    print(message)
                input(f"\n{Colors.YELLOW}Press Enter to continue...{Colors.ENDC}")
            else:
                print(f"{Colors.RED}Category not found!{Colors.ENDC}")
                time.sleep(1)

        elif choice == '4':
            success, history = app.view_history()
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
            input(f"\n{Colors.YELLOW}Press Enter to continue...{Colors.ENDC}")

        elif choice == '5':
            if not app.current_user:
                print(f"{Colors.RED}Please login first!{Colors.ENDC}")
                time.sleep(1)
                continue

            print_fancy("\nAvailable Categories:", Colors.YELLOW)
            for category in app.qcms:
                print(f"{Colors.BLUE}- {category}{Colors.ENDC}")
            
            category = input(f"\n{Colors.GREEN}Enter category: {Colors.ENDC}")
            if category in app.qcms:
                print_fancy(f"\nAvailable QCMs in {category}:", Colors.YELLOW)
                for title in app.qcms[category]:
                    print(f"{Colors.BLUE}- {title}{Colors.ENDC}")
                
                title = input(f"\n{Colors.GREEN}Enter QCM title: {Colors.ENDC}")
                success, message = app.show_correct_answers(category, title)
                if message:
                    print(message)
            else:
                print(f"{Colors.RED}Category not found!{Colors.ENDC}")
            input(f"\n{Colors.YELLOW}Press Enter to continue...{Colors.ENDC}")

        elif choice == '6':
            app.display_leaderboard()
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