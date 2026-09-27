# Multiplication Table Generator

## Mid Level

Write a program that asks the user for a number and displays its multiplication table.

### Requirements

The program should:

1. Ask the user:

   ```text
   Enter a number:
   ```
2. Print the multiplication table from **1 to 12**.
3. Ask:

   ```text
   Show another? (y/n):
   ```
4. If the user enters `y`, generate another multiplication table.
5. If the user enters `n`, print:

   ```text
   Goodbye!
   ```

### Extra Challenge

Ask the user to specify the range of the multiplication table.

For example:

```text
Enter a number: 7
Enter range: 20
```

This should generate the table from `1` to `20`.

Another possible range could be:

```text
5-15
```

### Harder Challenge

Format the multiplication table into a clean, readable grid using **f-strings**.

### Sample Output

```text
Enter a number: 7
7 x 1 = 7
7 x 2 = 14
...
7 x 12 = 84

Show another? (y/n): y

Enter a number: 3
3 x 1 = 3
...
3 x 12 = 36

Show another? (y/n): n
Goodbye!
```

### Concepts

* `for` loop
* `while` loop
* `range()`
* Conditional logic
