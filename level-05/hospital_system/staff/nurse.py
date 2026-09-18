from dataclasses import dataclass, field

from hospital_system.staff.doctor import HospitalStaff


@dataclass
class Nurse(HospitalStaff):
    shift: str = ""
    assigned_patients: list[str] = field(default_factory=list)

    def assign_patient(self, patient_id: str) -> None:
        if patient_id and patient_id not in self.assigned_patients:
            self.assigned_patients.append(patient_id)

    def remove_patient(self, patient_id: str) -> None:
        if patient_id in self.assigned_patients:
            self.assigned_patients.remove(patient_id)

    def get_staff_role(self) -> str:
        return "NURSE"

    def get_role(self) -> str:
        return "NURSE"