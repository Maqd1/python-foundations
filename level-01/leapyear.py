#Q3. The Leap Year Detective (Mid)
#A year is a leap year if:

#1. It is divisible by 4, AND
#2. It is NOT divisible by 100, UNLESS it is also divisible by 400.
#   Write a program that asks the user for a year (as an integer) and prints True if it's a leap year, and False if not.

#· Hint: Use the Modulo (%) operator and Logical (and/or) operators.
#· Goal: Master comparison, modulo, and complex logical conditions.

input_year = int(input("Enter a year to confirm if it is a leap year or not: "))

confirm = input_year % 4 == 0 and (input_year % 100 != 0 or input_year % 400 == 0)

print(confirm)