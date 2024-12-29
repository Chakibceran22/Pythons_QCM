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
        # For single choice questions, convert single correct answer to int if it's in a list
        correct = question['correct'] if isinstance(question['correct'], int) else question['correct'][0]
        return user_answer == correct
    
def display_correct_answer(question: dict):
    """Display the correct answer(s) for both types of questions"""
    if question.get('type') == 'multiple':
        print(f"{Colors.GREEN}Correct answers:{Colors.ENDC}")
        for ans in question['correct']:
            # Subtract 1 from the answer index since options are 0-based
            print(f"{Colors.GREEN}- {question['options'][ans-1]}{Colors.ENDC}")
    else:
        # For single choice questions, correct is a single number
        correct_idx = question['correct'] if isinstance(question['correct'], int) else question['correct'][0]
        print(f"{Colors.GREEN}Correct answer: {question['options'][correct_idx-1]}{Colors.ENDC}")


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

    def take_qcm(self, category: str, title: str, time_limit: int = 300) -> tuple[bool, str]:
        if not self.current_user:
            return False, f"{Colors.RED}Please login first!{Colors.ENDC}"

        if category not in self.qcms or title not in self.qcms[category]:
            return False, f"{Colors.RED}QCM not found!{Colors.ENDC}"

        questions = self.qcms[category][title]
        score = 0
        user_answers = []
        start_time = time.time()
        end_time = start_time + time_limit

        clear_screen()
        print_fancy(f"🎯 Starting QCM: {title}", Colors.YELLOW, bold=True)
        print_fancy(f"Category: {category}", Colors.BLUE)
        print_fancy(f"Total questions: {len(questions)}\n", Colors.BLUE)
        print_fancy(f"⏳ You have {time_limit // 60} minutes to complete the quiz.\n", Colors.RED)

        for i, q in enumerate(questions, 1):
            remaining_time = int(end_time - time.time())
            if remaining_time <= 0:
                print(f"{Colors.RED}Time's up!{Colors.ENDC}")
                break

            print(f"\n{Colors.BOLD}Question {i}/{len(questions)}{Colors.ENDC}")
            print(f"{Colors.YELLOW}{q['question']}{Colors.ENDC}\n")

            for j, option in enumerate(q['options'], 1):
                print(f"{Colors.BLUE}{j}. {option}{Colors.ENDC}")

            print(f"\n{Colors.YELLOW}⏳ Time remaining: {remaining_time} seconds{Colors.ENDC}")
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

def display_student_results(app):
    clear_screen()
    print_fancy("📊 Résultats des Étudiants 📊", Colors.YELLOW, bold=True)

    if not app.history:
        print(f"{Colors.RED}Aucun résultat trouvé !{Colors.ENDC}")
        time.sleep(2)
        return

    # Parcourt l'historique des étudiants
    for username, results in app.history.items():
        print(f"\n{Colors.BLUE}Étudiant : {username}{Colors.ENDC}")
        if not results:
            print(f"{Colors.RED}Aucun QCM complété.{Colors.ENDC}")
        else:
            for result in results:
                print(f"  - {Colors.GREEN}Date :{Colors.ENDC} {result['date']}")
                print(f"    {Colors.GREEN}Catégorie :{Colors.ENDC} {result['category']}")
                print(f"    {Colors.GREEN}Titre :{Colors.ENDC} {result['title']}")
                print(f"    {Colors.GREEN}Score :{Colors.ENDC} {result['score']}%")
                print(f"    {Colors.GREEN}Réponses correctes :{Colors.ENDC} {result['answers']}")
    input(f"\n{Colors.YELLOW}Appuyez sur Entrée pour retourner au menu...{Colors.ENDC}")
def add_qcm(app):
    """Permet au professeur d'ajouter une nouvelle catégorie ou un nouveau titre avec des questions."""
    print_fancy("\n🔧 Professeur - Ajouter un QCM", Colors.YELLOW, bold=True)

    # Charger les catégories existantes
    categories = app.qcms.keys()
    print_fancy("\nCatégories existantes:", Colors.BLUE)
    for category in categories:
        print(f"{Colors.BLUE}- {category}{Colors.ENDC}")

    print(f"{Colors.GREEN}\nVoulez-vous ajouter à une catégorie existante ou en créer une nouvelle?{Colors.ENDC}")
    print(f"{Colors.BLUE}1.{Colors.ENDC} Ajouter à une catégorie existante")
    print(f"{Colors.BLUE}2.{Colors.ENDC} Créer une nouvelle catégorie")

    choice = input(f"\n{Colors.GREEN}Votre choix (1 ou 2): {Colors.ENDC}")

    if choice == '1':
        # Ajouter à une catégorie existante
        category = input(f"\n{Colors.GREEN}Entrez le nom de la catégorie existante: {Colors.ENDC}")
        if category not in app.qcms:
            print(f"{Colors.RED}Catégorie introuvable!{Colors.ENDC}")
            return

    elif choice == '2':
        # Créer une nouvelle catégorie
        category = input(f"\n{Colors.GREEN}Entrez le nom de la nouvelle catégorie: {Colors.ENDC}")
        if category in app.qcms:
            print(f"{Colors.RED}Cette catégorie existe déjà!{Colors.ENDC}")
            return
        app.qcms[category] = {}

    else:
        print(f"{Colors.RED}Choix invalide!{Colors.ENDC}")
        return

    # Ajouter un nouveau titre à la catégorie
    title = input(f"\n{Colors.GREEN}Entrez le titre du nouveau QCM: {Colors.ENDC}")
    if title in app.qcms[category]:
        print(f"{Colors.RED}Ce titre existe déjà dans la catégorie!{Colors.ENDC}")
        return

    app.qcms[category][title] = []

    print_fancy("\nAjout des questions pour le titre.", Colors.YELLOW)
    while True:
        question_text = input(f"\n{Colors.GREEN}Entrez la question: {Colors.ENDC}")
        options = []

        print(f"\n{Colors.BLUE}Ajoutez les options (entrez une option vide pour arrêter):{Colors.ENDC}")
        while True:
            option = input(f"{Colors.GREEN}Option: {Colors.ENDC}")
            if option.strip() == "":
                break
            options.append(option)

        if len(options) < 2:
            print(f"{Colors.RED}Une question doit avoir au moins deux options!{Colors.ENDC}")
            continue

        print(f"\n{Colors.BLUE}Entrez le ou les numéros des réponses correctes (séparés par des espaces):{Colors.ENDC}")
        print(" ".join([f"{i + 1}. {opt}" for i, opt in enumerate(options)]))

        correct_answers = input(f"{Colors.GREEN}Réponses correctes: {Colors.ENDC}")
        correct_answers = list(map(int, correct_answers.split()))

        question_type = "multiple" if len(correct_answers) > 1 else "single"
        app.qcms[category][title].append({
            "question": question_text,
            "options": options,
            "correct": correct_answers,
            "type": question_type
        })

        another = input(f"\n{Colors.GREEN}Voulez-vous ajouter une autre question? (o/n): {Colors.ENDC}").lower()
        if another != 'o':
            break

    # Sauvegarder les modifications
    app.save_data('qcms.json', app.qcms)
    print_fancy("\n✅ QCM ajouté avec succès!", Colors.GREEN)

def display_menu_professeur(app):
    """Affiche le menu pour l'espace professeur."""
    while True:
        clear_screen()
        print_fancy("👨‍🏫 Espace Professeur 👩‍🏫", Colors.YELLOW, bold=True)
        print(f"{Colors.BLUE}1.{Colors.ENDC} Voir les résultats des étudiants")
        print(f"{Colors.BLUE}2.{Colors.ENDC} Ajouter un QCM")
        print(f"{Colors.BLUE}3.{Colors.ENDC} Retour au menu principal")

        choice = input(f"\n{Colors.GREEN}Entrez votre choix (1-2) : {Colors.ENDC}")

        if choice == '1':
            # Voir les résultats des étudiants
            display_student_results(app)
        elif choice == '2':
                        # Ajouter un QCM
            add_qcm(app)
        elif choice == '3':
            # Retour au menu principal
            break
        else:
            print(f"{Colors.RED}Choix invalide. Veuillez réessayer.{Colors.ENDC}")
            time.sleep(1)


def display_menu_student(app):
    while True:
        clear_screen()
        print_fancy("🎓 Espace Étudiant 🎓", Colors.YELLOW, bold=True)
        print(f"{Colors.BLUE}1.{Colors.ENDC} Register")
        print(f"{Colors.BLUE}2.{Colors.ENDC} Login")
        print(f"{Colors.BLUE}3.{Colors.ENDC} Take QCM")
        print(f"{Colors.BLUE}4.{Colors.ENDC} View History")
        print(f"{Colors.BLUE}5.{Colors.ENDC} Show Correct Answers")
        print(f"{Colors.BLUE}6.{Colors.ENDC} View Leaderboard")
        print(f"{Colors.RED}7.{Colors.ENDC} Retour au menu principal")

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
            break

        else:
            print(f"{Colors.RED}Invalid choice! Please try again.{Colors.ENDC}")
            time.sleep(1)


def display_menu(app):
    """Affiche le menu principal pour choisir entre l'espace étudiant et professeur."""
    while True:
        clear_screen()
        print_fancy("Bienvenue dans l'application QCM !", Colors.YELLOW, bold=True)
        print(f"{Colors.BLUE}1.{Colors.ENDC} Espace Étudiant")
        print(f"{Colors.BLUE}2.{Colors.ENDC} Espace Professeur")
        print(f"{Colors.RED}3.{Colors.ENDC} Quitter")

        choice = input(f"\n{Colors.GREEN}Entrez votre choix (1-3) : {Colors.ENDC}")

        if choice == '1':
            # Redirige vers l'espace étudiant
            display_menu_student(app)
        elif choice == '2':
            # rajouter lajout dun qcm 
            display_menu_professeur(app)
        elif choice == '3':
            print_fancy("\n👋 Merci d'avoir utilisé l'application QCM ! Au revoir !", Colors.GREEN, bold=True)
            time.sleep(1)
            break
        else:
            print(f"{Colors.RED}Choix invalide. Veuillez réessayer.{Colors.ENDC}")
            time.sleep(1)
def main():
    """Point d'entrée principal de l'application."""
    app = QCMApp()  # Crée une instance de l'application
    display_menu(app)  # Appelle le menu principal


if __name__ == "__main__":
    main()
