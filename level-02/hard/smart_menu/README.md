# Smart Menu System

## Hard Level — Question 7

Create a **CLI (Command Line Interface)** program that manages a simple todo list.

### Features

#### Add Task

Ask the user for a task name and add it to the list.

#### Remove Task

Ask for a task index and remove the task if the index is valid.

#### View Tasks

Display all tasks with their numbers.

#### Mark Complete

Ask for a task index and mark the task as completed by appending:

```text
[DONE]
```

#### Clear All

Ask the user to confirm with `y/n`, then clear all tasks if confirmed.

#### Exit

Print:

```text
Goodbye!
```

and stop the program.

### Technical Requirements

* Use `while True` for the main menu loop.
* Use `match` to handle menu selection.
* Use functions for each feature.
* Use `break` to exit the loop.
* Use `continue` for invalid selections.
* Use `pass` as a placeholder initially.
* Maintain a list of tasks.

### Scope

The tasks list should be accessible to all functions.

This can be achieved by either:

* Using a global variable
* Passing the list as a parameter

### Error Handling

Invalid menu option:

```text
Invalid option! Try again
```

Removing a non-existent task:

```text
Task not found!
```

Viewing an empty todo list:

```text
No tasks to show!
```

### Sample Interaction

```text
===== TODO MENU =====
1. Add task
2. Remove task
3. View tasks
4. Mark complete
5. Clear all
6. Exit
Choose option: 1
Enter task: Buy groceries
✅ Task added!

Choose option: 1
Enter task: Finish Python homework
✅ Task added!

Choose option: 3
Todo List:
1. Buy groceries
2. Finish Python homework

Choose option: 4
Enter task number: 2
✅ Marked as done!

Choose option: 3
Todo List:
1. Buy groceries
2. Finish Python homework [DONE]

Choose option: 6
Goodbye! 👋
```

## Concepts Tested

* `while` loops
* `match` or `if/elif`
* Functions with parameters and return values
* Scope: global vs local
* Lists: appending, removing, indexing
* `break`
* `continue`
* `pass`
* Conditional logic

## Quick Reference Cheat Sheet

### Conditionals

```python
if x > 0:
    print("Positive")
elif x < 0:
    print("Negative")
else:
    print("Zero")
```

### While Loop

```python
while condition:
    do_something()
```

### For Loop

```python
for item in collection:
    process(item)
```

### For Loop with `range()`

```python
for i in range(5):
    print(i)
```

Produces:

```text
0
1
2
3
4
```

### Break

```python
for i in range(10):
    if i == 5:
        break
```

Stops the loop when `i` reaches `5`.

### Continue

```python
for i in range(10):
    if i % 2 == 0:
        continue
    print(i)
```

Skips even numbers and prints only odd numbers.

### Pass

```python
if x == 0:
    pass
```

A placeholder for code that will be implemented later.

### Match

```python
match value:
    case 0:
        print("Zero")
    case _:
        print("Other")
```

### Function

```python
def add(a, b):
    return a + b

result = add(3, 5)
```

`result` becomes `8`.

### Scope

```python
global_var = 10

def test():
    local_var = 20
    print(global_var)  # Works
```

A local variable normally cannot be accessed outside the function where it was created.
