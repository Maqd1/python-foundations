##Q1. The Autobiographer (Easy)
#Write a program that asks the user for their first_name, last_name, and birth_year.

#· Calculate their age (assume current year is 2026).
#· Print: "Your name is [Full Name] and you are [Age] years old." using an f-string.
#· Goal: Practice input(), int(), f-strings, and arithmetic.

first_name = input("enter your first_name:")
last_name =input("enter your last_name:")
birth_year =int(input("enter your birth_year:"))

age = 2026 - birth_year
print(f"Your name is {first_name} {last_name} and you are {age} years old.")