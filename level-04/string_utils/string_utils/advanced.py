"""advanced.py - Advanced string operations"""
from collections import Counter
import re

def capitalize_words(text):
    """Capitalize the first letter of each word."""
    return text.title()

def remove_duplicates(text):
    """Remove consecutive duplicate characters."""
    result = ""
    for i in range(len(text)):
        if i == 0 or text[i]!= text[i-1]:
            result += text[i]
    return result

def count_words(text):
    """Return the number of words in text."""
    return len(text.split())

def most_common_words(text, n):
    """Return the n most common words as a dict {word: count}."""
    words = re.findall(r'\b\w+\b', text.lower())
    return dict(Counter(words).most_common(n))