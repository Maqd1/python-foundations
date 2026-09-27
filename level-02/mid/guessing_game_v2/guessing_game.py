

import random

secret_number = random.randint(1, 100)
max_attempt = 7
num_attempt = 0

while num_attempt < max_attempt:
    guess = int(input("Guess the number: "))
    num_attempt += 1
    attempt_left = max_attempt - num_attempt

    if guess > 100 or guess < 0:
        print("⚠️ THIS IS NOT A VALID RANGE! Please stay between 1 and 100.")
        continue

    if guess == secret_number:
        print("Congratulations, you got it right!")
        print(f"You got it right in {num_attempt} attempts out of the total of {max_attempt} attempts.")
        break
    elif guess > secret_number:
        print("Too high! 🔼")
        if abs(guess - secret_number) <= 5:
            print("You're close! 🔥")
    elif guess < secret_number:
        print("Too low! 🔽")
        if abs(guess - secret_number) <= 5:
            print("You're close! 🔥")

    if attempt_left > 0:
        print(f"You have {attempt_left} attempts left.\n")
    
    if num_attempt == max_attempt and guess != secret_number:
        print(f"💀 Game over! The number was {secret_number}")