"""basic.py - Basic string operations"""

def reverse(text):
    """Return the reversed string."""
    return text[::-1]

def is_palindrome(text):
    """Return True if text is a palindrome. Case-insensitive."""
    cleaned = ''.join(char.lower() for char in text if char.isalnum())
    return cleaned == cleaned[::-1]

def count_vowels(text):
    """Return the number of vowels in text."""
    vowels = 'aeiouAEIOU'
    return sum(1 for char in text if char in vowels)

def count_consonants(text):
    """Return the number of consonants in text."""
    return sum(1 for char in text if char.isalpha() and char.lower() not in 'aeiou')