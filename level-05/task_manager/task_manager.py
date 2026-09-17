from __future__ import annotations

from abc import ABC, abstractmethod
from contextlib import contextmanager
from dataclasses import dataclass, field, asdict
from datetime import date, datetime
from enum import Enum
import json
from pathlib import Path
from typing import Iterator


# ============================================================
# ENUMS
# ============================================================

class TaskStatus(Enum):
    NOT_STARTED = "NOT_STARTED"
    IN_PROGRESS = "IN_PROGRESS"
    REVIEW = "REVIEW"
    DONE = "DONE"


class Priority(Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    URGENT = "URGENT"


# ============================================================
# OBSERVER PATTERN
# ============================================================

class Observer(ABC):
    """Interface for objects that want to receive task updates."""

    @abstractmethod
    def update(self, task: "Task", message: str) -> None:
        pass


class EmailNotifier(Observer):
    """Simulates sending an email when a task changes."""

    def update(self, task: "Task", message: str) -> None:
        if task.assignee:
            print(
                f'📧 Email sent to {task.assignee}: '
                f'"{message}"'
            )


class Logger(Observer):
    """Logs task changes."""

    def update(self, task: "Task", message: str) -> None:
        print(f"📝 Logged: Task #{task.id} {message}")


class DashboardUpdater(Observer):
    """Simulates updating a project dashboard."""

    def update(self, task: "Task", message: str) -> None:
        print("📊 Dashboard updated")


# ============================================================
# DATA OBJECTS
# ============================================================

@dataclass
class Comment:
    author: str
    text: str
    created_at: str = field(
        default_factory=lambda: datetime.now().isoformat(
            timespec="seconds"
        )
    )


@dataclass
class Subtask:
    title: str
    completed: bool = False

    def complete(self) -> None:
        self.completed = True


@dataclass
class Task(Observer):
    """
    Represents a task.

    Task itself can receive observer updates through the Observer
    interface, while also maintaining a list of observers that it
    notifies when its status changes.
    """

    id: int
    title: str
    description: str
    priority: Priority
    due_date: date
    assignee: str | None = None
    _status: TaskStatus = field(
        default=TaskStatus.NOT_STARTED,
        repr=False
    )
    subtasks: list[Subtask] = field(default_factory=list)
    comments: list[Comment] = field(default_factory=list)
    _observers: list[Observer] = field(
        default_factory=list,
        repr=False,
        compare=False
    )

    # --------------------------------------------------------
    # PROPERTY: STATUS
    # --------------------------------------------------------

    @property
    def status(self) -> TaskStatus:
        return self._status

    @status.setter
    def status(self, new_status: TaskStatus) -> None:
        if not isinstance(new_status, TaskStatus):
            raise TypeError(
                "status must be a TaskStatus value."
            )

        old_status = self._status

        if old_status == new_status:
            return

        self._status = new_status

        message = (
            f"status changed to {new_status.value}"
        )

        self.notify_observers(message)

    # --------------------------------------------------------
    # OBSERVER METHODS
    # --------------------------------------------------------

    def add_observer(self, observer: Observer) -> None:
        if observer not in self._observers:
            self._observers.append(observer)

    def remove_observer(self, observer: Observer) -> None:
        if observer in self._observers:
            self._observers.remove(observer)

    def notify_observers(self, message: str) -> None:
        for observer in self._observers:
            observer.update(self, message)

    # --------------------------------------------------------
    # TASK OPERATIONS
    # --------------------------------------------------------

    def assign_to(self, username: str) -> None:
        if not username.strip():
            raise ValueError(
                "Assignee name cannot be empty."
            )

        self.assignee = username.strip()

    def add_subtask(self, title: str) -> None:
        if not title.strip():
            raise ValueError(
                "Subtask title cannot be empty."
            )

        self.subtasks.append(
            Subtask(title=title.strip())
        )

    def add_comment(self, author: str, text: str) -> None:
        if not author.strip():
            raise ValueError(
                "Comment author cannot be empty."
            )

        if not text.strip():
            raise ValueError(
                "Comment cannot be empty."
            )

        self.comments.append(
            Comment(
                author=author.strip(),
                text=text.strip()
            )
        )

    def is_overdue(self, today: date | None = None) -> bool:
        if today is None:
            today = date.today()

        return (
            self.due_date < today
            and self.status != TaskStatus.DONE
        )

    def complete_subtask(self, index: int) -> None:
        if index < 0 or index >= len(self.subtasks):
            raise IndexError("Invalid subtask index.")

        self.subtasks[index].complete()

    @property
    def completed_subtasks(self) -> int:
        return sum(
            subtask.completed
            for subtask in self.subtasks
        )

    # --------------------------------------------------------
    # OBSERVER INTERFACE
    # --------------------------------------------------------

    def update(self, task: "Task", message: str) -> None:
        """
        Allows Task to satisfy the Observer interface.

        This method is not required for the main notification flow,
        but demonstrates that Observer is a reusable interface.
        """
        pass

    # --------------------------------------------------------
    # DISPLAY
    # --------------------------------------------------------

    def display(self) -> None:
        print(f"\n{self.id}. {self.title}")
        print(f"   Priority: {self.priority.value}")
        print(f"   Status: {self.status.value}")
        print(
            f"   Assignee: "
            f"{self.assignee or 'Unassigned'}"
        )
        print(f"   Due: {self.due_date}")

        if self.subtasks:
            print(
                f"   Subtasks: "
                f"{self.completed_subtasks}/"
                f"{len(self.subtasks)} complete"
            )


@dataclass
class Project:
    name: str
    manager: str
    deadline: date
    tasks: list[Task] = field(default_factory=list)

    # --------------------------------------------------------
    # PROPERTY: NAME
    # --------------------------------------------------------

    @property
    def project_name(self) -> str:
        return self.name

    @project_name.setter
    def project_name(self, value: str) -> None:
        if not value.strip():
            raise ValueError(
                "Project name cannot be empty."
            )

        self.name = value.strip()

    # --------------------------------------------------------
    # TASK OPERATIONS
    # --------------------------------------------------------

    def add_task(self, task: Task) -> None:
        if any(existing.id == task.id for existing in self.tasks):
            raise ValueError(
                f"Task ID {task.id} already exists."
            )

        self.tasks.append(task)

    def delete_task(self, task_id: int) -> None:
        for task in self.tasks:
            if task.id == task_id:
                self.tasks.remove(task)
                return

        raise ValueError(
            f"Task #{task_id} was not found."
        )

    def get_task(self, task_id: int) -> Task:
        for task in self.tasks:
            if task.id == task_id:
                return task

        raise ValueError(
            f"Task #{task_id} was not found."
        )

    # --------------------------------------------------------
    # REPORTING
    # --------------------------------------------------------

    @property
    def completion_percentage(self) -> float:
        if not self.tasks:
            return 0.0

        completed = sum(
            task.status == TaskStatus.DONE
            for task in self.tasks
        )

        return completed / len(self.tasks) * 100

    def overdue_tasks(
        self,
        today: date | None = None
    ) -> list[Task]:

        return [
            task
            for task in self.tasks
            if task.is_overdue(today)
        ]

    def user_workload(self) -> dict[str, dict[str, int]]:
        workload: dict[str, dict[str, int]] = {}

        for task in self.tasks:
            if task.assignee is None:
                continue

            if task.assignee not in workload:
                workload[task.assignee] = {
                    "total": 0,
                    "overdue": 0,
                    "completed": 0
                }

            workload[task.assignee]["total"] += 1

            if task.is_overdue():
                workload[task.assignee]["overdue"] += 1

            if task.status == TaskStatus.DONE:
                workload[task.assignee]["completed"] += 1

        return workload

    def status_counts(self) -> dict[TaskStatus, int]:
        counts = {
            status: 0
            for status in TaskStatus
        }

        for task in self.tasks:
            counts[task.status] += 1

        return counts

    def generate_report(self) -> str:
        counts = self.status_counts()
        overdue = self.overdue_tasks()

        lines = [
            "📊 PROJECT REPORT",
            f"Project: {self.name}",
            f"Manager: {self.manager}",
            f"Deadline: {self.deadline}",
            f"Completion: {self.completion_percentage:.0f}%",
            f"Tasks: {len(self.tasks)}",
            "",
            f"  - Not Started: "
            f"{counts[TaskStatus.NOT_STARTED]}",
            f"  - In Progress: "
            f"{counts[TaskStatus.IN_PROGRESS]}",
            f"  - Review: "
            f"{counts[TaskStatus.REVIEW]}",
            f"  - Done: "
            f"{counts[TaskStatus.DONE]}",
            "",
            f"Overdue tasks: {len(overdue)}"
        ]

        return "\n".join(lines)


# ============================================================
# FILE CONTEXT MANAGER
# ============================================================

@contextmanager
def open_json_file(
    filename: str,
    mode: str
) -> Iterator:
    """
    Context manager for opening JSON files.

    The with statement guarantees that the file is closed
    after the operation.
    """

    file = open(
        filename,
        mode,
        encoding="utf-8"
    )

    try:
        yield file
    finally:
        file.close()


# ============================================================
# PERSISTENCE
# ============================================================

class TaskManager:
    def __init__(self, project: Project):
        self.project = project

    def save_json(self, filename: str) -> None:
        data = {
            "project": {
                "name": self.project.name,
                "manager": self.project.manager,
                "deadline": self.project.deadline.isoformat()
            },
            "tasks": [
                {
                    "id": task.id,
                    "title": task.title,
                    "description": task.description,
                    "priority": task.priority.value,
                    "status": task.status.value,
                    "due_date": task.due_date.isoformat(),
                    "assignee": task.assignee,
                    "subtasks": [
                        {
                            "title": subtask.title,
                            "completed": subtask.completed
                        }
                        for subtask in task.subtasks
                    ],
                    "comments": [
                        asdict(comment)
                        for comment in task.comments
                    ]
                }
                for task in self.project.tasks
            ]
        }

        with open_json_file(filename, "w") as file:
            json.dump(
                data,
                file,
                indent=4
            )

    @classmethod
    def load_json(
        cls,
        filename: str
    ) -> "TaskManager":

        with open_json_file(filename, "r") as file:
            data = json.load(file)

        project_data = data["project"]

        project = Project(
            name=project_data["name"],
            manager=project_data["manager"],
            deadline=date.fromisoformat(
                project_data["deadline"]
            )
        )

        for task_data in data["tasks"]:
            task = Task(
                id=task_data["id"],
                title=task_data["title"],
                description=task_data["description"],
                priority=Priority(
                    task_data["priority"]
                ),
                due_date=date.fromisoformat(
                    task_data["due_date"]
                ),
                assignee=task_data["assignee"],
                _status=TaskStatus(
                    task_data["status"]
                )
            )

            for subtask_data in task_data["subtasks"]:
                task.subtasks.append(
                    Subtask(
                        title=subtask_data["title"],
                        completed=subtask_data["completed"]
                    )
                )

            for comment_data in task_data["comments"]:
                task.comments.append(
                    Comment(**comment_data)
                )

            project.add_task(task)

        return cls(project)

    # --------------------------------------------------------
    # OBSERVER REGISTRATION
    # --------------------------------------------------------

    def register_default_observers(self) -> None:
        for task in self.project.tasks:
            task.add_observer(EmailNotifier())
            task.add_observer(Logger())
            task.add_observer(DashboardUpdater())

    # --------------------------------------------------------
    # HTML EXPORT
    # --------------------------------------------------------

    def export_html(self, filename: str) -> None:
        rows = []

        for task in self.project.tasks:
            overdue = (
                "⚠️ Yes"
                if task.is_overdue()
                else "No"
            )

            rows.append(
                f"""
                <tr>
                    <td>{task.id}</td>
                    <td>{task.title}</td>
                    <td>{task.status.value}</td>
                    <td>{task.priority.value}</td>
                    <td>{task.assignee or "Unassigned"}</td>
                    <td>{task.due_date}</td>
                    <td>{overdue}</td>
                </tr>
                """
            )

        html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{self.project.name} Report</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 40px;
        }}

        table {{
            border-collapse: collapse;
            width: 100%;
        }}

        th, td {{
            border: 1px solid #ccc;
            padding: 10px;
            text-align: left;
        }}

        th {{
            background: #f2f2f2;
        }}
    </style>
</head>
<body>

<h1>📊 {self.project.name}</h1>

<p>
    <strong>Manager:</strong>
    {self.project.manager}
</p>

<p>
    <strong>Deadline:</strong>
    {self.project.deadline}
</p>

<p>
    <strong>Completion:</strong>
    {self.project.completion_percentage:.0f}%
</p>

<h2>Tasks</h2>

<table>
    <tr>
        <th>ID</th>
        <th>Title</th>
        <th>Status</th>
        <th>Priority</th>
        <th>Assignee</th>
        <th>Due Date</th>
        <th>Overdue</th>
    </tr>

    {"".join(rows)}

</table>

</body>
</html>
"""

        with open_json_file(filename, "w") as file:
            file.write(html)


# ============================================================
# SAMPLE DATA
# ============================================================

def create_sample_project() -> Project:

    project = Project(
        name="Website Redesign",
        manager="Sarah",
        deadline=date(2026, 12, 15)
    )

    task1 = Task(
        id=1,
        title="Design Homepage",
        description="Create the new homepage design.",
        priority=Priority.HIGH,
        due_date=date(2026, 11, 20),
        assignee="John",
        _status=TaskStatus.IN_PROGRESS
    )

    task1.add_subtask("Create wireframe")
    task1.add_subtask("Design hero section")
    task1.add_subtask("Design navigation")
    task1.add_subtask("Design footer")
    task1.add_subtask("Review design")

    task1.complete_subtask(0)
    task1.complete_subtask(1)
    task1.complete_subtask(2)

    task2 = Task(
        id=2,
        title="Backend API",
        description="Build API endpoints.",
        priority=Priority.URGENT,
        due_date=date(2026, 11, 15),
        assignee="Damilola",
        _status=TaskStatus.DONE
    )

    task3 = Task(
        id=3,
        title="Mobile Responsiveness",
        description="Make the website responsive.",
        priority=Priority.MEDIUM,
        due_date=date(2026, 12, 1),
        assignee="Alice",
        _status=TaskStatus.NOT_STARTED
    )

    task4 = Task(
        id=4,
        title="Content Migration",
        description="Move existing website content.",
        priority=Priority.MEDIUM,
        due_date=date(2026, 11, 25),
        assignee="John",
        _status=TaskStatus.REVIEW
    )

    task5 = Task(
        id=5,
        title="Final Testing",
        description="Perform final QA testing.",
        priority=Priority.HIGH,
        due_date=date(2026, 12, 5),
        assignee="John",
        _status=TaskStatus.IN_PROGRESS
    )

    project.add_task(task1)
    project.add_task(task2)
    project.add_task(task3)
    project.add_task(task4)
    project.add_task(task5)

    return project


# ============================================================
# DISPLAY FUNCTIONS
# ============================================================

def display_project(project: Project) -> None:
    print("\n" + "=" * 60)
    print("✅ TASK MANAGER WITH OBSERVERS")
    print("=" * 60)

    print(f"\n📋 PROJECT: {project.name}")
    print(
        f"Tasks: {len(project.tasks)} | "
        f"Due: {project.deadline}"
    )

    print("\n📊 TASK OVERVIEW:")

    for task in project.tasks:
        task.display()


def display_workload(project: Project) -> None:
    print("\n👤 USER WORKLOAD:")

    workload = project.user_workload()

    for username, data in workload.items():
        line = (
            f"{username}: "
            f"{data['total']} tasks"
        )

        if data["overdue"]:
            line += (
                f" ({data['overdue']} overdue)"
            )

        if data["completed"]:
            line += (
                f" ({data['completed']} completed)"
            )

        print(line)


def display_overdue(project: Project) -> None:
    print("\n⚠️ OVERDUE TASKS:")

    overdue = project.overdue_tasks()

    if not overdue:
        print("No overdue tasks.")
        return

    for task in overdue:
        print(
            f"{task.id}. {task.title} "
            f"(Due: {task.due_date})"
        )


# ============================================================
# MAIN DEMO
# ============================================================

def main() -> None:

    project = create_sample_project()

    manager = TaskManager(project)
    manager.register_default_observers()

    display_project(project)

    # --------------------------------------------------------
    # STATUS CHANGE
    # --------------------------------------------------------

    print("\n📝 Change task status:")
    print("Task ID: 1")
    print("New status: REVIEW\n")

    task = project.get_task(1)
    task.status = TaskStatus.REVIEW

    # --------------------------------------------------------
    # ADD COMMENT
    # --------------------------------------------------------

    task.add_comment(
        "Sarah",
        "Please review the updated homepage."
    )

    # --------------------------------------------------------
    # WORKLOAD
    # --------------------------------------------------------

    display_workload(project)

    # --------------------------------------------------------
    # OVERDUE TASKS
    # --------------------------------------------------------

    display_overdue(project)

    # --------------------------------------------------------
    # PROJECT REPORT
    # --------------------------------------------------------

    print("\n" + project.generate_report())

    # --------------------------------------------------------
    # SAVE JSON
    # --------------------------------------------------------

    json_file = "tasks.json"

    manager.save_json(json_file)

    print(
        f"\n💾 Tasks saved to {json_file}"
    )

    # --------------------------------------------------------
    # EXPORT HTML
    # --------------------------------------------------------

    html_file = "project_report.html"

    manager.export_html(html_file)

    print(
        f"🌐 Report exported to {html_file}"
    )


if __name__ == "__main__":
    main()