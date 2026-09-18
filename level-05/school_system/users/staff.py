from dataclasses import dataclass

from school_system.users.person import Person


@dataclass
class AdminStaff(Person):
    employee_id: str
    role: str
    access_level: int = 1

    def get_role(self) -> str:
        return "ADMIN STAFF"

    def can_access(
        self,
        required_level: int
    ) -> bool:

        return self.access_level >= required_level

    def __str__(self) -> str:
        return (
            f"{self.name} "
            f"({self.employee_id})"
        )