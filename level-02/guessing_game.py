#The Guessing Game with Limited Attempts (Mid)

#Write a program that:

#    Generates a random number between 1-100

#    Gives the user 7 attempts to guess it

#    After each guess:

#        "Too high! 🔼" or "Too low! 🔽"

#        Shows remaining attempts: "You have X attempts left"

#    If they guess correctly: "🎉 You got it in X attempts!"

#    If they run out of attempts: "💀 Game over! The number was X"

#    Extra challenge: If they guess within 5 of the number, print "You're close! 🔥"

#Concepts: while loop, break, random, conditionals

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
    
    # Your excellent terminal check
    if num_attempt == max_attempt and guess != secret_number:
        print(f"💀 Game over! The number was {secret_number}")