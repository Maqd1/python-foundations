# 📚 Grade Book Manager

## Q1 — The Grade Book Manager (Easy)

Create a program that manages student grades using a **dictionary**.

The program should allow users to view grades, check individual students, add new students, and calculate basic statistics from the grade book.

---

## 📊 Initial Grade Book

Create a dictionary containing five students and their grades:

```python
grades = {
    "Alice": 85,
    "Bob": 92,
    "Charlie": 78,
    "Diana": 95,
    "Eve": 88
}
```

The **student names** are the dictionary keys, while their **grades** are the values.

---

# 📋 1. Display the Grade Book

Print the entire grade book.

The output should show all students and their grades.

---

# 🔍 2. Check a Student's Grade

Ask the user:

```text
Enter student name to check grade:
```

Check whether the student exists in the dictionary.

### If the student exists

Print their grade.

### If the student does not exist

Print:

```text
Student not found!
```

---

# ➕ 3. Add a New Student

Ask the user:

```text
Add new student? (y/n):
```

If the user enters `y`:

1. Ask for the student's name.
2. Ask for the student's grade.
3. Add the new student and grade to the dictionary.

For example:

```python
grades["Frank"] = 90
```

---

# 📊 4. Calculate Grade Statistics

Calculate and print the following:

### Average Grade

Calculate the average grade of all students.

### Highest Grade

Find:

* The highest grade.
* The student who received it.

### Lowest Grade

Find:

* The lowest grade.
* The student who received it.

---

# ⭐ 5. Extra Challenge

Ask the user to enter a minimum grade.

Then print all students whose grades are **above** that minimum.

For example:

```text
Enter minimum grade: 85

Students above 85:
Bob: 92
Diana: 95
Eve: 88
```

---

# 🧠 Concepts Tested

This exercise focuses on:

* Dictionaries
* Dictionary keys and values
* Dictionary membership
* Adding dictionary entries
* Accessing dictionary values
* Loops
* Conditional statements
* String methods
* Basic calculations
* Finding minimum and maximum values
* Working with user input
