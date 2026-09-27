'''
🟢 Easy Level (2 Questions)
Q1: The Calculator Module (Easy)

Create a module called calculator.py with these functions:

Requirements:

    Functions: add(), subtract(), multiply(), divide(), power(), sqrt()

    Add proper docstrings to each function

    Include error handling for division by zero and negative sqrt

    Create main.py that imports and uses the calculator

    In main.py, ask user for operation and two numbers

    Keep asking until user types 'quit'

Bonus:

    Add modulus() (%), floor_division() (//)

    Keep calculation history in a list

Sample Output:
text

🧮 CALCULATOR MODULE 🧮
1. Add
2. Subtract
3. Multiply
4. Divide
5. Power
6. Square Root
7. History
8. Quit

Choice: 1
Enter first number: 15
Enter second number: 7
Result: 15 + 7 = 22

Choice: 6
Enter number: 144
Result: √144 = 12.0

Choice: 7
📜 History:
1: 15 + 7 = 22
2: sqrt(144) = 12.0

Concepts: Function creation, docstrings, error handling, imports, loops
'''


import math

history = [] # to store all calculations

def add(a, b):
    """Return the sum of a and b."""
    result = a + b
    history.append(f"{a} + {b} = {result}")
    return result

def subtract(a, b):
    """Return the difference of a and b."""
    result = a - b
    history.append(f"{a} - {b} = {result}")
    return result

def multiply(a, b):
    """Return the product of a and b."""
    result = a * b
    history.append(f"{a} * {b} = {result}")
    return result

def divide(a, b):
    """Return a divided by b. Handles division by zero."""
    if b == 0:
        raise ZeroDivisionError("Cannot divide by zero")
    result = a / b
    history.append(f"{a} / {b} = {result}")
    return result

def power(a, b):
    """Return a raised to the power of b."""
    result = a ** b
    history.append(f"{a} ^ {b} = {result}")
    return result

def sqrt(a):
    """Return the square root of a. Handles negative numbers."""
    if a < 0:
        raise ValueError("Cannot take square root of a negative number")
    result = math.sqrt(a)
    history.append(f"sqrt({a}) = {result}")
    return result

# Bonus functions
def modulus(a, b):
    """Return the remainder of a divided by b."""
    if b == 0:
        raise ZeroDivisionError("Cannot divide by zero")
    result = a % b
    history.append(f"{a} % {b} = {result}")
    return result

def floor_division(a, b):
    """Return the floor division of a by b."""
    if b == 0:
        raise ZeroDivisionError("Cannot divide by zero")
    result = a // b
    history.append(f"{a} // {b} = {result}")
    return result

def get_history():
    """Return the calculation history."""
    return history


def show_menu():
    print("\n🧮 CALCULATOR MODULE 🧮")
    print("1. Add")
    print("2. Subtract")
    print("3. Multiply")
    print("4. Divide")
    print("5. Power")
    print("6. Square Root")
    print("7. History")
    print("8. Quit")

while True:
    show_menu()
    choice = input("Choice: ").strip().lower()

    if choice == '8' or choice == 'quit':
        print("Goodbye!")
        break

    try:
        if choice == '1':
            a = float(input("Enter first number: "))
            b = float(input("Enter second number: "))
            print(f"Result: {a} + {b} = {add(a, b)}")

        elif choice == '2':
            a = float(input("Enter first number: "))
            b = float(input("Enter second number: "))
            print(f"Result: {a} - {b} = {subtract(a, b)}")

        elif choice == '3':
            a = float(input("Enter first number: "))
            b = float(input("Enter second number: "))
            print(f"Result: {a} * {b} = {multiply(a, b)}")

        elif choice == '4':
            a = float(input("Enter first number: "))
            b = float(input("Enter second number: "))
            print(f"Result: {a} / {b} = {divide(a, b)}")

        elif choice == '5':
            a = float(input("Enter base number: "))
            b = float(input("Enter power: "))
            print(f"Result: {a} ^ {b} = {power(a, b)}")

        elif choice == '6':
            a = float(input("Enter number: "))
            print(f"Result: √{a} = {sqrt(a)}")

        elif choice == '7':
            print("\n📜 History:")
            hist = get_history()
            if not hist:
                print("No calculations yet.")
            else:
                for i, item in enumerate(hist, 1):
                    print(f"{i}: {item}")
        else:
            print("Invalid choice. Try again.")

    except (ValueError, ZeroDivisionError) as e:
        print(f"Error: {e}")