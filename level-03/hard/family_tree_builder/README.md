# 🌳 Family Tree Builder

## Q7 — The Family Tree Builder (Very Hard)

Create a family tree system using **deeply nested structures and advanced data manipulation**.

The program should allow the family tree to be searched, analysed, traversed, and displayed in different ways.

---

# 👨‍👩‍👧‍👦 1. Family Tree Structure

Build the family tree using nested dictionaries:

```python
family_tree = {
    "Grandfather": {
        "name": "Joseph",
        "spouse": "Mary",
        "children": {
            "John": {
                "birth_year": 1970,
                "spouse": "Jane",
                "children": {
                    "Alice": {
                        "birth_year": 1995,
                        "spouse": None,
                        "children": {}
                    },
                    "Bob": {
                        "birth_year": 1998,
                        "spouse": None,
                        "children": {}
                    }
                }
            },

            "Peter": {
                "birth_year": 1975,
                "spouse": "Susan",
                "children": {
                    "Carol": {
                        "birth_year": 2000,
                        "spouse": None,
                        "children": {}
                    }
                }
            }
        }
    }
}
```

The structure contains:

* Names
* Birth years
* Spouses
* Children
* Multiple generations

---

# 🔍 2. Required Functions

### `count_descendants(name)`

Count every descendant of a specified family member.

This includes:

* Children
* Grandchildren
* Great-grandchildren
* And so on

---

### `find_path(root, target)`

Find the path from the root member to a target member.

For example:

```text
Joseph → John → Alice
```

---

### `get_siblings(name)`

Return a list containing the person's siblings.

For example:

```python
get_siblings("Alice")
```

should return:

```python
["Bob"]
```

---

### `get_cousins(name)`

Return a list containing the person's cousins.

For example:

```python
get_cousins("Alice")
```

should return:

```python
["Carol"]
```

---

### `get_generation(name)`

Return the generation number of a family member.

The root is generation `0`.

For example:

```text
Joseph → 0
John   → 1
Alice  → 2
```

---

### `get_family_members()`

Return a list containing the names of all family members.

---

### `find_oldest()`

Find the oldest person in the family based on birth year.

---

### `find_youngest()`

Find the youngest person in the family based on birth year.

---

### `get_average_age()`

Calculate the average age of all family members.

Use **2026 as the current year**.

---

### `get_family_by_generation()`

Return a dictionary where:

* Keys are generation numbers.
* Values are lists of family members belonging to that generation.

For example:

```python
{
    0: ["Joseph"],
    1: ["John", "Peter"],
    2: ["Alice", "Bob", "Carol"]
}
```

---

# ⭐ 3. Bonus Features

### Add a New Family Member

Allow a new person to be added to the family tree.

Validate the input and check for duplicate names before adding the member.

---

### Visual Family Tree

Print the family tree as a visual diagram.

For example:

```text
Joseph (Grandfather)
  └── John
      ├── Alice
      └── Bob
  └── Peter
      └── Carol
```

---

### Find the Longest Branch

Find the family branch containing the greatest number of generations.

For example:

```text
Joseph → John → Alice
```

---

# 🖥️ Sample Output

```text
🌳 FAMILY TREE 🌳

👨👩👧👦 Family Members:

Joseph (Grandfather) [Generation 0]
  └── John [Generation 1]
      ├── Alice [Generation 2]
      └── Bob [Generation 2]
  └── Peter [Generation 1]
      └── Carol [Generation 2]

📊 FAMILY STATISTICS:
Total members: 7
Generations: 3
Average age: 37.8
Oldest: Joseph (88 years old)
Youngest: Carol (26 years old)

🔍 SEARCH RESULTS:
Path from root to Alice: Joseph → John → Alice
Alice's siblings: ['Bob']
Alice's cousins: ['Carol']
Alice's generation: 2

📊 MEMBERS BY GENERATION:
Generation 0: ['Joseph']
Generation 1: ['John', 'Peter']
Generation 2: ['Alice', 'Bob', 'Carol']

📏 Longest branch:
Joseph → John → Alice (3 generations)
```

---

# 🧠 Concepts Tested

This project focuses on:

* Deeply nested dictionaries
* Complex data traversal
* Recursive thinking and traversal
* Searching nested structures
* Set operations
* Finding relationships between records
* Dictionary comprehensions
* Advanced string formatting
* Generation tracking
* Statistical calculations
* Sorting and comparison
