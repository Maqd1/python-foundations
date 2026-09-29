from dataclasses import dataclass
from datetime import time


@dataclass(frozen=True)
class Schedule:
    day: str
    start_time: time
    end_time: time
    room: str
    instructor: str

    def __post_init__(self):
        if self.start_time >= self.end_time:
            raise ValueError(
                "Start time must be before end time."
            )

    def conflicts_with(
        self,
        other: "Schedule"
    ) -> bool:

        if self.day != other.day:
            return False

        return (
            self.start_time < other.end_time
            and other.start_time < self.end_time
        )

    def __str__(self) -> str:
        return (
            f"{self.day} "
            f"{self.start_time.strftime('%H:%M')}-"
            f"{self.end_time.strftime('%H:%M')} "
            f"| {self.room} "
            f"| {self.instructor}"
        )