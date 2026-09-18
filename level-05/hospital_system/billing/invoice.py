from dataclasses import dataclass, field
from datetime import date

from hospital_system.billing.insurance import Insurance
from hospital_system.billing.payment import Payment


@dataclass
class Invoice:
    invoice_id: str
    patient_id: str
    consultation_cost: float = 0.0
    procedure_costs: dict[str, float] = field(
        default_factory=dict
    )
    medication_costs: dict[str, float] = field(
        default_factory=dict
    )
    insurance: Insurance | None = None
    payments: list[Payment] = field(default_factory=list)
    issue_date: date = field(default_factory=date.today)
    status: str = "UNPAID"

    def add_procedure(
        self,
        procedure: str,
        cost: float,
    ) -> None:
        if cost < 0:
            raise ValueError(
                "Procedure cost cannot be negative."
            )

        self.procedure_costs[procedure] = cost

    def add_medication(
        self,
        medication: str,
        cost: float,
    ) -> None:
        if cost < 0:
            raise ValueError(
                "Medication cost cannot be negative."
            )

        self.medication_costs[medication] = cost

    @property
    def procedure_total(self) -> float:
        return sum(self.procedure_costs.values())

    @property
    def medication_total(self) -> float:
        return sum(self.medication_costs.values())

    @property
    def subtotal(self) -> float:
        return (
            self.consultation_cost
            + self.procedure_total
            + self.medication_total
        )

    @property
    def insurance_coverage(self) -> float:
        if self.insurance is None:
            return 0.0

        return self.insurance.calculate_coverage(
            self.subtotal
        )

    @property
    def patient_amount(self) -> float:
        return self.subtotal - self.insurance_coverage

    @property
    def total_paid(self) -> float:
        return sum(
            payment.amount
            for payment in self.payments
            if payment.is_completed
        )

    @property
    def balance(self) -> float:
        return max(
            0.0,
            self.patient_amount - self.total_paid
        )

    def add_payment(self, payment: Payment) -> None:
        if payment.invoice_id != self.invoice_id:
            raise ValueError(
                "Payment does not belong to this invoice."
            )

        self.payments.append(payment)

        if self.balance == 0:
            self.status = "PAID"
        elif self.total_paid > 0:
            self.status = "PARTIALLY_PAID"

    def apply_insurance(
        self,
        insurance: Insurance,
    ) -> None:
        self.insurance = insurance

    def __str__(self) -> str:
        return (
            f"Invoice {self.invoice_id} | "
            f"Patient: {self.patient_id} | "
            f"Total: ₦{self.subtotal:.2f} | "
            f"Balance: ₦{self.balance:.2f} | "
            f"{self.status}"
        )