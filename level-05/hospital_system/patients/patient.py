from dataclasses import dataclass, field
from datetime import date

from school_system.users.person import Person
from hospital_system.exceptions.medical_exceptions import (
    AdmissionError,
    InvalidPatientError,
)

from hospital_system.patients.medical_record import MedicalRecord
from hospital_system.patients.visit import Visit



@dataclass
class Patient(Person):
    patient_id: str
    blood_group: str
    allergies: list[str] = field(default_factory=list)
    emergency_contact_name: str = ""
    emergency_contact_phone: str = ""
    medical_history: list[str] = field(default_factory=list)
    medical_record: MedicalRecord = field(init=False)
    visits: list[Visit] = field(default_factory=list)


    def __post_init__(self):
        if not self.patient_id:
            raise InvalidPatientError(
                "Patient ID cannot be empty."
            )

        if not self.blood_group:
            raise InvalidPatientError(
                "Blood group cannot be empty."
            )

        self.medical_record = MedicalRecord(
            patient_id=self.patient_id
        )

    def add_allergy(self, allergy: str) -> None:
        if allergy and allergy not in self.allergies:
            self.allergies.append(allergy)

    def add_medical_history(self, history: str) -> None:
        if history and history not in self.medical_history:
            self.medical_history.append(history)

    def has_allergy(self, substance: str) -> bool:
        return substance.lower() in [
            allergy.lower()
            for allergy in self.allergies
        ]

    def get_role(self) -> str:
        return "PATIENT"

    def __str__(self) -> str:
        return f"{self.name} ({self.patient_id})"

    def add_visit(self, visit: Visit) -> None:
        if visit.patient_id != self.patient_id:
            raise InvalidPatientError(
                "Visit does not belong to this patient."
            )
    
        self.visits.append(visit)
    
    
    def get_visits(self) -> list[Visit]:
        return list(self.visits)

@dataclass
class Inpatient(Patient):
    admission_number: str = ""
    ward: str = ""
    room: str = ""
    admission_date: date | None = None
    discharge_date: date | None = None
    condition: str = "Stable"
    attending_doctor: str = ""

    def admit(
        self,
        admission_number: str,
        ward: str,
        room: str,
        admission_date: date,
        attending_doctor: str
    ) -> None:
        self.admission_number = admission_number
        self.ward = ward
        self.room = room
        self.admission_date = admission_date
        self.attending_doctor = attending_doctor
        self.discharge_date = None

    def discharge(self, discharge_date: date) -> None:
        if self.admission_date is None:
            raise AdmissionError(
                "Patient has not been admitted."
            )

        if discharge_date < self.admission_date:
            raise AdmissionError(
                "Discharge date cannot be before admission date."
            )

        self.discharge_date = discharge_date

    @property
    def is_admitted(self) -> bool:
        return (
            self.admission_date is not None
            and self.discharge_date is None
        )

    def get_role(self) -> str:
        return "INPATIENT"


@dataclass
class Outpatient(Patient):
    clinic_visits: list[str] = field(default_factory=list)
    referrals: list[str] = field(default_factory=list)

    def add_visit(self, visit: str) -> None:
        if visit:
            self.clinic_visits.append(visit)

    def add_referral(self, referral: str) -> None:
        if referral:
            self.referrals.append(referral)

    def get_role(self) -> str:
        return "OUTPATIENT"

@dataclass
class EmergencyPatient(Patient):
    emergency_reason: str = ""
    triage_level: int = 5
    emergency_status: str = "WAITING"

    def __post_init__(self):
        super().__post_init__()

        if not 1 <= self.triage_level <= 5:
            raise InvalidPatientError(
                "Triage level must be between 1 and 5."
            )

    def update_triage(self, level: int) -> None:
        if not 1 <= level <= 5:
            raise InvalidPatientError(
                "Triage level must be between 1 and 5."
            )

        self.triage_level = level

    def treat(self) -> None:
        self.emergency_status = "IN_TREATMENT"

    def discharge_emergency(self) -> None:
        self.emergency_status = "DISCHARGED"

    def get_role(self) -> str:
        return "EMERGENCY PATIENT"