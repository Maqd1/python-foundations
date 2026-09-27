# 🎯 Hard Number Guessing

## The Mastermind Number Cracking Game 🔢

Create an advanced number-guessing game where the player attempts to crack a secret code using feedback after every guess.

The game is inspired by the board game **Mastermind**, but uses numbers.

## Core Concept

The computer generates a secret number.

The player guesses the number and receives feedback describing how closely the guess matches the secret.

### Feedback

🟢 **Green**

Correct digit in the correct position.

🟡 **Yellow**

Correct digit in the wrong position.

🔴 **Red**

Wrong digit.

Digits are allowed to repeat.

## Technical Requirements

### 1. Secret Number Generation — Hard

* Generate a 3-digit number from `000` to `999`.
* Digits can repeat.
* Track the number of attempts.
* Allow the player to choose the secret number length:

  * 3 digits
  * 4 digits
  * 5 digits

### 2. Feedback System — Harder

Implement:

```python
def get_feedback(secret, guess):
    """Returns a tuple of (green_count, yellow_count, red_count)"""
    pass


def display_feedback(guess, green, yellow, red):
    """Visually displays the feedback with colors"""
    pass
```

`get_feedback()` should determine:

* Correct digits in the correct positions.
* Correct digits in incorrect positions.
* Digits that do not occur in the secret.

### 3. AI Helper — Hardest

Hints become available as the player makes incorrect guesses.

After **3 wrong guesses**:

```text
The sum of digits is X
```

After **5 wrong guesses**:

```text
One digit is X
```

After **7 wrong guesses**:

```text
The first digit is X
```

Each hint should have an associated point penalty.

### 4. Score System

Base points:

```text
100
```

Subtract:

```text
attempts × 5
```

### Digit Length Bonuses

| Length   | Bonus |
| -------- | ----: |
| 3 digits |    +0 |
| 4 digits |   +20 |
| 5 digits |   +50 |

### Hint Penalty

Subtract **15 points for every hint used**.

## 5. Statistics

Track:

* Games played
* Win rate
* Average attempts to win
* Best score
* Guess history for the current game

## Sample Output

```text
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

## Concepts Tested

* Functions
* Lists
* Dictionaries
* String manipulation
* `while` loops
* `break`
* Nested conditional logic
* List comprehensions
* `zip()`
* `enumerate()`
* Complex algorithm development
* Feedback processing
* Statistics tracking
