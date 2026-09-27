# Master Game

## 🎯 Bonus Challenge — All Five Projects in One File Structure

Create one master program that provides access to all five Core projects through a single menu.

The five projects are:

1. High-Low Guessing Game
2. ATM Banking System
3. Rock Paper Scissors Tournament
4. Adaptive Quiz App
5. Mastermind Number Cracking

The goal is to combine the projects into one program while keeping each game's logic inside its own function.

---

## Objective

Build a **Master Challenge Menu** that allows the user to choose which game or application they want to run.

The program should repeatedly display the menu until the user chooses to exit.

Example:

```text
==============================
       MASTER CHALLENGE
==============================

1. High-Low Guessing Game
2. ATM Banking System
3. Rock Paper Scissors Tournament
4. Adaptive Quiz App
5. Mastermind Number Cracking
6. Exit

Choose option:
```

---

## Required Functions

Each Core project should have its own function.

```python
def play_guessing_game():
    # All logic for Guessing Game
    pass

def run_atm_simulator():
    # All logic for ATM
    pass

def play_rps_tournament():
    # All logic for Rock Paper Scissors
    pass

def start_quiz():
    # All logic for Quiz
    pass

def play_mastermind():
    # All logic for Mastermind
    pass
```

Each function is responsible for starting and running its corresponding project.

---

## Main Menu

Create a `main()` function containing the program's main loop.

```python
def main():
    while True:
        print_menu()
        choice = input("Choose option: ")

        match choice:
            case "1":
                play_guessing_game()
            case "2":
                run_atm_simulator()
            case "3":
                play_rps_tournament()
            case "4":
                start_quiz()
            case "5":
                play_mastermind()
            case "6":
                print("Goodbye! 👋")
                break
            case _:
                print("Invalid choice! Try again.")
                continue
```

The menu should continue appearing after each project finishes.

---

## Menu Options

| Choice | Project                        | Function                |
| ------ | ------------------------------ | ----------------------- |
| 1      | High-Low Guessing Game         | `play_guessing_game()`  |
| 2      | ATM Banking System             | `run_atm_simulator()`   |
| 3      | Rock Paper Scissors Tournament | `play_rps_tournament()` |
| 4      | Adaptive Quiz App              | `start_quiz()`          |
| 5      | Mastermind Number Cracking     | `play_mastermind()`     |
| 6      | Exit                           | End program             |

---

## Program Entry Point

Use the standard Python entry-point pattern:

```python
if __name__ == "__main__":
    main()
```

This makes `main()` run when the file is executed directly.

---

## Expected Behaviour

### Choosing 1

```text
Choose option: 1

Starting High-Low Guessing Game...

[Guessing Game runs here]
```

When the game finishes, the user should return to the Master Challenge Menu.

### Choosing 2

```text
Choose option: 2

Starting ATM Banking System...

[ATM runs here]
```

When the ATM finishes, return to the main menu.

### Choosing 3

```text
Choose option: 3

Starting Rock Paper Scissors Tournament...

[RPS runs here]
```

### Choosing 4

```text
Choose option: 4

Starting Adaptive Quiz...

[Quiz runs here]
```

### Choosing 5

```text
Choose option: 5

Starting Mastermind...

[Mastermind runs here]
```

### Choosing 6

```text
Choose option: 6

Goodbye! 👋
```

The program terminates.

### Invalid Choice

```text
Choose option: 9

Invalid choice! Try again.
```

The program should return to the menu.

---

## Important Requirement

The five projects should remain logically separated.

Do not place all five projects directly inside `main()`.

Instead:

```text
main()
  │
  ├── play_guessing_game()
  │
  ├── run_atm_simulator()
  │
  ├── play_rps_tournament()
  │
  ├── start_quiz()
  │
  └── play_mastermind()
```

This makes the master program easier to understand, maintain, and extend.

---

## Concepts Practised

This bonus challenge combines many concepts learned throughout Level 02:

* Functions
* Function calls
* `while` loops
* `match`
* `case`
* `break`
* `continue`
* User input
* Conditional logic
* Program structure
* Scope
* Modular design
* Main program loops
* `if __name__ == "__main__":`
* Combining multiple projects into one application

