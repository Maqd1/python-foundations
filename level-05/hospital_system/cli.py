from datetime import date, datetime

from hospital_system.appointments.appointment import Appointment
from hospital_system.appointments.schedule import (
    AppointmentScheduler,
    StandardScheduling,
)
from hospital_system.billing.invoice import Invoice
from hospital_system.billing.payment import Payment
from hospital_system.pharmacy.inventory import Inventory
from hospital_system.pharmacy.medication import Medication
from hospital_system.services.emergency import (
    EmergencyAlert,
    EmergencyResponseSystem,
    EmergencyService,
    PatientTracker,
    ResourceAllocator,
    StaffNotifier,
)
from hospital_system.services.lab import LabTest, Laboratory
from hospital_system.services.radiology import (
    RadiologyDepartment,
    RadiologyScan,
)
from hospital_system.services.reporting import HospitalReporter


class HospitalCLI:

    def __init__(self):
        self.scheduler = AppointmentScheduler(
            StandardScheduling()
        )

        self.inventory = Inventory()
        self.laboratory = Laboratory()
        self.radiology = RadiologyDepartment()

        self.response_system = EmergencyResponseSystem()

        self.notifier = StaffNotifier()
        self.resource_allocator = ResourceAllocator()
        self.patient_tracker = PatientTracker()

        self.response_system.subscribe(self.notifier)
        self.response_system.subscribe(
            self.resource_allocator
        )
        self.response_system.subscribe(
            self.patient_tracker
        )

        self.emergency_service = EmergencyService(
            self.response_system
        )

        self.invoices: list[Invoice] = []
        self.patients: list[str] = []

    def display_menu(self) -> None:
        print("\n=== Hospital Management System ===")
        print("1. Register patient")
        print("2. Schedule appointment")
        print("3. Request lab test")
        print("4. Request radiology scan")
        print("5. Register emergency")
        print("6. Add medication to inventory")
        print("7. Create invoice")
        print("8. View hospital report")
        print("0. Exit")

    def register_patient(self) -> None:
        patient_id = input("Patient ID: ").strip()

        if not patient_id:
            print("Patient ID cannot be empty.")
            return

        if patient_id in self.patients:
            print("Patient already exists.")
            return

        self.patients.append(patient_id)

        print(
            f"Patient {patient_id} registered successfully."
        )

    def schedule_appointment(self) -> None:
        appointment_id = input(
            "Appointment ID: "
        ).strip()

        patient_id = input(
            "Patient ID: "
        ).strip()

        doctor_id = input(
            "Doctor ID: "
        ).strip()

        reason = input(
            "Reason: "
        ).strip()

        appointment = Appointment(
            appointment_id=appointment_id,
            patient_id=patient_id,
            doctor_id=doctor_id,
            appointment_time=datetime.now(),
            reason=reason,
        )

        try:
            self.scheduler.schedule(appointment)
            print("Appointment scheduled successfully.")
        except ValueError as error:
            print(f"Error: {error}")

    def request_lab_test(self) -> None:
        test_id = input("Lab test ID: ").strip()
        patient_id = input("Patient ID: ").strip()
        test_name = input("Test name: ").strip()
        doctor_id = input("Doctor ID: ").strip()

        test = LabTest(
            test_id=test_id,
            patient_id=patient_id,
            test_name=test_name,
            requested_by=doctor_id,
            requested_date=date.today(),
        )

        self.laboratory.request_test(test)

        print("Laboratory test requested successfully.")

    def request_radiology_scan(self) -> None:
        scan_id = input("Scan ID: ").strip()
        patient_id = input("Patient ID: ").strip()
        scan_type = input("Scan type: ").strip()
        body_part = input("Body part: ").strip()
        doctor_id = input("Doctor ID: ").strip()

        scan = RadiologyScan(
            scan_id=scan_id,
            patient_id=patient_id,
            scan_type=scan_type,
            body_part=body_part,
            requested_by=doctor_id,
            requested_date=date.today(),
        )

        self.radiology.request_scan(scan)

        print(
            "Radiology scan requested successfully."
        )

    def register_emergency(self) -> None:
        alert_id = input("Emergency ID: ").strip()
        patient_id = input("Patient ID: ").strip()
        emergency_type = input(
            "Emergency type: "
        ).strip()
        message = input("Message: ").strip()

        try:
            severity = int(
                input("Severity (1-5): ").strip()
            )

            alert = EmergencyAlert(
                alert_id=alert_id,
                patient_id=patient_id,
                emergency_type=emergency_type,
                severity=severity,
                message=message,
            )

            self.emergency_service.register_emergency(
                alert
            )

            print(
                "Emergency registered successfully."
            )

        except ValueError as error:
            print(f"Error: {error}")

    def add_medication(self) -> None:
        medication_id = input(
            "Medication ID: "
        ).strip()

        name = input("Medication name: ").strip()
        dosage = input("Dosage: ").strip()
        form = input("Form: ").strip()

        try:
            unit_price = float(
                input("Unit price: ").strip()
            )

            expiry = date.fromisoformat(
                input(
                    "Expiry date (YYYY-MM-DD): "
                ).strip()
            )

            quantity = int(
                input("Quantity: ").strip()
            )

            medication = Medication(
                medication_id=medication_id,
                name=name,
                dosage=dosage,
                form=form,
                unit_price=unit_price,
                expiry_date=expiry,
            )

            self.inventory.add_medication(
                medication,
                quantity,
            )

            print(
                "Medication added to inventory."
            )

        except ValueError as error:
            print(f"Error: {error}")

    def create_invoice(self) -> None:
        invoice_id = input(
            "Invoice ID: "
        ).strip()

        patient_id = input(
            "Patient ID: "
        ).strip()

        try:
            consultation_cost = float(
                input(
                    "Consultation cost: "
                ).strip()
            )

            invoice = Invoice(
                invoice_id=invoice_id,
                patient_id=patient_id,
                consultation_cost=consultation_cost,
            )

            self.invoices.append(invoice)

            print(
                f"Invoice created: "
                f"₦{invoice.subtotal:.2f}"
            )

        except ValueError as error:
            print(f"Error: {error}")

    def show_report(self) -> None:
        reporter = HospitalReporter()

        report = reporter.generate_report(
            patients=self.patients,
            appointments=self.scheduler.appointments,
            emergencies=self.emergency_service.cases.values(),
            lab_tests=self.laboratory.tests,
            radiology_scans=self.radiology.scans,
            inventory=self.inventory,
            invoices=self.invoices,
        )

        print()
        print(report)

    def run(self) -> None:
        while True:
            self.display_menu()

            choice = input(
                "Choose an option: "
            ).strip()

            if choice == "1":
                self.register_patient()

            elif choice == "2":
                self.schedule_appointment()

            elif choice == "3":
                self.request_lab_test()

            elif choice == "4":
                self.request_radiology_scan()

            elif choice == "5":
                self.register_emergency()

            elif choice == "6":
                self.add_medication()

            elif choice == "7":
                self.create_invoice()

            elif choice == "8":
                self.show_report()

            elif choice == "0":
                print("Goodbye.")
                break

            else:
                print("Invalid option.")