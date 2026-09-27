'''
Q2: The String Utilities Package (Easy)

Create a package called string_utils with modules for different string operations.

Requirements:

    Create package structure:
    text

    string_utils/
        __init__.py
        basic.py
        advanced.py

    basic.py functions:

        reverse(text) → Returns reversed string

        is_palindrome(text) → True/False (case-insensitive)

        count_vowels(text) → Returns count

        count_consonants(text) → Returns count

    advanced.py functions:

        capitalize_words(text) → Capitalizes each word

        remove_duplicates(text) → Removes consecutive duplicates

        count_words(text) → Returns word count

        most_common_words(text, n) → Returns n most common words

    __init__.py should import key functions

    Create main.py that imports and uses the package

Sample Output:
text

📝 STRING UTILITIES PACKAGE 📝

Text: "Hello world, hello Python"

Basic operations:
Reverse: "nohtyP olleh ,dlrow olleH"
Is palindrome? False
Vowels: 6
Consonants: 13

Advanced operations:
Capitalized: "Hello World, Hello Python"
Removed duplicates: "Helo world, helo Python"
Word count: 5
Most common words (2): hello:2, Python:1

Concepts: Package creation, module imports, string methods, dictionary comprehensions
'''

"""main.py - Test the string_utils package"""

from string_utils import *

text = input('Text: "')

print('\n📝 STRING UTILITIES PACKAGE 📝')
print(f'\nText: "{text}"')

print("\nBasic operations:")
print(f'Reverse: "{reverse(text)}"')
print(f'Is palindrome? {is_palindrome(text)}')
print(f'Vowels: {count_vowels(text)}')
print(f'Consonants: {count_consonants(text)}')

print("\nAdvanced operations:")
print(f'Capitalized: "{capitalize_words(text)}"')
print(f'Removed duplicates: "{remove_duplicates(text)}"')
print(f'Word count: {count_words(text)}')

n = 2
common = most_common_words(text, n)
common_str = ", ".join([f"{k}:{v}" for k, v in common.items()])
print(f'Most common words ({n}): {common_str}')