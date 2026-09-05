'''
4️⃣ ✅ HARD TODO APP
The Smart Todo with Deadlines and Priorities 📋

Build an advanced todo app with project management features.

Data Structure:
python

todo_data = {
    "projects": {
        "Work": {
            "tasks": [
                {
                    "id": 1,
                    "title": "Complete Python project",
                    "description": "Finish the inventory system",
                    "priority": 1,  # 1=Highest, 5=Lowest
                    "status": "In Progress",  # Not Started, In Progress, Completed, Archived
                    "deadline": "2026-03-25",
                    "created": "2026-03-15",
                    "completed": None,
                    "subtasks": [
                        {"title": "Write code", "done": True},
                        {"title": "Test", "done": False},
                        {"title": "Deploy", "done": False}
                    ],
                    "tags": ["python", "project"],
                    "estimated_hours": 8,
                    "actual_hours": 0
                }
            ]
        },
        "Personal": {
            "tasks": []
        }
    },
    "tags": ["python", "project", "work", "urgent"],
    "completed_count": 0,
    "total_count": 0
}

Requirements:

    Task Management:

        add_task(title, project, priority=3, deadline=None) → Create task

        edit_task(task_id, **kwargs) → Edit any field

        delete_task(task_id) → Delete task

        view_tasks(project=None, status=None, priority=None) → Filtered view

        view_task(task_id) → Show full task details

    Organization (HARD):

        add_project(name) → Create project

        delete_project(name) → Delete project (move tasks to archive)

        move_task(task_id, new_project) → Move between projects

        add_tag(task_id, tag) → Add tag to task

        view_by_tag(tag) → Show all tasks with tag

    Smart Features (HARDER):

        get_overdue_tasks() → Tasks past deadline

        get_tasks_by_priority(priority) → Tasks with specific priority

        get_upcoming_deadlines(days) → Tasks due in next X days

        complete_task(task_id) → Mark complete, track completion time

        archive_completed() → Move completed tasks to archive

    Statistics and Reporting (HARDEST):

        get_project_stats(project) → Tasks done, in progress, etc.

        get_productivity_report() → Tasks done per day/week

        get_time_analysis() → Estimated vs actual hours

        get_priority_distribution() → Tasks by priority level

        get_tags_cloud() → Most used tags

    Search (VERY HARD):

        search_tasks(query) → Search by title, description, tags, project

        advanced_search(**filters) → Combine multiple filters

    Data Persistence:

        Auto-save on every change

        Export/import JSON

Sample Output:
text

✅ SMART TODO MANAGER ✅

📋 TODAY'S OVERVIEW:
Work: 3 tasks (2 due soon)
Personal: 2 tasks (1 overdue)

⚠️ OVERDUE TASKS (1):
1. Pay electricity bill (Personal) - Due: 2026-03-18

📅 UPCOMING (Next 3 days):
1. Complete Python project (Work) - Due: 2026-03-25
2. Buy groceries (Personal) - Due: 2026-03-22

====================================
1. View Tasks
2. Add Task
3. Edit Task
4. Complete Task
5. View Projects
6. Analytics
7. Search
8. Exit

Choice: 1

📁 Project: Work
Priority: All | Status: All

[1] 🔴 Complete Python project
    Status: In Progress | Priority: High
    Deadline: 2026-03-25 (5 days left)
    Tags: #python #project
    Subtasks: 2/3 completed
    Est: 8h | Actual: 0h

[2] 🟡 Write documentation
    Status: Not Started | Priority: Medium
    Deadline: 2026-03-28
    Tags: #documentation

[3] 🟢 Send weekly report
    Status: Completed | Priority: Low
    Completed: 2026-03-20

====================================
Choice: 1 (View Task 1)

📌 TASK DETAILS
ID: 1
Title: Complete Python project
Project: Work
Description: Finish the inventory system
Priority: 1 (Highest)
Status: In Progress
Deadline: 2026-03-25 (5 days left)
Created: 2026-03-15
Completed: None

Subtasks:
✅ Write code
❌ Test
❌ Deploy

Tags: #python #project
Est. Hours: 8
Actual Hours: 0

====================================
1. Edit Task
2. Add Subtask
3. Toggle Subtask
4. Complete Task
5. Move Task
6. Back

Choice: 6

📊 PRODUCTIVITY REPORT (March 2026)
====================================
Total Tasks: 15
Completed: 8 (53%)
In Progress: 4 (27%)
Not Started: 3 (20%)

📈 COMPLETION TREND:
Week 1: 2 tasks
Week 2: 3 tasks
Week 3: 3 tasks

📊 PROJECT BREAKDOWN:
Work: 5/8 completed (62%)
Personal: 2/4 completed (50%)
Learning: 1/3 completed (33%)

🏷️ TAG CLOUD:
#python (5)  #work (4)  #project (3)
#urgent (2)  #documentation (2)

⏰ TIME ANALYSIS:
Total estimated: 45 hours
Total actual: 32 hours
Efficiency: 71%

Concepts Tested: Deeply nested dictionaries, list comprehensions, complex filtering, date/time handling, sorting with multiple keys, statistical analysis, string methods, file I/O
'''


from datetime import datetime, timedelta
import json
import os

# ==========================================
# GLOBAL STATE & CONSTANTS
# ==========================================

DATA_FILE = "todo_data.json"

# Master Data Structure
todo_data = {
    "projects": {
        "Work": {"tasks": []},
        "Personal": {"tasks": []},
    },
    "tags": ["python", "project", "work", "urgent"],
    "completed_count": 0,
    "total_count": 0,
    "next_task_id": 1,
}

# ==========================================
# DATA PERSISTENCE
# ==========================================


def save_data():
    """Saves the current todo_data dictionary to JSON."""
    with open(DATA_FILE, "w") as f:
        json.dump(todo_data, f, indent=4)


def load_data():
    """Loads todo_data from JSON file if it exists; otherwise seeds initial data."""
    global todo_data
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as f:
                loaded = json.load(f)
                todo_data.update(loaded)
        except Exception:
            seed_sample_data()
    else:
        seed_sample_data()


def seed_sample_data():
    """Populates initial sample tasks for demonstration."""
    add_task(
        title="Complete Python project",
        project="Work",
        description="Finish the inventory system",
        priority=1,
        deadline="2026-03-25",
        subtasks=[
            {"title": "Write code", "done": True},
            {"title": "Test", "done": False},
            {"title": "Deploy", "done": False},
        ],
        tags=["python", "project"],
        estimated_hours=8,
    )
    add_task(
        title="Pay electricity bill",
        project="Personal",
        description="Pay via bank app",
        priority=1,
        deadline="2026-03-18",
        tags=["urgent"],
        estimated_hours=1,
    )


# ==========================================
# HELPER FUNCTIONS
# ==========================================


def find_task_by_id(task_id):
    """Searches across all projects for a task matching task_id."""
    for p_name, p_data in todo_data["projects"].items():
        for task in p_data["tasks"]:
            if task["id"] == task_id:
                return task, p_name
    return None, None


def update_counts():
    """Recalculates global statistics for total and completed task counts."""
    total = 0
    completed = 0
    for p_data in todo_data["projects"].values():
        for t in p_data["tasks"]:
            total += 1
            if t["status"] == "Completed":
                completed += 1
    todo_data["total_count"] = total
    todo_data["completed_count"] = completed


# ==========================================
# TASK MANAGEMENT OPERATIONS
# ==========================================


def add_task(
    title,
    project="Personal",
    description="",
    priority=3,
    deadline=None,
    subtasks=None,
    tags=None,
    estimated_hours=0,
):
    """Creates a new task and appends it to the specified project."""
    if project not in todo_data["projects"]:
        add_project(project)

    task_id = todo_data["next_task_id"]
    todo_data["next_task_id"] += 1

    task = {
        "id": task_id,
        "title": title,
        "description": description,
        "priority": priority,
        "status": "In Progress" if subtasks else "Not Started",
        "deadline": deadline,
        "created": datetime.now().strftime("%Y-%m-%d"),
        "completed": None,
        "subtasks": subtasks or [],
        "tags": tags or [],
        "estimated_hours": estimated_hours,
        "actual_hours": 0,
    }

    todo_data["projects"][project]["tasks"].append(task)

    # Maintain unique master tag collection
    if tags:
        for tg in tags:
            if tg not in todo_data["tags"]:
                todo_data["tags"].append(tg)

    update_counts()
    save_data()
    return task_id


def edit_task(task_id, **kwargs):
    """Edits any attributes of an existing task using key-value updates."""
    task, _ = find_task_by_id(task_id)
    if not task:
        return False

    for key, value in kwargs.items():
        if key in task and value is not None:
            task[key] = value

    save_data()
    return True


def delete_task(task_id):
    """Deletes a task by ID across all projects."""
    for p_name, p_data in todo_data["projects"].items():
        for i, task in enumerate(p_data["tasks"]):
            if task["id"] == task_id:
                del p_data["tasks"][i]
                update_counts()
                save_data()
                return True
    return False


def complete_task(task_id, actual_hours=None):
    """Marks a task completed, sets completion timestamp, and resolves subtasks."""
    task, _ = find_task_by_id(task_id)
    if task:
        task["status"] = "Completed"
        task["completed"] = datetime.now().strftime("%Y-%m-%d")
        if actual_hours is not None:
            task["actual_hours"] = actual_hours
        for st in task["subtasks"]:
            st["done"] = True
        update_counts()
        save_data()
        return True
    return False


# ==========================================
# ORGANIZATION & CATEGORIZATION
# ==========================================


def add_project(name):
    """Adds a new project category if it does not already exist."""
    if name not in todo_data["projects"]:
        todo_data["projects"][name] = {"tasks": []}
        save_data()


def delete_project(name):
    """Deletes a project and safely moves its active tasks to 'Personal'."""
    if name in todo_data["projects"]:
        if "Personal" not in todo_data["projects"]:
            add_project("Personal")
        if name != "Personal":
            todo_data["projects"]["Personal"]["tasks"].extend(
                todo_data["projects"][name]["tasks"]
            )
            del todo_data["projects"][name]
            save_data()


def move_task(task_id, new_project):
    """Moves a task from its current project to a new target project."""
    task, old_project = find_task_by_id(task_id)
    if task and old_project:
        add_project(new_project)
        todo_data["projects"][old_project]["tasks"].remove(task)
        todo_data["projects"][new_project]["tasks"].append(task)
        save_data()
        return True
    return False


def add_tag(task_id, tag):
    """Attaches a tag to a specific task and registers it globally."""
    task, _ = find_task_by_id(task_id)
    if task:
        if tag not in task["tags"]:
            task["tags"].append(tag)
        if tag not in todo_data["tags"]:
            todo_data["tags"].append(tag)
        save_data()
        return True
    return False


# ==========================================
# SEARCH & FILTERING ENGINE
# ==========================================


def get_overdue_tasks():
    """Returns all non-completed tasks past their deadline."""
    overdue = []
    today = datetime.now().strftime("%Y-%m-%d")
    for p_name, p_data in todo_data["projects"].items():
        for t in p_data["tasks"]:
            if (
                t["deadline"]
                and t["deadline"] < today
                and t["status"] != "Completed"
            ):
                overdue.append((t, p_name))
    return overdue


def get_upcoming_deadlines(days=3):
    """Returns non-completed tasks due within the given timeframe."""
    upcoming = []
    today = datetime.now().date()
    target = today + timedelta(days=days)
    for p_name, p_data in todo_data["projects"].items():
        for t in p_data["tasks"]:
            if t["deadline"] and t["status"] != "Completed":
                try:
                    d_date = datetime.strptime(
                        t["deadline"], "%Y-%m-%d"
                    ).date()
                    if today <= d_date <= target:
                        upcoming.append((t, p_name))
                except ValueError:
                    continue
    return upcoming


def search_tasks(query):
    """Case-insensitive search across task attributes and tags."""
    q = query.lower()
    results = []
    for p_name, p_data in todo_data["projects"].items():
        for t in p_data["tasks"]:
            if (
                q in t["title"].lower()
                or q in t["description"].lower()
                or any(q in tag.lower() for tag in t["tags"])
                or q in p_name.lower()
            ):
                results.append((t, p_name))
    return results


# ==========================================
# REPORTING & ANALYTICS
# ==========================================


def get_productivity_report():
    """Calculates completion rates, time logs, and tag usage distributions."""
    all_tasks = [
        t for p in todo_data["projects"].values() for t in p["tasks"]
    ]
    total = len(all_tasks)
    if total == 0:
        return None

    completed = sum(1 for t in all_tasks if t["status"] == "Completed")
    in_progress = sum(1 for t in all_tasks if t["status"] == "In Progress")
    not_started = sum(1 for t in all_tasks if t["status"] == "Not Started")

    est_hours = sum(t["estimated_hours"] for t in all_tasks)
    act_hours = sum(t["actual_hours"] for t in all_tasks)

    tag_counts = {}
    for t in all_tasks:
        for tag in t["tags"]:
            tag_counts[tag] = tag_counts.get(tag, 0) + 1

    return {
        "total": total,
        "completed": completed,
        "in_progress": in_progress,
        "not_started": not_started,
        "est_hours": est_hours,
        "act_hours": act_hours,
        "tag_counts": tag_counts,
    }


# ==========================================
# USER INTERFACE / CLI RENDERING
# ==========================================


def print_dashboard():
    """Displays key task metrics, overdue warnings, and upcoming deadlines."""
    print("\n✅ SMART TODO MANAGER ✅")
    print("\n📋 TODAY'S OVERVIEW:")

    for p_name, p_data in todo_data["projects"].items():
        count = len(p_data["tasks"])
        due_soon = sum(
            1
            for t in p_data["tasks"]
            if t["deadline"] and t["status"] != "Completed"
        )
        print(f"  • {p_name}: {count} tasks ({due_soon} pending)")

    overdue = get_overdue_tasks()
    if overdue:
        print(f"\n⚠️ OVERDUE TASKS ({len(overdue)}):")
        for t, p in overdue:
            print(f"  ❌ {t['title']} ({p}) - Due: {t['deadline']}")

    upcoming = get_upcoming_deadlines(3)
    if upcoming:
        print("\n📅 UPCOMING (Next 3 days):")
        for t, p in upcoming:
            print(f"  ⏳ {t['title']} ({p}) - Due: {t['deadline']}")

    print("=" * 45)


def display_task_details(task, p_name):
    """Outputs full structured details for a single selected task."""
    print("\n📌 TASK DETAILS")
    print(f"ID: {task['id']}")
    print(f"Title: {task['title']}")
    print(f"Project: {p_name}")
    print(f"Description: {task['description']}")

    p_map = {1: "1 (Highest)", 2: "2 (High)", 3: "3 (Medium)", 4: "4 (Low)"}
    print(f"Priority: {p_map.get(task['priority'], task['priority'])}")
    print(f"Status: {task['status']}")
    print(f"Deadline: {task['deadline'] or 'None'}")
    print(f"Created: {task['created']}")
    print(f"Completed: {task['completed'] or 'None'}")

    print("\nSubtasks:")
    if task["subtasks"]:
        for st in task["subtasks"]:
            mark = "✅" if st["done"] else "❌"
            print(f"  {mark} {st['title']}")
    else:
        print("  None")

    tags_str = " ".join(f"#{t}" for t in task["tags"])
    print(f"\nTags: {tags_str or 'None'}")
    print(f"Est. Hours: {task['estimated_hours']}")
    print(f"Actual Hours: {task['actual_hours']}")
    print("=" * 45)


# ==========================================
# MAIN INTERACTIVE LOOP
# ==========================================


def main():
    load_data()

    while True:
        print_dashboard()
        print("1. View Tasks")
        print("2. Add Task")
        print("3. Edit Task")
        print("4. Complete Task")
        print("5. View Analytics")
        print("6. Search Tasks")
        print("7. Exit")

        choice = input("\nChoice: ").strip()

        if choice == "1":
            print("\n📁 Projects:")
            projects = list(todo_data["projects"].keys())
            for idx, p in enumerate(projects, 1):
                print(f"  {idx}. {p}")

            p_choice = input(
                "\nSelect project number (or press Enter for All): "
            ).strip()
            selected_p = (
                projects[int(p_choice) - 1]
                if p_choice.isdigit() and 0 < int(p_choice) <= len(projects)
                else None
            )

            tasks_to_show = []
            for p_name, p_data in todo_data["projects"].items():
                if selected_p is None or selected_p == p_name:
                    for t in p_data["tasks"]:
                        tasks_to_show.append((t, p_name))

            if not tasks_to_show:
                print("No tasks found.")
                continue

            print("\n--- TASKS ---")
            for t, p in tasks_to_show:
                p_icon = (
                    "🔴"
                    if t["priority"] == 1
                    else "🟡" if t["priority"] <= 3 else "🟢"
                )
                sub_done = sum(1 for st in t["subtasks"] if st["done"])
                sub_info = (
                    f" | Subtasks: {sub_done}/{len(t['subtasks'])}"
                    if t["subtasks"]
                    else ""
                )
                print(f"[{t['id']}] {p_icon} {t['title']} ({p})")
                print(
                    f"    Status: {t['status']} | Deadline: {t['deadline']}{sub_info}"
                )

            view_id = input(
                "\nEnter Task ID to view details (or press Enter): "
            ).strip()
            if view_id.isdigit():
                t_obj, p_obj = find_task_by_id(int(view_id))
                if t_obj:
                    display_task_details(t_obj, p_obj)
                    sub_opt = input(
                        "1. Complete Task | 2. Add Subtask | 3. Back: "
                    ).strip()
                    if sub_opt == "1":
                        act = input("Enter actual hours spent: ").strip()
                        complete_task(
                            t_obj["id"],
                            float(act)
                            if act.replace(".", "", 1).isdigit()
                            else 0,
                        )
                    elif sub_opt == "2":
                        st_title = input("Subtask title: ").strip()
                        if st_title:
                            t_obj["subtasks"].append(
                                {"title": st_title, "done": False}
                            )
                            save_data()

        elif choice == "2":
            title = input("Task title: ").strip()
            if not title:
                continue
            project = input("Project name [Personal]: ").strip() or "Personal"
            desc = input("Description: ").strip()
            prio = input("Priority (1=Highest, 4=Lowest) [3]: ").strip()
            prio = int(prio) if prio.isdigit() else 3
            deadline = input("Deadline (YYYY-MM-DD): ").strip() or None
            est = input("Estimated hours [0]: ").strip()
            est = float(est) if est.replace(".", "", 1).isdigit() else 0
            tags_input = input("Tags (comma separated): ").strip().split(",")
            tags = [t.strip() for t in tags_input if t.strip()]

            tid = add_task(
                title=title,
                project=project,
                description=desc,
                priority=prio,
                deadline=deadline,
                tags=tags,
                estimated_hours=est,
            )
            print(f"✅ Task created with ID: {tid}")

        elif choice == "3":
            tid = input("Enter Task ID to edit: ").strip()
            if tid.isdigit():
                t_obj, _ = find_task_by_id(int(tid))
                if t_obj:
                    new_title = input(
                        f"New title [{t_obj['title']}]: "
                    ).strip()
                    new_desc = input(
                        f"New desc [{t_obj['description']}]: "
                    ).strip()
                    edit_task(
                        int(tid),
                        title=new_title or None,
                        description=new_desc or None,
                    )
                    print("✅ Task updated.")

        elif choice == "4":
            tid = input("Enter Task ID to mark complete: ").strip()
            if tid.isdigit():
                act = input("Enter actual hours spent: ").strip()
                hrs = (
                    float(act) if act.replace(".", "", 1).isdigit() else 0
                )
                if complete_task(int(tid), hrs):
                    print("🎉 Task completed!")

        elif choice == "5":
            rep = get_productivity_report()
            if rep:
                print("\n📊 PRODUCTIVITY REPORT")
                print("=" * 45)
                print(f"Total Tasks: {rep['total']}")
                pct = (rep["completed"] / rep["total"]) * 100
                print(f"Completed: {rep['completed']} ({pct:.1f}%)")
                print(f"In Progress: {rep['in_progress']}")
                print(f"Not Started: {rep['not_started']}")
                print(f"⏰ Total Estimated Hours: {rep['est_hours']}h")
                print(f"⏱️ Total Actual Hours: {rep['act_hours']}h")
                print("\n🏷️ TAG CLOUD:")
                for tag, count in rep["tag_counts"].items():
                    print(f"  #{tag} ({count})")
                print("=" * 45)

        elif choice == "6":
            q = input("Enter search query: ").strip()
            res = search_tasks(q)
            print(f"\n🔍 Search Results ({len(res)}):")
            for t, p in res:
                print(
                    f"  [{t['id']}] {t['title']} ({p}) - Status: {t['status']}"
                )

        elif choice == "7":
            print("\nGoodbye! Stay productive! 👋")
            break


if __name__ == "__main__":
    main()