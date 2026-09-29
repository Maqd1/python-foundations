from dataclasses import dataclass, field
from typing import List

from core.school_system.users.teacher import Teacher


@dataclass
class Department:
    name: str
    code: str
    head: Teacher | None = None
    teachers: List[Teacher] = field(default_factory=list)

    def add_teacher(self, teacher: Teacher) -> None:
        if teacher not in self.teachers:
            self.teachers.append(teacher)

    def remove_teacher(self, teacher: Teacher) -> None:
        if teacher in self.teachers:
            self.teachers.remove(teacher)

    def set_head(self, teacher: Teacher) -> None:
        if teacher not in self.teachers:
            self.add_teacher(teacher)

        self.head = teacher

    def get_teacher(self, teacher_id: str) -> Teacher | None:
        for teacher in self.teachers:
            if teacher.person_id == teacher_id:
                return teacher

        return None

    def __str__(self) -> str:
        return f"{self.code} - {self.name}"