# Guessing Game with Limited Attempts

## Mid Level

Write a program that generates a random number and gives the user a limited number of attempts to guess it.

### Requirements

The program should:

1. Generate a random number between **1 and 100**.
2. Give the user **7 attempts** to guess the number.
3. After each incorrect guess:

   * Print `Too high! 🔼` if the guess is too high.
   * Print `Too low! 🔽` if the guess is too low.
   * Show the remaining attempts:

     ```text
     You have X attempts left
     ```
4. If the user guesses correctly:

   ```text
   🎉 You got it in X attempts!
   ```
5. If the user uses all attempts without guessing correctly:

   ```text
   💀 Game over! The number was X
   ```

### Extra Challenge

If the user's guess is within **5** of the secret number, print:

```text
You're close! 🔥
```

### Concepts

* `while` loop
* `break`
* `random`
* Conditional logic

### Example Flow

```text
Enter your guess: 60
Too high! 🔼
You have 6 attempts left

Enter your guess: 45
Too low! 🔽
You have 5 attempts left

Enter your guess: 50
🎉 You got it in 3 attempts!
```
