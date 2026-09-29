from dataclasses import dataclass, field
from datetime import date


@dataclass
class Visit:
    visit_id: str
    patient_id: str
    visit_date: date
    doctor: str
    reason: str
    diagnosis: str = ""
    treatment: str = ""
    notes: list[str] = field(default_factory=list)

    def add_note(self, note: str) -> None:
        if note:
            self.notes.append(note)

    def record_diagnosis(self, diagnosis: str) -> None:
        self.diagnosis = diagnosis

    def record_treatment(self, treatment: str) -> None:
        self.treatment = treatment

    def __str__(self) -> str:
        return (
            f"Visit {self.visit_id} | "
            f"{self.visit_date} | "
            f"Doctor: {self.doctor} | "
            f"Reason: {self.reason}"
        )
