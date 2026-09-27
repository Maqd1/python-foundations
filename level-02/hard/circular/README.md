# Circular Number Sequence

## Hard Level — Question 6

Write a program that generates a **circular number sequence**.

### Rule

Starting from `1`, each number is the sum of the previous two numbers. The result is limited to a maximum value and **wraps around** when it exceeds that value.

For a maximum value of `20`:

```text
1, 1, 2, 3, 5, 8, 13, 1, 14, 15, 9, 4, 13, 17, 10, 7, 17, ...
```

### Logic

1. Start with:

   ```python
   a = 1
   b = 1
   ```
2. Print the current number.
3. Calculate the next number:

   ```text
   next = a + b
   ```
4. If `next` is greater than the maximum value, wrap it back into the valid range.
5. Continue the process for the required number of iterations.

### Required Functions

#### `calculate_next(a, b, max_val)`

Returns the next number. The result must be less than or equal to `max_val`.

#### `generate_sequence(length, max_val)`

Generates and returns a list containing the requested number of values.

#### `display_sequence(sequence)`

Displays the sequence neatly.

### Concepts

* `while` loops
* Functions
* Parameters
* Return values
* Modulo for wrapping

### Sample Output

For `max = 20` and `length = 10`:

```text
Sequence length: 10
Max value: 20
[1, 1, 2, 3, 5, 8, 13, 1, 14, 15]
```

### Harder Variation

Display the sequence as a grid:

```text
1  1  2  3  5
8  13 1  14 15
9  4  13 17 10
```

### Additional Concepts

* Nested loops
* `for` loops
* Functions
* List manipulation
