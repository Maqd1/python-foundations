'''
Q6: The Task Manager with Observers (Hard)

Create a task management system with observer pattern for notifications.

Requirements:

    Task System:

        Task: id, title, description, priority, status, due_date, assignee

        Project: name, tasks, manager, deadline

        TaskStatus: enum (NOT_STARTED, IN_PROGRESS, REVIEW, DONE)

    Observer Pattern:

        Observer interface with update() method

        Implement: EmailNotifier, Logger, DashboardUpdater

        Tasks notify observers when status changes

    Task Operations:

        Create/delete tasks

        Assign to users

        Change status

        Add subtasks

        Add comments

    Reporting:

        Generate project reports

        Track overdue tasks

        User workload analysis

    Persistence:

        Save/load tasks (JSON)

        Export reports (HTML)

    Advanced OOP Features:

        Dataclasses for data objects

        Context managers for file operations

        Property decorators for validation

Sample Output:
text

✅ TASK MANAGER WITH OBSERVERS ✅

📋 PROJECT: Website Redesign
Tasks: 5 | Due: 2026-12-15

📊 TASK OVERVIEW:
1. Design Homepage (IN_PROGRESS)
   Assignee: John
   Due: 2026-11-20
   Subtasks: 3/5 complete

2. Backend API (DONE)
   Assignee: Damilola
   Due: 2026-11-15

3. Mobile Responsiveness (NOT_STARTED)
   Assignee: Alice
   Due: 2026-12-01

📝 Change task status:
Task ID: 1
New status: REVIEW

📧 Email sent to John: "Your task 'Design Homepage' status changed to REVIEW"
📝 Logged: Task #1 status updated to REVIEW
📊 Dashboard updated

👤 USER WORKLOAD:
John: 3 tasks (1 overdue)
Alice: 2 tasks
Damilola: 1 task (completed)

⚠️ OVERDUE TASKS:
1. Design Homepage (Due: 2026-11-20) - 5 days overdue

📊 PROJECT REPORT:
Project: Website Redesign
Completion: 40%
Tasks: 5
  - In Progress: 2
  - Review: 1
  - Done: 2

Next milestone: Complete Design by 2026-11-25
Risks: Mobile responsiveness behind schedule

Concepts: Observer pattern, dataclasses, context managers, property decorators, JSON serialization, enums
'''