# 🔢 Matrix Transposer

## Q4 — The Matrix Transposer (Mid)

Write a program that transposes a matrix represented as a **2D list**.

Transposing a matrix means converting its **rows into columns** and its **columns into rows**.

---

# 📊 1. Create a Matrix

Start with this 3×3 matrix:

```python
matrix = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]
```

The matrix has:

* 3 rows
* 3 columns

---

# 🔄 2. Create `transpose()`

Write a function:

```python
transpose(matrix)
```

The function should:

1. Accept a 2D list.
2. Convert its rows into columns.
3. Return the transposed matrix.

For example:

```text
Original:

1  2  3
4  5  6
7  8  9


Transposed:

1  4  7
2  5  8
3  6  9
```

---

# 🖨️ 3. Create `print_matrix()`

Create a function:

```python
print_matrix(matrix, title)
```

The function should:

* Accept a matrix.
* Accept a title.
* Print the title.
* Display the matrix in a readable grid format.

For example:

```text
Original Matrix (3x3):
1  2  3
4  5  6
7  8  9
```

---

# ⭐ 4. Extra Challenge 1 — Any Matrix Size

Modify the program so that `transpose()` works with matrices of different dimensions.

For example:

### 3×4 matrix

```text
1  2  3  4
5  6  7  8
9  10 11 12
```

should become a **4×3 matrix**.

### 4×3 matrix

The function should also work when the matrix has more rows than columns.

The solution should not be hard-coded specifically for 3×3 matrices.

---

# ⭐ 5. Extra Challenge 2 — User Input

Allow the user to create their own matrix.

The program should ask the user for the required dimensions and values, then:

1. Build the matrix.
2. Display the original matrix.
3. Transpose it.
4. Display the transposed matrix.

---

# 🔥 6. Harder Challenge — Symmetric Matrix

Determine whether a matrix is **symmetric**.

A matrix is symmetric when:

```python
matrix == transpose(matrix)
```

For a matrix to be symmetric, it must also have the same number of rows and columns.

For example:

```text
1  2  3
2  4  5
3  5  6
```

is symmetric because its rows and columns mirror each other.

---

# 🖥️ Sample Output

```text
Original Matrix (3x3):
1  2  3
4  5  6
7  8  9

Transposed Matrix (3x3):
1  4  7
2  5  8
3  6  9

Is symmetric? True
```

Another example:

```text
Matrix 2 (2x4):
1  2  3  4
5  6  7  8

Transposed Matrix (4x2):
1  5
2  6
3  7
4  8

Is symmetric? False
```

---

# 🧠 Concepts Tested

This exercise focuses on:

* Nested lists
* 2D lists
* Rows and columns
* Nested loops
* List comprehensions
* Functions
* Function parameters
* Return values
* Matrix dimensions
* Comparing lists
* Basic matrix operations
