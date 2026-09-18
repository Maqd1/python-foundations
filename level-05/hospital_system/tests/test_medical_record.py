from datetime import date

import pytest

from hospital_system.patients.medical_record import (
    Diagnosis,
    LabResult,
    MedicalRecord,
    Treatment,
    VitalSigns,
)


def test_vital_signs():
    vitals = VitalSigns(
        blood_pressure="130/85",
        heart_rate=78,
        temperature=37.2,
        oxygen_saturation=98,
        glucose=5.6,
    )

    assert vitals.heart_rate == 78
    assert vitals.temperature == 37.2
    assert vitals.oxygen_saturation == 98


def test_invalid_vital_signs():
    with pytest.raises(ValueError):
        VitalSigns(
            blood_pressure="130/85",
            heart_rate=0,
            temperature=37.2,
            oxygen_saturation=98,
            glucose=5.6,
        )


def test_lab_result():
    result = LabResult(
        test_name="Glucose",
        result="5.6",
        reference_range="3.9-5.5",
        test_date=date(2026, 9, 5),
        unit="mmol/L",
    )

    assert result.test_name == "Glucose"
    assert result.unit == "mmol/L"


def test_diagnosis():
    diagnosis = Diagnosis(
        condition="Hypertension",
        diagnosis_date=date(2025, 8, 10),
        treatment="Amlodipine 5mg daily",
        outcome="Stable",
    )

    assert diagnosis.condition == "Hypertension"
    assert diagnosis.outcome == "Stable"


def test_treatment_status():
    treatment = Treatment(
        description="Amlodipine 5mg daily",
        start_date=date(2026, 9, 5),
    )

    assert treatment.status == "ACTIVE"

    treatment.complete()

    assert treatment.status == "COMPLETED"


def test_medical_record_composition():
    record = MedicalRecord(patient_id="P2024-5678")

    diagnosis = Diagnosis(
        condition="Type 2 Diabetes",
        diagnosis_date=date(2026, 1, 20),
        treatment="Metformin 500mg BD",
        outcome="Under management",
    )

    treatment = Treatment(
        description="Metformin 500mg BD",
        start_date=date(2026, 9, 5),
    )

    vitals = VitalSigns(
        blood_pressure="130/85",
        heart_rate=78,
        temperature=37.2,
        oxygen_saturation=98,
        glucose=5.6,
    )

    lab = LabResult(
        test_name="HbA1c",
        result="7.2",
        reference_range="< 5.7",
        test_date=date(2026, 9, 5),
        unit="%",
    )

    record.add_diagnosis(diagnosis)
    record.add_treatment(treatment)
    record.add_vital_signs(vitals)
    record.add_lab_result(lab)

    assert len(record.diagnoses) == 1
    assert len(record.treatments) == 1
    assert len(record.vital_signs) == 1
    assert len(record.lab_results) == 1
    assert record.latest_vital_signs == vitals


def test_active_treatments():
    record = MedicalRecord(patient_id="P2024-5678")

    active = Treatment(
        description="Metformin",
        start_date=date(2026, 9, 5),
    )

    completed = Treatment(
        description="Old treatment",
        start_date=date(2026, 1, 1),
    )

    completed.complete()

    record.add_treatment(active)
    record.add_treatment(completed)

    assert len(record.active_treatments) == 1
    assert record.active_treatments[0] == active
