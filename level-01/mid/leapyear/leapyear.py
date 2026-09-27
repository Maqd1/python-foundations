

input_year = int(input("Enter a year to confirm if it is a leap year or not: "))

confirm = input_year % 4 == 0 and (input_year % 100 != 0 or input_year % 400 == 0)

print(confirm)