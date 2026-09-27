# The Precise Age Calculator

## Difficulty

Core

## Task

Write a program that asks the user for:

- Birth day
- Birth month
- Birth year
- Current day
- Current month
- Current year

Calculate and display:

- The user's exact age in years, months, and days
- The total number of days the user has been alive
- How many days remain until their next birthday

If the birthday is today, print:

```text
Happy Birthday! 🎂
```

The program must correctly handle:

Different numbers of days in each month
Leap years
Birthdays that have not yet occurred this year
Birthdays that have already occurred this year
A birthday occurring today

## Hint

- Use a list containing the number of days in each month:
    month_days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

- A leap year can be checked using:
    (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)

## Goal

Build confidence with date calculations, leap-year logic, multiple conditions, and careful handling of edge cases.

## Concepts Tested
- input()
- int()
- if/elif/else
- Comparison operators
- Arithmetic
- Modulo (%)
- Boolean logic
- Lists
- String formatting