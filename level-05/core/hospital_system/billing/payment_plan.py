from dataclasses import dataclass


@dataclass
class PaymentPlan:
    plan_id: str
    invoice_id: str
    total_amount: float
    installments: int
    amount_paid: float = 0.0

    def __post_init__(self):
        if self.total_amount <= 0:
            raise ValueError("Payment plan amount must be greater than zero.")

        if self.installments <= 0:
            raise ValueError("Installments must be greater than zero.")

        if self.amount_paid < 0:
            raise ValueError("Amount paid cannot be negative.")

        if self.amount_paid > self.total_amount:
            raise ValueError("Amount paid cannot exceed the total amount.")

    @property
    def installment_amount(self) -> float:
        return self.total_amount / self.installments

    @property
    def balance(self) -> float:
        return max(0.0, self.total_amount - self.amount_paid)

    @property
    def installments_paid(self) -> int:
        return min(
            self.installments,
            int(self.amount_paid // self.installment_amount),
        )

    @property
    def is_completed(self) -> bool:
        return self.balance == 0

    def make_payment(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("Payment amount must be greater than zero.")

        if self.amount_paid + amount > self.total_amount:
            raise ValueError("Payment cannot exceed the remaining balance.")

        self.amount_paid += amount
