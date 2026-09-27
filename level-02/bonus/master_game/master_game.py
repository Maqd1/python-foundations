try:
    from guessing_game_v2 import main as play_guessing_game
except ImportError:
    def play_guessing_game():
        print("⚠️ guessing_game_v2.py not found (or its entry function isn't named 'main').")


try:
    from atm_simulator import main as run_atm_simulator
except ImportError:
    def run_atm_simulator():
        print("⚠️ atm_simulator.py not found (or its entry function isn't named 'main').")


try:
    from rock_paper_scissors import main as play_rps_tournament
except ImportError:
    def play_rps_tournament():
        print("⚠️ rock_paper_scissors.py not found (or its entry function isn't named 'main').")


try:
    from quiz_app import main as start_quiz
except ImportError:
    def start_quiz():
        print("⚠️ quiz_app.py not found (or its entry function isn't named 'main').")


try:
    from number_guessing import main as play_mastermind
except ImportError:
    def play_mastermind():
        print("⚠️ number_guessing.py not found (or its entry function isn't named 'main').")


def print_menu():
    print("\n" + "=" * 40)
    print("MASTER CHALLENGE MENU")
    print("=" * 40)
    print("1. High-Low Guessing Game")
    print("2. ATM Banking System")
    print("3. Rock Paper Scissors Tournament")
    print("4. Adaptive Quiz App")
    print("5. Mastermind Number Cracking")
    print("6. Exit")


def main():
    while True:
        print_menu()
        choice = input("Choose option: ").strip()

        match choice:
            case "1":
                play_guessing_game() 

            case "2":
                run_atm_simulator()

            case "3":
                play_rps_tournament()

            case "4":
                start_quiz()

            case "5":
                play_mastermind() 

            case "6":
                print("Goodbye! 👋")
                break

            case _:
                print("Invalid choice! Try again.")
                continue


if __name__ == "__main__":
    main()