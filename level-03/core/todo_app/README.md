# ✅ Core Project: Todo App

## The Smart Todo with Deadlines and Priorities 📋

Build an advanced todo application with **task management, projects, priorities, deadlines, subtasks, tags, analytics, search, and persistent data storage**.

The application should go beyond simply adding and removing tasks. It should provide tools for organizing work, tracking productivity, analyzing time, and finding tasks efficiently.

---

# 📊 Data Structure

The system uses deeply nested dictionaries and lists to represent projects, tasks, subtasks, tags, deadlines, and productivity information.

```python
todo_data = {
    "projects": {
        "Work": {
            "tasks": [
                {
                    "id": 1,
                    "title": "Complete Python project",
                    "description": "Finish the inventory system",
                    "priority": 1,
                    "status": "In Progress",
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
```

### Priority Levels

```text
1 = Highest
2 = High
3 = Medium
4 = Low
5 = Lowest
```

### Task Statuses

```text
Not Started
In Progress
Completed
Archived
```

---

# 📋 1. Task Management

Implement the fundamental task-management operations.

### `add_task(title, project, priority=3, deadline=None)`

Create a new task and add it to the specified project.

### `edit_task(task_id, **kwargs)`

Edit any supported field of an existing task.

### `delete_task(task_id)`

Delete a task from the system.

### `view_tasks(project=None, status=None, priority=None)`

Display tasks with optional filters for:

* Project
* Status
* Priority

### `view_task(task_id)`

Display the complete details of a specific task.

---

# 📁 2. Organization — HARD

Implement tools for organizing tasks and projects.

### `add_project(name)`

Create a new project.

### `delete_project(name)`

Delete a project while moving its tasks to the archive.

### `move_task(task_id, new_project)`

Move an existing task from one project to another.

### `add_tag(task_id, tag)`

Add a tag to a task.

### `view_by_tag(tag)`

Display all tasks associated with a particular tag.

---

# 🧠 3. Smart Features — HARDER

Implement features that use dates, priorities, and task status.

### `get_overdue_tasks()`

Return tasks whose deadlines have passed.

### `get_tasks_by_priority(priority)`

Return tasks with the specified priority level.

### `get_upcoming_deadlines(days)`

Find tasks whose deadlines fall within the next specified number of days.

### `complete_task(task_id)`

Mark a task as completed and record its completion time.

### `archive_completed()`

Move completed tasks into the archive.

---

# 📊 4. Statistics and Reporting — HARDEST

The application should analyze task and productivity data.

### `get_project_stats(project)`

Return statistics for a project, including tasks that are:

* Completed
* In Progress
* Not Started
* Archived

### `get_productivity_report()`

Analyze completed tasks by day and week.

### `get_time_analysis()`

Compare:

* Estimated hours
* Actual hours
* Overall efficiency

### `get_priority_distribution()`

Show how tasks are distributed across priority levels.

### `get_tags_cloud()`

Identify the most frequently used tags.

---

# 🔎 5. Search — VERY HARD

Implement flexible task searching.

### `search_tasks(query)`

Search across:

* Task title
* Description
* Tags
* Project

### `advanced_search(**filters)`

Allow multiple search filters to be combined.

---

# 💾 6. Data Persistence

The application must preserve task data between sessions.

Requirements:

* Automatically save data after every change.
* Export data to JSON.
* Import data from JSON.

---

# 🖥️ Sample Interface

```text
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
```

---

# 📁 Task View

```text
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
```

---

# 📌 Task Details

```text
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
```

---

# 📈 Productivity Report

```text
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

#python (5)
#work (4)
#project (3)
#urgent (2)
#documentation (2)

⏰ TIME ANALYSIS:

Total estimated: 45 hours
Total actual: 32 hours
Efficiency: 71%
```

---

# 🧠 Concepts Tested

This project tests the ability to work with:

* Deeply nested dictionaries
* Lists
* List comprehensions
* Complex filtering
* Date and time handling
* `datetime`
* Sorting with multiple keys
* Statistical analysis
* String methods
* File I/O
* JSON persistence
* Search algorithms
* Task organization
* Priority systems
* Deadline calculations
* Productivity analysis
