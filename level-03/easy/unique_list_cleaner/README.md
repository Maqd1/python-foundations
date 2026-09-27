# 🧹 Unique List Cleaner

## Q2 — The Unique List Cleaner (Easy)

Write a program that removes duplicate values from lists.

The program should demonstrate how **sets** can be used to remove duplicates, while the extra challenge requires preserving the original order using a combination of a **list and set**.

---

# 🔢 1. Numbers List

Create a list containing duplicate numbers:

```python
numbers = [
    1, 2, 2, 3, 4, 4, 4, 5,
    6, 6, 7, 8, 8, 8, 9, 9
]
```

---

# 👥 2. Names List

Create a list containing duplicate names:

```python
names = [
    "John",
    "Jane",
    "John",
    "Bob",
    "Jane",
    "Alice",
    "Bob"
]
```

---

# 🧹 3. Remove Duplicates Using a Set

Use a **set** to remove duplicate values from the lists.

For example:

```python
unique_numbers = list(set(numbers))
```

The set automatically keeps only one occurrence of each value.

Convert the set back to a list when necessary.

---

# 📋 4. Display the Original and Cleaned Lists

Print both the original list and the list after removing duplicates.

For the numbers, the output should show the original values and the unique values.

Also do the same for the names.

---

# 🔢 5. Count Removed Duplicates

Calculate how many duplicate values were removed.

The number of duplicates removed can be found by comparing the lengths of the original and cleaned lists.

For example:

```python
duplicates_removed = len(numbers) - len(cleaned_numbers)
```

---

# ⭐ 6. Extra Challenge — Preserve Original Order

A normal set does not provide the intended way to preserve the original order of the list.

Create a solution that:

* Removes duplicates.
* Keeps the first occurrence of each value.
* Preserves the original order.

### Hint

Use a combination of:

* A list to store the cleaned values.
* A set to keep track of values already seen.

For example, conceptually:

```text
Original:
John → Jane → John → Bob → Jane → Alice → Bob

First John   → keep
First Jane   → keep
Second John  → skip
First Bob    → keep
Second Jane  → skip
First Alice  → keep
Second Bob   → skip

Result:
John → Jane → Bob → Alice
```

---

# 🖥️ Sample Output

```text
Original: [1, 2, 2, 3, 4, 4, 4, 5, 6, 6, 7, 8, 8, 8, 9, 9]
Cleaned: [1, 2, 3, 4, 5, 6, 7, 8, 9]
Removed 7 duplicates!

Names original: ['John', 'Jane', 'John', 'Bob', 'Jane', 'Alice', 'Bob']
Names cleaned (preserving order): ['John', 'Jane', 'Bob', 'Alice']
Removed 3 duplicates!
```

---

# 🧠 Concepts Tested

This exercise focuses on:

* Sets
* Lists
* `len()`
* Type conversion
* Membership testing
* Removing duplicates
* Preserving list order
* Using a set for efficient membership checks
