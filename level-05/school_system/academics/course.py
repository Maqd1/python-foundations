from dataclasses import dataclass, field
from typing import List

from school_system.academics.schedule import Schedule


@dataclass
class Course:
    course_code: str
    title: str
    description: str
    credits: int
    department: str
    prerequisites: List[str] = field(
        default_factory=list
    )
    schedule: Schedule | None = None
    capacity: int = 30

    def __post_init__(self):
        if not self.course_code:
            raise ValueError(
                "Course code cannot be empty."
            )

        if self.credits <= 0:
            raise ValueError(
                "Course credits must be greater than zero."
            )

        if self.capacity <= 0:
            raise ValueError(
                "Course capacity must be greater than zero."
            )

    def add_prerequisite(
        self,
        course_code: str
    ) -> None:

        if course_code not in self.prerequisites:
            self.prerequisites.append(course_code)

    def has_prerequisites(self) -> bool:
        return bool(self.prerequisites)

    def set_schedule(
        self,
        schedule: Schedule
    ) -> None:

        self.schedule = schedule

    def __str__(self) -> str:
        return (
            f"{self.course_code} - "
            f"{self.title} "
            f"({self.credits} Credits)"
        )