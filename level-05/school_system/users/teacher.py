from dataclasses import dataclass, field
from datetime import date
from typing import List

from school_system.users.person import Person


@dataclass
class Teacher(Person):
    employee_id: str
    department: str

    assigned_courses: List[str] = field(
        default_factory=list
    )

    office_hours: str = ""

    def get_role(self) -> str:
        return "TEACHER"

    def assign_course(
        self,
        course_code: str
    ) -> None:

        if course_code not in self.assigned_courses:
            self.assigned_courses.append(
                course_code
            )

    def remove_course(
        self,
        course_code: str
    ) -> None:

        if course_code in self.assigned_courses:
            self.assigned_courses.remove(
                course_code
            )

    def __str__(self) -> str:
        return (
            f"{self.name} "
            f"({self.employee_id})"
        )