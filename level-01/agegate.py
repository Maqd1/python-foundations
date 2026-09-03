#Q4. The Age Gate (Mid)
#Write a program that asks for the user's age (as an integer).

#· If they are 18 or older, print: "Access granted. Welcome!"
#· If they are under 18, calculate how many years until they turn 18 and print: "Access denied. You need X more years."
#· Goal: Use if/else conditionals (introduced here as a prerequisite for the hard ones) combined with assignment and arithmetic.

user_age = int(input("What is your age? "))
remaining = 18 - user_age

if user_age >= 18:
    print("Access granted. Welcome!")
else:
    print(f"Access denied. You need {remaining} more years")