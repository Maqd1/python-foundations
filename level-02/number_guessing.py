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