from datetime import date, timedelta

import pytest

from hospital_system.exceptions.medical_exceptions import (
    InventoryError,
    PrescriptionError,
)
from hospital_system.pharmacy.medication import Medication
from hospital_system.pharmacy.prescription import Prescription
from hospital_system.pharmacy.inventory import Inventory


def make_medication(
    medication_id="MED001",
    expiry_date=None,
):
    return Medication(
        medication_id=medication_id,
        name="Paracetamol",
        dosage="500mg",
        form="Tablet",
        unit_price=500.0,
        expiry_date=expiry_date
        or date.today() + timedelta(days=90),
    )


def test_medication_creation():
    medication = make_medication()

    assert medication.name == "Paracetamol"
    assert medication.unit_price == 500.0
    assert medication.is_expired is False


def test_expired_medication():
    medication = make_medication(
        expiry_date=date.today() - timedelta(days=1)
    )

    assert medication.is_expired is True


def test_prescription_creation():
    prescription = Prescription(
        prescription_id="RX001",
        patient_id="PAT001",
        doctor_id="DOC001",
        medication_id="MED001",
        dosage="500mg",
        frequency="Twice daily",
        duration_days=7,
        prescribed_date=date.today(),
    )

    assert prescription.is_active is True
    assert prescription.duration_days == 7


def test_invalid_prescription_duration():
    with pytest.raises(PrescriptionError):
        Prescription(
            prescription_id="RX001",
            patient_id="PAT001",
            doctor_id="DOC001",
            medication_id="MED001",
            dosage="500mg",
            frequency="Once daily",
            duration_days=0,
            prescribed_date=date.today(),
        )


def test_prescription_status_changes():
    prescription = Prescription(
        prescription_id="RX001",
        patient_id="PAT001",
        doctor_id="DOC001",
        medication_id="MED001",
        dosage="500mg",
        frequency="Twice daily",
        duration_days=7,
        prescribed_date=date.today(),
    )

    prescription.complete()

    assert prescription.status == "COMPLETED"
    assert prescription.is_active is False

    prescription.cancel()

    assert prescription.status == "CANCELLED"


def test_add_medication_to_inventory():
    inventory = Inventory()
    medication = make_medication()

    inventory.add_medication(
        medication,
        quantity=50,
        reorder_level=10,
    )

    assert inventory.get_quantity("MED001") == 50


def test_remove_medication_from_inventory():
    inventory = Inventory()
    medication = make_medication()

    inventory.add_medication(medication, 50)
    inventory.remove_medication("MED001", 10)

    assert inventory.get_quantity("MED001") == 40


def test_insufficient_stock_is_rejected():
    inventory = Inventory()
    medication = make_medication()

    inventory.add_medication(medication, 5)

    with pytest.raises(InventoryError):
        inventory.remove_medication("MED001", 10)


def test_expired_medication_cannot_be_dispensed():
    inventory = Inventory()

    medication = make_medication(
        expiry_date=date.today() - timedelta(days=1)
    )

    inventory.add_medication(medication, 20)

    with pytest.raises(InventoryError):
        inventory.remove_medication("MED001", 1)


def test_restock():
    inventory = Inventory()
    medication = make_medication()

    inventory.add_medication(medication, 10)
    inventory.restock("MED001", 25)

    assert inventory.get_quantity("MED001") == 35


def test_reorder_alert():
    inventory = Inventory()
    medication = make_medication()

    inventory.add_medication(
        medication,
        quantity=5,
        reorder_level=10,
    )

    alerts = inventory.get_reorder_alerts()

    assert len(alerts) == 1
    assert alerts[0].medication.medication_id == "MED001"


def test_expiring_soon():
    inventory = Inventory()

    medication = make_medication(
        expiry_date=date.today() + timedelta(days=10)
    )

    inventory.add_medication(medication, 20)

    expiring = inventory.get_expiring_soon(days=30)

    assert len(expiring) == 1
