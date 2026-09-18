from dataclasses import dataclass

from hospital_system.staff.doctor import HospitalStaff


@dataclass
class Admin(HospitalStaff):
    role: str = ""
    access_level: int = 1

    def __post_init__(self):
        if self.access_level < 1:
            raise ValueError(
                "Access level must be at least 1."
            )

    def can_access(self, required_level: int) -> bool:
        return self.access_level >= required_level

    def get_staff_role(self) -> str:
        return "ADMIN"

    def get_role(self) -> str:
        return "ADMIN"