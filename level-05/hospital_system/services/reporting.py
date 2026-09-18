from dataclasses import dataclass

from hospital_system.appointments.appointment import Appointment
from hospital_system.billing.invoice import Invoice
from hospital_system.pharmacy.inventory import Inventory
from hospital_system.services.emergency import EmergencyAlert
from hospital_system.services.lab import LabTest
from hospital_system.services.radiology import RadiologyScan


@dataclass
class HospitalReport:
    patients: int = 0
    appointments: int = 0
    active_appointments: int = 0
    emergencies: int = 0
    active_emergencies: int = 0
    pending_lab_tests: int = 0
    pending_radiology_scans: int = 0
    inventory_items: int = 0
    reorder_alerts: int = 0
    expired_medications: int = 0
    unpaid_invoices: int = 0
    outstanding_balance: float = 0.0

    def __str__(self) -> str:
        return (
            "=== Hospital Report ===\n"
            f"Patients: {self.patients}\n"
            f"Appointments: {self.appointments}\n"
            f"Active appointments: "
            f"{self.active_appointments}\n"
            f"Emergencies: {self.emergencies}\n"
            f"Active emergencies: "
            f"{self.active_emergencies}\n"
            f"Pending lab tests: "
            f"{self.pending_lab_tests}\n"
            f"Pending radiology scans: "
            f"{self.pending_radiology_scans}\n"
            f"Inventory items: {self.inventory_items}\n"
            f"Reorder alerts: {self.reorder_alerts}\n"
            f"Expired medications: "
            f"{self.expired_medications}\n"
            f"Unpaid invoices: {self.unpaid_invoices}\n"
            f"Outstanding balance: "
            f"₦{self.outstanding_balance:.2f}"
        )


class HospitalReporter:

    def generate_report(
        self,
        patients: list,
        appointments: list[Appointment],
        emergencies: list[EmergencyAlert],
        lab_tests: list[LabTest],
        radiology_scans: list[RadiologyScan],
        inventory: Inventory,
        invoices: list[Invoice],
    ) -> HospitalReport:

        active_appointments = [
            appointment
            for appointment in appointments
            if appointment.is_active
        ]

        active_emergencies = [
            emergency
            for emergency in emergencies
            if not emergency.resolved
        ]

        pending_lab_tests = [
            test
            for test in lab_tests
            if test.status in {
                "REQUESTED",
                "IN_PROGRESS",
            }
        ]

        pending_radiology_scans = [
            scan
            for scan in radiology_scans
            if scan.status in {
                "REQUESTED",
                "IN_PROGRESS",
            }
        ]

        unpaid_invoices = [
            invoice
            for invoice in invoices
            if invoice.balance > 0
        ]

        outstanding_balance = sum(
            invoice.balance
            for invoice in invoices
        )

        return HospitalReport(
            patients=len(patients),
            appointments=len(appointments),
            active_appointments=len(active_appointments),
            emergencies=len(emergencies),
            active_emergencies=len(active_emergencies),
            pending_lab_tests=len(pending_lab_tests),
            pending_radiology_scans=len(
                pending_radiology_scans
            ),
            inventory_items=len(inventory.items),
            reorder_alerts=len(
                inventory.get_reorder_alerts()
            ),
            expired_medications=len(
                inventory.get_expired_medications()
            ),
            unpaid_invoices=len(unpaid_invoices),
            outstanding_balance=outstanding_balance,
        )
