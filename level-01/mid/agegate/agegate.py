

user_age = int(input("What is your age? "))
remaining = 18 - user_age

if user_age >= 18:
    print("Access granted. Welcome!")
else:
    print(f"Access denied. You need {remaining} more years")