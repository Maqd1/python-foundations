from datetime import date

import pytest

from hospital_system.staff import Doctor, Nurse, Admin


def test_doctor_creation():
    doctor = Doctor(
        name="Adaobi Okonkwo",
        date_of_birth=date(1985, 4, 12),
        contact="08011111111",
        address="Lagos, Nigeria",
        employee_id="DOC-001",
        department="Cardiology",
        specialty="Cardiology",
    )

    assert doctor.name == "Adaobi Okonkwo"
    assert doctor.employee_id == "DOC-001"
    assert doctor.specialty == "Cardiology"
    assert doctor.get_staff_role() == "DOCTOR"
    assert doctor.get_role() == "DOCTOR"


def test_doctor_schedule():
    doctor = Doctor(
        name="Adaobi Okonkwo",
        date_of_birth=date(1985, 4, 12),
        contact="08011111111",
        address="Lagos, Nigeria",
        employee_id="DOC-001",
        department="Cardiology",
        specialty="Cardiology",
    )

    doctor.add_schedule("Monday 10:00-14:00")
    doctor.add_schedule("Wednesday 09:00-12:00")

    assert len(doctor.schedule) == 2

    doctor.remove_schedule("Monday 10:00-14:00")

    assert doctor.schedule == ["Wednesday 09:00-12:00"]


def test_doctor_certifications():
    doctor = Doctor(
        name="Adaobi Okonkwo",
        date_of_birth=date(1985, 4, 12),
        contact="08011111111",
        address="Lagos, Nigeria",
        employee_id="DOC-001",
        department="Cardiology",
        specialty="Cardiology",
    )

    doctor.add_certification("MBBS")
    doctor.add_certification("FWACP")
    doctor.add_certification("MBBS")

    assert doctor.certifications == ["MBBS", "FWACP"]


def test_nurse_patient_assignment():
    nurse = Nurse(
        name="Chidinma Okafor",
        date_of_birth=date(1990, 7, 20),
        contact="08022222222",
        address="Lagos, Nigeria",
        employee_id="NUR-001",
        department="General Medicine",
        shift="Morning",
    )

    nurse.assign_patient("P2024-5678")
    nurse.assign_patient("P2024-9999")

    assert len(nurse.assigned_patients) == 2

    nurse.remove_patient("P2024-5678")

    assert nurse.assigned_patients == ["P2024-9999"]


def test_nurse_role():
    nurse = Nurse(
        name="Chidinma Okafor",
        date_of_birth=date(1990, 7, 20),
        contact="08022222222",
        address="Lagos, Nigeria",
        employee_id="NUR-001",
        department="General Medicine",
        shift="Morning",
    )

    assert nurse.get_staff_role() == "NURSE"
    assert nurse.get_role() == "NURSE"


def test_admin_access_control():
    admin = Admin(
        name="Tunde Adeyemi",
        date_of_birth=date(1982, 2, 10),
        contact="08033333333",
        address="Lagos, Nigeria",
        employee_id="ADM-001",
        department="Administration",
        role="Hospital Administrator",
        access_level=3,
    )

    assert admin.can_access(1) is True
    assert admin.can_access(3) is True
    assert admin.can_access(4) is False


def test_invalid_admin_access_level():
    with pytest.raises(ValueError):
        Admin(
            name="Tunde Adeyemi",
            date_of_birth=date(1982, 2, 10),
            contact="08033333333",
            address="Lagos, Nigeria",
            employee_id="ADM-001",
            department="Administration",
            role="Hospital Administrator",
            access_level=0,
        )


def test_staff_activation():
    doctor = Doctor(
        name="Adaobi Okonkwo",
        date_of_birth=date(1985, 4, 12),
        contact="08011111111",
        address="Lagos, Nigeria",
        employee_id="DOC-001",
        department="Cardiology",
        specialty="Cardiology",
    )

    assert doctor.active is True

    doctor.deactivate()

    assert doctor.active is False

    doctor.activate()

    assert doctor.active is True
