#📅 HARD AGE CALCULATOR

#The Precise Age Calculator 🎯

#Write a program that:

#1. Asks for birth date: day, month, year
#2. Asks for current date: day, month, year (or use today's date)
#3. Calculates exact age in:
#   · Years (e.g., 28)
#   · Months (e.g., 28 years and 5 months)
#   · Days (e.g., 28 years, 5 months, and 12 days)
#   · Total days alive (e.g., 10,412 days)
#4. Prints a birthday countdown: "Your next birthday is in 187 days!"

#🚨 The Hard Part: You must handle:

#· Months with different days (28, 30, 31)
#· February in leap years
#· If the user's birthday hasn't occurred yet this year, subtract a year
#· Edge case: If today is their birthday, print "Happy Birthday! 🎂"

#Concepts Tested:

#· int() conversion
#· if/elif/else logic
#· Comparison operators
#· Arithmetic operators
#· Modulo (%) for calculations
#· Boolean logic for date comparisons
#· String formatting

#Hints:

#· Use days_in_month logic: [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
#· Leap year check: (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)




day = int(input("What day were you born? "))
month = int(input("What month were you born? "))
year = int(input("What year were you born? "))

curr_day = int(input("What day is it today? "))
curr_month = int(input("What month is it today? "))
curr_year = int(input("What year is it today? "))

years = curr_year - year
months = curr_month - month

if months < 0:
    years -= 1
    months += 12

print(f"{years} years and {months} months")

def is_leap(y):
    return (y % 4 == 0 and y % 100 != 0) or (y % 400 == 0)

days_in_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

days = curr_day - day

if days < 0:
    months -= 1
    # figure out which month we're borrowing from
    borrow_month = curr_month - 1
    prev_year = curr_year
    if borrow_month == 0:
        borrow_month = 12
        prev_year -= 1

    if borrow_month == 2 and is_leap(prev_year):
        days += 29
    else:
        days += days_in_month[borrow_month - 1]

print(f"{years} years, {months} months, and {days} days")

def day_of_year(d, m, y):
    dim = days_in_month.copy()
    if is_leap(y):
        dim[1] = 29  # February gets an extra day
    return sum(dim[:m - 1]) + d

total_days = 0
for y in range(year, curr_year):
    total_days += 366 if is_leap(y) else 365

total_days += day_of_year(curr_day, curr_month, curr_year) - day_of_year(day, month, year)

print(f"Total days alive: {total_days}")

current_doy = day_of_year(curr_day, curr_month, curr_year)
birthday_doy_this_year = day_of_year(day, month, curr_year)

if birthday_doy_this_year == current_doy:
    print("Happy Birthday! 🎂")
elif birthday_doy_this_year > current_doy:
    days_until = birthday_doy_this_year - current_doy
    print(f"Your next birthday is in {days_until} days!")
else:
    days_in_curr_year = 366 if is_leap(curr_year) else 365
    birthday_doy_next_year = day_of_year(day, month, curr_year + 1)
    days_until = (days_in_curr_year - current_doy) + birthday_doy_next_year
    print(f"Your next birthday is in {days_until} days!")