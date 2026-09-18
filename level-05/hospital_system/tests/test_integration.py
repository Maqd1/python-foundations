from datetime import date, datetime, timedelta

from hospital_system.appointments import (
    Appointment,
    AppointmentScheduler,
    StandardScheduling,
)
from hospital_system.billing import Invoice, Payment
from hospital_system.pharmacy import Inventory, Medication
from hospital_system.services import (
    EmergencyAlert,
    EmergencyResponseSystem,
    EmergencyService,
    LabTest,
    Laboratory,
    RadiologyDepartment,
    RadiologyScan,
    StaffNotifier,
)


def test_hospital_workflow():
    # Patient
    patient_id = "P100"

    # Appointment
    scheduler = AppointmentScheduler(
        StandardScheduling()
    )

    appointment = Appointment(
        appointment_id="A100",
        patient_id=patient_id,
        doctor_id="D100",
        appointment_time=datetime.now(),
        reason="General consultation",
    )

    scheduler.schedule(appointment)

    assert appointment.status == "CONFIRMED"

    # Laboratory
    laboratory = Laboratory()

    lab_test = LabTest(
        test_id="L100",
        patient_id=patient_id,
        test_name="Blood Test",
        requested_by="D100",
        requested_date=date.today(),
    )

    laboratory.request_test(lab_test)
    laboratory.start_test("L100")

    assert lab_test.status == "IN_PROGRESS"

    # Radiology
    radiology = RadiologyDepartment()

    scan = RadiologyScan(
        scan_id="R100",
        patient_id=patient_id,
        scan_type="X-Ray",
        body_part="Chest",
        requested_by="D100",
        requested_date=date.today(),
    )

    radiology.request_scan(scan)
    radiology.start_scan("R100")

    assert scan.status == "IN_PROGRESS"

    # Pharmacy
    inventory = Inventory()

    medication = Medication(
        medication_id="M100",
        name="Paracetamol",
        dosage="500mg",
        form="Tablet",
        unit_price=500.0,
        expiry_date=date.today()
        + timedelta(days=365),
    )

    inventory.add_medication(
        medication,
        quantity=20,
    )

    inventory.remove_medication(
        "M100",
        2,
    )

    assert inventory.get_quantity("M100") == 18

    # Billing
    invoice = Invoice(
        invoice_id="I100",
        patient_id=patient_id,
        consultation_cost=5000.0,
    )

    invoice.add_medication(
        "Paracetamol",
        1000.0,
    )

    payment = Payment(
        payment_id="PAY100",
        invoice_id="I100",
        amount=6000.0,
        payment_date=date.today(),
        method="CASH",
    )

    invoice.add_payment(payment)

    assert invoice.status == "PAID"
    assert invoice.balance == 0

    # Emergency
    response_system = EmergencyResponseSystem()
    notifier = StaffNotifier()

    response_system.subscribe(notifier)

    emergency_service = EmergencyService(
        response_system
    )

    alert = EmergencyAlert(
        alert_id="E100",
        patient_id=patient_id,
        emergency_type="Severe Reaction",
        severity=1,
        message="Patient requires immediate attention.",
    )

    emergency_service.register_emergency(alert)

    assert len(notifier.notifications) == 1
    assert patient_id in notifier.notifications[0]
