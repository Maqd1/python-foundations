# The Modulo Clock

## Difficulty

Hard

## Task

Write a program that asks the user for a total number of seconds.

Convert the total seconds into:

- Hours
- Minutes
- Seconds

Print the result in this format:

```text
Hours: X
Minutes: Y
Seconds: Z
```

For example, if the user enters:

3665

the program should print:

Hours: 1
Minutes: 1
Seconds: 5

## Hint

Use floor division (//) and modulo (%).

The formulas are:

hours = total_seconds // 3600
minutes = (total_seconds % 3600) // 60
seconds = total_seconds % 60

## Goal

Understand how division and modulo can be combined to break a total value into meaningful units.

## Concepts Tested
- input()
- int()
- Floor division (//)
- Modulo (%)
- Arithmetic
- Variables
- Formatted output