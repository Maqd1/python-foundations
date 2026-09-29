# Task Manager with Observers

A task management system built with Python's object-oriented programming features.

The project manages projects, tasks, subtasks, comments, assignments, statuses, reporting, JSON persistence, and HTML report generation.

It also demonstrates the **Observer Pattern**, where task observers automatically receive notifications when a task's status changes.

## Features

### Task Management

- Create tasks
- Delete tasks
- Assign tasks to users
- Change task status
- Set task priority
- Set due dates
- Add subtasks
- Add comments
- Detect overdue tasks

### Project Management

- Create projects
- Store project tasks
- Assign a project manager
- Set project deadlines
- Calculate project completion
- Generate project reports

### Observer Pattern

Tasks maintain a collection of observers.

Implemented observers:

- `EmailNotifier`
- `Logger`
- `DashboardUpdater`

When a task's status changes, the task notifies all registered observers.

Example:

```text
📧 Email sent to John: "Your task 'Design Homepage' status changed to REVIEW"
📝 Logged: Task #1 status changed to REVIEW
📊 Dashboard updated