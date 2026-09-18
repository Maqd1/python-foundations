from datetime import date

import pytest

from hospital_system.patients import (
    EmergencyPatient,
    Inpatient,
    Outpatient,
    Patient,
)
from hospital_system.exceptions.medical_exceptions import (
    AdmissionError,
    InvalidPatientError,
)
from hospital_system.patients import Visit


def create_patient(patient_class=Patient, **kwargs):
    data = {
        "name": "Damilola Ogunleye",
        "date_of_birth": date(1996, 3, 15),
        "contact": "08012345678",
        "address": "Lagos, Nigeria",
        "patient_id": "P2024-5678",
        "blood_group": "O+",
        "allergies": ["Penicillin", "Latex"],
        "emergency_contact_name": "John Ogunleye",
        "emergency_contact_phone": "08098765432",
    }

    data.update(kwargs)

    return patient_class(**data)


def test_patient_creation():
    patient = create_patient()

    assert patient.name == "Damilola Ogunleye"
    assert patient.patient_id == "P2024-5678"
    assert patient.blood_group == "O+"
    assert patient.has_allergy("penicillin")


def test_patient_add_allergy_and_history():
    patient = create_patient()

    patient.add_allergy("Aspirin")
    patient.add_medical_history("Malaria")

    assert "Aspirin" in patient.allergies
    assert "Malaria" in patient.medical_history


def test_invalid_patient():
    with pytest.raises(InvalidPatientError):
        create_patient(patient_id="")


def test_inpatient_admission_and_discharge():
    patient = create_patient(Inpatient)

    patient.admit(
        admission_number="ADM-2026-09-05-001",
        ward="General Medicine",
        room="304-B",
        admission_date=date(2026, 9, 5),
        attending_doctor="Dr. Adaobi Okonkwo",
    )

    assert patient.is_admitted is True
    assert patient.room == "304-B"

    patient.discharge(date(2026, 9, 10))

    assert patient.is_admitted is False
    assert patient.discharge_date == date(2026, 9, 10)


def test_invalid_discharge_date():
    patient = create_patient(Inpatient)

    patient.admit(
        admission_number="ADM-001",
        ward="General Medicine",
        room="304-B",
        admission_date=date(2026, 9, 5),
        attending_doctor="Dr. Adaobi Okonkwo",
    )

    with pytest.raises(AdmissionError):
        patient.discharge(date(2026, 9, 1))


def test_outpatient_visits_and_referrals():
    patient = create_patient(Outpatient)

    patient.add_visit("Cardiology consultation")
    patient.add_referral("Ophthalmology")

    assert "Cardiology consultation" in patient.clinic_visits
    assert "Ophthalmology" in patient.referrals


def test_emergency_patient_triage():
    patient = create_patient(
        EmergencyPatient,
        emergency_reason="Chest pain",
        triage_level=2,
    )

    assert patient.triage_level == 2
    assert patient.emergency_status == "WAITING"

    patient.update_triage(1)
    patient.treat()

    assert patient.triage_level == 1
    assert patient.emergency_status == "IN_TREATMENT"


def test_invalid_triage_level():
    with pytest.raises(InvalidPatientError):
        create_patient(
            EmergencyPatient,
            triage_level=6,
        )

def test_patient_has_medical_record():
    patient = create_patient()

    assert patient.medical_record.patient_id == patient.patient_id
    assert len(patient.medical_record.diagnoses) == 0


def test_patient_visits():
    patient = create_patient()

    visit = Visit(
        visit_id="VIS-001",
        patient_id=patient.patient_id,
        visit_date=date(2026, 9, 5),
        doctor="Dr. Adaobi Okonkwo",
        reason="Chest pain",
    )

    visit.record_diagnosis("Hypertensive crisis")
    visit.record_treatment("Amlodipine 10mg")
    visit.add_note("Monitor blood pressure every 4 hours.")

    patient.add_visit(visit)

    assert len(patient.visits) == 1
    assert patient.visits[0].diagnosis == "Hypertensive crisis"
    assert patient.visits[0].treatment == "Amlodipine 10mg"