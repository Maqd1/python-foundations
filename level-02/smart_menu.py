'''
Q7: The Smart Menu System (Hard)

Create a CLI (Command Line Interface) program that manages a simple "todo" list.

Features:

    Add task → Asks for task name, adds to list

    Remove task → Asks for index, removes from list (if valid)

    View tasks → Shows all tasks with numbers

    Mark complete → Asks for index, marks as done (append [DONE] to task)

    Clear all → Confirms (asks y/n), then clears

    Exit → Prints "Goodbye!" and stops

Technical Requirements:

    Use while True for the main loop

    Use match to handle menu selection

    Use functions for each feature

    Use break to exit the loop

    Use continue for invalid selections

    Use pass as a placeholder initially

    Maintain a list of tasks

Scope (Variables): The tasks list should be accessible to all functions. Use a global or pass as parameter.

Error Handling:

    Invalid menu option → "Invalid option! Try again"

    Removing non-existent task → "Task not found!"

    Empty todo list → "No tasks to show!"

Sample Interaction:
text

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

Concepts Tested:

    while loops

    match (or if/elif)

    Functions (with parameters and return values)

    Scope (global vs local)

    Lists (appending, removing, indexing)

    break, continue, pass

    Conditional logic

📋 Quick Reference Cheat Sheet
python

# CONDITIONALS
if x > 0:
    print("Positive")
elif x < 0:
    print("Negative")
else:
    print("Zero")

# WHILE LOOP
while condition:
    do_something()

# FOR LOOP
for item in collection:
    process(item)

# FOR WITH RANGE
for i in range(5):  # 0,1,2,3,4
    print(i)

# BREAK
for i in range(10):
    if i == 5:
        break  # Stop at 5

# CONTINUE
for i in range(10):
    if i % 2 == 0:
        continue  # Skip even numbers
    print(i)  # Only odd numbers

# PASS
if x == 0:
    pass  # TODO: handle this case

# MATCH
match value:
    case 0:
        print("Zero")
    case _:
        print("Other")

# FUNCTION
def add(a, b):
    return a + b

result = add(3, 5)  # 8

# SCOPE
global_var = 10
def test():
    local_var = 20
    print(global_var)  # ✅ Works
    # print(local_var) # ❌ ERROR (outside function)


'''


# --- FUNCTIONS (The Workers) ---

def add_task(task_list):
    task_name = input("Enter task: ")
    task_list.append(task_name)
    print("✅ Task added!")

def view_tasks(task_list):
    if len(task_list) == 0:
        print("No tasks to show!")
        return  
        
    print("\nTodo List:")
    for i in range(len(task_list)):
        display_number = i + 1
        task = task_list[i]
        print(f"{display_number}. {task}")

def remove_task(task_list):
    if len(task_list) == 0:
        print("No tasks to remove!")
        return

    user_input = input("Enter task number: ")
    index = int(user_input) - 1
    
    if index >= 0 and index < len(task_list):
        task_list.pop(index)
        print("✅ Task removed!")
    else:
        print("Task not found!")

def mark_complete(task_list):
    if len(task_list) == 0:
        print("No tasks to mark!")
        return

    user_input = input("Enter task number: ")
    index = int(user_input) - 1
    
    if index >= 0 and index < len(task_list):
        task_list[index] = task_list[index] + " [DONE]"
        print("✅ Marked as done!")
    else:
        print("Task not found!")

def clear_all(task_list):
    if len(task_list) == 0:
        print("No tasks to clear!")
        return

    confirm = input("Are you sure you want to clear all tasks? (y/n): ")
    if confirm.lower() == 'y':
        task_list.clear()
        print("✅ All tasks cleared!")
    else:
        print("Action cancelled.")


# --- MAIN PROGRAM (The Manager) ---

tasks = [] # Our master list

# The infinite loop goes at the very end so it has access to all the functions above it
while True:
    print("\n===== TODO MENU =====")
    print("1. Add task")
    print("2. Remove task")
    print("3. View tasks")
    print("4. Mark complete")
    print("5. Clear all")
    print("6. Exit")
    
    choice = input("Choose option: ")
    
    match choice:
        case "1":
            add_task(tasks)
        case "2":
            remove_task(tasks)
        case "3":
            view_tasks(tasks)
        case "4":
            mark_complete(tasks)
        case "5":
            clear_all(tasks)
        case "6":
            print("Goodbye! 👋")
            break 
        case _:
            print("Invalid option! Try again")
            continue