from dataclasses import dataclass
from datetime import date
from enum import Enum


class AttendanceStatus(Enum):
    PRESENT = "PRESENT"
    ABSENT = "ABSENT"
    LATE = "LATE"


@dataclass(frozen=True)
class Attendance:
    student_id: str
    course_code: str
    date: date
    status: AttendanceStatus

    def __str__(self) -> str:
        return (
            f"{self.course_code} | "
            f"{self.date} | "
            f"{self.status.value}"
        )