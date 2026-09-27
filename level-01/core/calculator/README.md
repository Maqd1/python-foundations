# The Memory Calculator

## Difficulty

Core

## Task

Write a calculator that supports these operations:

- Addition (`+`)
- Subtraction (`-`)
- Multiplication (`*`)
- Division (`/`)
- Floor division (`//`)
- Modulo (`%`)
- Exponentiation (`**`)

The calculator should:

1. Ask the user for two numbers.
2. Ask for an operator.
3. Calculate and display the result.
4. Store the result in memory.
5. Ask whether the user wants to continue using the current result.

If the user chooses `y`, use the current result as the first number in the next calculation.

For example:

```text
10 + 5 = 15

Continue? y

15 * 2 = 30
```

If the user chooses n, start a fresh calculation with two new numbers.

The user should also be able to type quit to exit the calculator at any time.

## Goal

Build a calculator that uses loops, variables, reassignment, input handling, and a stored result instead of performing only one calculation.

## Concepts Tested
- Variables
- Variable reassignment
- input()
- float()
- Arithmetic operators
- Comparison operators
- Logical operators
- while
- Conditional statements
- String formatting
- Input validation