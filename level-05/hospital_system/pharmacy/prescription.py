from dataclasses import dataclass
from datetime import date

from hospital_system.exceptions.medical_exceptions import (
    PrescriptionError,
)


@dataclass
class Prescription:
    prescription_id: str
    patient_id: str
    doctor_id: str
    medication_id: str
    dosage: str
    frequency: str
    duration_days: int
    prescribed_date: date
    status: str = "ACTIVE"

    def __post_init__(self):
        if self.duration_days <= 0:
            raise PrescriptionError(
                "Prescription duration must be greater than zero."
            )

    def complete(self) -> None:
        self.status = "COMPLETED"

    def cancel(self) -> None:
        self.status = "CANCELLED"

    @property
    def is_active(self) -> bool:
        return self.status == "ACTIVE"

    def __str__(self) -> str:
        return (
            f"{self.prescription_id} | "
            f"Patient: {self.patient_id} | "
            f"Medication: {self.medication_id} | "
            f"{self.dosage} | "
            f"{self.frequency} | "
            f"{self.duration_days} days | "
            f"{self.status}"
        )