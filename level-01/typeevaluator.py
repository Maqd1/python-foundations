#Q7. The Dynamic Type Evaluator (Hard)
#Write a program that asks the user for one single value (e.g., "123", "3.14", "Hello", or "" (just press enter)).

#· Store it as a variable user_input.
#· Print the following without using if statements (only use type conversion and boolean logic):
#  1. "Is it a number (int)? " followed by True or False (Hint: try converting it using int(), but beware—it might crash! Figure out how to handle it, or use string methods like .isdigit()).
#  2. "Boolean value: " followed by the boolean equivalent of the input.
#  3. "Length of string: " followed by the number of characters.
#· Goal: Combine type conversion, string methods (.isdigit()), len(), and bool() logic. This forces you to think about how Python evaluates data in edge cases (empty string, numbers, etc.).

value = input("Enter a single value: ")

is_number = value.isdigit()
is_boolean = bool(value)
length = len(value)

print(f"Is it a number (int)? {is_number}")
print(f"Boolean value: {is_boolean}")
print(f"Length of string: {length}")