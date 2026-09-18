from abc import ABC, abstractmethod
from dataclasses import dataclass, field

from school_system.users.person import Person


@dataclass
class HospitalStaff(Person, ABC):
    employee_id: str
    department: str
    certifications: list[str] = field(default_factory=list)
    active: bool = True

    def add_certification(self, certification: str) -> None:
        if certification and certification not in self.certifications:
            self.certifications.append(certification)

    def deactivate(self) -> None:
        self.active = False

    def activate(self) -> None:
        self.active = True

    @abstractmethod
    def get_staff_role(self) -> str:
        """Return the specific hospital staff role."""
        pass


@dataclass
class Doctor(HospitalStaff):
    specialty: str = ""
    schedule: list[str] = field(default_factory=list)

    def add_schedule(self, schedule: str) -> None:
        if schedule:
            self.schedule.append(schedule)

    def remove_schedule(self, schedule: str) -> None:
        if schedule in self.schedule:
            self.schedule.remove(schedule)

    def get_staff_role(self) -> str:
        return "DOCTOR"

    def get_role(self) -> str:
        return "DOCTOR"

    def __str__(self) -> str:
        return f"Dr. {self.name} ({self.employee_id})"