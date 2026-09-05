'''
Q2: The Unique List Cleaner (Easy)
Write a program that removes duplicates from a list.
Requirements:

Create a list with duplicate values:
python

numbers = [1, 2, 2, 3, 4, 4, 4, 5, 6, 6, 7, 8, 8, 8, 9, 9]names = ["John", "Jane", "John", "Bob", "Jane", "Alice", "Bob"]
Remove duplicates using a set
Print the original list and the cleaned list
Count how many duplicates were removed
Extra challenge: Preserve the original order (hint: use a list + set combination)
Sample Output:
text

Original: [1, 2, 2, 3, 4, 4, 4, 5, 6, 6, 7, 8, 8, 8, 9, 9]Cleaned: [1, 2, 3, 4, 5, 6, 7, 8, 9]Removed 7 duplicates!Names original: ['John', 'Jane', 'John', 'Bob', 'Jane', 'Alice', 'Bob']Names cleaned (preserving order): ['John', 'Jane', 'Bob', 'Alice']Removed 3 duplicates!
Concepts: Sets, lists, len(), type conversion, membership
'''


# ==========================================
# PART 1: NUMBERS (Basic set conversion)
# ==========================================
numbers = [1, 2, 2, 3, 4, 4, 4, 5, 6, 6, 7, 8, 8, 8, 9, 9]

# Removing duplicates using set conversion
cleaned_numbers = sorted(list(set(numbers)))
num_duplicates_removed = len(numbers) - len(cleaned_numbers)

print(f"Original: {numbers}")
print(f"Cleaned: {cleaned_numbers}")
print(f"Removed {num_duplicates_removed} duplicates!\n")


# ==========================================
# PART 2: NAMES (Order-preserving challenge)
# ==========================================
names = ["John", "Jane", "John", "Bob", "Jane", "Alice", "Bob"]

# Extra Challenge: Preserve original insertion order using a set for lookup
seen = set()
cleaned_names = []

for name in names:
    if name not in seen:
        cleaned_names.append(name)
        seen.add(name)

names_duplicates_removed = len(names) - len(cleaned_names)

print(f"Names original: {names}")
print(f"Names cleaned (preserving order): {cleaned_names}")
print(f"Removed {names_duplicates_removed} duplicates!")# ==========================================
# PART 1: NUMBERS (Basic set conversion)
# ==========================================
numbers = [1, 2, 2, 3, 4, 4, 4, 5, 6, 6, 7, 8, 8, 8, 9, 9]

# Removing duplicates using set conversion
cleaned_numbers = sorted(list(set(numbers)))
num_duplicates_removed = len(numbers) - len(cleaned_numbers)

print(f"Original: {numbers}")
print(f"Cleaned: {cleaned_numbers}")
print(f"Removed {num_duplicates_removed} duplicates!\n")


# ==========================================
# PART 2: NAMES (Order-preserving challenge)
# ==========================================
names = ["John", "Jane", "John", "Bob", "Jane", "Alice", "Bob"]

# Extra Challenge: Preserve original insertion order using a set for lookup
seen = set()
cleaned_names = []

for name in names:
    if name not in seen:
        cleaned_names.append(name)
        seen.add(name)

names_duplicates_removed = len(names) - len(cleaned_names)

print(f"Names original: {names}")
print(f"Names cleaned (preserving order): {cleaned_names}")
print(f"Removed {names_duplicates_removed} duplicates!")