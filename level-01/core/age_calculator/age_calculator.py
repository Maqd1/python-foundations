
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