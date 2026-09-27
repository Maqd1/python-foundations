


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