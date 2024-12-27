# File: qcm_manager.py
import time
from datetime import datetime
from typing import Dict, List, Union
from colors import Colors
from display import clear_screen, print_fancy

class QCMManager:
    def __init__(self, file_handler):
        self.file_handler = file_handler
        self.qcms = self.file_handler.load_data('qcms.json', {})
        self.history = self.file_handler.load_data('history.json', {})
        self.user_scores = self.file_handler.load_data('scores.json', {})

    def handle_question_input(self, question: dict) -> Union[int, list]:
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

    def check_answer(self, question: dict, user_answer: Union[int, list]) -> bool:
        if question.get('type') == 'multiple':
            return sorted(user_answer) == sorted(question['correct'])
        else:
            return user_answer == question['correct']

    def display_correct_answer(self, question: dict):
        if question.get('type') == 'multiple':
            print(f"{Colors.GREEN}Correct answers:{Colors.ENDC}")
            for ans in question['correct']:
                print(f"{Colors.GREEN}- {question['options'][ans-1]}{Colors.ENDC}")
        else:
            print(f"{Colors.GREEN}Correct answer: {question['options'][question['correct']-1]}{Colors.ENDC}")

    def take_qcm(self, username: str, category: str, title: str) -> tuple[bool, str]:
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
            
            answer = self.handle_question_input(q)
            user_answers.append(answer)
            
            if self.check_answer(q, answer):
                score += 1
                print(f"{Colors.GREEN}✓ Correct!{Colors.ENDC}")
            else:
                print(f"{Colors.RED}✗ Incorrect!{Colors.ENDC}")
                print("\nThe correct answer(s):")
                self.display_correct_answer(q)
            
            time.sleep(1)

        self._save_result(username, category, title, score, len(questions), start_time)
        return True, ""

    def _save_result(self, username: str, category: str, title: str, score: int, total_questions: int, start_time: float):
        time_taken = time.time() - start_time
        percentage = (score / total_questions) * 100

        if username not in self.user_scores:
            self.user_scores[username] = {'total_score': 0, 'quizzes_taken': 0}
        if username not in self.history:
            self.history[username] = []

        self.user_scores[username]['total_score'] += percentage
        self.user_scores[username]['quizzes_taken'] += 1

        result = {
            'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'category': category,
            'title': title,
            'score': percentage,
            'time_taken': time_taken,
            'correct_answers': score,
            'total_questions': total_questions
        }

        self.history[username].append(result)
        self.file_handler.save_data('history.json', self.history)
        self.file_handler.save_data('scores.json', self.user_scores)

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

    def view_history(self, username: str) -> tuple[bool, List[Dict]]:
        if username not in self.history:
            return False, f"{Colors.YELLOW}No history found!{Colors.ENDC}"
        return True, self.history[username]

    def show_correct_answers(self, category: str, title: str) -> tuple[bool, str]:
        if category not in self.qcms or title not in self.qcms[category]:
            return False, f"{Colors.RED}QCM not found!{Colors.ENDC}"
        
        questions = self.qcms[category][title]
        print_fancy(f"\n📝 Correct answers for {title}:", Colors.YELLOW, bold=True)
        for i, q in enumerate(questions, 1):
            print(f"\n{Colors.BOLD}Question {i}:{Colors.ENDC} {q['question']}")
            self.display_correct_answer(q)
        return True, ""