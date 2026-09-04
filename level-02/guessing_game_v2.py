'''
Core 1

🎮 CORE GUESSING GAME

The High-Low Challenge with Multiplayer Mode 🏆

Create a guessing game with these advanced features:

Core Features:

1. Two modes:
   · Single Player: Player guesses against the computer
   · Multiplayer: Two players take turns guessing
2. Difficulty Levels:
   · Easy: 1-20 (10 attempts)
   · Medium: 1-50 (7 attempts)
   · Hard: 1-100 (5 attempts)
   · Impossible: 1-500 (3 attempts)
3. Scoring System:
   · Base points: 100 for winning
   · Bonus points: (max_attempts - attempts_used) x 10
   · Penalty: -10 points for each wrong guess (but not below 0)
4. Hints System:
   · Player can use 3 hints per game
   · Hint: "The number is even/odd" or "The number is divisible by 5"
   · Using a hint costs 15 points

Multiplayer Mode (HARDEST PART):

· Player 1 sets the number
· Player 2 guesses (or vice versa)
· Roles switch after each game
· Track wins for both players across multiple rounds

Technical Requirements:

python
# Function signatures (you must implement these)
def select_difficulty():
    """Returns (max_number, max_attempts) based on user choice"""
    pass

def generate_number(max_num, player1=None):
    """If player1 is provided, use their number; otherwise generate random"""
    pass

def give_hint(number, attempts_left):
    """Returns a hint string based on the number"""
    pass

def calculate_score(attempts_used, max_attempts, hints_used):
    """Returns the final score"""
    pass

def display_stats(player1_wins, player2_wins, player1_score, player2_score):
    """Shows game statistics"""
    pass


Sample Output:


🎯 HIGH-LOW CHALLENGE 🎯
1. Single Player
2. Multiplayer
Choice: 1

Select Difficulty:
1. Easy (1-20, 10 attempts)
2. Medium (1-50, 7 attempts)
3. Hard (1-100, 5 attempts)
4. Impossible (1-500, 3 attempts)
Choice: 2

I'm thinking of a number between 1-50.
You have 7 attempts.

Attempt 1: 25
Too low! 🔽 (6 attempts left)
[Score: 100]

Attempt 2: 40
Too high! 🔼 (5 attempts left)
[Score: 90]

Attempt 3: 32
Too low! 🔽 (4 attempts left)
Would you like a hint? (y/n): y
Hint: The number is even
[Hint used - Score: 75]

Attempt 4: 36
Too low! 🔽 (3 attempts left)

Attempt 5: 42
🎉 CORRECT! You got it in 5 attempts!

🏆 FINAL SCORE: 120
(100 base + 20 bonus - 0 penalties - 15 hints)

Play again? (y/n): y


Concepts Tested: while loops, nested conditionals, functions with multiple return values, scope, break, continue, pass, range(), list/dict for storing stats

'''

import random


def select_difficulty():
    """Returns (max_number, max_attempts) based on user choice"""
    while True:
        print("\nSelect Difficulty:")
        print("1. Easy (1-20, 10 attempts)")
        print("2. Medium (1-50, 7 attempts)")
        print("3. Hard (1-100, 5 attempts)")
        print("4. Impossible (1-500, 3 attempts)")

        choice = input("Choice: ").strip()

        match choice:
            case "1":
                print("Easy mode selected")
                return 20, 10
            case "2":
                print("Medium mode selected")
                return 50, 7
            case "3":
                print("Hard mode selected")
                return 100, 5
            case "4":
                print("Impossible mode selected")
                return 500, 3
            case _:
                print(f"Hmm!!! you inputted {choice}")
                print("⚠️ Invalid choice! Please select 1, 2, 3, or 4.")


def generate_number(max_num, player1=None):
    """If player1 is provided, use their number; otherwise generate random."""
    if player1 is not None:
        return player1
    return random.randint(1, max_num)


def give_hint(number, hints_used):
    """Returns a hint string based on the secret number and hint iteration count."""
    if hints_used == 1:
        if number % 2 == 0:
            return "The number is EVEN."
        return "The number is ODD."
    elif hints_used == 2:
        if number % 5 == 0:
            return "The number IS divisible by 5."
        return "The number IS NOT divisible by 5."
    else:
        if number % 10 == 0:
            return "The number IS divisible by 10."
        return f"The last digit of the number is {number % 10}."


def calculate_score(attempts_used, max_attempts, hints_used, won=True):
    """Returns the final calculated score."""
    if not won:
        return 0

    base_score = 100
    bonus = (max_attempts - attempts_used) * 10
    penalties = (attempts_used - 1) * 10
    hint_cost = hints_used * 15

    total_score = base_score + bonus - penalties - hint_cost
    return max(0, total_score)


def display_stats(player1_wins, player2_wins, player1_score, player2_score):
    """Shows global game statistics."""
    print("\n" + "=" * 35)
    print("      🏆 GAME STATISTICS 🏆      ")
    print("=" * 35)
    print(f"Player 1 - Wins: {player1_wins} | Total Score: {player1_score}")
    print(f"Player 2 - Wins: {player2_wins} | Total Score: {player2_score}")
    print("=" * 35 + "\n")


def main():
    # Overall persistent session stats across rounds
    p1_wins, p2_wins = 0, 0
    p1_score, p2_score = 0, 0

    # Role switcher for Multiplayer mode (True = P1 sets / P2 guesses)
    p1_sets_number = True

    while True:
        print("\n🎯 HIGH-LOW CHALLENGE 🎯")
        print("1. Single Player")
        print("2. Multiplayer")
        print("3. Exit Game")

        mode_choice = input("Choice: ").strip()

        if mode_choice == "3":
            print("\nThanks for playing! Goodbye! 👋")
            break

        if mode_choice not in ["1", "2"]:
            print("⚠️ Invalid selection. Please enter 1, 2, or 3.")
            continue

        # Setup Game
        max_num, max_att = select_difficulty()

        if mode_choice == "1":
            guesser_name = input("What is your tech name: ")
            if guesser_name == "":
                guesser_name = "Player"
            secret = generate_number(max_num)
            print(f"\nOkay {guesser_name},\nI'm thinking of a number between 1-{max_num}.")
        else:
            setter_name = "Player 1" if p1_sets_number else "Player 2"
            guesser_name = "Player 2" if p1_sets_number else "Player 1"

            print(f"\n🎮 {setter_name}'s turn to set the secret number!")

            # Safely prompt the setting player for a number in secret
            while True:
                try:
                    secret_input = int(input(f"{setter_name}, enter a secret number (1-{max_num}): "))
                    if 1 <= secret_input <= max_num:
                        secret = generate_number(max_num, player1=secret_input)
                        break
                    print(f"⚠️ Number must be between 1 and {max_num}!")
                except ValueError:
                    print("⚠️ Please enter a valid integer.")

            # Scroll screen down so the guesser can't see the set number
            print("\n" * 50)
            print(f"🎮 {guesser_name}'s turn to guess! Number is set between 1-{max_num}.")

        print(f"You have {max_att} attempts.")

        # Gameplay Loop
        num_attempt = 0
        hints_used = 0
        won = False

        while num_attempt < max_att:
            num_attempt += 1

            # Validate input guess
            try:
                guess = int(
                    input(f"\nAttempt {num_attempt}/{max_att} - Enter guess: ")
                )
            except ValueError:
                print("⚠️ Please enter a valid number!")
                num_attempt -= 1  # Do not penalize for malformed text input
                continue

            if guess < 1 or guess > max_num:
                print(f"⚠️ Stay between 1 and {max_num}!")
                num_attempt -= 1
                continue

            # Check Guess
            if guess == secret:
                won = True
                print(
                    f"\n🎉 CORRECT! {guesser_name} got it in {num_attempt} attempts!"
                )
                break
            elif guess > secret:
                print("Too high! 🔼")
            else:
                print("Too low! 🔽")

            if abs(guess - secret) <= 5:
                print("You're close! 🔥")

            attempts_left = max_att - num_attempt

            # Hint Option logic
            if attempts_left > 0 and hints_used < 3:
                want_hint = (
                    input("Would you like a hint? (costs 15 pts) (y/n): ")
                    .strip()
                    .lower()
                )
                if want_hint == "y":
                    hints_used += 1
                    hint_msg = give_hint(secret, hints_used)
                    print(f"💡 HINT #{hints_used}: {hint_msg}")

            if attempts_left > 0:
                print(f"({attempts_left} attempts left)")

        # End of Round Scoring
        if not won:
            print(f"\n💀 Game over! The secret number was {secret}.")

        round_score = calculate_score(num_attempt, max_att, hints_used, won=won)
        print(f"\n🏆 ROUND SCORE: {round_score}")
        print(f"(100 base + {(max_att - num_attempt)*10 if won else 0} bonus - {(num_attempt-1)*10} penalties - {hints_used*15} hints)")

        # Update persistent stats
        if mode_choice == "1":
            if won:
                p1_wins += 1
            p1_score += round_score
        else:
            if won:
                if p1_sets_number:
                    p2_wins += 1
                    p2_score += round_score
                else:
                    p1_wins += 1
                    p1_score += round_score
            # Switch roles for next round
            p1_sets_number = not p1_sets_number

        display_stats(p1_wins, p2_wins, p1_score, p2_score)

        again = input("Play another round? (y/n): ").strip().lower()
        if again != "y":
            print("\nReturning to main menu...")


if __name__ == "__main__":
    main()