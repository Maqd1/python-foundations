from dataclasses import dataclass
from datetime import datetime


@dataclass
class Appointment:
    appointment_id: str
    patient_id: str
    doctor_id: str
    appointment_time: datetime
    reason: str
    priority: int = 3
    status: str = "SCHEDULED"

    def cancel(self) -> None:
        self.status = "CANCELLED"

    def confirm(self) -> None:
        self.status = "CONFIRMED"

    def reschedule(self, new_time: datetime) -> None:
        self.appointment_time = new_time

    @property
    def is_active(self) -> bool:
        return self.status in {"SCHEDULED", "CONFIRMED"}

    def __str__(self) -> str:
        return (
            f"{self.appointment_id} | "
            f"Patient: {self.patient_id} | "
            f"Doctor: {self.doctor_id} | "
            f"{self.appointment_time} | "
            f"{self.status}"
        )