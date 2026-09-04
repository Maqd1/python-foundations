'''
Core 5

🎯 HARD NUMBER GUESSING

The Mastermind Number Cracking Game 🔢

Create an advanced number guessing game where players crack a secret code with feedback!

Core Concept: The computer picks a 3-digit number (digits can repeat) and the player has to guess it. After each guess, the computer gives feedback:

· 🟢 Green: Correct digit in the correct position
· 🟡 Yellow: Correct digit in the wrong position
· 🔴 Red: Wrong digit

This is like the board game Mastermind but with numbers!

Technical Requirements:

1. Secret Number Generation (HARD):
   · Generate a 3-digit number (000-999)
   · Track how many attempts
   · Allow player to choose length: 3, 4, or 5 digits
2. Feedback System (HARDER):
   ```python
   def get_feedback(secret, guess):
       """Returns a tuple of (green_count, yellow_count, red_count)"""
       pass
   
   def display_feedback(guess, green, yellow, red):
       """Visually displays the feedback with colors"""
       pass
   ```
3. AI Helper (HARDEST):
   · After 3 wrong guesses, offer a "hint" button
   · Hint reveals: "The sum of digits is X"
   · After 5 wrong guesses: "One digit is X"
   · After 7 wrong guesses: "The first digit is X"
4. Score System:
   · Points = 100 - (attempts × 5)
   · Bonus for digit length: 3 digits = no bonus, 4 digits = +20, 5 digits = +50
   · Penalty for using hints: -15 points per hint
5. Statistics:
   · Games played
   · Win rate
   · Average attempts to win
   · Best score
   · Guess history for current game

Sample Output:

```
🔢 MASTERMIND NUMBER CRACKER 🔢

Select difficulty (3/4/5 digits): 3

I'm thinking of a 3-digit number (000-999).
You have unlimited attempts.

⏰ Attempt 1: 123
🔴🔴🔴 (0 correct, 0 misplaced)
No digits match! You haven't used any of the secret digits.

⏰ Attempt 2: 456
🟡🔴🔴 (0 correct, 1 misplaced)
One digit is in the number but in the wrong position.

⏰ Attempt 3: 465
🟢🟡🔴 (1 correct, 1 misplaced)
One digit is exactly right!

⚠️ Hint available! Use it? (y/n): y
💡 Hint: The sum of digits is 15
Penalty: -15 points

⏰ Attempt 4: 475
🟢🟢🔴 (2 correct, 0 misplaced)
Two digits are exactly right!

⏰ Attempt 5: 478
🎉🎉🎉 ALL GREEN! You cracked the code!

✅ Secret number was: 478

📊 GAME STATISTICS:
Attempts: 5
Points: 100 - (5×5) - 15 = 60
Digits: 3
Hints used: 1
Time: 1 minute 23 seconds

Would you like to see your guess history? (y/n): y

📈 GUESS HISTORY:
1. 123 → 🔴🔴🔴
2. 456 → 🟡🔴🔴
3. 465 → 🟢🟡🔴
4. 475 → 🟢🟢🔴
5. 478 → 🟢🟢🟢

Play again? (y/n): n

📊 ALL-TIME STATISTICS:
Games played: 5
Wins: 4 (80%)
Average attempts: 6.5
Best score: 75
Total points: 235
```

Concepts Tested: Functions with lists/dicts, string manipulation, while loops with break conditions, nested conditional logic, list comprehensions (for checking digits), zip() for pairing digits, enumerate() for index tracking, complex algorithm development

---
'''

import random
import time

# ==========================================
# GLOBAL STATS & DATA STRUCTURES
# ==========================================

stats = {
    "games_played": 0,
    "wins": 0,
    "total_attempts_won": 0,
    "best_score": 0,
    "total_points": 0,
}

# ==========================================
# FEEDBACK ALGORITHM
# ==========================================


def get_feedback(secret, guess):
    """Calculates green (exact match), yellow (wrong position), and red (not found) counts.

    Handles duplicate digits accurately using a 2-pass algorithm.
    """
    length = len(secret)
    green = 0
    yellow = 0

    secret_unmatched = []
    guess_unmatched = []

    # Pass 1: Check for exact position matches (Greens)
    for s_char, g_char in zip(secret, guess):
        if s_char == g_char:
            green += 1
        else:
            secret_unmatched.append(s_char)
            guess_unmatched.append(g_char)

    # Pass 2: Check for misplaced digits (Yellows) among remaining unmatched digits
    for g_char in guess_unmatched:
        if g_char in secret_unmatched:
            yellow += 1
            secret_unmatched.remove(g_char)  # Consume matched digit

    red = length - (green + yellow)
    return green, yellow, red


def display_feedback(guess, green, yellow, red):
    """Formats and prints visual feedback indicators."""
    indicators = ("🟢" * green) + ("🟡" * yellow) + ("🔴" * red)
    print(f"{indicators} ({green} correct, {yellow} misplaced)")

    if green == len(guess):
        print("🎉🎉🎉 ALL GREEN! You cracked the code!")
    elif green > 0 and yellow > 0:
        print(f"{green} digit(s) exact, {yellow} digit(s) misplaced.")
    elif green > 0:
        print(f"{green} digit(s) exactly right!")
    elif yellow > 0:
        print(f"{yellow} digit(s) in the number but in wrong position.")
    else:
        print("No digits match!")


# ==========================================
# GAME LOGIC
# ==========================================


def play_game():
    print("\n🔢 MASTERMIND NUMBER CRACKER 🔢\n")

    # Select length
    while True:
        length_input = input("Select difficulty (3/4/5 digits): ").strip()
        if length_input in ["3", "4", "5"]:
            length = int(length_input)
            break
        print("Invalid choice! Please choose 3, 4, or 5.")

    # Secret number setup (padded with leading zeros if necessary)
    secret_int = random.randint(0, (10**length) - 1)
    secret = str(secret_int).zfill(length)

    max_range = (10**length) - 1
    min_range_str = "0" * length
    print(
        f"\nI'm thinking of a {length}-digit number ({min_range_str}-{max_range})."
    )
    print("You have unlimited attempts.\n")

    attempts = 0
    hints_used = 0
    hints_revealed = {"sum": False, "one_digit": False, "first_digit": False}
    guess_history = []  # Stores tuples: (guess_str, feedback_str)

    start_time = time.time()

    while True:
        attempts += 1

        # Validate input
        while True:
            guess = input(f"⏰ Attempt {attempts}: ").strip()
            if len(guess) == length and guess.isdigit():
                break
            print(f"Please enter a valid {length}-digit number.")

        green, yellow, red = get_feedback(secret, guess)
        feedback_str = ("🟢" * green) + ("🟡" * yellow) + ("🔴" * red)
        guess_history.append((guess, feedback_str))

        display_feedback(guess, green, yellow, red)

        # Check win condition
        if green == length:
            end_time = time.time()
            elapsed_seconds = int(end_time - start_time)
            mins, secs = divmod(elapsed_seconds, 60)
            time_formatted = (
                f"{mins} minute(s) {secs} seconds"
                if mins
                else f"{secs} seconds"
            )

            # Score calculation
            base_score = 100 - (attempts * 5)
            length_bonus = 0 if length == 3 else (20 if length == 4 else 50)
            hint_penalty = hints_used * 15
            final_score = max(0, base_score + length_bonus - hint_penalty)

            print(f"\n✅ Secret number was: {secret}")
            print("\n📊 GAME STATISTICS:")
            print(f"Attempts: {attempts}")
            print(
                f"Points: 100 - ({attempts}×5) + {length_bonus} (bonus) - {hint_penalty} (hints) = {final_score}"
            )
            print(f"Digits: {length}")
            print(f"Hints used: {hints_used}")
            print(f"Time: {time_formatted}")

            # Update overall stats
            stats["games_played"] += 1
            stats["wins"] += 1
            stats["total_attempts_won"] += attempts
            stats["total_points"] += final_score
            if final_score > stats["best_score"]:
                stats["best_score"] = final_score

            break

        # AI Helper Hints
        if attempts >= 3 and not hints_revealed["sum"]:
            use_hint = (
                input("\n⚠️ Hint available! Use it? (y/n): ").strip().lower()
            )
            if use_hint == "y":
                hints_used += 1
                hints_revealed["sum"] = True
                digit_sum = sum(int(d) for d in secret)
                print(f"💡 Hint: The sum of digits is {digit_sum}")
                print("Penalty: -15 points\n")

        elif attempts >= 5 and not hints_revealed["one_digit"]:
            use_hint = (
                input("\n⚠️ Hint available! Use it? (y/n): ").strip().lower()
            )
            if use_hint == "y":
                hints_used += 1
                hints_revealed["one_digit"] = True
                sample_digit = random.choice(list(secret))
                print(f"💡 Hint: One digit is {sample_digit}")
                print("Penalty: -15 points\n")

        elif attempts >= 7 and not hints_revealed["first_digit"]:
            use_hint = (
                input("\n⚠️ Hint available! Use it? (y/n): ").strip().lower()
            )
            if use_hint == "y":
                hints_used += 1
                hints_revealed["first_digit"] = True
                print(f"💡 Hint: The first digit is {secret[0]}")
                print("Penalty: -15 points\n")

    # Display history option
    show_hist = (
        input("\nWould you like to see your guess history? (y/n): ")
        .strip()
        .lower()
    )
    if show_hist == "y":
        print("\n📈 GUESS HISTORY:")
        for idx, (g, fb) in enumerate(guess_history, 1):
            print(f"{idx}. {g} → {fb}")


# ==========================================
# MAIN ROUTINE & ALL-TIME STATS
# ==========================================


def display_all_time_stats():
    print("\n" + "=" * 35)
    print("📊 ALL-TIME STATISTICS:")
    print("=" * 35)

    played = stats["games_played"]
    wins = stats["wins"]

    if played == 0:
        print("No games played yet.")
        return

    win_rate = (wins / played) * 100
    avg_attempts = stats["total_attempts_won"] / wins if wins > 0 else 0

    print(f"Games played: {played}")
    print(f"Wins: {wins} ({win_rate:.0f}%)")
    print(f"Average attempts: {avg_attempts:.1f}")
    print(f"Best score: {stats['best_score']}")
    print(f"Total points: {stats['total_points']}")


def main():
    while True:
        play_game()
        again = input("\nPlay again? (y/n): ").strip().lower()
        if again != "y":
            display_all_time_stats()
            print("\nThanks for playing!")
            break


if __name__ == "__main__":
    main()