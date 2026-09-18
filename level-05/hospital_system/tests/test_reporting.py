from datetime import date, datetime, timedelta

from hospital_system.appointments.appointment import Appointment
from hospital_system.billing.invoice import Invoice
from hospital_system.pharmacy.inventory import Inventory
from hospital_system.pharmacy.medication import Medication
from hospital_system.services.emergency import EmergencyAlert
from hospital_system.services.lab import LabTest
from hospital_system.services.radiology import RadiologyScan
from hospital_system.services.reporting import HospitalReporter


def test_generate_empty_report():
    reporter = HospitalReporter()
    inventory = Inventory()

    report = reporter.generate_report(
        patients=[],
        appointments=[],
        emergencies=[],
        lab_tests=[],
        radiology_scans=[],
        inventory=inventory,
        invoices=[],
    )

    assert report.patients == 0
    assert report.appointments == 0
    assert report.emergencies == 0
    assert report.outstanding_balance == 0


def test_report_counts_appointments():
    reporter = HospitalReporter()
    inventory = Inventory()

    appointment1 = Appointment(
        appointment_id="A001",
        patient_id="P001",
        doctor_id="D001",
        appointment_time=datetime.now(),
        reason="Checkup",
    )

    appointment2 = Appointment(
        appointment_id="A002",
        patient_id="P002",
        doctor_id="D001",
        appointment_time=datetime.now()
        + timedelta(hours=1),
        reason="Follow-up",
    )

    appointment2.cancel()

    report = reporter.generate_report(
        patients=["P001", "P002"],
        appointments=[
            appointment1,
            appointment2,
        ],
        emergencies=[],
        lab_tests=[],
        radiology_scans=[],
        inventory=inventory,
        invoices=[],
    )

    assert report.patients == 2
    assert report.appointments == 2
    assert report.active_appointments == 1


def test_report_counts_active_emergencies():
    reporter = HospitalReporter()
    inventory = Inventory()

    emergency1 = EmergencyAlert(
        alert_id="E001",
        patient_id="P001",
        emergency_type="Trauma",
        severity=2,
        message="Urgent.",
    )

    emergency2 = EmergencyAlert(
        alert_id="E002",
        patient_id="P002",
        emergency_type="Fall",
        severity=4,
        message="Requires attention.",
    )

    emergency2.resolve()

    report = reporter.generate_report(
        patients=["P001", "P002"],
        appointments=[],
        emergencies=[
            emergency1,
            emergency2,
        ],
        lab_tests=[],
        radiology_scans=[],
        inventory=inventory,
        invoices=[],
    )

    assert report.emergencies == 2
    assert report.active_emergencies == 1


def test_report_counts_pending_services():
    reporter = HospitalReporter()
    inventory = Inventory()

    lab_test = LabTest(
        test_id="LAB001",
        patient_id="P001",
        test_name="Blood Test",
        requested_by="D001",
        requested_date=date.today(),
    )

    scan = RadiologyScan(
        scan_id="RAD001",
        patient_id="P001",
        scan_type="X-Ray",
        body_part="Chest",
        requested_by="D001",
        requested_date=date.today(),
    )

    report = reporter.generate_report(
        patients=["P001"],
        appointments=[],
        emergencies=[],
        lab_tests=[lab_test],
        radiology_scans=[scan],
        inventory=inventory,
        invoices=[],
    )

    assert report.pending_lab_tests == 1
    assert report.pending_radiology_scans == 1


def test_report_inventory_alerts():
    reporter = HospitalReporter()

    inventory = Inventory()

    medication = Medication(
        medication_id="MED001",
        name="Paracetamol",
        dosage="500mg",
        form="Tablet",
        unit_price=100.0,
        expiry_date=date.today()
        + timedelta(days=90),
    )

    inventory.add_medication(
        medication,
        quantity=5,
        reorder_level=10,
    )

    report = reporter.generate_report(
        patients=[],
        appointments=[],
        emergencies=[],
        lab_tests=[],
        radiology_scans=[],
        inventory=inventory,
        invoices=[],
    )

    assert report.inventory_items == 1
    assert report.reorder_alerts == 1


def test_report_invoice_balance():
    reporter = HospitalReporter()
    inventory = Inventory()

    invoice = Invoice(
        invoice_id="INV001",
        patient_id="P001",
        consultation_cost=5000.0,
    )

    report = reporter.generate_report(
        patients=["P001"],
        appointments=[],
        emergencies=[],
        lab_tests=[],
        radiology_scans=[],
        inventory=inventory,
        invoices=[invoice],
    )

    assert report.unpaid_invoices == 1
    assert report.outstanding_balance == 5000.0


def test_report_string():
    reporter = HospitalReporter()
    inventory = Inventory()

    report = reporter.generate_report(
        patients=["P001"],
        appointments=[],
        emergencies=[],
        lab_tests=[],
        radiology_scans=[],
        inventory=inventory,
        invoices=[],
    )

    output = str(report)

    assert "Hospital Report" in output
    assert "Patients: 1" in output
