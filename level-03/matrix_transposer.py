'''
Q4: The Matrix Transposer (Mid)

Write a program that transposes a matrix (2D list).

Requirements:

    Create a 3×3 matrix:
    python

    matrix = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9]
    ]

    Write a function transpose(matrix) that:

        Takes a 2D list (matrix)

        Returns the transposed matrix (rows become columns)

    Also create a function print_matrix(matrix, title):

        Prints the matrix in a grid format

        Shows the title

    Extra challenge 1: Handle matrices of any size (3×4, 4×3, etc.)

    Extra challenge 2: Ask the user to input their own matrix

    Harder: Verify if the matrix is symmetric (matrix == transpose)

Sample Output:
text

Original Matrix (3x3):
1  2  3
4  5  6
7  8  9

Transposed Matrix (3x3):
1  4  7
2  5  8
3  6  9

Is symmetric? True

---

Matrix 2 (2x4):
1  2  3  4
5  6  7  8

Transposed Matrix (4x2):
1  5
2  6
3  7
4  8

Is symmetric? False

Concepts: Nested lists, nested loops, list comprehensions, functions with return values
'''


def transpose(matrix):
    """Returns a new matrix with rows and columns swapped. Works for any m x n size."""
    rows = len(matrix)
    cols = len(matrix[0]) if rows > 0 else 0
    return [[matrix[r][c] for r in range(rows)] for c in range(cols)]


def print_matrix(matrix, title):
    rows = len(matrix)
    cols = len(matrix[0]) if rows > 0 else 0
    print(f"{title} ({rows}x{cols}):")
    for row in matrix:
        print("  ".join(str(value) for value in row))


def is_symmetric(matrix):
    """A matrix is symmetric only if it's square AND equal to its own transpose.
    Comparing the lists directly handles the 'not square' case for free —
    a non-square matrix and its transpose have different dimensions, so
    Python's list equality returns False without needing a separate check."""
    return matrix == transpose(matrix)


def get_matrix_from_user():
    while True:
        try:
            rows = int(input("Enter number of rows: "))
            cols = int(input("Enter number of columns: "))
            if rows <= 0 or cols <= 0:
                print("Rows and columns must be positive numbers.")
                continue
            break
        except ValueError:
            print("Please enter valid whole numbers.")

    matrix = []
    print(f"Enter each row as {cols} number(s) separated by spaces.")
    for r in range(rows):
        while True:
            raw = input(f"Row {r + 1}: ").strip().split()
            if len(raw) != cols:
                print(f"Expected {cols} number(s), got {len(raw)}. Try again.")
                continue
            try:
                row = [int(value) for value in raw]
            except ValueError:
                print("Please enter valid integers only.")
                continue
            matrix.append(row)
            break

    return matrix


def demo(matrix, label):
    print_matrix(matrix, f"{label} Matrix")
    print()
    transposed = transpose(matrix)
    print_matrix(transposed, "Transposed Matrix")
    print(f"\nIs symmetric? {is_symmetric(matrix)}")


def main():
    matrix = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9],
    ]
    demo(matrix, "Original")

    print("\n" + "-" * 20 + "\n")

    matrix2 = [
        [1, 2, 3, 4],
        [5, 6, 7, 8],
    ]
    demo(matrix2, "Matrix 2")

    use_own = input("\nWould you like to enter your own matrix? (y/n): ").strip().lower()
    if use_own == "y":
        print("\n" + "-" * 20 + "\n")
        user_matrix = get_matrix_from_user()
        demo(user_matrix, "Your")


if __name__ == "__main__":
    main()