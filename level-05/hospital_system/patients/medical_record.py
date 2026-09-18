from dataclasses import dataclass, field
from datetime import date, datetime


@dataclass(frozen=True)
class VitalSigns:
    blood_pressure: str
    heart_rate: int
    temperature: float
    oxygen_saturation: int
    glucose: float

    def __post_init__(self):
        if self.heart_rate <= 0:
            raise ValueError("Heart rate must be greater than zero.")

        if self.temperature <= 0:
            raise ValueError("Temperature must be greater than zero.")

        if not 0 <= self.oxygen_saturation <= 100:
            raise ValueError(
                "Oxygen saturation must be between 0 and 100."
            )

        if self.glucose < 0:
            raise ValueError("Glucose cannot be negative.")

    def __str__(self) -> str:
        return (
            f"BP: {self.blood_pressure} | "
            f"HR: {self.heart_rate} bpm | "
            f"Temp: {self.temperature}°C | "
            f"SpO2: {self.oxygen_saturation}% | "
            f"Glucose: {self.glucose} mmol/L"
        )


@dataclass
class LabResult:
    test_name: str
    result: str
    reference_range: str
    test_date: date
    unit: str = ""

    def __str__(self) -> str:
        unit = f" {self.unit}" if self.unit else ""

        return (
            f"{self.test_name}: "
            f"{self.result}{unit} "
            f"(Reference: {self.reference_range})"
        )


@dataclass
class Diagnosis:
    condition: str
    diagnosis_date: date
    treatment: str
    outcome: str

    def __str__(self) -> str:
        return (
            f"{self.condition} | "
            f"{self.diagnosis_date} | "
            f"Treatment: {self.treatment} | "
            f"Outcome: {self.outcome}"
        )


@dataclass
class Treatment:
    description: str
    start_date: date
    end_date: date | None = None
    status: str = "ACTIVE"

    def complete(self) -> None:
        self.status = "COMPLETED"

    def stop(self) -> None:
        self.status = "STOPPED"


@dataclass
class MedicalRecord:
    patient_id: str
    diagnoses: list[Diagnosis] = field(default_factory=list)
    treatments: list[Treatment] = field(default_factory=list)
    vital_signs: list[VitalSigns] = field(default_factory=list)
    lab_results: list[LabResult] = field(default_factory=list)

    def add_diagnosis(self, diagnosis: Diagnosis) -> None:
        self.diagnoses.append(diagnosis)

    def add_treatment(self, treatment: Treatment) -> None:
        self.treatments.append(treatment)

    def add_vital_signs(self, vitals: VitalSigns) -> None:
        self.vital_signs.append(vitals)

    def add_lab_result(self, result: LabResult) -> None:
        self.lab_results.append(result)

    @property
    def latest_vital_signs(self) -> VitalSigns | None:
        if not self.vital_signs:
            return None

        return self.vital_signs[-1]

    @property
    def active_treatments(self) -> list[Treatment]:
        return [
            treatment
            for treatment in self.treatments
            if treatment.status == "ACTIVE"
        ]

    def __str__(self) -> str:
        return (
            f"Medical Record | "
            f"Patient: {self.patient_id} | "
            f"Diagnoses: {len(self.diagnoses)} | "
            f"Lab Results: {len(self.lab_results)}"
        )